#!/usr/bin/python

import os
import sys
import argparse
import ConfigParser

from Tkinter import *
import tkFileDialog

from epics import PV

if sys.platform == "win32" or sys.platform == "cygwin":
	import winsound

#Base64 versions of button images to keep things in a single file
#Encoder/Decoder at http://www.motobit.com/util/base64-decoder-encoder.asp
no_icon = """
R0lGODlhEAAQAMZrAMYJCbAPD8gJCccKCbMQD8cNDcQODcUODckNDb4TEtYNDcQSEtcNDdgNDcYS
Eb8UE74XFr8XFtQSEccXFtYTEsgXFtcTEtgTEdgTEr8aGcAaGbIgH7AhIdIYF9MYF78eHcwbGsEe
HdgYF9oYF8wcGtkZGLMlJNMdHNQdHNoeHdseHdseHtUiINYiIdskItwkItcoJdgoJt0qJ9QtK781
M9AxL9EyL7k5N8E3Nd4wLc80Mro6ONA1M884NtE5Nt82Mt82M+A3NL9BQMBCQNM9OtU+OuE7N+I7
N8ZDQcdDQd0+Ot4+O8RFROM9OcZGRMVHRcZIReRAPOJBPcVJSORBPcdKSORDP+VDP91HRd5HRORG
QuZGQuZJRedJRd1OS+ZMR95OS+dMR+dMSORPS+ZRTN5TUOBTUOBWUuJXU+ZYU+hZVP//////////
/////////////////////////////////////////////////////////////////////////yH5
BAEKAH8ALAAAAAAQABAAAAevgH9/N0OChoZCO4Y0aWhVh4JTZ2o4fxxjYWFmUIdPZWJfZCZ/RFxa
W2BOgkxeW1pdRYY9VlJRWUlIWFRSVz6QOk1GR0tKR0ZNPJCCNUFAP0BAQTbKhjM51zkzG9R/HzAy
4DIxIdQZLC8u6S4vLRqQECcrKSokICrzKBGGCR0lIiMVBE0YIaKEhwd/AkiwQAGDg0MLLlCwIIHA
nwINGBxQZkABAwSGBgjgBmAkt5OBAAA7"""

yes_icon = """
R0lGODlhEAAQAKU3AADHAAnFCQDLAADNAAHeAQDfAADhAADmAADpABzlHADxAADyAAbwBgD0AAD5
AAv2CyvsKxzzHBn1GT/mPwf9BwP/Aw3/DRL/El7iXl3qXW/lb032TUn+SUn/SWb0ZnTvdE7/ToPq
g2v4a6Pko5Psk57pnoz5jIH+gYz/jK/yr5f+l6D7oK75rqP/o6b/pqv+q7X/tbj/uMX6xb3+vcb/
xsn+ycj/yP///////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAAAZQwJ9w
SCwaj0jkKFks1WRMIWlGs6WYoRcsxmJqVC3XyvgZYk4olMmYEXl+CQ6oszlOIBEGxXKRIAMECAoO
FQ9MAAUICw1RPwIGB41CA5KVlkEAOw=="""

add_icon = """
R0lGODlhEAAQAMZsAA4TNRMZPxQaQxYbRRccSRceSxgeThshUxsiVBwjXR4lYR8lXx4lYyAmWx8n
Zh8naSAoaSMpWSIpbCQqZSQrYyQrZSUrYyUrZiUsZiYsaCYsaiYtaiYtayYtbCkvZSgvbicvcikv
bykwcCkwcykxdCoxdSoxdioxdy0zbC0zbi00cC00dC40ci01dS41fS01gy82fi42hS83gC83gjA3
gC83gy83hTA4hzU8hj1EkD1FlkJJmlRdyVVeyFVey1Zfyldfylhgy1hhy1pizVpjzFtkzlxkzl1l
0F1mz15mz15m0F5m0V5n0V9nz19n0F9n0l9n02Bo0GBo0WBo0mBo02Fp0WFp0mNr02Nr1WRs1GRs
1WVt1WVt1mZu1mdu1mdu12hv12hv2Gdw2Whw12px2Wtz2mxz2m103G5122923XF43XN64f//////
/////////////////////////////////////////////////////////////////////////yH5
BAEKAH8ALAAAAAAQABAAAAeFgH+Cg38xL4SIhC8+PA+JiTY/QBCPiDVBQg6VhDNDRAybgzJFRgqP
ICYlJSQ6SU44IiEhHxN/LlBLTE9TUk1RVlhcXF1iCDRMTk5SUlXNV1lbW11gDX8LHRwbGjvPORgV
FhYHjythYwWhgixkZATpfyplZgPvKWdoAu8ea2oA738RIjwKBAA7"""

