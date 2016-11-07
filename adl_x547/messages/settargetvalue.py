from adl_x547.message import Message, Response

class SetTargetValueMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(20)
    
    def create_response(self, raw_bytes):
        return SetTargetValueResponse(raw_bytes)

    def set_voltage(self, voltage):
        self.set_integer(0, voltage)
        
    def set_current(self, current):
        self.set_integer(2, current)
        
    def set_power(self, power):
        self.set_integer(4, power)
        
class SetTargetValueResponse(Response):
    def _valid(self):
        return self.get_function_code() == 20
    
    def get_voltage(self):
        return self.get_integer(0)
    
    def get_current(self):
        return self.get_integer(2)
    
    def get_power(self):
        return self.get_integer(4)
