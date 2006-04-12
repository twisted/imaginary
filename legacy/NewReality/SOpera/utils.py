# Space Opera - A Multiplayer Science Fiction Game Engine
# Copyright (C) 2002 Jean-Paul Calderone
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

from __future__ import generators

def format(object, perLine = 4, width = 80):
    accum = ''
    i = len(object)
    j = 0
    x = width / perLine
    if type(object) in (list, tuple):
        while j < i:
            accum = accum + '%-*s' % (x, object[j])
            if j % perLine == perLine - 1:
                accum = accum + '\r\n'
            j = j + 1
    elif type(object) is dict:
        for k in object.items():
            accum = accum + '%-*s -> %-*s' % (x / 2 - 2, k[0], x / 2 - 2, k[1])
            accum = accum + '\r\n'
    else:
        accum = repr(object)
    return accum

def fibonacci(c = None):
    i, x, y = 0, 1, 1
    while c is not None and i < c or c is None and 1:
        yield y
        x, y = x + y, x
        i = i + 1
