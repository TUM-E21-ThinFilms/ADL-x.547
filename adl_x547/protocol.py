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

import slave
import logging

from threading import Semaphore

from slave.transport import Timeout
from slave.protocol import Protocol

class CommunicationError(Exception):
    pass

class ADLProtocol(Protocol):
    def __init__(self, slave_addr=0, logger=None):

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())

        self.logger = logger
        self.receiver = slave_addr
        self.semaphore = Semaphore(1)

    def set_logger(self, logger):
        self.logger = logger

    def clear(self, transport):
        self.logger.debug("Clearing message queue")
        while True:
            try:
                transport.read_bytes(32)
            except slave.transport.Timeout:
                return
        
    def send_message(self, transport, message):
        
        message.set_slave_addr(self.receiver)
        message.finish()
        
        data = message.to_binary()
        self.logger.debug('Send: "%s"', message)

        transport.write(data)

    def _do_query(self, transport, message):

        self.send_message(transport, message)

        length = message.response_length()

        try:
            raw_response = transport.read_bytes(length)
        except slave.transport.Timeout:
            raise CommunicationError('Could not read response. Timeout')

        if length <= 1:
            return message.create_response(raw_response)

        self.logger.debug('Response (%s bytes): "%s"', str(len(raw_response)), " ".join(map(hex, raw_response)))

        response_as_hex = []

        for i in range(0, length):
            response_as_hex.append(raw_response[i])

        response = message.create_response(response_as_hex)

        if not response.is_valid():
            raise CommunicationError('Received an invalid response packet.')

        status = response.get_status()

        if status.get_error() > 0 or status.get_error_on_execution() > 0 or status.get_error_code() > 0:
            self.logger.error('Received error code: %s', status.get_error_code())

        return response


    def query(self, transport, message):
        try:
            # We need here a semaphore, to block threads:
            # Turning the sputter on, and changing the power while running
            # might interfere two messages. In order to fix this, only
            # let one query pass thrugh the serial interface at one time (until
            # the response has been read).
            self.semaphore.acquire()
            self._do_query(transport, message)
        except Exception as e:
            raise e
        finally:
            self.semaphore.release()


    def write(self, transport, message):
        return self.query(transport, message)
