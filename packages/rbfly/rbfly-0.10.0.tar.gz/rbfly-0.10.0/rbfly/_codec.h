//
// rbfly - a library for RabbitMQ Streams using Python asyncio
//
// Copyright (C) 2021-2024 by Artur Wroblewski <wrobell@riseup.net>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

/**
 * Definitions for byte swapping functions for various platforms.
 */

#if defined(__APPLE__)

#include <libkern/OSByteOrder.h>

#define htobe64(x) OSSwapHostToBigInt64(x)
#define be64toh(x) OSSwapBigToHostInt64(x)

#elif defined(__FreeBSD__)

#include <sys/endian.h>

#else

#include <endian.h>

#endif
