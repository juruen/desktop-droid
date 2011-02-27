#! /usr/bin/env python
#
# Copyright (c) 2011 Warp Networks, S.L. All rights reserved.
#
# Author: Javier Uruen Val (juruen@warp.es)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from desktop_droid import websocket
from PyQt4 import QtCore

class ServerConnection(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    def slot_start_connection(self, server, identifier):
        print "slot start connection"
        self.server = str(server)
        self.identifier = str(identifier)
        self.websocket = None
        self.connect()

    def connect(self):
        if (self.websocket):
                try:
                    self.websocket.close()
                    self.websocket = None
                except:
                    print "Couldn't close socket properly"

        uri = "ws://%s/subscribe/%s" % (self.server, self.identifier)
        print "connectiong to uri %s" % (uri)

        try:
            self.websocket = websocket.create_connection(uri)
        except:
            print "Scheduling reconnect in 10 seconds"
            QtCore.QTimer.singleShot(10000, self.connect)
            return

        self.fd_notifier = QtCore.QSocketNotifier(
            self.websocket.io_sock.fileno(),
            QtCore.QSocketNotifier.Read
        )
        QtCore.QObject.connect(
            self.fd_notifier,
            QtCore.SIGNAL("activated(int)"),
            self.slot_activated
        )

    def slot_activated(self, fd):
        try:
           cmd = self.websocket.recv()
        except:
            self.fd_notifier.setEnabled(False)
            self.connect()
            return

        print "cmd received: %s" % cmd
        if cmd == "ring":
            print "emmiting signal"
            self.emit(QtCore.SIGNAL('ring'))

