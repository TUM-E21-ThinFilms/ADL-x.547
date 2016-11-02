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

from adl_x547.message import Message, Response

class CurrentControlMessage(Message):
    
    def __init__(self):
        self.set_function_code(10)
        
    def set_current(self, voltage):
        voltage = voltage & 0xFFFF
        self.set_byte(0, (voltage << 8) & 0xFF)
        self.set_byte(1, voltage & 0xFF)
    
    def create_response(self, raw_bytes):
        return CurrentControlResponse(raw_bytes)

class CurrentControlResponse(Response):
    def _valid(self):
        return self.get_function_code() == 10

    def get_current(self):
        return self.get_byte(0) << 8 | self.get_byte(1)