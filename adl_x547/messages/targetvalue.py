from adl_x547.message import Message, Response

class TargetValueMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(4)
    
    def create_response(self, raw_bytes):
        return TargetValueResponse(raw_bytes)

class TargetValueResponse(Response):
    def _valid(self):
        return self.get_function_code() == 4
    
    def get_target(self):
        return self.get_byte(0) << 8 | self.get_byte(1)
