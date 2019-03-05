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

from e21_util.log import get_sputter_logger
from e21_util.transport import Serial
from e21_util.ports import Ports

from adl_x547.protocol import ADLProtocol
from adl_x547.driver import ADLSputterDriver


class ADLSputterFactory(object):

    @staticmethod
    def create(transport, logger):
        return ADLSputterDriver(ADLProtocol(transport, logger))

    def get_logger(self):
        return get_sputter_logger('ADL Sputter', 'adlsputter.log')

    def create_sputter(self, device=None, logger=None):
        if logger is None:
            logger = self.get_logger()

        if device is None:
            device = Ports().get_port(Ports.DEVICE_ADL_A)

        protocol = ADLProtocol(logger=logger)
        return ADLSputterDriver(Serial(device, 9600, 8, 'E', 1, 0.05), protocol)

    def create_sputter_a(self):
        return self.create_sputter()

    def create_sputter_b(self, device=None, logger=None):
        if logger is None:
            logger = self.get_logger()

        if device is None:
            device = Ports().get_port(Ports.DEVICE_ADL_B)

        protocol = ADLProtocol(logger=logger)
        return ADLSputterDriver(Serial(device, 9600, 8, 'E', 1, 0.05), protocol)
