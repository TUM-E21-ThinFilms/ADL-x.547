from adl_x547.message import Message, Response

class ReadTargetValueMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(21)
    
    def create_response(self, raw_bytes):
        return ReadTargetValueResponse(raw_bytes)
        
class ReadTargetValueResponse(Response):
    def _valid(self):
        return self.get_function_code() == 21
    
    def get_voltage(self):
        return self.get_integer(0)
    
    def get_current(self):
        return self.get_integer(2)
    
    def get_power(self):
        return self.get_integer(4)
