
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


from adl_x547.protocol import ADLProtocol

from adl_x547.messages.status import *
from adl_x547.messages.temperature import *
from adl_x547.messages.readcoefficients import *
from adl_x547.messages.operationshours import *
from adl_x547.messages.setramp import *
from adl_x547.messages.readramp import *
from adl_x547.messages.activateramp import *
from adl_x547.messages.deactivateramp import *
from adl_x547.messages.turnon import *
from adl_x547.messages.turnoff import *
from adl_x547.messages.actualvalue import *
from adl_x547.messages.targetvalue import *
from adl_x547.messages.readtargetvalue import *
from adl_x547.messages.voltagecontrol import *
from adl_x547.messages.currentcontrol import *
from adl_x547.messages.powercontrol import *

class ADLSputterDriver(object):

    MODE_VOLTAGE = 1
    MODE_CURRENT = 2
    MODE_POWER   = 3

    ADL_GS_05_1000_VOLTAGE = 1000
    ADL_GS_05_1000_POWER = 500
    ADL_GS_05_1000_CURRENT = 0.9

    MODEL_ADL_GS_05_1000 = 'GS 05/1000'

    def __init__(self, protocol, model=None, slave_address=0):

        assert isinstance(protocol, ADLProtocol)
        self._protocol = protocol

        if model is None:
            model = self.MODEL_ADL_GS_05_1000

        self._slave_addr = slave_address
        self.max_power, self.max_voltage, self.max_current = None, None, None
        self.set_model(model)

    def set_model(self, model):
        """ Sets the ADL-model. This sets the max_power, max_current and max_voltage parameters

        :param model: MODEL_ADL_GS_05_1000
        """
        if model is self.MODEL_ADL_GS_05_1000:
            self.max_power, self.max_voltage, self.max_current = self.ADL_GS_05_1000_POWER, self.ADL_GS_05_1000_VOLTAGE, self.ADL_GS_05_1000_CURRENT
            return True

        raise ValueError("Unknown model %s" % model)

    def get_rating(self, rating_type):
        """ Returns the maximum rating of the device model, i.e. voltage, current or power#
        :param rating_type: what rating to retrieve? voltage, current or power e.g MODE_VOLTAGE
        :return int the maximum rating of the device.
        """
        if not rating_type in [self.MODE_CURRENT, self.MODE_POWER, self.MODE_VOLTAGE]:
            raise ValueError("rating type must be either MODE_CURRENT, MODE_POWER or MODE_VOLTAGE")

        if rating_type == self.MODE_CURRENT:
            return self.max_current
        if rating_type == self.MODE_POWER:
            return self.max_power
        if rating_type == self.MODE_VOLTAGE:
            return self.max_voltage

    def send_message(self, message):
        """ Sends the messages, via the protocol

        :param message: instance of Message
        :return: Returns the device response as Response instance
        """
        message.set_slave_addr(self._slave_addr)
        return self._protocol.query(message)

    def clear(self):
        """ Clears the protocol buffer       """
        self._protocol.clear()
    
    def get_status(self):
        """ Returns the status of the device as StatusResponse """
        msg = StatusMessage()
        return self.send_message(msg)

    def get_temperature(self):
        """ Returns the temperature of the device as TemperaturResponse """
        msg = TemperatureMessage()
        return self.send_message(msg)

    def get_coefficients(self):
        """ Returns the used device coefficients as ReadCoefficientsResponse"""
        msg = ReadCoefficientsMessage()
        return self.send_message(msg)

    def get_operationshours(self):
        """ Returns the current operation hours as OperationsHoursResponse"""
        msg = OperationsHoursMessage()
        return self.send_message(msg)

    def set_ramp(self, time):
        """ Sets the ramp time and returns this time as SetRampResponse"""
        msg = SetRampMessage()
        msg.set_time(time)
        return self.send_message(msg)

    def get_ramp(self):
        """ Reads the ramp time - set by set_ramp - and returns it via ReadRampResponse """
        msg = ReadRampMessage()
        return self.send_message(msg)

    def activate_ramp(self):
        """ Activates the ramp, returns ActivateRampResponse """
        msg = ActivateRampMessage()
        return self.send_message(msg)

    def deactivate_ramp(self):
        """ Deactivates the ramp, returns DeActivateRampResponse """
        msg = DeActivateRampMessage()
        return self.send_message(msg)

    def turn_on(self):
        """ Turns the device on (sputtering) and returns TurnOnResponse """
        msg = TurnOnMessage()
        return self.send_message(msg)

    def turn_off(self):
        """ Turns off the device and returns TurnOffResponse """
        msg = TurnOffMessage()
        return self.send_message(msg)

    def get_actual_value(self):
        """ Returns the actual value (voltage, current and power) via  ActualValueResponse """
        msg = ActualValueMessage()
        return self.send_message(msg)

    def get_target_value(self):
        """ Returns the target value. Either voltage, current or power (not all) and only if in the corresponding mode is set. Returns TargetValueResponse """
        msg = TargetValueMessage()
        return self.send_message(msg)
    
    def get_target_values(self):
        """ Returns all target values (current, power and voltage) via ReadTargetValueResponse"""
        msg = ReadTargetValueMessage()
        return self.send_message(msg)

    def set_mode(self, mode, value, convert=True, coeff=4095):
        """ Sets the regulating mode

        :param mode: MODE_CURRENT, MODE_POWER or MODE_VOLTAGE
        :param value: the value for the mode
        :param convert: (bool) whether the value should be converted with the coeff via convert_into_*
        :param coeff: the coefficient for converting.
        :return: See set_mode_*
        """
        if mode not in [self.MODE_CURRENT, self.MODE_POWER, self.MODE_VOLTAGE]:
            raise ValueError("mode must be either current, power or voltage")

        if mode == self.MODE_CURRENT:
            if convert:
                value = self.convert_into_current(value, coeff=coeff)

            return self.set_mode_i(value)
        elif mode == self.MODE_POWER:
            if convert:
                value = self.convert_into_power(value, coeff=coeff)

            return self.set_mode_p(value)
        elif mode == self.MODE_VOLTAGE:
            if convert:
                value = self.convert_into_voltage(value, coeff=coeff)

            return self.set_mode_u(value)

    def set_mode_u(self, voltage):
        """ Sets Voltage Mode
        Use convert_into_voltage to convert absolute voltages into relative ones

        :param voltage: the desired relative voltage in percent of max_voltage in voltage_coefficient steps
        :return: VoltageControlResponse
        """
        msg = VoltageControlMessage()
        msg.set_voltage(voltage)
        return self.send_message(msg)

    def set_mode_i(self, current):
        """ Sets Current Mode
        Use convert_into_current to convert absolute currents into relative ones

        :param voltage: the desired relative current in percent of max_current in current_coefficient steps
        :return: VoltageControlResponse
        """
        msg = CurrentControlMessage()
        msg.set_current(current)
        return self.send_message(msg)

    def set_mode_p(self, power):
        """ Sets Power Mode
        Use convert_into_power to convert absolute power into relative ones

        :param voltage: the desired relative power in percent of max_power in power_coefficient steps
        :return: VoltageControlResponse
        """
        msg = PowerControlMessage()
        msg.set_power(power)
        return self.send_message(msg)

    def convert_into_voltage(self, voltage, max_voltage=None, coeff=4095):
        """ Converts an absolute voltage to a relative voltage (understood by the device) by the formula
            voltage = relative_voltage / coeff * max_voltage
            To convert the absolute value 200 V to the relative value, using the model GS 05/1000 and coefficient 4095:
                convert_into_voltage(200, 500, 4095) = 1638 [rel V]

        :param voltage: Voltage to convert to relative
        :param max_voltage: maximum voltage of the device
        :param coeff: conversion coefficient
        :return: the relative voltage
        """
        if max_voltage is None:
            max_voltage = self.max_voltage
        return int(float(voltage)/max_voltage * coeff)
    
    def convert_into_power(self, power, max_power=None, coeff=4095):
        """ See convert_into_voltage """
        if max_power is None:
            max_power = self.max_power
        return int(float(power)/max_power * coeff)
    
    def convert_into_current(self, current, max_current=None, coeff=4095):
        """ See convert_into_voltage """
        if max_current is None:
            max_current = self.max_current
        return int(float(current)/max_current * coeff)

    def convert_from_power(self, power, max_power=None, coeff=4095):
        """ Converts and relative power (understood by the device) to an absolute value (understood by the user) """
        if max_power is None:
            max_power = self.max_power
        return self.convert_to_absolute(power, max_power, coeff)

    def convert_from_voltage(self, voltage, max_voltage=None, coeff=4095):
        if max_voltage is None:
            max_voltage = self.max_voltage
        return self.convert_to_absolute(voltage, max_voltage, coeff)

    def convert_from_current(self, current, max_current=None, coeff=4095):
        if max_current is None:
            max_current = self.max_current
        return self.convert_to_absolute(current, max_current, coeff)

    def convert_to_absolute(self, relative_value, max_rating, coeff):
        """ Converts a relative value (voltage, power, current) to its absolute value
            To convert the relative value 4000 [rel W] to the absolute value, using the model GS 05/1000 and
            coefficient 4095:
                convert_to_absolute(4000, 1000, 4095) = 977 W
        :param relative_value: the value which should be converted
        :param max_rating: the maximum rating of the value. E.g. the model GS 05/1000 has a max rating of 1000 Watt
        :param coeff: the coefficient used to convert (depends on the device settings)
        """
        return float(relative_value) / coeff * max_rating
