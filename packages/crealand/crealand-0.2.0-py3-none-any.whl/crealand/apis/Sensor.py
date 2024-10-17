from Constant import DestType,HangPointType
from utils.utils import call_api, call_api_async

# 超声波传感器

class Ultrasonic:
    _sensors = {}

    # 前端处理传感器信息绑定
    def add_sensor(self,sensor_name: str, runtime_id: int, attachment_id: int=HangPointType.BOTTOM) ->None:
        if not isinstance(sensor_name, str) or not isinstance(runtime_id, int) or not isinstance(attachment_id, int):
            raise ValueError("Invalid arguments: sensor_name must be a string, runtime_id and attachment_id must be integers.")
        self._sensors[sensor_name] = (runtime_id, attachment_id)

    def get_sensor(self,sensor_name: str) -> list[int]:
        if sensor_name in self._sensors:
            return self._sensors[sensor_name]
        else:
            raise KeyError(f"Sensor '{sensor_name}' not found")

    @staticmethod
    async def get_obstacle_distance(sensor: list[int])->float:
        # 假设 call_api 函数已经定义
        length = await call_api(DestType.UNITY, 'sensor.rayRanging', [sensor[0], sensor[1]])
        return length

    def sensor_on_ultrasonic(sensor: list[int],compare:str,value:float)->bool:
        if compare == '>' and value > await self.get_obstacle_distance(sensor):
            return True
        elif compare == '<' and value < await self.get_obstacle_distance(sensor):
            return True
        else:

class Auditory:

    _decibel_val=0

    # 获取声音强度
    def get_decibel_value(self):
        return 0

    # 开始分贝识别
    def start_decibel_recognition(self):
        # openDecibelDetectionPage
        call_api(DestType.WEB_IDE, 'openDecibelDetectionPage', [{'type':'open'}])

    # 结束分贝识别
    def stop_decibel_recognition(self):
        call_api(DestType.WEB_IDE, 'openDecibelDetectionPage', [{'type':'end'}])

    # 判断声音强度
    def check_decibel_value(self, compare: str, decibel_value: float):
        return 0


class Visual:
    _sensors = {}

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, sensor_name: str, runtime_id: int, attachment_id: int=HangPointType.BOTTOM):
        self._sensors[sensor_name] = (runtime_id, attachment_id)
        pass

    # 获取传感器信息
    def get_sensor_impl(self, sensor_name: str):
        return self._sensors[sensor_name]

    # 打开或关闭传感器画面
    def open_visual_sensor(self, action_type: bool=True,sensor: list[int]):
        if action_type:
            func_name = 'sensor.openVirsual'
        else:
            func_name = 'sensor.closeVirsual'
        call_api(DestType.UNITY,func_name,[sensor[0], sensor[1]])
        pass

    # 获取传感器信息
    def get_sensor(self, sensor_name: str):
        return self.get_sensor_impl(sensor_name)


class Temperature:

    _sensors = {}

    def __init__(self,sensor_name,id):
        self.data={sensor_name:sensor_name,id:id}

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, sensor_name: str, runtime_id: int, attachment_id: int=HangPointType.BOTTOM):
        self._sensors[sensor_name] = (runtime_id, attachment_id)
        call_api(DestType.UNITY,'sensor.attachTemperature',[runtime_id])
        pass
    
    # 获取传感器信息
    def get_sensor_impl(self,runtime_id: int):
        call_api(DestType.UNITY,'sensor.getTemperature',[runtime_id])
        return self._sensors[sensor_name]
    
    # 设置判定区域温度

    def set_temperature(self, area_id: int, temp_val: float):
        temp_val = max(-40, min(temp_val, 120))
        call_api(DestType.UNITY,'sensor.setTemperature',[area_id,temp_val])
        pass

    # 持续检测判定区域温度

    def continuously_monitor_temperature(self, area: int):
        pass

    # 获取温度值

    def get_temperature_value(self, temperature_sensor: list[int]):
        call_api(DestType.UNITY,'sensor.getTemperature',[temperature_sensor[0],temperature_sensor[1]])
        return 10



class Humidity:

    _sensors = {}

    def __init__(self):
        self.set_sensor = set_sensor_impl
        self.get_sensor = get_sensor_impl

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, sensor_name: str, runtime_id: int):
        self._sensors[sensor_name] = runtime_id
        pass
    
    # 获取传感器信息
    def get_sensor_impl(self, sensor_name: str):
        return self._sensors[sensor_name]

    # 设置判定区域湿度

    def set_humidity(self, area_id: int, humidity_val: float):
        call_api(DestType.UNITY,'sensor.setHumidity',[area_id,humidity_val])
        pass

    # 持续检测判定区域湿度

    def continuously_monitor_humidity(self, judge_area_id: int):
        pass

    # 获取湿度值

    def get_humidity_value(self, humidity_sensor: list[int]):
        call_api(DestType.UNITY,'sensor.getHumidity',[humidity_sensor[0],humidity_sensor[1]])
        return 10

    # 判断湿度值

    def check_humidity_value(self, humidity_sensor: dict, compare: str, humidity_value: float):
        humidity_value = max(0, min(humidity_value, 100))
        return 10


class Gravity:

    _sensors = {}

    def __init__(self):
        self.set_sensor = set_sensor_impl
        self.get_sensor = get_sensor_impl

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, sensor_name: str, area_id: int):
        self._sensors[sensor_name] = area_id
        call_api(DestType.UNITY,'sensor.attachGravity',[area_id])
        pass
    
    # 获取传感器信息
    def get_sensor_impl(self, sensor_name: str):
        return self._sensors[sensor_name]

    # 设置对象重力

    def set_gravity(self, runtime_id: str, gravity_value: float):
        sensor_info = self._sensors[sensor_name]
        gravity_value= max(0, min(gravity_value, 10000))
        call_api(DestType.UNITY,'sensor.setGravity',[sensor_info[0],gravity_value])
        pass

    # 获取重力值

    def get_gravity_value(self, sensor_info: dict):
        call_api(DestType.UNITY,'sensor.getGravity',[sensor_info[0]])
        return 10


class Sensor:
    def __init__(self):
        self.Ultrasonic = Ultrasonic()
        self.Auditory = Auditory()
        self.Visual = Visual()
        self.Temperature = Temperature()
        self.Humidity = Humidity()
        self.Gravity = Gravity()


Sensor = Sensor()

Sensor.Ultrasonic.add_sensor('sensor1', 1, 1)
Sensor.Ultrasonic.add_sensor('sensor2', 2, 2)

print(Sensor.Ultrasonic.get_sensor('sensor1'))
