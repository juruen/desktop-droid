#! /usr/bin/env python
#
# Copyright (c) 2011 Warp Networks, S.L. All rights reserved.
#
# Author: Javier Uruen (juruen@warp.es)
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

from desktop_droid.ui import configurationdialog
from desktop_droid import desktop_droid_qrc
from PyQt4 import QtGui, QtCore

class ConfigurationDialog(QtGui.QDialog, configurationdialog.Ui_ConfigurationDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connect(self, QtCore.SIGNAL('accepted()'), self.slot_accepted)

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon(':/icons/phone.png'))
        self.trayIcon.show()

    def slot_accepted(self):
        settings = QtCore.QSettings()
        settings.setValue("identifier", self.idLineEdit.text())
        settings.setValue("server", self.serverLineEdit.text())
        print "emiting coniguration done"
        self.emit(
            QtCore.SIGNAL('configuration_done'),
            self.serverLineEdit.text(),
            self.idLineEdit.text(),
        )


    def slot_ring(self):
        print "slot ring"
        self.show_message("Ring!!!", "You have an incoming call!")

    def show_message(self, title, message):
        self.trayIcon.showMessage(
            title,
            message,
            QtGui.QSystemTrayIcon.Information,
            0
        )
