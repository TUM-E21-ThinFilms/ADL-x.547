from controllers.adl.message import Message, Response

class DeActivateRampMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(32)

    def create_response(self, raw_bytes):
        return DeActivateRampResponse(raw_bytes)

class DeActivateRampResponse(Response):
    def _valid(self):
        return self.get_function_code() == 32
