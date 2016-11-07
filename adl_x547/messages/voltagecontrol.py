from adl_x547.message import Message, Response

class VoltageControlMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(9)
        
    def set_voltage(self, voltage):
	    self.set_integer(0, voltage)
    
    def create_response(self, raw_bytes):
        return VoltageControlResponse(raw_bytes)

class VoltageControlResponse(Response):
    def _valid(self):
        return self.get_function_code() == 9

    def get_voltage(self):
        return self.get_byte(0) << 8 | self.get_byte(1)
