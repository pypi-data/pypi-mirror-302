import asyncio
import websockets
import json
import threading
import uuid
from logger_setup import setup_logger

logger = setup_logger()

global_event_loop = None
global_ws_client = None
global_listen_task = None
global_callback = None

class Callback:
    def __init__(self):
        self.callback_dict = {}
        self.broadcast_dict = {}

    def registerCallback(self, cb_id, cb):
        self.callback_dict[cb_id] = cb

    def registerBroadcast(self, info, cb):
        if info not in self.broadcast_dict:
            self.broadcast_dict[info] = []
            
        self.broadcast_dict[info].append(cb)

    def trigger(self, cb_id, *args, **kwargs):
        if cb_id in self.callback_dict:
            logger.info(f'Find the callback: {cb_id}')
            loop = get_event_loop()
            task = asyncio.run_coroutine_threadsafe(self.callback_dict[cb_id](), loop)
            task.result()

    def broadcast(self, info, *args, **kwargs):
        if info in self.broadcast_dict:
            logger.info(f'Find the callback: {info}')
            loop = get_event_loop()
            for cb in self.broadcast_dict[info]:
                task = asyncio.run_coroutine_threadsafe(cb(), loop)
                task.result()

def init_callback():
    global global_callback
    if global_callback is None:
        global_callback = Callback()
    return global_callback

def get_callback():
    global global_callback
    return global_callback

# 会话管理器
class WebSocketClient:
    def __init__(self, uri: str, event_list: list):
        self.uri = uri
        self.event_list = event_list
        self.subscribe_event_msg_id_list = [None for _ in event_list]
        self.failed_event_list = []
        self.session_id = None
        self.get_session_id_msg_id = None
        self.websocket = None
        self.connect_lock = threading.Lock()
        self.connected = False
        self.reconnect_interval = 5  # 重连间隔（秒）
        self.condition = asyncio.Event()
        self.init_index = True
        self.sync_msg_response = {}
        self.sync_msg_condition = {}

    async def connect(self):
        with self.connect_lock:
            if self.connected:
                return
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info(f'Connected to {self.uri}')
            await self.getSessionID()
            for i in range(len(self.event_list)):
                msg_id = await self.subscribeEvent(self.event_list[i])
                self.subscribe_event_msg_id_list[i] = msg_id
                
    async def sendMessage(self, method: str, params=None):
        logger.info('Start to send message.')
        if self.websocket and self.connected:
            msg_id = str(uuid.uuid4())
            message = json.dumps({
                'id': msg_id,
                'method': method, 
                'params': [params] if params else [], 
                'jsonrpc':'2.0'
            })
            await self.websocket.send(message)
            logger.info(f'Sent message: {message}')
            if method == 'crealand-api-transfer':
                return params['bridgeMsg']['id']
            else:
                return msg_id
        else:
            return None

    async def subscribeEvent(self, event_name: str):
        logger.info(f'Start to subscribe the event {event_name}.')
        return await self.sendMessage('rpc.on', event_name)
    
    async def unsubscribeEvent(self, event_name: str):
        logger.info(f'Start to unsubscribe the event {event_name}.')
        return await self.sendMessage('rpc.off', event_name)

    async def getSessionID(self):
        logger.info('Start to get session id.')
        msg_id = await self.sendMessage('crealand-get-sessionid')
        self.get_session_id_msg_id = msg_id

    async def sendToCrealandApiTransferAsync(self, dest: str, session_id: str, bridge_msg: dict):
        logger.info('Send message to crealand-api-transfer asynchronously.')
        params = {
            'method': 'call',
            'src' : 'sdk',
            'dest' : dest,
            'bridgeMsg': bridge_msg,
            'sessionID': session_id
        }
        if await self.sendMessage('crealand-api-transfer', params):
            return True
        else:
            return False

    async def sendToCrealandApiTransfer(self, dest: str, session_id: str, bridge_msg: dict):
        logger.info('Send message to crealand-api-transfer synchronously.')
        params = {
            'method': 'call',
            'src' : 'sdk',
            'dest' : dest,
            'bridgeMsg': bridge_msg,
            'sessionID': session_id
        }
        msg_id = await self.sendMessage('crealand-api-transfer', params)
        logger.info(msg_id)
        self.sync_msg_response[msg_id] = None
        self.sync_msg_condition[msg_id] = asyncio.Event()
        await self.sync_msg_condition[msg_id].wait()
        return self.sync_msg_response[msg_id]

    async def listen(self):
        try:
            msg_response_id = None
            msg_response = None
            is_success = False
            async for message in self.websocket:
                data = json.loads(message)
                logger.info(f'Received message: {data}')
                if 'id' in data:
                    if data['id'] == self.get_session_id_msg_id:
                        if 'result' in data:
                            logger.info(f'Received session_id: {data["result"]}')
                            self.session_id = data['result']
                        else:
                            logger.info('Fail to get the session_id.')
                            await asyncio.sleep(self.reconnect_interval)
                            await self.getSessionID()
                    elif data['id'] in self.subscribe_event_msg_id_list:
                        index = self.subscribe_event_msg_id_list.index(data['id'])
                        event_name = self.event_list[index]
                        if 'result' in data:
                            if event_name in data['result'] and data['result'][event_name] == 'ok':
                                logger.info(f'Subscribed to the event {event_name}')
                                if event_name in self.failed_event_list:
                                    self.failed_event_list.remove(event_name)
                            else:
                                logger.info(f'Fail to subscribe the event {event_name}')
                                self.failed_event_list.append(event_name)
                                await asyncio.sleep(self.reconnect_interval)
                                msg_id = await self.subscribeEvent(event_name)
                                self.subscribe_event_msg_id_list[index] = msg_id
                        else:
                            logger.info(f'Fail to subscribe the event {event_name}')
                            self.failed_event_list.append(event_name)
                            await asyncio.sleep(self.reconnect_interval)
                            msg_id = await self.subscribeEvent(event_name)
                            self.subscribe_event_msg_id_list[index] = msg_id
                elif 'notification' in data:
                    if data['notification'] in self.event_list:
                        if ('params' in data and len(data['params']) > 0 
                            and 'bridgeMsg' in data['params'][0] 
                            and 'id' in data['params'][0]['bridgeMsg']
                            and 'code' in data['params'][0]['bridgeMsg']):
                            if data['params'][0]['bridgeMsg']['code'] == 0:
                                if 'data' in data['params'][0]['bridgeMsg']:
                                    #logger.info(f'Received event {data["notification"]} params: {data["params"][0]["bridgeMsg"]["id"]}')
                                    msg_response_id = data['params'][0]['bridgeMsg']['id']
                                    msg_response = data['params'][0]['bridgeMsg']['data']
                                    if ('type' in data['params'][0]['bridgeMsg']['data']
                                        and data['params'][0]['bridgeMsg']['data']['type'] == 'trigger'):
                                            is_success = True
                            else:
                                if 'msg' in data['params'][0]['bridgeMsg']:
                                    msg_response_id = data['params'][0]['bridgeMsg']['id']
                                    msg_response = data['params'][0]['bridgeMsg']['msg']
                        elif (msg_response_id and 'params' in data and len(data['params']) > 0
                            and 'msgId' in data['params'][0] and 'msgEnd' in data['params'][0]
                            and data['params'][0]['msgId'] == msg_response_id
                            and data['params'][0]['msgEnd']):
                                logger.info(f'message id: {msg_response_id}')
                                if is_success:
                                    logger.info('Trigger the callback')
                                    api_callback = get_callback()
                                    api_callback.trigger(msg_response_id, msg_response)
                                    is_success = False
                                if (msg_response_id in self.sync_msg_response 
                                    and msg_response_id in self.sync_msg_condition):
                                    self.sync_msg_response[msg_response_id] = msg_response
                                    self.sync_msg_condition[msg_response_id].set()

                                msg_response_id = None
                                msg_response = None

                if self.init_index and self.session_id and len(self.failed_event_list) == 0:
                    self.init_index = False
                    self.condition.set()
        except websockets.ConnectionClosed:
            logger.error('WebSocket connection closed, attempting to reconnect...')
            self.connected = False
            await self.reconnect()

    async def reconnect(self):
        while not self.connected:
            with self.connect_lock:
                if not self.connected:
                    await asyncio.sleep(self.reconnect_interval)
                    await self.connect()

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info('WebSocket connection closed')

