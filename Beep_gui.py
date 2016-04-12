#!/usr/bin/python

"""
Scan Completion Alert w/GUI

	2014/01/20 - K. Lang - Initial
"""


import os

from Tkinter import *

from epics import PV


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
				os.system("paplay ./complete.oga")


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


	def createWidgets(self):
		#Split display into three sections
		self.top = Frame(self)
		
		self.top_labels = Frame(self.top)
		self.top_values = Frame(self.top)
		self.bottom = Frame(self)

		self.pvlabel = Label(self.top_labels)
		self.pvlabel["text"] = "PV Name: "
		self.pvlabel.pack({"side":"top"})
		
		self.targetlabel = Label(self.top_labels)
		self.targetlabel["text"] = "Target Val: "
		self.targetlabel.pack({"side":"bottom"})
		
		self.pvname = Entry(self.top_values, width=30)
		self.pvname.pack({"side":"top"})
		
		self.target = Entry(self.top_values, width=30)
		self.target.pack({"side":"bottom"})

		self.connection = Label(self.bottom)
		self.connection.config(width=30)
		self.connection.pack({"side":"right"})

		self.watch = Button(self.bottom)
		self.watch["text"] = "Watch"
		self.watch.pack({"side": "left"})

		self.top_labels.pack({"side":"left"})
		self.top_values.pack({"side":"right"})
		self.top.pack({"side":"top"})
		self.bottom.pack({"side":"bottom"})

		"""
			Hitting enter in the text field should work the same as pressing
		the watch button.
		"""		
		self.pvname.bind("<Return>", lambda x: self.switch_pv())
		self.target.bind("<Return>", lambda x: self.change_target())
		self.watch["command"] = self.switch_pv


	def __init__(self, master=None):
		Frame.__init__(self, master)

		self.pv = None
		self.last_value = None
		self.target_value = 1
		self.connected = False

		self.pack()
		self.createWidgets()

		#We need to call this once and it will run continuously
		self.update_visual()



if __name__ == "__main__":
	if 'PYEPICS_LIBCA' not in os.environ:
		os.environ['PYEPICS_LIBCA'] = "/APSshare/epics/base-3.14.12.3/lib/linux-x86_64/libca.so"

	root = Tk()
	app = Application(master=root)

	root.protocol("WM_DELETE_WINDOW", app.on_exit)
	app.master.title("Scan Monitor")

	app.mainloop()
