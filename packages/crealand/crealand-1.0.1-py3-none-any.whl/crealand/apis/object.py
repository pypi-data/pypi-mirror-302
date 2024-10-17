from typing import Dict, Literal, Union
from utils.utils import call_api, call_api_async
from constant import DestType, FilterStyle


# 信息
class Info:

    # 别名对象id
    @staticmethod
    def get_alias_id(
        nickname: str = "别名1",
    ):
        result = call_api(
            DestType.UNITY, DestType.UNITY + "alias.getByAlias", [nickname]
        )
        return result

    # 获取configID的对象id
    @staticmethod
    def get_object_id(runtime_id) -> int:
        result = call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.getConfigID",
            {"runtime_id": runtime_id},
        )
        return result

    # 获取对象的空间坐标crealand.apis.Object
    @staticmethod
    def get_object_coordinates(runtime_id: int) -> list[float]:
        result = call_api(
            DestType.UNITY, DestType.UNITY + "actor.getCoordinate", [runtime_id]
        )
        return result

    # 获取判定区域中的对象id
    @staticmethod
    def get_id_in_area(area_id: int, config_ids: list[str]) -> list[int]:
        result = call_api(
            DestType.UNITY,
            DestType.UNITY + "editableTrigger.getEnterTriggerIDs",
            [area_id, config_ids],
        )
        return result

    # 获取空间坐标某个轴的值
    @staticmethod
    def get_spatial_coordinates(coordinate: list[float], axis: str) -> float:
        AXIS = {"X": 0, "Y": 1, "Z": 2}
        return coordinate[AXIS[axis]]

    # 获取对象的运动方向向量
    @staticmethod
    def get_motion_vector(runtime_id: int) -> list[float]:
        result = call_api(
            DestType.UNITY, DestType.UNITY + "character.getMoveDirection", [runtime_id]
        )
        return result


class Camera:

    # 获取相机ID
    @classmethod
    def get_default_id(self):
        return call_api_async(
            DestType.UNITY, DestType.UNITY + DestType.UNITY + "camera.getDefaultID"
        )

    # 获取空间坐标
    @classmethod
    def get_object_coordinates(self, runtime_id: int) -> list[float]:
        result = call_api(
            DestType.UNITY, DestType.UNITY + "actor.getCoordinate", [runtime_id]
        )
        return result

    # 相机移动
    @classmethod
    def move_to(self, time: float, coordinate: list[float], block: bool):
        new_time = max(0, time)
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.moveTo",
            [self.get_default_id(), new_time, coordinate, block],
        )

    # 调整FOV
    @classmethod
    def adjust_FOV(self, time: float, fov: float):
        new_time = max(0, time)
        new_fov = max(60, min(fov, 120))
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.adjustFOV",
            [self.get_default_id(), new_time, new_fov],
        )

    # 相机锁定朝向并移动
    @classmethod
    def move_while_looking(
        self,
        coordinate_1: list[float],
        time: float,
        coordinate_2: list[float],
        block: bool,
    ):
        new_time = max(0, time)
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.moveWhileLooking",
            [self.get_default_id(), new_time, coordinate_2, coordinate_1, block],
        )

    # 获取相机坐标
    @classmethod
    def get_camera_coordinate(self) -> list[float]:
        result = self.get_object_coordinates(self.get_default_id())
        return result

    # 相机朝向
    @classmethod
    def look_at(self, coordinate: list[float]):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.lookAt",
            [self.get_default_id(), coordinate],
        )

    # 相机跟随
    @classmethod
    def follow_target(self, runtime_id: int, distance: float, is_rotate: bool):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.followTarget",
            [self.get_default_id(), runtime_id, distance, is_rotate],
        )

    # 相机结束跟随
    @classmethod
    def end_follow_target(self):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.stopFollowing",
            [
                self.get_default_id(),
            ],
        )

    # 相机 滤镜
    @classmethod
    def filters(self, filter_name: str, state: bool):
        CAMERA_EFFECTS = {"fog": 1}
        STATES = {"start": True, "stop": False}
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "camera.openEffect",
            [self.get_default_id(), CAMERA_EFFECTS[filter_name], STATES[state]],
        )


