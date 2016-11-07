from controllers.adl.message import Message, Response

class StatusMessage(Message):   
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(13)
    
    def create_response(self, raw_bytes):
        return StatusResponse(raw_bytes)

class StatusResponse(Response):
    def _valid(self):
        return self.get_function_code() == 13
