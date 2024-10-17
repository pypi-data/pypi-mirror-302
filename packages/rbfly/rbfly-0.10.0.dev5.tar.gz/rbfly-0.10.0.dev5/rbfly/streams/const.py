#
# rbfly - a library for RabbitMQ Streams using Python asyncio
#
# Copyright (C) 2021-2024 by Artur Wroblewski <wrobell@riseup.net>
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
#

VERSION = 1

DEFAULT_FRAME_SIZE = 1024 ** 2 # 1 MB
DEFAULT_HEARTBEAT = 60  # in seconds

# TODO: make default credit and max queue size configurable per
# subscription
# see also: https://gitlab.com/wrobell/rbfly/-/issues/5
# max memory: (INITIAL_CREDIT + QUEUE_MAX_SIZE) * DEFAULT_FRAME_SIZE
INITIAL_CREDIT = 128
QUEUE_MAX_SIZE = 256

KEY_DECLARE_PUBLISHER = 0x01
KEY_PUBLISH = 0x02
KEY_PUBLISH_CONFIRM = 0x03
KEY_PUBLISH_ERROR = 0x04
KEY_QUERY_PUBLISHER_SEQUENCE = 0x05
KEY_DELETE_PUBLISHER = 0x06
KEY_SUBSCRIBE = 0x07
KEY_DELIVER = 0x08
KEY_CREDIT = 0x09
KEY_STORE_OFFSET = 0x0a
KEY_QUERY_OFFSET = 0x0b
KEY_UNSUBSCRIBE = 0x0c
KEY_CREATE_STREAM = 0x0d
KEY_DELETE_STREAM = 0x0e
KEY_METADATA_QUERY = 0x0f
KEY_PEER_PROPERTIES = 0x11
KEY_SASL_HANDSHAKE = 0x12
KEY_SASL_AUTHENTICATE = 0x13
KEY_TUNE = 0x14
KEY_OPEN = 0x15
KEY_CLOSE = 0x16
KEY_HEARTBEAT = 0x17

RESPONSE_CODES = {
    0x01: 'OK',
    0x02: 'Stream does not exist',
    0x03: 'Subscription ID already exists',
    0x04: 'Subscription ID does not exist',
    0x05: 'Stream already exists',
    0x06: 'Stream not available',
    0x07: 'SASL mechanism not supported',
    0x08: 'Authentication failure',
    0x09: 'SASL error',
    0x0a: 'SASL challenge',
    0x0b: 'SASL authentication failure loopback',
    0x0c: 'Virtual host access failure',
    0x0d: 'Unknown frame',
    0x0e: 'Frame too large',
    0x0f: 'Internal error',
    0x10: 'Access refused',
    0x11: 'Precondition failed',
    0x12: 'Publisher does not exist',
    0x13: 'No offset',
}

# populate the module with response ids for each RabbitMQ Streams request
# key
_GLOBALS = globals()
_RESPONSES = [
    ('RESPONSE_{}'.format(k), v | 0x8000) for k, v in _GLOBALS.items()
    if k.startswith('KEY_')
]
_GLOBALS.update(_RESPONSES)

# vim: sw=4:et:ai