class Motion:
    # 创建对象
    @classmethod
    def create_object_coordinate(self, config_id: str, coordinate: list[float]):
        result = call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.createObject",
            [config_id, coordinate],
        )

    # 测距
    @staticmethod
    def ray_ranging(runtime_id: int, attachment_id: int):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.rayRanging",
            [runtime_id, attachment_id, 20],
        )

    # 移动
    @staticmethod
    def move_to(runtime_id: int, coordinate: list[float]):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.setObjectPosition",
            [
                runtime_id,
                coordinate,
            ],
        )

    # 朝向
    @staticmethod
    def face_towards(runtime_id: int, coordinate: list[float]):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.setObjectTowardPosition",
            [
                runtime_id,
                coordinate,
            ],
        )

    # 前进
    @staticmethod
    def move_forward(
        runtime_id: int, speed: float, distance: float, block: bool = False
    ):
        new_speed = max(1, min(speed, 5))
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.moveForwardByDistance",
            [
                runtime_id,
                new_speed,
                distance,
                block,
            ],
        )

    # 对象旋转
    @staticmethod
    def rotate(runtime_id: int, time: float, angle: float, block: bool = False):
        new_time = max(time, 0)
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.rotateUpAxisByAngle",
            [
                runtime_id,
                angle,
                new_time,
                block,
            ],
        )

    # 云台旋转 & 机械臂旋转
    @staticmethod
    def ptz(runtime_id: int, angle: float, block: bool = False):
        print(block)
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.rotatePTZUpAxisByAngle",
            [runtime_id, angle, abs(angle) / 30, block],
        )

    # 播放动作
    @staticmethod
    def action(runtime_id: int, action: str, block: bool = False):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.playAnimation",
            [runtime_id, action, block],
        )

    # # 将对象吸附到挂点
    # @staticmethod
    # def attach_to_anchor_point(adsorbed_id: int, adsorb_id: int, attachment_id: int):
    #     call_api_async(
    #         DestType.UNITY,
    #         DestType.UNITY + "actor.attach",
    #         [adsorbed_id, adsorb_id, attachment_id],
    #     )

    # 绑定挂点
    @staticmethod
    def bind_to_object_point(
        runtime_id_1: int,
        attachment_id_1: str,
        runtime_id_2: int,
        attachment_id_2: str,
    ):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.bindAnchor",
            [runtime_id_1, attachment_id_1, runtime_id_2, attachment_id_2],
        )

    def bind_to_object_point11(
        runtime_id_1: int,
        attachment_id_1: Dict[Literal["attach_id", "attach_name"] : Union[int, str]],
        runtime_id_2: int,
        attachment_id_2: Dict[Literal["id", "attachment_id_1"] : Union[int, str]],
    ):
        pass

    bind_to_object_point11({"A": 1, "B": 1})

    # 解除绑定
    @staticmethod
    def detach(runtime_id: int):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.detach",
            [
                runtime_id,
            ],
        )

    # 向画面空间前进
    @staticmethod
    def move_towards_screen_space(
        runtime_id: int, speed: float = 1, direction: list[float] = [0, 0, 1]
    ):
        new_speed = max(1, min(speed, 5))
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.moveByVelocity",
            [
                runtime_id,
                new_speed,
                2,
                direction,
            ],
        )

    # 旋转运动方向向量
    @staticmethod
    def rotate_to_direction(
        runtime_id: int, angle: float = 0, direction: list[float] = [0, 0, 1]
    ):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "actor.rotateUpAxisByDirection",
            [runtime_id, angle, direction, False],
        )

    # 停止运动
    @staticmethod
    def stop(runtime_id: int):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "character.stop",
            [runtime_id],
        )

    # 设置别名
    @classmethod
    def create_object(
        self,
        config_id: int,
        nickname: str,
        coordinate: list[float] = [0, 0, 1],
    ):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "alias.setAlias",
            [
                nickname,
                self.create_object_coordinate(config_id, coordinate),
            ],
        )

    # 销毁对象
    @staticmethod
    def destroy(runtime_id: int):
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "alias.destoryObject",
            [
                runtime_id,
            ],
        )

    # 上升
    @staticmethod
    def rise(
        runtime_id: int, speed: float = 3, height: float = 10, block: bool = False
    ):
        new_speed = max(1, min(speed, 5))
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "alias.moveUpByDistance",
            [runtime_id, height, new_speed, block],
        )

    # 获取离自身距离的坐标
    @staticmethod
    def get_object_local_position(
        runtime_id: int, coordinate: list[float] = [1, 2, 3], distance: float = 0
    ):
        result = call_api_async(
            DestType.UNITY,
            DestType.UNITY + "alias.getObjectLocalPosition",
            [runtime_id, coordinate, distance],
        )
        return result

    # 移动到指定坐标
    @staticmethod
    def move_by_point(
        runtime_id: int, time: float, coordinate: list[float], block: bool = False
    ):
        new_time = max(time, 0)
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "alias.moveByPoint",
            [runtime_id, new_time, coordinate, block],
        )

    # 绕坐标轴旋转
    @staticmethod
    def rotate_by_origin_and_axis(
        runtime_id: int,
        time: float,
        point_1: str,
        coordinate_1: list[float],
        point_2: str,
        coordinate_2: list[float],
        angle: float,
        block: bool = False,
    ):
        new_time = max(time, 0)
        call_api_async(
            DestType.UNITY,
            DestType.UNITY + "alias.rotateByOringinAndAxis",
            [
                runtime_id,
                coordinate_1,
                point_1,
                coordinate_2,
                point_2,
                angle,
                new_time,
                block,
            ],
        )


