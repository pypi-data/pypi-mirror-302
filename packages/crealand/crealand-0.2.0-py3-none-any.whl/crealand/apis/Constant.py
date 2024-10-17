# call api 通信
from enum import Enum


class DestType(Enum):
    UNITY = "unity"
    WEB_IDE = "web-ide"


# 键盘按键
class KeyboardType:
    SHIFT_LEFT = "ShiftLeft"
    SHIFT_RIGHT = "ShiftRight"
    Control_Left = "ControlLeft"
    Control_Right = "ControlRight"
    SPACE = "Space"
    Arrow_Up = "ArrowUp"
    Arrow_Down = "ArrowDown"
    Arrow_Left = "ArrowLeft"
    Arrow_Right = "ArrowRight"
    A = "KeyA"
    B = "KeyB"
    C = "KeyC"
    D = "KeyD"
    E = "KeyE"
    F = "KeyF"
    G = "KeyG"
    H = "KeyH"
    I = "KeyI"
    J = "KeyJ"
    K = "KeyK"
    L = "KeyL"
    M = "KeyM"
    N = "KeyN"
    O = "KeyO"
    P = "KeyP"
    Q = "KeyQ"
    R = "KeyR"
    S = "KeyS"
    T = "KeyT"
    U = "KeyU"
    V = "KeyV"
    W = "KeyW"
    X = "KeyX"
    Y = "KeyY"
    Z = "KeyZ"
    DIGIT_0 = "Digit0"
    DIGIT_1 = "Digit1"
    DIGIT_2 = "Digit2"
    DIGIT_3 = "Digit3"
    DIGIT_4 = "Digit4"
    DIGIT_5 = "Digit5"
    DIGIT_6 = "Digit6"
    DIGIT_7 = "Digit7"
    DIGIT_8 = "Digit8"
    DIGIT_9 = "Digit9"
    NUM_0 = "Numpad0"
    NUM_1 = "Numpad1"
    NUM_2 = "Numpad2"
    NUM_3 = "Numpad3"
    NUM_4 = "Numpad4"
    NUM_5 = "Numpad5"
    NUM_6 = "Numpad6"
    NUM_7 = "Numpad7"
    NUM_8 = "Numpad8"
    NUM_9 = "Numpad9"


# 鼠标按键动作
class KeyActiveType:
    KEY_DOWN = "keydown"
    KEY_UP = "keyup"


# 键盘按键动作
class KeyboardActiveType:
    KEY_DOWN = "keydown"
    KEY_UP = "keyup"
    KEY_PRESS = "keypress"


# 鼠标按键
class MouseKeyType:
    LEFT = 0
    RIGHT = 1
    MIDDLE = 2


# 挂点
class HangPointType:
    BOTTOM = 1
    CAMERA = 2
    LEFT_FRONT_WHEEL = 3
    RIGHT_FRONT_WHEEL = 4
    LEFT_HAND = 10
    RIGHT_HAND = 11
    ITEM_HANGING_POINT = 100
    CAMERA_FOLLOW_POINT = 1000
    TOP = 2000


# 角色动作
class Actions:

    PICK = "Pick"
    PLACE = "Place"
    LAUGH = "Laugh"
    HAPPY = "Happy"
    THINK = "Think"
    CONFUSE = "Confuse"
    SAD = "Sad"
    TALK = "Talk"
    GREET = "Greet"
    NO = "No"
    YES = "Yes"
    LOOKAROUND = "LookAround"
    APOLOGIZE = "Apologize"
    APPLAUD = "Applaud"
    BOW = "Bow"
    ANGRY = "Angry"
    FAINT = "Faint"
    ARMRESET = "ArmReset"
    DOWNPICK = "DownPick"
    UPPICK = "UpPick"
    REPAIR = "Repair"
    STANDGUARD = "StandGuard"


# 三维坐标值
class Axis:
    X = "X"
    Y = "Y"
    Z = "Z"


# 坐标类型 本地坐标或世界坐标
class AxisType:
    LOCAL = "local"
    WORLD = "world"


# 说话语气
class Tone:
    BOBO_ANGRY = "img_bobo_angry.png"
    BOBO_EXPRESSION = "img_bobo_expression.png"
    BOBO_SADNESS = "img_bobo_sadness.png"
    BOBO_SHY = "img_bobo_shy.png"
    BOBO_SMILE = "img_bobo_smile.png"
    BOBO_SURPRISE = "img_bobo_surprise.png"
    UU_ANGRY = "img_UU_angry.png"
    UU_EXPRESSION = "img_UU_expression.png"
    UU_SADNESS = "img_UU_sadness.png"
    UU_SHY = "img_UU_shy.png"
    UU_SMILE = "img_UU_smile.png"
    UU_SURPRISE = "img_UU_surprise.png"
    X_ANGRY = "img_x_angry.png"
    X_EXPRESSION = "img_x_expression.png"
    X_SADNESS = "img_x_sadness.png"
    X_SHY = "img_x_shy.png"
    X_SMILE = "img_x_smile.png"
    X_SURPRISE = "img_x_surprise.png"
    Y_ANGRY = "img_y_angry.png"
    Y_SADNESS = "img_y_expression.png"
    Y_SADNESS = "img_y_sadness.png"
    Y_SHY = "img_y_shy.png"
    Y_SMILE = "img_y_smile.png"
    Y_SURPRISE = "img_y_surprise.png"


# 音量大小
class Volume:
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"


# 立绘对话选项
class OptionName:
    OPTION01 = "option1"
    OPTION02 = "option2"
    OPTION03 = "option3"


# 提示面板展示内容
class ResultType:
    SUCCESS = "success"
    FAIL = "fail"
    START = "start"


# Toast提示位置
class ToastPosition:
    TOP = "top"
    BOTTOM = "bottom"
    MIDDLE = "middle"


# Toast提示状态
class ToastState:
    DYNAMIC = "dynamic"
    STATIC = "static"


# 手势方向
class Direction:
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


# 滤镜类型
class FilterStyle:
    FOG = "fog"


# 对象的动作
class ActionType:
    ENTER = "enter"
    LEAVE = "leave"
