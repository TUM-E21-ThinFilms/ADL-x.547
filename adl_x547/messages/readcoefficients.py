from controllers.adl.message import Message, Response

class ReadCoefficientsMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(112)
        
    def create_response(self, raw_bytes):
        return ReadCoefficientsResponse(raw_bytes)

class ReadCoefficientsResponse(Response):
    def _valid(self):
        return self.get_function_code() == 112
    
    def get_voltage(self):
        return self.get_integer(0)
    
    def get_current(self):
        return self.get_integer(2)
    
    def get_power(self):
        return self.get_integer(4)
