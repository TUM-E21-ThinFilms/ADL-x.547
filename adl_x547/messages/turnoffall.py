from controllers.adl.message import Message, Response

class TurnOffAllMessage(Message):
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(131)
    
    def create_response(self, raw_bytes):
        return TurnOffAllResponse(raw_bytes)

class TurnOffAllResponse(Response):
    def _valid(self):
        return self.get_function_code() == 131
    
