from PyQt5 import QtWidgets
from oasys.menus.menu import OMenu

class XMyMenu(OMenu):

    def __init__(self):
        super().__init__(name="My Tools")

        self.addSubMenu("My Tool 1")
        self.addSubMenu("My Tool 2")
        self.addSeparator()
        self.openContainer()
        self.addContainer("My Container 1")
        self.addSubMenu("My Tool 3")
        self.closeContainer()

    def executeAction_1(self, action):
        self.showWarningMessage("My Tool 1")

    def executeAction_2(self, action):
        self.showWarningMessage("My Tool 2")

    def executeAction_3(self, action):
        self.showWarningMessage("My Tool 3")

    def showConfirmMessage(self, message, informative_text):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(message)
        msgBox.setInformativeText(informative_text)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        ret = msgBox.exec_()
        return ret

    def showWarningMessage(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def showCriticalMessage(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
