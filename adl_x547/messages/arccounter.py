from adl_x547.message import Message, Response

class ArcCounterMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(6)
    
    def create_response(self, raw_bytes):
        return ArcCounterResponse(raw_bytes)

class ArcCounterResponse(Response):
    def _valid(self):
        return self.get_function_code() == 6
    
    def get_arc_count(self):
        return self.get_byte(2) << 8 | self.get_byte(3)
    
  
