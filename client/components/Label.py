from PyQt5 import QtWidgets, QtGui

class Label(QtWidgets.QLabel):
	def __init__(self, view, text, resize, move, font):
		super().__init__(text, view)
		self.resize(*resize)
		self.move(*move)
		self.setFont(font)
