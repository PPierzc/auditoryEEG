import sys
from router import router

class StateManager(object):
	def __init__(self, defaultView=None):
		self.current_view = defaultView
		self.state = {
			'participant': {
				'name': '',
				'age': 0,
				'gender': 'female'
			},
			'ui': {
				'count_down_iterator': 5
			}
		}

	def push(self, view_name):
		if hasattr(self, 'window'):
			self.window.unmount()

		self.current_view = router[view_name]

		self.window = self.current_view(self)
		self.window.show()

	def quit(self):
		self.window.destroy()
		sys.exit()