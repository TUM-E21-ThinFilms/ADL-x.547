from adl_x547.message import Message, Response

class ActualValueMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(2)
    
    def create_response(self, raw_bytes):
        return ActualValueResponse(raw_bytes)

class ActualValueResponse(Response):
    def _valid(self):
        return self.get_function_code() == 2
    
    def get_voltage(self):
        return self.get_byte(0) << 8 | self.get_byte(1)
    
    def get_current(self):
        return self.get_byte(2) << 8 | self.get_byte(3)
    
    def get_power(self):
        return self.get_byte(4) << 8 | self.get_byte(5)    
