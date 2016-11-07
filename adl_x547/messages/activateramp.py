from adl_x547.message import Message, Response

class ActivateRampMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(31)
        
    def create_response(self, raw_bytes):
        return ActivateRampResponse(raw_bytes)

class ActivateRampResponse(Response):
    def _valid(self):
	    return True
#        return self.get_function_code() == 31
