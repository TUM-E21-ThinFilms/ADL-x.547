from controllers.adl.message import Message, Response

class CurrentControlMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(10)
        
    def set_current(self, current):
	    self.set_integer(0, current)
    
    def create_response(self, raw_bytes):
        return CurrentControlResponse(raw_bytes)

class CurrentControlResponse(Response):
    def _valid(self):
        return self.get_function_code() == 10

    def get_current(self):
        return self.get_byte(0) << 8 | self.get_byte(1)
