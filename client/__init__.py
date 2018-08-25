import sys
import qdarkstyle
from PyQt5 import QtWidgets, QtGui

from state_manager import StateManager
from views.menu import Menu

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

sm = StateManager()
sm.push('menu')

app.exec_()