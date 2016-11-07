from controllers.adl.message import Message, Response
from controllers.adl.messages.null import NullResponse

class ResetMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(130)
        
    def create_response(self, raw_bytes):
        return NullResponse(raw_bytes)

    def response_length(self):
	    return 1
