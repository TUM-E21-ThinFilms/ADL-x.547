from controllers.adl.message import Message, Response

class TurnOffMessage(Message):
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(2)
    
    def create_response(self, raw_bytes):
        return TurnOffResponse(raw_bytes)

class TurnOffResponse(Response):
    def _valid(self):
        return self.get_function_code() == 2
    
