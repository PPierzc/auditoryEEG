from PyQt5 import QtWidgets, QtGui, QtCore

from strings import strings

class Default(QtWidgets.QWidget):
	def __init__(self, sm):
		super(Default, self).__init__()
		self.sm = sm

		self.title_font = QtGui.QFont("Andale Mono", 36, QtGui.QFont.Bold)
		self.btn_font = QtGui.QFont("Andale Mono", 20, QtGui.QFont.Bold)
		self.input_font = QtGui.QFont("Andale Mono", 18, QtGui.QFont.Bold)
		self.label_font = QtGui.QFont("Andale Mono", 16, QtGui.QFont.Bold)
		self.large_font = QtGui.QFont("Andale Mono", 128, QtGui.QFont.Bold)

		self.setWindowTitle(strings.APP_NAME)

		self.resize(500, 500)
		self.move(600, 200)

		self.render()

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(1000)

	def render(self):
		pass

	def update(self):
		pass

	def unmount(self):
		self.destroy()