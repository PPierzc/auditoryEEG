from PyQt5 import QtWidgets, QtGui

from strings import strings
from .default import Default
from components.Label import Label

class RecordSetup(Default):

	def render(self):
		self.title = Label(
			view=self,
			text=strings.record_setup_title,
			resize=(400, 50),
			move=(100,25),
			font=self.title_font
		)

		self.name_label = Label(
			view=self,
			text=strings.name,
			resize=(400, 50),
			move=(10, 100),
			font=self.label_font
		)

		self.name_input = QtWidgets.QLineEdit(self)
		self.name_input.resize(400, 50)
		self.name_input.move(10, 140)
		self.name_input.setFont(self.input_font)

		self.age_label = Label(
			view=self,
			text=strings.age,
			resize=(400, 50),
			move=(10, 200),
			font=self.label_font
		)

		self.age_input = QtWidgets.QLineEdit(self)
		self.age_input.resize(200, 50)
		self.age_input.move(10, 240)
		self.age_input.setFont(self.input_font)

		self.gender_label = Label(
			view=self,
			text=strings.gender,
			resize=(400, 50),
			move=(10, 300),
			font=self.label_font
		)

		self.gender_input = QtWidgets.QCheckBox(self)
		self.gender_input.resize(200, 50)
		self.gender_input.move(200, 300)
		self.gender_input.setFont(self.input_font)

		self.submit_btn = QtWidgets.QPushButton(strings.submit, self)
		self.submit_btn.resize(100, 50)
		self.submit_btn.move(10, 400)
		self.submit_btn.setFont(self.btn_font)
		self.submit_btn.clicked.connect(self.on_submit_click)

		self.back_btn = QtWidgets.QPushButton(strings.back, self)
		self.back_btn.resize(100, 50)
		self.back_btn.move(130, 400)
		self.back_btn.setFont(self.btn_font)
		self.back_btn.clicked.connect(self.on_back_click)

	def on_submit_click(self):
		name = self.name_input.text()
		age = int(self.age_input.text())
		gender = 'female' if self.gender_input.checkState() else 'male'

		self.sm.state['participant']['name'] = name
		self.sm.state['participant']['age'] = age
		self.sm.state['participant']['gender'] = gender

		self.sm.push('record_trials')


	def on_back_click(self):
		self.sm.push('menu')