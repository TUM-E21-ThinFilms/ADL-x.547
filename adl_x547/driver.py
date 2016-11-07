from slave.driver import Driver, Command
from slave.types import String, BitSequence
from protocol import ADLProtocol

from messages.status import *
from messages.temperatur import *
from messages.readcoefficients import *
from messages.operationshours import *
from messages.setramp import *
from messages.readramp import *
from messages.activateramp import *
from messages.deactivateramp import *
from messages.turnon import *
from messages.turnoff import *
from messages.actualvalue import *
from messages.targetvalue import *
from messages.readtargetvalue import *
from messages.voltagecontrol import *
from messages.currentcontrol import *
from messages.powercontrol import *

import time
import threading

class ADLSputterDriver(Driver):
    # Handling Base Classes
    def __init__(self, transport, protocol=None):
        if protocol == None:
            protocol = ADLProtocol()

        super(ADLSputterDriver, self).__init__(transport, protocol)
        self.protocol = protocol

    def send_message(self, message):
        return self._protocol.query(self._transport, message)

    def clear(self):
        self._protocol.clear(self._transport)
    
    def get_status(self):
        msg = StatusMessage()
        return self.send_message(msg)

    def get_temperatur(self):
        msg = TemperaturMessage()
        return self.send_message(msg)

    def get_coefficients(self):
        msg = ReadCoefficientsMessage()
        return self.send_message(msg)

    def get_operationshours(self):
        msg = OperationsHoursMessage()
        return self.send_message(msg)

    def set_ramp(self, time):
        msg = SetRampMessage()
        msg.set_time(time)
        return self.send_message(msg)

    def get_ramp(self):
        msg = ReadRampMessage()
        return self.send_message(msg)
	
    def activate_ramp(self):
        msg = ActivateRampMessage()
        return self.send_message(msg)

    def deactivate_ramp(self):
        msg = DeActivateRampMessage()
        return self.send_message(msg)

    def turn_on(self):
        msg = TurnOnMessage()
        return self.send_message(msg)

    def turn_off(self):
        msg = TurnOffMessage()
        return self.send_message(msg)

    def get_actual_value(self):
        msg = ActualValueMessage()
        return self.send_message(msg)

    def get_target_value(self):
        msg = TargetValueMessage()
        return self.send_message(msg)
    
    def get_target_values(self):
        msg = ReadTargetValueMessage()
        return self.send_message(msg)

    def get_actual_value(self):
        msg = ActualValueMessage()
        return self.send_message(msg)
 
    def set_mode_u(self, voltage):
        msg = VoltageControlMessage()
        msg.set_voltage(voltage)
        return self.send_message(msg)

    def set_mode_i(self, current):
        msg = CurrentControlMessage()
        msg.set_current(current)
        return self.send_message(msg)

    def set_mode_p(self, power):
        msg = PowerControlMessage()
        msg.set_power(power)
        return self.send_message(msg)

    def turn_on_cont(self):
        self.thread = TurnOnThread()
        self.thread.daemon = True
        self.thread.set_driver(self)
        self.thread.start()	

    def turn_off_cont(self):
    	if not self.thread is None:
	    self.thread.stop()

        time.sleep(1)
        self.turn_off()

class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = False

    def run(self):
	    while not self._stop:
	        self.do_execute()

    def stop(self):
        self._stop = True

    def do_execute():
	    pass

class TurnOnThread(StoppableThread):

    def set_driver(self, driver):
	    self.driver = driver

    def do_execute(self):
	    self.driver.turn_on()
	    time.sleep(1)		
