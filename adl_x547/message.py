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

import struct

def concate_byte_list(ls):
    return b"".join(ls)

def byte_to_binary(number)
    return struct.pack('>B', number)

def binary_to_byte(binary)
    return struct.unpack('>B', binary)[0]

# Byte  Content
# 0     Slave Address
# 1     Function Code
# 2     Master-to-Slave Byte 0 
# 3     Master-to-Slave Byte 1
# 4     Master-to-Slave Byte 2
# 5     Master-to-Slave Byte 3
# 6     Master-to-Slave Byte 4
# 7     Master-to-Slave Byte 5
# 8     Master-to-Slave Byte 6
# 9     Master-to-Slave Byte 7
# 10    CRC Low Byte
# 11    CRC High Byte
# 12    Terminator: 59_dec
class Message(object):
    def __init__(self):
        self.msg = 13*[0]
        self.set_terminator()
        
    def set_function_code(self, function_code):
        if function_code > 255 or function_code < 0:
            raise ValueError("invalid function code")
            
        self.msg[1] = function_code & 0xFF
        
    def set_byte(self, index, byte):
        if index < 0 or index > 7:
            raise ValueError("index out of range: 0-7")
            
        if byte > 255 or byte < 0:
            raise ValueError("byte out of range: 0-255")
            
        self.msg[index+2] = byte & 0xFF
        
    def get_byte(self, index):
        if index < 0 or index > 7:
            raise ValueError("index out of range: 0-7")
            
        return self.msg[index+2]
        
    def get_function_code(self):
        return self.msg[1]
        
    def set_slave_addr(self, slave_addr):
        self.msg[0] = (slave_addr & 0xFF)
        
    def get_slave_addr(self):
        return self.msg[0]
        
    def set_terminator(self):
        self.msg[12] = 0x3B # = 59_dev
    
    def get_terminator(self):
        return self.msg[12]
                          
    def compute_crc(self):
        crc = sum(self.msg[0:9]) & 0xFFFF
        self.msg[10] = crc & 0xFF
        self.msg[11] = (crc >> 8) & 0xFF
                
    def get_crc(self):
        return self.msg[10] | (self.msg[11] << 8)
        
    def finish(self):
        self.compute_crc()
        self.set_terminator()
        
    def to_binary(self):
        return concate_byte_list(map(byte_to_binary, self.msg))
        
    def create_response(self, raw_response):
        raise ValueError("Not implemented in child class")
        
    def set_integer(self, index, integer):
        if index < 0 or index > 6:
            raise ValueError("index out of range: 0-6")
        
        integer = integer & 0xFFFF
        self.set_byte(index, (integer << 8) & 0xFF)
        self.set_byte(index + 1, integer & 0xFF)

# Byte  Content
# 0     Slave Address
# 1     Function Code
# 2     Status Byte 0
# 3     Status Byte 1
# 4     Status Byte 2
# 5     Slave-to-Master Byte 0
# 6     Slave-to-Master Byte 1
# 7     Slave-to-Master Byte 2
# 8     Slave-to-Master Byte 3
# 9     Slave-to-Master Byte 4
# 10    Slave-to-Master Byte 5
# 11    Slave-to-Master Byte 6
# 12    Slave-to-Master Byte 7
# 13    CRC Low Byte
# 14    CRC High Byte
# 15    Terminator: 13_dec

class Response(object):
    def __init__(self, response_array):
        if not len(response_array) == 16:
            raise ValueError("length of response_array must be 16")
        
        self.resp = response_array
        
    def get_slave_addr(self):
        return self.resp[0]
    
    def get_function_code(self):
        return self.resp[1]
    
    def get_status(self):
        return Status(self.resp[2:4])
        
    def get_byte(self, index):
        if index < 0 or index > 7:
            raise ValueError("index out of range: 0-7")
        
        return self.resp[index + 5]
        
    def get_crc(self):
        return self.msg[13] | (self.msg[14] << 8) 
    
    def is_valid_crc(self):
        return sum(self.msg[0:12]) & 0xFFFF == self.get_crc()
    
    def _valid(self):
        # may implement validation for subclasses
        return True
    
    def is_valid(self):
        return self.is_valid_crc() && self.resp[15] == 0xD && self._valid()
    
    def get_integer(self, index):
        if index < 0 or index > 6:
            raise ValueError("index out of range: 0-6")
            
        return self.get_byte(index) << 8 | self.get_byte(index + 1)
    
    def response_length(self):
        return 16
    
class Status(object):
    def __init__(self, status_bytes):
        if not len(status_bytes) == 3:
            raise ValueError("lenght of status bytes must be 3")
            
        self.stat = status_bytes
        
    def get_raw(self, index):
        if index < 0 or index > 2:
            raise ValueError("index out of range: 0-2")
        
        return self.resp[index]
    
    def get_active_toggle(self):
        return self.get_raw(0) & 1
    
    def get_interlock(self):
        return self.get_raw(0) & 2
    
    def get_remote(self):
        return self.get_raw(0) & 4
    
    def get_setpoint_ok(self):
        return self.get_raw(0) & 8
    
    def get_mains_on(self):
        return self.get_raw(0) & 16
    
    def get_dc_on(self):
        return self.get_raw(0) & 32
    
    def get_pulse_on(self):
        return self.get_raw(0) & 64
    
    def get_plasma(self):
        return self.get_raw(0) & 128
            
    def get_mode_p(self):
        return self.get_raw(1) & 1
    
    def get_mode_u(self):
        return self.get_raw(1) & 2
    
    def get_mode_i(self):
        return self.get_raw(1) & 4
    
    def get_mode_u_ign(self):
        return self.get_raw(1) & 8
    
    def get_ramp_enabled(self):
        return self.get_raw(1) & 16
    
    def get_joule_mode_enabled(self):
        return self.get_raw(1) & 32
    
    def get_joule_reached(self):
        return self.get_raw(1) & 64
    
    def get_pulse_on_enabled(self):
        return self.get_raw(1) & 128
    
    def get_error(self):
        return self.get_raw(2) & 1
    
    def get_error_on_execution(self):
        return self.get_raw(2) & 2
    
    def get_watchdog(self):
        return self.get_raw(2) & 4
    
    def get_error_code(self):
        return self.get_raw(2) >> 3