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

# System imports
import popen2, getpass, socket

def sendPwd(name, email, pwd):
    sendmail(email, 'Your character has been created',
        'Your character, %s, has been created with the password %s.' % (name, pwd)
    )

def sendmail(address, subject, body):
    data = """To: %s
From: %s@%s
Subject: %s

%s
.
""" % (address, getpass.getuser(), socket.getfqdn(), subject, body)

    r, w = popen2.popen2('/usr/sbin/sendmail %s' % address)
    w.write(data)
    w.close()
