from protocol import ADLProtocol
from driver import ADLSputterDriver
from slave.transport import Serial
import logging

logger = logging.getLogger('ADL Sputter')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('adlsputter.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

class ADLSputterFactory:
    def create_sputter(self):
        protocol = ADLProtocol(logger=logger)
        protocol.set_name("ADL x.547 Sputter")
        return ADLSputterDriver(Serial('/dev/ttyUSB11', 9600, 8, 'E', 1, 0.05), protocol)