save_icon = """
R0lGODlhEAAQAMZ5ADNkpDZmpTpqp0Nwq1V4qVJ5rU96sFl5plh+r16ArlmBtWCCr2SCrGKDr2GD
smOEsoGBgWOFsl+GuGOGtWWGsmaHtWyHr2qJtWaLu2yKtWeMu2mMuW2RvnSRuY6OjnWTu5KSknSX
wpOTkpOTk3mXwJSUlHmYwJWVlXqaw5eXl5mZmYicuZ2dnYWkyaGhoZGjvaSkpJimuqampqenp6io
qJyqvampqaqqqqurq6ysrK2tra6urq+vr7CwsLGxsbKysrW1ta63wq23xba2tri4uLK5w7m5ubu7
u729vb6+vr++vcDAwMDBwsLCwsPDw8TExMXFxcHGzsbGxsjIyMPJ0cfJzMrKysvLy8vLzczMzMvN
0c3Nzc3Nzs/Pz9HR0dPS0NbV1NbW1dbW1tjY2NXZ3dnZ2drZ2NrZ2dra2tvb293b2t3d3eDd2t/f
3+Dg4OHh4eLh4OLi4uPk5eTk5OXk5OXl5ebl5eXm5ubm5v///////////////////////////yH5
BAEKAH8ALAAAAAAQABAAAAe6gH+Cg4SFhRQfFwSGhRkmJC0oCYyGDCEblIJKamwvHBgrXF9MhlUW
EQ8aEhMVB1oihD50ZB0KBgMCDlRmRoRLdXBRCwEACEJnaFeEYmtiYEUNBTFZXmNdNII3cWttaF5B
NVhhaWVjQ4JQc21ucXh3cnZva2ltToJIW1ZTUk9NS0lIjhAhAkMQEBwpXNjQsePGjh40eOgYYZBI
Dhw8fPjQ4eMHDh88TghKIWMGDBYqUpQoAcKDSwiZKAUCADs="""

sound_icon = """
R0lGODlhEAAQAOcAAAAAAAEBAQICAgMDAwQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA0NDQ4O
Dg8PDxAQEBERERISEhMTExQUFBUVFRYWFhcXFxgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEh
ISIiIiMjIyQkJCUlJSYmJicnJygoKCkpKSoqKisrKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0
NDU1NTY2Njc3Nzg4ODk5OTo6Ojs7Ozw8PD09PT4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdH
R0hISElJSUpKSktLS0xMTE1NTU5OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWFlZWVpa
WltbW1xcXF1dXV5eXl9fX2BgYGFhYWJiYmNjY2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra2xsbG1t
bW5ubm9vb3BwcHFxcXJycnNzc3R0dHV1dXZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CA
gIGBgYKCgoODg4SEhIWFhYaGhoeHh4iIiImJiYqKiouLi4yMjI2NjY6Ojo+Pj5CQkJGRkZKSkpOT
k5SUlJWVlZaWlpeXl5iYmJmZmZqampubm5ycnJ2dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaam
pqenp6ioqKmpqaqqqqurq6ysrK2tra6urq+vr7CwsLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5
ubq6uru7u7y8vL29vb6+vr+/v8DAwMHBwcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKysvLy8zM
zM3Nzc7Ozs/Pz9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f
3+Dg4OHh4eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp6erq6uvr6+zs7O3t7e7u7u/v7/Dw8PHx8fLy
8vPz8/T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///yH5BAEKAPsALAAAAAAQABAA
AAi5APe5O4euoMGD6NoJ9CAjhsMYMmrUaBhjRRBe52T828hRmjiO//iUQhcD5L9tLTLU2mgPjymS
JqnpiFGB3r+WL0uClBal251GN13C3Bnl2r8pQXOarCbF2r+X+ITq3DjulROj9spFVfpvnpsaIXJk
44hzqBMBAADQ4EZW6j9fFtICMNOvrVJqKhQ8YKIOZNkV//whm2SLX756iO2xk2OqXRA+d/oE8oOn
smU5Znjt41XqlOfPoE1pDggAOw=="""
	

