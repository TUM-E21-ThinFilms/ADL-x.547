from controllers.adl.message import Message, Response

class SetRampMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(30)        
    
    def set_time(self, time):
        self.set_integer(2, time)
   
    def create_response(self, raw_bytes):
        return SetRampResponse(raw_bytes)

class SetRampResponse(Response):
    def _valid(self):
        return self.get_function_code() == 30

    def get_time(self):
        return self.get_integer(2)
    
