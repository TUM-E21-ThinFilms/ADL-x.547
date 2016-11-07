from controllers.adl.message import Message, Response

class PowerControlMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(11)
        
    def set_power(self, power):
	    self.set_integer(0, power)
    
    def create_response(self, raw_bytes):
        return PowerControlResponse(raw_bytes)

class PowerControlResponse(Response):
    def _valid(self):
        return self.get_function_code() == 11

    def get_power(self):
        return self.get_byte(0) << 8 | self.get_byte(1)
