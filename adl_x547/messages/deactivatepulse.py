from adl_x547.message import Message, Response

class DeActivatePulseMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(51)
        
    def create_response(self, raw_bytes):
        return DeActivatePulseResponse(raw_bytes)

class DeActivatePulseResponse(Response):
    def _valid(self):
        return self.get_function_code() == 51
