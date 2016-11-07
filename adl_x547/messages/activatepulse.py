from controllers.adl.message import Message, Response

class ActivatePulseMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(50)
        
    def create_response(self, raw_bytes):
        return ActivatePulseResponse(raw_bytes)

class ActivatePulseResponse(Response):
    def _valid(self):
        return self.get_function_code() == 50
