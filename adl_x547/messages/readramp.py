from controllers.adl.message import Message, Response

class ReadRampMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(33)
    
    def create_response(self, raw_bytes):
        return ReadRampResponse(raw_bytes)

class ReadRampResponse(Response):
    def _valid(self):
        return self.get_function_code() == 33

    def get_time(self):
        return self.get_integer(2)
    
