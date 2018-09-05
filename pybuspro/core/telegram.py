import json


# DTO class
class Telegram:
    def __init__(self, udp_address=None, payload=None, operate_code=None, source_device_type=None,
                 source_address=None, target_address=None, raw_data=None):
        self.udp_address = udp_address
        self.payload = payload
        self.operate_code = operate_code
        self.source_device_type = source_device_type
        self.raw_data = raw_data
        self.source_address = source_address
        self.target_address = target_address

    def __str__(self):
        """Return object as readable string."""

        return json.JSONEncoder().encode([
            {"name": "source_address", "value": self.source_address},
            {"name": "source_device_type", "value": str(self.source_device_type)},
            {"name": "target_address", "value": self.target_address},
            {"name": "operate_code", "value": str(self.operate_code)},
            {"name": "payload", "value": str(self.payload)},
            {"name": "udp_address", "value": self.udp_address},
            {"name": "raw_data", "value": str(self.raw_data)}
        ])

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
