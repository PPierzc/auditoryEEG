from PyQt5 import QtWidgets, QtGui, QtCore
import time

from strings import strings
from .default import Default
from components.Label import Label

class RecordTrials(Default):
	def render(self):
		self.title = Label(
			view = self,
			text = self.sm.state['participant']['name'],
			resize = (400, 50),
			move = (10,25),
			font = self.title_font
		)

		self.countDown = Label(
			view=self,
			text=str(self.sm.state['ui']['count_down_iterator']),
			resize=(400, 128),
			move=(215, 140),
			font=self.large_font
		)


	def update(self):
		if (self.sm.state['ui']['count_down_iterator'] > 1):
			self.sm.state['ui']['count_down_iterator'] -= 1
			self.countDown.setText(str(self.sm.state['ui']['count_down_iterator']))
		else:
			self.countDown.destroy()
			self.countDown = None