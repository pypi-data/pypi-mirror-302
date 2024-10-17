from crealand.utils.utils import call_api_async, call_api
from crealand.apis.Constant import (
    DestType,
    OptionName,
    ResultType,
    ToastPosition,
    ToastState,
    Volume,
)
from typing import Literal, Type


class Dialogue:

    # 立绘对话 初始化
    @staticmethod
    def init(self):
        call_api(DestType.WEB_IDE, "prepareDialogBoard", [{}])
        pass

    # 立绘对话 显示
    @staticmethod
    def show(
        obj_name: str,
        volume: str,
        content: str,
        url: str,
        tone: str,
    ):
        call_api(
            DestType.WEB_IDE,
            "showDialog",
            [
                {
                    "speaker": obj_name,
                    "type": volume,
                    "txt": content,
                    "voiceId": url,
                    "imgId": tone,
                }
            ],
        )

    # 立绘对话 设置选项
    @staticmethod
    def set_option(opt_name: str, content: str):
        options = {}
        options[opt_name] = content
        call_api(
            DestType.WEB_IDE,
            "setDialogOptions",
            [{"options": options}],
        )

        pass

    # 立绘对话 判断选项
    # @staticmethod
    # def check_options(self, opt_name: str = OptionName.OPTION01):
    #     result = call_api(DestType.WEB_IDE, "checkDialogOption", [opt_name])
    #     return True

    # 立绘对话 显示
    @staticmethod
    def set_options_show(is_show: bool = True):
        result = call_api(DestType.WEB_IDE, "toggleDialogBoard", [{"show": is_show}])
        return result.msg


class HelpPane:
    # 帮助面板 初始化
    @staticmethod
    def init():
        call_api(DestType.WEB_IDE, "prepareHelpboard", {})

    # 帮助面板 设置标题
    @staticmethod
    def set_title(title: str, url: str):
        call_api(
            DestType.WEB_IDE,
            "addHelpItem",
            [
                {
                    "title": title,
                    "imgId": url,
                }
            ],
        )

    # 帮助面板 显示
    @staticmethod
    def show(is_show: bool = True):
        call_api(
            DestType.WEB_IDE,
            "toggleHelpboard",
            [
                {
                    "show": is_show,
                }
            ],
        )


class TaskPane:

    # 任务面板 设置标题
    @staticmethod
    def set_task(title: str, nickname: str):
        call_api(
            DestType.WEB_IDE,
            "createTaskboard",
            [
                {
                    "title": title,
                    "alias": nickname,
                }
            ],
        )

    # 任务面板 设置任务项
    @staticmethod
    def set_task_progress(
        task_name: str, subtasks_content: str, completed_tasks: int, total_tasks: int
    ):
        call_api(
            DestType.WEB_IDE,
            "setTaskboard",
            [
                {
                    "alias": task_name,
                    "taskName": subtasks_content,
                    "process": [max(0, completed_tasks), max(1, total_tasks)],
                }
            ],
        )

    # 任务面板 显示
    @staticmethod
    def set_task_show(task_name: str, is_show: bool = True):
        call_api(
            DestType.WEB_IDE,
            "toggleTaskboard",
            [{"alias": task_name, "show": is_show}],
        )


class Speak:
    # 说
    @staticmethod
    def text(self, runtime_id: int, content: str, time: int):
        call_api_async(
            DestType.UNITY, DestType.UNITY + "actor.speak", [runtime_id, content, time]
        )

    # 说-img
    @staticmethod
    def speak_image(runtime_id: int, url: str, time: int):
        call_api_async(
            DestType.UNITY, DestType.UNITY + "actor.speakImage", [runtime_id, url, time]
        )


class Interactive:
    # 提示面板显示
    @staticmethod
    def set_tip_show(option: str = ResultType.START):
        call_api(
            DestType.WEB_IDE,
            "showTipboardResult",
            [
                {
                    "result": option,
                }
            ],
        )

    # 提示面板显示
    @staticmethod
    def set_toast(
        content: str,
        position: str = ToastPosition.TOP,
        state: str = ToastState.DYNAMIC,
    ):
        call_api(
            DestType.WEB_IDE,
            "toast",
            [
                {
                    "position": position,
                    "mode": state,
                    "txt": content,
                }
            ],
        )
