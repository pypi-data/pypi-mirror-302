from core.bridge.interface import call_api, call_api_async
from core.websocket.websocket_client import get_callback
from logger_setup import setup_logger

logger = setup_logger()

def test_call_api():
    response = call_api('web-ide', 'apis.sayHello', ['hello'])
    logger.info(f'call_api response: {response}')

def test_call_api_async(callback):
    def event_cb(err, data):
        try:
            logger.info(f'Trigger the event callback. err: {err}, data: {data}')
            if 'type' in data:
                logger.info('This is an event trigger.')
                if data['type'] == 'trigger':
                    logger.info('The type is trigger.')
                    callback(err, data)
            else:
                logger.info('This is an api trigger.')
                callback(err, data)
            logger.info('Finished!')
        except Exception as e:
            logger.error(f'{e}')

    response = call_api_async('web-ide', 'apis.sayHello', ['hello'], event_cb)
    if response:
        logger.info('call_api response: True')
    else:
        logger.info('call_api response: False')
