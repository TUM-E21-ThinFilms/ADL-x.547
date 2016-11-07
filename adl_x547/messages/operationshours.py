from controllers.adl.message import Message, Response

class OperationsHoursMessage(Message):
    
    def __init__(self):
        Message.__init__(self)
        self.set_function_code(100)
        
    def create_response(self, raw_bytes):
        return OperationsHoursResponse(raw_bytes)

class OperationsHoursResponse(Response):
    def _valid(self):
        return self.get_function_code() == 100

    def get_turn_on_hours(self):
        return self.get_integer(2)
    
    def get_overall_hours(self):
        return self.get_integer(0)
