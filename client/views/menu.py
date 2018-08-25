from PyQt5 import QtWidgets, QtGui

from strings import strings
from .default import Default

class Menu(Default):
	def render(self):
		label = QtWidgets.QLabel(strings.MENU_TITLE, self)
		label.resize(400, 50)
		label.move(120, 25)
		label.setFont(self.title_font)

		record_btn = QtWidgets.QPushButton(strings.record, self)
		record_btn.resize(240, 300)
		record_btn.move(5, 100)
		record_btn.setFont(self.btn_font)
		record_btn.clicked.connect(self.on_record_click)

		analyse_btn = QtWidgets.QPushButton(strings.analyse, self)
		analyse_btn.resize(240, 300)
		analyse_btn.move(255, 100)
		analyse_btn.setFont(self.btn_font)

	def on_record_click(self):
		self.sm.push('record_setup')
