
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

from slave.driver import Driver, Command
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

    MODE_VOLTAGE = 1
    MODE_CURRENT = 2
    MODE_POWER   = 3

    ADL_GS_05_1000_VOLTAGE = 1000
    ADL_GS_05_1000_POWER = 500
    ADL_GS_05_1000_CURRENT = 0.9

    MODEL_ADL_GS_05_1000 = 'GS 05/1000'

    def __init__(self, transport, protocol=None, model=None):
        if protocol == None:
            protocol = ADLProtocol()

        super(ADLSputterDriver, self).__init__(transport, protocol)
        self.protocol = protocol

        if model is None:
            model=self.MODEL_ADL_GS_05_1000

        self.max_power, self.max_voltage, self.max_current = None, None, None
        self.set_model(model)

    def set_model(self, model):
        if model is self.MODEL_ADL_GS_05_1000:
            self.max_power, self.max_voltage, self.max_current = self.ADL_GS_05_1000_POWER, self.ADL_GS_05_1000_VOLTAGE, self.ADL_GS_05_1000_CURRENT
            return True

        raise ValueError("Unknown model %s" % model)

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

    def set_mode(self, mode, value, convert=True, coeff=4095):
        if mode not in [self.MODE_CURRENT, self.MODE_POWER, self.MODE_VOLTAGE]:
            raise ValueError("mode must be either current, power or voltage")

        if mode == self.MODE_CURRENT:
            if convert:
                value = self.convert_into_current(value, coeff)

            return self.set_mode_i(value)
        elif mode == self.MODE_POWER:
            if convert:
                value = self.convert_into_power(value, coeff)

            return self.set_mode_p(value)
        elif mode == self.MODE_VOLTAGE:
            if convert:
                value = self.convert_into_voltage(value, coeff)

            return self.set_mode_u(value)

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

    def convert_into_voltage(self, voltage, max_voltage=None, coeff=4095):
        if max_voltage is None:
            max_voltage = self.max_voltage
        return int(float(voltage)/max_voltage * coeff)
    
    def convert_into_power(self, power, max_power=None, coeff=4095):
        if max_power is None:
            max_power = self.max_power
        return int(float(power)/max_power * coeff)
    
    def convert_into_current(self, current, max_current=None, coeff=4095):
        if max_current is None:
            max_current = self.max_current
        return int(float(current)/max_current * coeff)
