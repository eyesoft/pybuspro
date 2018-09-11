from ..core.telegram import Telegram
from ..helpers.enums import OperateCode


class Control:
    def __init__(self, buspro):
        self._buspro = buspro
        self.subnet_id = None
        self.device_id = None

    @staticmethod
    def build_telegram_from_control(control):
        telegram = None
        print("build")
        if control is None:
            return None

        if type(control) == SingleChannelControl:
            telegram = Telegram()
            telegram.target_address = (control.subnet_id, control.device_id)
            telegram.operate_code = OperateCode.SingleChannelControl
            telegram.payload = [control.channel_number, control.channel_level,
                                control.running_time_minutes, control.running_time_seconds]
        elif type(control) == SceneControl:
            telegram = Telegram()
            telegram.target_address = (control.subnet_id, control.device_id)
            telegram.operate_code = OperateCode.SceneControl
            telegram.payload = [control.area_number, control.scene_number]
        elif type(control) == ReadStatusOfChannels:
            telegram = Telegram()
            telegram.target_address = (control.subnet_id, control.device_id)
            telegram.operate_code = OperateCode.ReadStatusOfChannels
            telegram.payload = []
        elif type(control) == GenericControl:
            telegram = Telegram()
            telegram.target_address = (control.subnet_id, control.device_id)
            telegram.operate_code = control.operate_code
            telegram.payload = control.payload

        return telegram

    @property
    def telegram(self):
        return self.build_telegram_from_control(self)

    async def send(self):
        telegram = self.telegram
        await self._buspro.network_interface.send_telegram(telegram)


class GenericControl(Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.payload = None
        self.operate_code = None


class SingleChannelControl(Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.channel_number = None
        self.channel_level = None
        self.running_time_minutes = None
        self.running_time_seconds = None


class SceneControl(Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.area_number = None
        self.scene_number = None


class ReadStatusOfChannels(Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        pass