def init_event_loop():
    global global_event_loop
    if global_event_loop is None:
        global_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(global_event_loop)
    return global_event_loop

def get_event_loop():
    global global_event_loop
    return global_event_loop

def get_ws_client():
    global global_ws_client
    return global_ws_client

def get_listen_task():
    global global_listen_task
    return global_listen_task

async def ws_connect_async():
    global global_ws_client
    #uri = 'ws://10.10.18.78:29080'
    uri = 'ws://10.10.18.153:29080'
    event_list = ['crealand-event-oncall-sdk']
    global_ws_client = WebSocketClient(uri, event_list)
    # 尝试连接并订阅事件
    await global_ws_client.connect()
    # 在后台监听事件
    global global_listen_task
    global_listen_task = asyncio.create_task(global_ws_client.listen())
    # 阻塞直到获取session_id和订阅事件成功
    await global_ws_client.condition.wait()

def ws_connect():
    # 获取全局事件循环
    loop = init_event_loop()
    loop.run_until_complete(ws_connect_async())
    loop.run_forever()
    
def ws_close():
    task = get_listen_task()
    if task:
        task.cancel()
    loop = get_event_loop()
    if loop:
        loop.stop()
        while True:
            if not loop.is_running():
                ws_client = get_ws_client()
                # for i in range(len(ws_client.event_list)):
                #     loop.run_until_complete(ws_client.unsubscribeEvent(ws_client.event_list[i]))
                loop.run_until_complete(ws_client.close())
                loop.close()
                break
