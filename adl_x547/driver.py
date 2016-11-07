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
from slave.types import Mapping, Float, String, Integer, Boolean, SingleType
from protocol import ADLProtocol
from messages.turnon import TurnOnMessage()
from messages.turnoff import TurnOffMessage()

class ADLSputterDriver(Driver):

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = ADLProtocol()
        
        self.thread = None
        
        super(ADLSputterDriver, self).__init__(transport, protocol)

    def query_command(self, cmd):
        return self._protocol.query(self._transport, cmd)

    def turn_on(self):
        return self.query_command(TurnOnMessage())
    
    def turn_off(self):
        return self.query_command(TurnOnMessage())
