import asyncio
import uuid
from typing import Literal
from utils.websocket_client import get_ws_client, get_event_loop, get_callback
from logger_setup import setup_logger

logger = setup_logger()


# 限制参数值范围
def value_range(
    val: float,
    min: float = float("-inf"),
    max: float = float("-inf"),
):
    if val < min:
        val = min
    elif val > max:
        val = max
    return val


def Handle_point(value: tuple):
    result = {"id": value[0]}
    if value[1] != None:
        result["name"] = value[1]
    return result


# call API
def call_api(dest: Literal["web-ide", "unity"], func_name: str, func_args: list):
    logger.info(dest, func_name, func_args)
    bridge_msg = {
        "id": str(uuid.uuid4()),
        "func": func_name,
        "args": func_args if func_args else [],
        "callback": "callbackName",
    }

    loop = get_event_loop()
    ws_client = get_ws_client()
    task = asyncio.run_coroutine_threadsafe(
        ws_client.sendToCrealandApiTransfer(dest, ws_client.session_id, bridge_msg),
        loop,
    )
    result = task.result()
    return result


def call_api_async(
    dest: Literal["web-ide", "unity"], func_name: str, func_args: list, callback
):
    logger.info(dest, func_name, func_args, callback.__name__)
    bridge_msg_id = str(uuid.uuid4())
    bridge_msg = {
        "id": bridge_msg_id,
        "func": func_name,
        "args": func_args if func_args else [],
        "callback": "callbackName",
    }

    loop = get_event_loop()
    ws_client = get_ws_client()
    task = asyncio.run_coroutine_threadsafe(
        ws_client.sendToCrealandApiTransferAsync(
            dest, ws_client.session_id, bridge_msg
        ),
        loop,
    )
    result = task.result()
    if callback:
        event_callback = get_callback()
        event_callback.registerCallback(bridge_msg_id, callback)

    return result
