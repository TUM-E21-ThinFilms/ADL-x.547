from controllers.adl.message import Message, Response

class VoltageControlIgnitionMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(12)
        
    def set_voltage(self, voltage):
	    self.set_integer(0, voltage)
    
    def create_response(self, raw_bytes):
        return VoltageControlIgnitionResponse(raw_bytes)

class VoltageControlIgnitionResponse(Response):
    def _valid(self):
        return self.get_function_code() == 12

    def get_voltage(self):
	return self.get_integer(0)
