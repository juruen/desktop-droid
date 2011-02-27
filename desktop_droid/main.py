#! /usr/bin/env python
#
# Copyright (c) 2011 Warp Networks, S.L. All rights reserved.
#
# Author: Javier Uruen Val (juruen@warp.es
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

import desktop_droid
import sys

from PyQt4 import QtGui, QtCore
from desktop_droid import configurationdialog
from desktop_droid import serverconnection


def main():

        app = QtGui.QApplication(sys.argv)
        app.setOrganizationName("WarpNetworks")
        app.setApplicationName("Desktop Droid")

        if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
            QtGui.QMessageBox.critical(
                0,
                "Systray",
                "Couldn't detect any sustem try on the system"
            )
            return 1

        app.setQuitOnLastWindowClosed(False)

        settings = QtCore.QSettings()
        identifier = settings.value("identifier", "").toString()
        server = settings.value("server", "people.warp.es:3000").toString()
        dialog = configurationdialog.ConfigurationDialog()
        dialog.idLineEdit.setText(identifier)
        dialog.serverLineEdit.setText(server)
        dialog.show()

        server_connection = serverconnection.ServerConnection(None)

        QtCore.QObject.connect(
            server_connection,
            QtCore.SIGNAL("ring"),
            dialog.slot_ring
        )

        QtCore.QObject.connect(
            dialog,
            QtCore.SIGNAL("configuration_done"),
            server_connection.slot_start_connection
        )

        sys.exit(app.exec_())