class LabelLine(Frame):
	def __init__(self, master, add_func=None, save_func=None):
		Frame.__init__(self, master)
	
		self.pvlabel = Label(self, text="PV Name", width=30)
		self.pvlabel.grid(row=0, column=0, padx=(0,5), pady=(5,5))
		
		self.targetlabel = Label(self, text="Target Val", width=10, anchor="e")
		self.targetlabel.grid(row=0, column=1, padx=(0,5), pady=(5,5))
		
		self.placeholder = Label(self, width=9)
		self.placeholder.grid(row=0, column=2, padx=(0,7), pady=(5,5))

		self.button_frame = Frame(self)
		
		self.addimage = PhotoImage(data=add_icon)
		self.add_button = Button(self.button_frame, image=self.addimage, command=add_func)
		self.add_button.grid(row=0, column=2, padx=(0,5))
		
		self.saveimage = PhotoImage(data=save_icon)
		self.save_button = Button(self.button_frame, image=self.saveimage, command=save_func)
		self.save_button.grid(row=0, column=1, padx=(0,5))
	
		self.button_frame.grid(row=0, column=3, padx=(4,5), pady=(5,5))
		

	
class SoundPopup(Toplevel):
	def __init__(self, accept_func=None):
		Toplevel.__init__(self)
		
		self.title("Sound Config")
		
		self.llabel = Label(self, text="Linux Sound:")
		self.llabel.grid(row=0, column=0, padx=(0,5), pady=(5,5))
		
		self.wlabel = Label(self, text="Windows Sound:")
		self.wlabel.grid(row=1, column=0, padx=(0,5), pady=(0,5))
		
		self.tlabel = Label(self, text="Win Sound Type:")
		self.tlabel.grid(row=2, column=0, padx=(0,5), pady=(0,5))
		
		self.lentry = Entry(self, width=20)
		self.lentry.grid(row=0, column=1, padx=(0,5), pady=(5,5))
		
		self.wentry = Entry(self, width=20)
		self.wentry.grid(row=1, column=1, padx=(0,5), pady=(0,5))
		
		self.tentry = Entry(self, width=20)
		self.tentry.grid(row=2, column=1, padx=(0,5), pady=(0,5))
		
		self.button_frame = Frame(self)
		
		self.noimage = PhotoImage(data=no_icon)
		self.no_button = Button(self.button_frame, image=self.noimage, command=self.destroy)
		self.no_button.grid(row=0, column=0, padx=(0,5), pady=(0,5))
		
		self.yesimage = PhotoImage(data=yes_icon)
		self.yes_button = Button(self.button_frame, image=self.yesimage, command=accept_func)
		self.yes_button.grid(row=0, column=1, padx=(0,5), pady=(0,5))
		
		self.button_frame.grid(row=3, column=1, sticky="e")
		
		
		
class PVLine(Frame):

	def disconnect(self):
		if self.pv:
			self.pv.disconnect()

		self.connected = False
	
	def connect(self):
		if len(self.pvname.get()):
			self.pv = PV(self.pvname.get(), connection_callback=self.connection_monitor)		
			self.pv.add_callback(self.status_change)
		
	#PV value callback
	def status_change(self, value, char_value=None, **kws):
		if self.last_value == None:
			self.last_value = char_value
			return
	
		if char_value != self.last_value:
			self.last_value = char_value
			
			if char_value == self.target_value:
				if sys.platform == "linux2":
					os.system("paplay " + self.LinuxSound)
				elif sys.platform == "win32" or sys.platform == "cygwin":
					if self.WindowsSoundType == "ALIAS":
						winsound.PlaySound(self.WindowsSound, winsound.SND_ALIAS)
					elif self.WindowsSoundType == "PATH":
						winsound.PlaySound(self.WindowsSound, winsound.SND_FILENAME)

	#PV connection callback
	def connection_monitor(self, **kws):
		if kws["conn"]:
			self.connected = True
			self.last_value = None
		else:
			self.connected = False
	
	#Switch from one pv to another
	def switch_pv(self):
		self.disconnect()
		self.connect()

	def change_target(self):
		self.last_value = None
		self.target_value = None
		
		if len(self.target.get()):
			self.target_value = self.target.get()
	
	#Use tkinter's event queue to update connection status
	def update_visual(self):
		if self.connected:
			self.connection.config(text="Connected", fg="sea green")
		else:
			self.connection.config(text="Not Connected", fg="red")

		self.master.after(250, self.update_visual)
		
		
	def settings_accept(self):
		self.LinuxSound = self.popup.lentry.get()
		self.WindowsSound = self.popup.wentry.get()
		self.WindowsSoundType = self.popup.tentry.get()
		self.popup.destroy()
		
	def popup(self):	
		self.popup = SoundPopup(self.settings_accept)
		self.popup.focus_force()
		
		self.popup.lentry.insert(0, self.LinuxSound)
		self.popup.wentry.insert(0, self.WindowsSound)
		self.popup.tentry.insert(0, self.WindowsSoundType)
	
	def __init__(self, master, config={}):
		Frame.__init__(self, master)
		
		self.pv = None
		self.connected = False
		self.last_value = None
		self.target_value = config.get("target", 1)
		
		self.LinuxSound = config.get("linux_sound", "/usr/share/sounds/freedesktop/stereo/complete.oga")
		self.WindowsSound = config.get("windows_sound", "SystemExclamation")
		self.WindowsSoundType = config.get("windows_sound_type", "ALIAS")
		
		self.pvname = Entry(self, width=30)
		self.pvname.insert(0, config.get("name", ''))
		self.pvname.grid(row=0, column=0, padx=(0,5), pady=(0,5))
		
		self.target = Entry(self, width=10, justify="right")
		self.target.insert(0, self.target_value)
		self.target.grid(row=0, column=1, padx=(0,5), pady=(0,5))
		
		self.connection = Label(self, width=12)
		self.connection.grid(row=0, column=2, padx=(0,5), pady=(0,5))
		
		self.settings_image = PhotoImage(data=sound_icon)
		self.settings = Button(self, image=self.settings_image, command=self.popup)
		self.settings.grid(row=0, column=3, padx=(0,5), pady=(0,5))
		
		self.pvname.bind("<Return>",   lambda x: self.switch_pv())
		self.pvname.bind("<FocusOut>", lambda x: self.switch_pv())
		self.target.bind("<Return>",   lambda x: self.change_target())
		self.target.bind("<FocusOut>", lambda x: self.change_target())
			
		self.connect()
		self.update_visual()
	
	
		
