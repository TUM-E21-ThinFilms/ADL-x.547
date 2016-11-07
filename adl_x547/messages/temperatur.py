from controllers.adl.message import Message, Response

class TemperaturMessage(Message):
    
    def __init__(self):
	    Message.__init__(self)
        self.set_function_code(101)
        
    def create_response(self, raw_bytes):
        return TemperaturResponse(raw_bytes)

class TemperaturResponse(Response):
    def _valid(self):
        return self.get_function_code() == 101

    def get_temperatur(self):
        return self.get_integer(0)