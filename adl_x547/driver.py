# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import threading

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

class ADLSputterDriver(Driver):
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

    def convert_into_voltage(self, voltage, max_voltage=1000, coeff=4095):
        return voltage/max_voltage * coeff
    
    def convert_into_power(self, power, max_power=500, coeff=4095):
        return power/max_power * coeff
    
    def convert_into_current(self, current, max_current=0.9, coeff=4095):
        return current/max_current * coeff