class Application(Frame):
	def on_exit(self):
		for each in self.pvs:
			each.disconnect()
		
		self.quit()
	
	def add_pv(self, config={}):
		self.numlabels.append(Label(self, text=(str(self.num_pvs + 1) + ": ")))
		self.numlabels[self.num_pvs].grid(row=(self.num_pvs + 1), column=0, padx=(5,0))
		
		self.pvs.append(PVLine(self, config=config))
		self.pvs[self.num_pvs].grid(row=(self.num_pvs + 1), column=1)
		
		self.num_pvs = self.num_pvs + 1
		
		
	def save_config(self):
		f = tkFileDialog.asksaveasfile(mode='w', title="Save Configurations As...")
		
		if f:
			config = ConfigParser.RawConfigParser()
			
			config.add_section("MAIN")
			config.set("MAIN", "NUMBER_OF_PVS", str(self.num_pvs))
			
			for i in range(self.num_pvs):
				index = "PV_" + str(i)
				config.add_section(index)
				
				config.set(index, "NAME", self.pvs[i].pvname.get())
				config.set(index, "TARGET", self.pvs[i].target.get())
				config.set(index, "LINUX_SOUND", self.pvs[i].LinuxSound)
				config.set(index, "WINDOWS_SOUND", self.pvs[i].WindowsSound)
				config.set(index, "WINDOWS_SOUND_TYPE", self.pvs[i].WindowsSoundType)
				
			config.write(f)
	
			
	def __init__(self, master=None, config={}):
		Frame.__init__(self, master)
		
		master.protocol("WM_DELETE_WINDOW", self.on_exit)
		master.title("Scan Monitor")
		
		self.num_pvs = 0
		self.numlabels = []
		self.pvs = []
		
		self.labels = LabelLine(self, add_func=self.add_pv, save_func=self.save_config)
		self.labels.grid(row=0, column=1)
				
		for i in range(int(config.get("NUMBER_OF_PVS", 1))):
			self.add_pv(config=config.get("PV_" + str(i), {}))
	

if __name__ == "__main__":
	if 'PYEPICS_LIBCA' not in os.environ:
		os.environ['PYEPICS_LIBCA'] = "/APSshare/epics/base-3.14.12.3/lib/linux-x86_64/libca.so"

	config={}
		
	parser = argparse.ArgumentParser(description="PV Status Alarm Script")
	parser.add_argument("-c", "--config", metavar="conf", dest="config_path", action="store", default=None, help="path to configuration file")
	
	cmd_args = parser.parse_args()
	
	if cmd_args.config_path:
		parser = ConfigParser.RawConfigParser()
		parser.read(cmd_args.config_path)
		
		if parser.has_option("MAIN", "NUMBER_OF_PVS"):
			config["NUMBER_OF_PVS"] = parser.get("MAIN", "NUMBER_OF_PVS")
			parser.remove_section("MAIN")
		
		for section in parser.sections():
			config[section] = {}
			
			for option in parser.options(section):
				config[section][option] = parser.get(section, option)
	
	
	app = Application(master=Tk(), config=config)
	app.pack()
	
	app.mainloop()
