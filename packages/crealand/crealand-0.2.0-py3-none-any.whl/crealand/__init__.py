__version__ = '0.1.0'

from crealand.apis import *
from crealand.utils import *

import threading

from crealand.utils.websocket_client import ws_connect, ws_close, get_ws_client
from logger_setup import setup_logger

logger = setup_logger()

def initialize():
    try:
        threading.Thread(target=ws_connect, args=()).start()
        while True:
            ws_client = get_ws_client()
            if ws_client and ws_client.session_id:
                break
        while True:
            pass
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    finally:
        logger.info('Start to execute the close function.')
        ws_close()
        logger.info('Close function has finished.')

initialize()

