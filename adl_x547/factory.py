from protocol import ADLProtocol
from driver import ADLSputterDriver
from slave.transport import Serial
import logging



class ADLSputterFactory:
    
    def get_logger(self):
        logger = logging.getLogger('ADL Sputter')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler('adlsputter.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger
    
    def create_sputter(self, device='/dev/ttyUSB11', logger=None):
        if logger is None:
            logger = self.get_logger()
            
        protocol = ADLProtocol(logger=logger)
        protocol.set_name("ADL x.547 Sputter")
        return ADLSputterDriver(Serial(device, 9600, 8, 'E', 1, 0.05), protocol)

