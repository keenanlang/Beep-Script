#!/usr/bin/python


import os
import sys

from Tkinter import *

from epics import PV

if sys.platform == "win32" or sys.platform == "cygwin":
	import winsound


def load_config(config_path):
	config = {}

	if config_path:
		with open(config_path, "r") as config_file:
			for line in config_file:
				name, val = line.split(":")
				
				config[name.strip()] = val.strip()
		
	return config
	
	
class Application(Frame):

	"""
	PV value callback
	"""
	def status_change(self, value, **kws):
		if self.last_value == None:
			self.last_value = value
			return
	
		if value != self.last_value:
			self.last_value = value
			
			if value == self.target_value:
				if sys.platform == "linux2":
					os.system("paplay " + self.config.get("LINUX_SOUND_PATH", "/usr/share/sounds/freedesktop/stereo/complete.oga"))
				elif sys.platform == "win32" or sys.platform == "cygwin":
					if self.config.get("WINDOWS_SOUND_TYPE", "ALIAS") == "ALIAS":
						winsound.PlaySound(self.config.get("WINDOWS_SOUND_PATH","SystemExclamation"), winsound.SND_ALIAS)
					elif self.config.get("WINDOWS_SOUND_TYPE") == "PATH":
						winsound.PlaySound(self.config.get("WINDOWS_SOUND_PATH"), winsound.SND_FILENAME)
					


	"""
	PV connection callback
	"""
	def connection_monitor(self, **kws):
		if kws["conn"]:
			self.connected = True
			self.last_value = None
		else:
			self.connected = False


	"""
		Because tkinter isn't built to allow multi-threaded access, we have to
	define a function that is continuously put on the tk event queue to update
	the connection status.
	"""
	def update_visual(self):
		if self.pv and self.connected:
			self.connection.config(text="Connected", fg="sea green")
		else:
			self.connection.config(text="Not Connected", fg="red")

		self.master.after(250, self.update_visual)


	"""
	Handles watching a new pv when currently watching another
	"""
	def switch_pv(self):
		if self.pv:
			self.pv.disconnect()
		
		self.connected = False
		self.pv = PV(self.pvname.get(), connection_callback=self.connection_monitor)
		
		self.change_target()
		
		self.pv.add_callback(self.status_change)

	def change_target(self):
		if len(self.target.get()):
			self.target_value = int(self.target.get())


	"""
	Clean up PV connection when we exit
	"""
	def on_exit(self):
		if self.pv:
			self.pv.disconnect()

		self.connected = False
		self.quit()	

	def create_widgets(self):
		self.pvlabel = Label(self)
		self.pvlabel["text"] = "PV Name: "
		self.pvlabel.grid(row=0, column=0)
		
		self.targetlabel = Label(self)
		self.targetlabel["text"] = "Target Val: "
		self.targetlabel.grid(row=1, column=0)
		
		self.pvname = Entry(self, width=30)
		self.pvname.insert(0, self.config.get("DEFAULT_PV_NAME", ""))
		self.pvname.grid(row=0, column=1)
		
		self.target = Entry(self, width=30)
		self.target.insert(0, str(self.target_value))
		self.target.grid(row=1, column=1)

		self.connection = Label(self)
		self.connection.config(width=30)
		self.connection.grid(row=2, column=1)

		self.watch = Button(self)
		self.watch["text"] = "Watch"
		self.watch.grid(row=2, column=0)
		
		"""
			Hitting enter in the text field should work the same as pressing
		the watch button.
		"""		
		self.pvname.bind("<Return>", lambda x: self.switch_pv())
		self.target.bind("<Return>", lambda x: self.change_target())
		self.watch["command"] = self.switch_pv


	def __init__(self, master=None, config={}):
		Frame.__init__(self, master)

		self.config = config
		
		self.pv = None
		self.last_value = None
		self.target_value = int(self.config.get("DEFAULT_TARGET_VALUE", 1))
		self.connected = False

		self.pack()
		self.create_widgets()

		#We need to call this once and it will run continuously
		self.update_visual()
	

if __name__ == "__main__":
	if 'PYEPICS_LIBCA' not in os.environ:
		os.environ['PYEPICS_LIBCA'] = "/APSshare/epics/base-3.14.12.3/lib/linux-x86_64/libca.so"
		
	config_path = None
	
	if len(sys.argv) > 1:
		config_path = sys.argv[1]
		
	root = Tk()
	app = Application(master=root, config=load_config(config_path))
	
	root.protocol("WM_DELETE_WINDOW", app.on_exit)
	app.master.title("Scan Monitor")

	app.mainloop()
