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
from threading import Semaphore

from e21_util.error import CommunicationError
from e21_util.interface import Loggable
from e21_util.serial_connection import AbstractTransport, SerialTimeoutException


class ADLProtocol(Loggable):
    def __init__(self, transport, logger):
        super(ADLProtocol, self).__init__(logger)
        assert isinstance(transport, AbstractTransport)

        self._transport = transport
        self._semaphore = Semaphore(1)

    def clear(self):
        with self._transport:
            self._logger.debug("Clearing message queue")
            while True:
                try:
                    transport.read_bytes(32)
                except SerialTimeoutException:
                    return

    def send_message(self, message):

        message.finish()
        data = message.to_binary()

        self._logger.debug('Send "{}"'.format(message))
        self._transport.write(data)

    def _do_query(self, message):

        self.send_message(message)

        length = message.response_length()

        try:
            raw_response = self._transport.read_bytes(length)
        except SerialTimeoutException:
            raise CommunicationError('Could not read response. Timeout')

        if length <= 1:
            return message.create_response(raw_response)

        self._logger.debug('Response ({} bytes): "{}"'.format(len(raw_response), " ".join(map(hex, raw_response))))

        response_as_hex = []

        for i in range(0, length):
            response_as_hex.append(raw_response[i])

        response = message.create_response(response_as_hex)

        if not response.is_valid():
            raise CommunicationError('Received an invalid response packet.')

        status = response.get_status()

        if status.get_error() > 0 or status.get_error_on_execution() > 0 or status.get_error_code() > 0:
            self._logger.error('Received error code: {}'.format(status.get_error_code()))

        return response

    def query(self, message):
        # Note that: Process locking != Semaphore locking
        # Since: Semaphores only work with threads
        # the with statement uses a process lock.
        with transport:
            try:
                # We need here a semaphore, to block threads:
                # Turning the sputter on, and changing the power while running
                # might interfere two messages. In order to fix this, only
                # let one query pass through the serial interface at one time (until
                # the response has been read).
                self._semaphore.acquire()
                return self._do_query(message)
            except Exception as e:
                raise e
            finally:
                self._semaphore.release()

    def write(self, message):
        return self.query(message)
