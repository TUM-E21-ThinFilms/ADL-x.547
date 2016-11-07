from adl_x547.message import Message, Response

class NullResponse(Response):
    def __init__(self, response_array):
        pass
    
    def is_valid(self):
        return True
    
