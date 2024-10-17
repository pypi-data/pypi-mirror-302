__version__ = '0.1.0'

from crealand.apis import *
from crealand.utils import *

import threading

from crealand.core.websocket.websocket_client import ws_connect, ws_close, get_ws_client, init_callback
from crealand.logger_setup import setup_logger

logger = setup_logger()

def initialize():
    try:
        threading.Thread(target=ws_connect, args=()).start()
        while True:
            ws_client = get_ws_client()
            if ws_client and ws_client.session_id:
                break
        init_callback()
    except Exception as e:
        logger.error(f'An error occurred: {e}')

initialize()

