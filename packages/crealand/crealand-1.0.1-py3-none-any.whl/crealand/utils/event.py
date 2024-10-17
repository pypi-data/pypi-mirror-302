import asyncio
import uuid
from typing import Literal
from utils.websocket_client import get_ws_client, get_event_loop, get_callback
from logger_setup import setup_logger

logger = setup_logger()

def sendMsg(func_name, func_args, dest, cb):
    ws_client = get_ws_client()
    bridge_msg_id = str(uuid.uuid4())
    logger.info(f'callback id: {bridge_msg_id}')
    bridge_msg = {
        'id': bridge_msg_id,
        'func': func_name,
        'args': func_args if func_args else [],
        'callback': 'callbackName'
    }
    params = {
        'method': 'call',
        'src' : 'sdk',
        'dest' : dest,
        'bridgeMsg': bridge_msg,
        'sessionID': ws_client.session_id
    }
    
    loop = get_event_loop()
    task = asyncio.run_coroutine_threadsafe(ws_client.sendMessage('crealand-api-transfer', params), loop)
    result = task.result()
    if cb:
        event_callback = get_callback()
        event_callback.registerCallback(bridge_msg_id, cb)
    return result

def onBroadcastEvent(info, cb):
    event_callback = get_callback()
    event_callback.registerBroadcast(info, cb)

def sendBroadcast(info):
    event_callback = get_callback()
    event_callback.broadcast(info)

# Crealand IDE-WEB
def onInputsMouseEvent(click, button, cb):
    func_args = [
        'InputsMouseEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'click', 
                'type': 'and', 
                'conditions': {
                    '==': click
                }}, {
                'name': 'button', 
                'type': 'and', 
                'conditions': {
                    '==': button
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')
    

def onInputsKeyboardEvent(click, button, cb):
    logger.info(f'callback name: {cb.__name__}')
    func_args = [
        'InputsKeyboardEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'click', 
                'type': 'and', 
                'conditions': {
                    '==': click
                }}, {
                'name': 'button', 
                'type': 'and', 
                'conditions': {
                    '==': button
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onAIFigureEvent(number, cb):
    func_args = [
        'AIFigureEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'number', 
                'type': 'and', 
                'conditions': {
                    '==': number
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onAIGestureEvent(direction, cb):
    func_args = [
        'AIGestureEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'direction', 
                'type': 'and', 
                'conditions': {
                    '==': direction
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onAIAsrEvent(text, cb):
    func_args = [
        'AIAsrEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'text', 
                'type': 'and', 
                'conditions': {
                    '==': text
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onSoundDecibelEvent(decibel_value, cb):
    func_args = [
        'SoundDecibelEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'decibel_value', 
                'type': 'and', 
                'conditions': {
                    '==': decibel_value
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onSensorSoundEvent(compare, decibel_value, cb):
    func_args = [
        'SensorSoundEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'decibel_value', 
                'type': 'and', 
                'conditions': {
                    compare: decibel_value
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        dest='web-ide', 
        cb=cb
    )
    logger.info(f'result: {result}')

# Crealand IDE-3D
def onAreaObjectEvent(runtime_id, action, area_id, cb):
    func_args = [
        runtime_id, 
        action, 
        area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    result = sendMsg(
        func_name='editableTrigger.onEventRuntimeIdTrigger', 
        func_args=func_args, 
        dest='unity', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onAreaClassEvent(config_id, action, area_id, cb):
    func_args = [
        config_id, 
        action, 
        area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    result = sendMsg(
        func_name='editableTrigger.onEventConfigIdTrigger', 
        func_args=func_args, 
        dest='unity', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onSensorUltrasonicEvent(runtime_id, attachment_id, compare, distance, cb):
    func_args = [
        runtime_id, 
        attachment_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'distance', 
                'type': 'and', 
                'conditions': {
                    compare: distance
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='sensor.onEventRayRanging', 
        func_args=func_args, 
        dest='unity', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onSensorTemperatureEvent(temperature_sensor, compare, temperature, cb):
    func_args = [
        temperature_sensor, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'temperature', 
                'type': 'and', 
                'conditions': {
                    compare: temperature
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='sensor.onEventTemperature', 
        func_args=func_args, 
        dest='unity', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onSensorHumidityEvent(humidity_sensor, compare, humidity_value, cb):
    func_args = [
        humidity_sensor, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'humidity_value', 
                'type': 'and', 
                'conditions': {
                    compare: humidity_value
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='sensor.onEventHumidity', 
        func_args=func_args, 
        dest='unity', 
        cb=cb
    )
    logger.info(f'result: {result}')

def onSensorGravityEvent(gravity_sensor, compare, gravity_value, cb):
    func_args = [
        gravity_sensor, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'gravity_value', 
                'type': 'and', 
                'conditions': {
                    compare: gravity_value
                }}
            ]
        }
    ]
    result = sendMsg(
        func_name='sensor.onEventGravity', 
        func_args=func_args, 
        dest='unity', 
        cb=cb
    )
    logger.info(f'result: {result}')

def startTemperatureDetection(judge_area_id):
    func_args = [
        judge_area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    result = sendMsg(
        func_name='sensor.startTemperatureDetection', 
        func_args=func_args, 
        dest='unity', 
        cb=None
    )
    logger.info(f'result: {result}')

def startHumidityDetection(judge_area_id):
    func_args = [
        judge_area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    result = sendMsg(
        func_name='sensor.startHumidityDetection', 
        func_args=func_args, 
        dest='unity', 
        cb=None
    )
    logger.info(f'result: {result}')