class Property:
    # 新增自定义属性
    @staticmethod
    def add_attr(runtime_id: int, attr_name: str, attr_value: str):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.addCustomProp",
            [runtime_id, attr_name, attr_value],
        )

    # 删除自定义属性
    @staticmethod
    def del_attr(runtime_id: int, attr_name: str):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.delCustomProp",
            [runtime_id, attr_name],
        )

    # 修改自定义属性
    @staticmethod
    def set_attr(runtime_id: int, attr_name: str, attr_value: str):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.setCustomProp",
            [runtime_id, attr_name, attr_value],
        )

    # 获取自定义属性的值
    @staticmethod
    def get_value(runtime_id: int, attr_name: str):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.getCustomProp",
            [runtime_id, attr_name],
        )

    # 获取自定义属性组中某一项的值
    @staticmethod
    def get_value_by_Idx(runtime_id: int, index: int):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.getCustomPropValueByIdx",
            [runtime_id, index],
        )

    # 获取自定义属性组中某一项的名称
    @staticmethod
    def get_key_by_Idx(runtime_id: int, index: int):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.getCustomPropKeyByIdx",
            [runtime_id, index],
        )


class Show:
    # 3d文本
    # @staticmethod def set_3D_text_status_rgb( runtime_id: int, color: str, size: int, text: str):
    #
    #     if color[0] == '#':
    #         color = webcolors.hex_to_rgb(color)
    #         color = webcolors.name_to_hex(color)
    #     else:
    #         color = webcolors.name_to_hex(color)
    #         color = webcolors.hex_to_rgb(color)
    #
    #     print(webcolors.hex_to_name("#daa520"), color[0], {'R': color[0], 'G': color[1], 'B': color[2]})

    # 3d文本-RGB
    @staticmethod
    def set_3D_text_status_rgb(runtime_id: int, rgb: list[int], size: int, text: str):
        call_api(
            DestType.UNITY,
            DestType.UNITY + "actor.set3DTextStatus",
            [runtime_id, rgb, size, text],
        )


class Object:
    @classmethod
    def __init__(self):
        self.Info = Info()
        self.Camera = Camera()
        self.Motion = Motion()
        self.Property = Property()
        self.Show = Show()


Object = Object()

# print(Object.Info.get_alias_id())
