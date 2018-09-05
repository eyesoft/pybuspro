
# DTO class
class Telegram:
    def __init__(self, source_address=None, source_device_type=None, target_address=None, operate_code=None, payload=None):
        self.source_address = source_address
        self.source_device_type = source_device_type
        self.target_address = target_address
        self.operate_code = operate_code
        self.payload = payload
    
    def __str__(self):
        """Return object as readable string."""
        return '<Telegram source_address="{0}", source_device_type="{1}" ' \
            'target_address="{2}" operate_code="{3}" ' \
            'payload="{4}" />'.format(
                self.source_address,
                self.source_device_type,
                self.target_address,
                self.operate_code,
                self.payload)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
