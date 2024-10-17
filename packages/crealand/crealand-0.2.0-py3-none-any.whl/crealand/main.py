import threading

from apis.Constant import KeyActiveType, KeyboardType, HangPointType
from utils.test_call_api import test_call_api, test_call_api_async
from utils.event import onInputsKeyboardEvent, onSensorUltrasonicEvent
from utils.websocket_client import ws_connect, ws_close, get_ws_client, init_callback
from logger_setup import setup_logger

logger = setup_logger()

def callback():
    logger.info('test')

# 主函数
def main():
    try:
        threading.Thread(target=ws_connect, args=()).start()
        while True:
            ws_client = get_ws_client()
            if ws_client and ws_client.session_id:
                break
        init_callback()
        #test_call_api()
        #test_call_api_async()
        #onInputsKeyboardEvent(KeyActiveType.KEY_DOWN, KeyboardType.Arrow_Down, callback)
        onSensorUltrasonicEvent(1, (HangPointType.BOTTOM), '<=', 10.0, callback)
        while True:
            pass
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    finally:
        logger.info('Start to execute the close function.')
        ws_close()
        logger.info('Close function has finished.')

# 运行主函数
if __name__ == "__main__":
    main()
