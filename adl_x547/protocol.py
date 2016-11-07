from slave.protocol import Protocol
import logging
from message import Message, Response

class CommunicationError(Exception):
    pass

class ADLProtocol(Protocol):
    def __init__(self, slave_addr=0, logger=None):

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())

        self.logger = logger

        self.name = 'ADL'
        self.receiver = slave_addr

    def set_logger(self, logger):
        self.logger = logger

    def send_message(self, transport, message):
        
        message.set_slave_addr(self.receiver)
        message.finish()
        
        data = message.to_binary()
        self.logger.debug('Send: "%s"', message)

        transport.write(data)
        
    def query(self, transport, message):
        
        self.send_message(transport, message)
        
        length = message.response_length()

        raw_response = transport.read_bytes(length)
        
        if length <= 1:
            return message.create_response(raw_response)
        
        # every resposne has 16 Bytes length.
        
        self.logger.debug('Response (%s bytes): "%s"', str(len(raw_response)), " ".join(map(hex, raw_response)))
       
        response_as_hex = []
        
        for i in range(0, length):
            response_as_hex.append(raw_response[i])
        
        response = message.create_response(response_as_hex)

        if not response.is_valid():
            raise CommunicationError('Received an invalid response packet.')
        
        status = response.get_status()
        
        if status.get_error() > 0 or status.get_error_on_execution() > 0 or status.get_error_code() > 0:
            self.logger.error('Received error code: %s', status.get_error_code())            
        
        return response

    def write(self, transport, message):
        return self.query(transport, message)
