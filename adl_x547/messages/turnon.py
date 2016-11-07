from controllers.adl.message import Message, Response

class TurnOnMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(1)
    
    def create_response(self, raw_bytes):
        return TurnOnResponse(raw_bytes)

class TurnOnResponse(Response):
    def _valid(self):
        return self.get_function_code() == 1
    
