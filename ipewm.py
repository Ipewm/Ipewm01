#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ipewm.py
#  
#  Copyright 2023 paroni <paroni@debian>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import os
import json
import sys
import subprocess

# Change path so we find Xlib
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Xlib import X, display, Xutil

#from Xlib.xobject import cursor

#variables,list,dict 
path = "/usr/share/applications"
fjson = "appli.json"

catedict = {"AudioVideo":{},
	"Development":{},
	"Documentation":{},
	"Education":{},
	"Game":{},
	"Graphics":{},
	"Network":{},
	"Office":{},
	"Settings":{},
	"System":{},
	"Utility":{},
	"Pcmanfm": {},
	"UpDate":{},
	"Exit":{},
	"Poweroff":{}}

catewins = {}
appliwins = {}

framewins = {}

#colors
#0x000000 ->black
#0xff0000 -> red
#0x00ff00 -> green
#0xff00ff -> violet
#0xffff00 -> yellow
#0x0000ff -> blue
#0x00ffff -> syan
#0xffffff -> white 

#class frame

class Frame(object):
	
	def __init__(self,s=None,r=None,wmdel=None):
		
		self.rootwin = r
		self.s = s
		
		self.titlename = " "
		
		self.appwin = 0
		
		self.wmdelete = wmdel
		
		self.fwin = self.rootwin.create_window(
			10,10,10,10, 6,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=0x00ff00,
			border_pixel=0x00ff00,
			event_mask=( X.SubstructureNotifyMask | X.SubstructureRedirectMask |
				X.EnterWindowMask | X.LeaveWindowMask |
				X.ButtonPressMask | X.ButtonReleaseMask 
				#| X.ButtonMotionMask
				),
			colormap=X.CopyFromParent
			)
		
		
		self.titlewin = 0
		self.closewin = 0
		
		self.gc = None
		
	
	def framecolor(self,entry=True):
		
		#print(f"framecolor")
		if entry:
			self.fwin.change_attributes(background_pixel=0x0000ff)
			self.fwin.change_attributes(border_pixel=0x0000ff)
			
		else:
			self.fwin.change_attributes(background_pixel=0x00ff00)
			self.fwin.change_attributes(border_pixel=0x00ff00)
	
	def maptitle(self,x=1,y=1):
		
		self.titlewin.configure(
		x = x,
		y = y,
		#height = h,
		#width = w,
		stack_mode = X.Above
		)
		self.titlewin.map()
		self.titlewin.clear_area(width=200,height=20)
		self.titlewin.draw_text(self.gc,10,13,self.titlename)
	
	def unmaptitlewin(self):
		
		self.titlewin.unmap()
			
	def mapwin(self):
		
		#self.fwin.configure(stack_mode=X.Above)
		self.fwin.raise_window()
		self.fwin.map()
	
	def maketitlewin(self):
		
		self.titlewin = self.fwin.create_window(
			10, 10, 300, 20, 1,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=0xffffff,
			border_pixel=0x00ff00,
			event_mask=( 
				X.EnterWindowMask | X.LeaveWindowMask |
				X.ButtonPressMask | X.ButtonReleaseMask
				),
			colormap=X.CopyFromParent
			)
		
		self.closewin = self.titlewin.create_window(
			278, 0, 20, 20, 1,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=0xff00ff,
			border_pixel=0x00ff00,
			event_mask=( 
				X.EnterWindowMask | X.LeaveWindowMask |
				X.ButtonPressMask | X.ButtonReleaseMask
				),
			colormap=X.CopyFromParent
			)
		
		#self.closewin.set_wm_protocols([self.wmdelete])
		
		self.gc = self.titlewin.create_gc(
            foreground = self.s.black_pixel,
            background = self.s.white_pixel,
            )
		
		self.closewin.map()
		
		
	def maprequest(self,win=None,parent=None,x=1,y=1,w=100,h=100,name=None,popup=False):
		
		#fix
		#print(f"frame maprequest: {win}, parent: {parent}")
		
		#print(f"attr: {win.get_attributes()}")
			
		self.appwin = win
		
		self.appattr = win.get_geometry()
		
		self.titlename = name
		
		#print(f"maprequest appattr: x: {self.appattr.x}, y: {self.appattr.y}, w: {self.appattr.width}, h: {self.appattr.height}\
		#\nname: {self.titlename}, appattr: {self.appattr}")
		
		#fix
		#self.trans = win.get_wm_transient_for()
		
		if popup:
			#self.maketitlewin()
			#print(f"maprequest popup, x: {x},y: {y}, w: {w}, h: {h}")
			
			self.x = x + 20
			self.y = y + 15
			
		else:
			
			self.maketitlewin()
			self.x = self.appattr.x
			self.y = self.appattr.y
			
		
		self.fwin.configure(
		x = self.x,
		y = self.y,
		height = self.appattr.height,
		width = self.appattr.width,
		stack_mode = X.Above
		)
		self.appwin.reparent(parent=self.fwin,x=0,y=0)
	
		self.appwin.change_attributes(event_mask=(X.EnterWindowMask))
		
		self.fwin.map_sub_windows()
		self.mapwin()
		
	def destroywin(self, win=None):
		
		#fix
		#print(f"frame destroy, win: {win}")
		
		self.fwin.destroy_sub_windows()
		
	
#menu class

class Menu(object):
	
	def __init__(self,s=None,r=None):
		
		self.rootwin = r
		self.s = s
		self.wcate = 1
		self.cwin_x = 1
		self.cwin_y = 1
		self.wappli = 1
		
		self.cwin = self.rootwin.create_window(
			10, 10, 50, 60, 0,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=self.s.white_pixel,
			#border_pixel=0x00ff00,
			event_mask=(
				X.EnterWindowMask |
				X.LeaveWindowMask
				#X.ButtonPressMask |
				#X.ButtonReleaseMask
				),
			colormap=X.CopyFromParent
			)
		self.awin = self.rootwin.create_window(
			0, 0, 1, 1, 0,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=self.s.white_pixel,
			event_mask=(
				X.EnterWindowMask |
				X.LeaveWindowMask
				# ~ X.ButtonPressMask |
				# ~ X.ButtonReleaseMask
				),
			colormap=X.CopyFromParent
			)
			
		self.gc = self.cwin.create_gc(
            foreground = self.s.black_pixel,
            background = self.s.white_pixel,
            )
            
		self.gcactive = self.cwin.create_gc(
            foreground = 0x000000,
            background = 0x0000ff,
            )
	
	def buildcwin(self):
		
		self.wcate = maxlen(d=catedict.keys())*8
		self.py = 0
		
		for i in catedict.keys():
			#print(f'menu: {i}, len: {self.wcate}, app: {list(catedict[i])}')
			l=[]
			l.append(i)
			l.append(list(catedict[i]))
			
			self.win = self.cwin.create_window(
			0, self.py, self.wcate, 20, 1,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=self.s.white_pixel,
			border_pixel=0x00ff00,
			event_mask=(
				X.ButtonPressMask |
				X.ButtonReleaseMask |
				X.EnterWindowMask |
				X.LeaveWindowMask
				),
			colormap=X.CopyFromParent
			)
			self.win.map()
			
			catewins[self.win] = l
			self.py += 20
		
		#print(f'{self.py}, {self.wcate}', )
		self.cwin.configure(
		#x = x,
		#y = y,
		height = self.py,
		width = self.wcate
		)	
	
	def buildawin(self,c=None, k=None):
		
		self.wappli = maxlen(d=c)*8
		self.ay = 0
		
		#print(f'appli: {c}, {k},{list(catedict.keys()). index(k)}, {self.cwin_y}, maxlen: {self.wappli}')
		
		if self.wappli == 0: 
			
			self.unmapwin()
			return
		
		for i in c:
			
			#print(f'{i}, len: {self.wappli}')
			
			l=[]
			l.append(i)
			l.append(catedict[k][i]['Exec'])
			
			self.win = self.awin.create_window(
			0, self.ay, self.wappli, 20, 1,
			self.s.root_depth,
			X.CopyFromParent,
			X.CopyFromParent,

			# special attribute values
			background_pixel=self.s.white_pixel,
			border_pixel=0x00ff00,
			event_mask=(
				X.ButtonPressMask |
				X.ButtonReleaseMask |
				X.EnterWindowMask |
				X.LeaveWindowMask
				),
			colormap=X.CopyFromParent
			)
			self.win.map()
			#self.win.draw_text(self.gc,1,10,i)
			appliwins[self.win] = l
			self.ay += 20
		
		self.awin.configure(
		x = self.wcate+self.cwin_x,
		y = self.cwin_y+(list(catedict.keys()).index(k)*20),
		height = self.ay,
		width = self.wappli
		)
		#self.awin.set_input_focus(X.RevertToParent,X.CurrentTime)
		#self.awin.configure(stack_mode=X.Above)
		self.awin.raise_window()
		self.awin.map()
		
	def unmapwin(self):
		self.awin.unmap()
		self.cwin.unmap()
	
	def drawtextappli(self,win=None):
		
		#print(f'drawappli: {appliwins}')
		
		for i in appliwins:
			
			if i == win:
				i.change_attributes(background_pixel=0x00aaff)
				i.clear_area(width=self.wappli,height=20)
				i.draw_text(self.gcactive,1,10,appliwins[i][0])
				
			else:	
				i.change_attributes(background_pixel=0x55ffff)
				i.clear_area(width=self.wappli,height=20)
				i.draw_text(self.gc,1,10,appliwins[i][0])
			
	def drawtextcate(self,win=None):
		
		for i in catewins:
			
			if win == i:
				i.change_attributes(background_pixel=0x00FF09)
				i.clear_area(width=self.wcate,height=20)
				i.draw_text(self.gcactive,1,10,catewins[i][0])
				
			else:
				i.change_attributes(background_pixel=0xaaffff)
				i.clear_area(width=self.wcate,height=20)
				i.draw_text(self.gc,1,10,catewins[i][0])
	
	def configcwin(self,x=1,y=1,w=50,h=60):
		
		self.cwin_x = x
		self.cwin_y = y
		
		self.cwin.configure(
		x = self.cwin_x,
		y = self.cwin_y
		#height = h,
		#width = w
		)
		
		#self.cwin.set_input_focus(X.RevertToParent,X.CurrentTime)
		#self.cwin.configure(stack_mode=X.Above)
		self.cwin.raise_window()
		self.cwin.map()
	
	def exe(self,ex=None):
	
		mexe = ['/bin/sh','-c']
		
		mexe.append(ex[1])
		
		subprocess.Popen(mexe)
		
		self.unmapwin()
		
	
	def enterwin(self, win=None, childwin=None,cate=True):
		
		#print(f'class enter: {win},{childwin}')
		
		if win in catewins.keys() and cate and childwin == 0:
			#print(f'if class enter: {win}, {len(catewins[win][1])}')

			if len(catewins[win][1]) != 0:
				self.buildawin(c=catewins[win][1], k=catewins[win][0])
				self.drawtextappli(win=win)
				
			else:
				self.awin.unmap()
				
			self.drawtextcate(win=win)
		
		elif  win in appliwins.keys() and childwin == 0:
			
			#print(f'appli: {win}')
			self.drawtextappli(win=win)
			
	
	def leavewin(self,win=None, childwin=None, cate=True):
		
		#print(f'class leave: {win},{childwin}')
		
		if win in catewins.keys() and cate and childwin != 0:
			#print(f'if class leave: {win}')
			self.awin.unmap()

#functions

def maxlen(d=None):
	"""found max len d"""
	maxl = 0
	
	for i in d:
		
		if len(i) > maxl:
			maxl = len(i)
		
	#print(maxl)
	
	return maxl

def findWinFramewins(win=0):
	"""find obj in framewins"""
	for obj in framewins:
		
		if win in framewins[obj]:
			
			return obj
	
	return None
	
def readDesktop(p=None):
	"""read applications dir f.desktop files
	-> open f.desktop files and read Name,Category,Exec,Icon lines
	-> add catedict Name,Category,Exec,Icon
	-> write f.json file
	"""
	
	desktoplist = os.listdir(p)
	
	for i in desktoplist:
		
		if i.endswith(".desktop"):
		
			#print(f"{i}, type: {type(i)}")
			#s = 0
			with open(p+"/"+i) as f:

				r = f.readlines()		
				d = {}
				
				for j in r: 
					
					if j.startswith("Categories"): 
						d["Categories"] = j[j.rindex('=')+1:-1]
					
					if j.startswith("Name="): 
						d["Name"] = j[j.rindex('=')+1:-1]
							
					if j.startswith("Exec"): 
						d["Exec"] = j[j.rindex('=')+1:-1]
						
						
					if j.startswith("Icon="): 
						d["Icon"] = j[j.rindex('=')+1:-1]
							
				#applilist.append(l)
				cate = d.get('Categories')

				if cate != None:
					
					#print(f"find category: {d.get('Categories')},type: {type(d.get('Categories'))},split: {cate.rsplit(sep=';')}")
					
					for k in catedict.keys():
						
						if cate.find(k) != -1: 
							#print(f"find {k}")
							d.pop("Categories")
							catedict[k][d["Name"]] = d
							catedict[k][d["Name"]].pop("Name")

							break
	
	f = open(fjson, "w")
	json.dump(catedict,f,sort_keys=False, indent=4)		
	f.close()
	
def readJson():
	"""read f.json file
	-> update catedict
	"""
	#print("menu say:")
	
	f = open(fjson,"r")
	infojson = json.load(f)
	f.close()
	
	#print(infojson)
	
	catedict.update(infojson)

#test		
def wmTest(win=None):
	"""wm test """
	
	try:
		
		state = win.get_wm_state()
		hints = win.get_wm_hints()
		normal_hints = win.get_wm_normal_hints()
		name = win.get_wm_name()
		attr = win.get_attributes()
		geom = win.get_geometry()	
		
		f = open("wm_test","a+")
		#infojson = json.load(f)
		f.write(f"\n\nwm test win: {win}, name: {name}, state: {state},\nhints: {hints},\nnormal_hints: {normal_hints},\geom: {geom},\nattr: {attr}")
		f.close()
			
		print(f"wm test win: {win}, name: {name}, state: {state},\nhints: {hints},\nnormal_hints: {normal_hints}")
		
	except:
		
		print("wm test: errors")

def main(args):
	
	ipewmfilelist = os.listdir(".")
	
	#print(f"main: {ipewmfilelist}: test: {fjson in ipewmfilelist}")
	
	if fjson in ipewmfilelist: readJson()
	else: readDesktop(path)
	
	f = open("wm_test","w")
	#infojson = json.load(f)
	f.write(" ")
	f.close()
	
	#connet X11
	d = display.Display()
	s = d.screen()
	
	#wm root
	rootwin = s.root
	
	#X.StructureNotifyMask 	
	rootwin.change_attributes(event_mask=(X.SubstructureRedirectMask |
			#X.ButtonReleaseMask | 
			X.ButtonPressMask | X.EnterWindowMask ))
	
	#menuobj
	menuObj = Menu(s=s,r=rootwin)
	menuObj.buildcwin()
	trans = None
	title = None
	appname = None
	
	# Set some WM info
	WM_DELETE_WINDOW = d.intern_atom('WM_DELETE_WINDOW')
	WM_PROTOCOLS = d.intern_atom('WM_PROTOCOLS')
	
	
	#eventloop
	while 1:
		e = d.next_event()
		#print(e)
		
		if e.type == X.DestroyNotify:
			
			#fix
			#sys.exit(0)
			
			frameobj = findWinFramewins(win=e.window)
			
			if frameobj != None:
				#frameobj.destroywin(win=e.window)
			
				#print(f"x.DestroyNotify: win: {e.window}, frameobj: {frameobj}")
			
			
				if trans != None and trans == framewins[frameobj][4]:
				
					#print(f"destroynot trans: {framewins[frameobj][4]}")
					#remWinframewins(obj=frameobj, win=framewins[frameobj][2])
				
					trans = None					
					
				framewins.__delitem__(frameobj)
			
			frameobj = findWinFramewins(win=e.window)
			
			if frameobj != None:
				#print(f"destroy2 win: {e.window},")
				#frameobj.destroywin(win=e.window)
				framewins[frameobj][0].destroy()
				framewins.__delitem__(frameobj)
			
			print(f"destroynotify: {framewins}")
			
			
		elif e.type == X.ButtonPress:
			
			#print(f"buttonpress win: {e.window}")
			
			if trans != None: continue
			
			if e.window == rootwin:
				menuObj.configcwin(x=e.event_x,y=e.event_y)
				menuObj.drawtextcate()
			
			elif e.window in catewins.keys():
				#print(f'{e.window}: values: {catewins[e.window][0]}')
				
				if catewins[e.window][0] == 'UpDate':
					#print(f'{e.window}: values: {catewins[e.window][0]}')
					readDesktop(path)
					
				elif catewins[e.window][0] == 'Exit':
					#print(f'{e.window}: values: {catewins[e.window][0]}')
						
					break
					
				elif catewins[e.window][0] == 'Poweroff':
					
					#poweroff -> work
					ex = ["/bin/sh","-c","/sbin/poweroff"]
					subprocess.Popen(ex)
					
				elif catewins[e.window][0] == 'Pcmanfm':
					
					subprocess.Popen(["/bin/sh","-c","pcmanfm"])
				
				menuObj.unmapwin()	
					
			elif e.window in appliwins.keys():
				#print(f'{appliwins[e.window]}')
				name = appliwins[e.window][0]
				menuObj.exe(ex=appliwins[e.window])
				
			else:
				#print(f"buttonpress else win: {e.window}, child: {e.child}")
	
				#move, rezise win: mouse-1 -> move, mouse-3 -> rezise
				e.window.grab_pointer(True,X.ButtonReleaseMask | X.PointerMotionMask, X.GrabModeAsync, X.GrabModeAsync, 
				e.window, X.NONE, X.CurrentTime)
				start = e
				attr = e.window.get_geometry()
				e.window.raise_window()
				
				frameobj = findWinFramewins(win=e.window)
				
				if frameobj != None:
					appwin = framewins[frameobj][2]
					attr_app = framewins[frameobj][2].get_geometry()
				
					#print(f"attr_app: {attr_app}")
				
				# ~ if e.window == framewins[frameobj][1]:
					# ~ frameobj.unmaptitlewin()
					# ~ title = None
					
					if e.window == framewins[frameobj][3]:
						
						framewins[frameobj][0].unmap()
						
						frameobj.destroywin(win=e.window)
						title = None
								
					if (e.event_x > -6 and e.event_x <= -1) and e.event_y <= attr.width -20 and start.detail == 1:
						frameobj.maptitle(x=e.event_x,y=e.event_y)
						title = framewins[frameobj][1]		
		
		elif e.type == X.ButtonRelease:
			#print(f"ButtonRelease: {e.window}, {e.root} ")
			d.ungrab_pointer(time=X.CurrentTime)
			
		elif e.type == X.MotionNotify:	
			#print(f"motion: x:{attr.x}, y: {attr.y}, h: {attr.height}, w: {attr.width},start.detail: {start.detail}")
			
			#print(f"motion: x:{attr.x}, y: {attr.y}, h: {attr.height}, w: {attr.width},start.detail: {start.detail}")
			
			if e.event_x < attr.width-10 and e.event_y < 10:
				
				#move win
				xdiff = e.root_x - start.root_x
				ydiff = e.root_y - start.root_y
				e.window.configure(
						x = attr.x + (start.detail == 1 and xdiff or 0),
						y = attr.y + (start.detail == 1 and ydiff or 0),
						#width = max(1, attr.width + (start.detail == 3 and xdiff or 0)),
						#height = max(1, attr.height + (start.detail == 3 and ydiff or 0))
						)
						
			else:	
				#rezise width and height
				xdiff = e.root_x - start.root_x
				ydiff = e.root_y - start.root_y
				e.window.configure(
						#x = attr.x + (start.detail == 1 and xdiff or 0),
						#y = attr.y + (start.detail == 1 and ydiff or 0),
						width = max(attr.width, attr.width + (start.detail == 3 and xdiff or 0)),
						height = max(attr.height, attr.height + (start.detail == 3 and ydiff or 0))
						)
				
				#x = attr.x + (start.detail == 1 and xdiff or 0),
				#y = attr.y + (start.detail == 1 and ydiff or 0)
						
				appwin.configure(
						x = 0,
						y = 0,
						width = max(attr_app.width, attr_app.width + (start.detail == 3 and xdiff or 0)),
						height = max(attr_app.height, attr_app.height + (start.detail == 3 and ydiff or 0))
						)
		
		elif e.type == X.EnterNotify:
			#print(f'entry: {e.window}, {e.child}, {e.flags}, {e.root},app: {e.window.get_geometry()}')
			
			if trans != None: continue
			
			if e.window == rootwin:
				menuObj.unmapwin()
				
				if title != None: title.unmap()
			
			elif e.window == menuObj.cwin or e.window in catewins.keys():
				#print(f'cwin: {e.window}, {e.child}')
				menuObj.enterwin(win=e.window,childwin=e.child)
				
			elif e.window == menuObj.awin or e.window in appliwins.keys():
				menuObj.enterwin(win=e.window,childwin=e.child, cate =False)
			
			else:
				frameobj = findWinFramewins(win=e.window)
				
				if frameobj != None:
				
					if title != None and e.window == framewins[frameobj][2]: title.unmap()
				
					if e.window == framewins[frameobj][0]:
						frameobj.framecolor()
						#e.window.raise_window()
				
				
		elif e.type == X.LeaveNotify:
			#print(f'leave: {e.window}, {e.child}, {e.flags}, {e.root}')
			
			if trans != None: continue
			
			if e.window == menuObj.cwin or e.window in catewins.keys():
				#print(f'cwin: {e.window}, {e.child}')
				menuObj.leavewin(win=e.window,childwin=e.child)
				
			elif e.window == menuObj.awin or e.window in appliwins.keys():
				menuObj.leavewin(win=e.window,childwin=e.child)
				
			else:
				frameobj = findWinFramewins(win=e.window)
				
				if frameobj != None:
					
					if e.window == framewins[frameobj][0]:
						frameobj.framecolor(entry=False)
				
				
		elif e.type == X.ConfigureRequest:
			#fix ->
			
			#wmTest(win=e.window)
			
			appname = e.window.get_wm_name()
			normal_hints = e.window.get_wm_normal_hints()
			
			#print(f"gonfigrequest: parent: {e.parent}, win: {e.window},\nmask: {e.value_mask}, sibling: {e.sibling}\n,stack_mode: {e.stack_mode}")
			
			attr_con = e.window.get_attributes()
			
			#print(f"configurereq x: {e.x},y: {e.y},width: {e.width}, height: {e.height},border_width: {e.border_width},\nattr: {e.window.get_attributes()}")
			
			if e.parent == rootwin:
				
				#
				if e.width <=10 or e.height <=10: continue
				
				if appname == "LibreOffice 7.0": 
					e.window.configure(
						x = 100,
						y = 100,
						width = e.width,
						height = e.height
						)
				else:	
					e.window.configure(
						x = e.x,
						y = e.y,
						width = e.width,
						height = e.height
						)
			
			else:				
						
				if attr_con.map_state == 2: 
					#fix
					print(f"confreq map_state2: win: {e.window}, parent: {e.parent}")
					
						
					e.window.configure(
							#x = e.x,
							#y = e.y,
							width = e.width,
							height = e.height
							)
					
					e.parent.configure(
							#x = e.x,
							#y = e.y,
							width = e.width,
							height = e.height
							)
							
					
					#continue
			
			frameobj = findWinFramewins(win=e.window)
			
			#print(f"configrequest: {frameobj}")
			
			if frameobj != None:
				
				frameobj.titlename = e.window.get_wm_name()
				
			
			
		elif e.type == X.MapRequest:
			#fix
			
			#appname = e.window.get_wm_name()
			
			#print(f"mapreg, type: {type(appname)}, appname: {appname}")
			
			if type(appname) is str:
			
				if len(appname) == 0: appname = name
			
			#print(f"loop maprequest: parent: {e.parent}, win: {e.window}, appname: {appname}")
			
			
			attr_win = e.window.get_attributes()
			#: {attr_w.class}
			#print(f"loop mapreq attr_win, override_redirect: {attr_win.override_redirect},map_stat: {attr_win.map_state},")
			
			trans = e.window.get_wm_transient_for()
			
			#print(f"trans: {trans}")
			
			f = Frame(s=s,r=rootwin,wmdel= WM_DELETE_WINDOW)
			
			if trans != None:
				
				frameobj = findWinFramewins(win=trans)
				geom = framewins[frameobj][0].get_geometry()
				#print(f"loop trans: geom: {trans.get_geometry()}, fwin geom: {framewins[frameobj][0].get_geometry()}")
				
				f.maprequest(win=e.window,parent=e.parent,name=appname,x=geom.x,y=geom.y,w=geom.width,h=geom.height,popup=True)
			
			
			
			else:
				f.maprequest(win=e.window,parent=e.parent,name=appname)
			
			l = []
			l.append(f.fwin)
			l.append(f.titlewin)
			l.append(f.appwin)
			l.append(f.closewin)
			l.append(trans)
			l.append(appname)
			framewins[f] = l
				
			print(framewins)
			
			
		elif e.type == X.UnmapNotify:
			
			#fix
			#print(f"unmapnotify: win: {e.window}, from_conf: {e.from_configure}, event: {e.event}")
			
			frameobj = findWinFramewins(win=e.window)
			
			#print(f"unmapnot: {frameobj}")
			
			if frameobj != None:
			
				if e.event == framewins[frameobj][0] and e.window == framewins[frameobj][2]:
					e.event.unmap()
					
			else:
				e.window.unmap()
		
		elif e.type == X.MapNotify:
			
			#fix
			#print(f"mapnotify: win: {e.window}, event: {e.event}")	
			
			frameobj = findWinFramewins(win=e.window)
			
			if frameobj != None:
			
				if e.event == framewins[frameobj][0] and e.window == framewins[frameobj][2]:
					e.event.map()
		
		# ~ elif e.type == X.CreateNotify:
			
			# ~ print(f"createnotify: parent: {e.parent}, win: {e.window},\nx: {e.x}, y: {e.y},\
			# ~ \nwidth: {e.width}, height: {e.height},\
			# ~ \nborder_width: {e.border_width}, override: {e.override}")
			
		elif e.type == X.ClientMessage:
			
			#FIXME 334
			#print(f"X.ClientMessage: {e.client_type}, win: {e.window} ")
			
			if e.client_type == WM_PROTOCOLS:
				fmt, data = e.data
				if fmt == 32 and data[0] == WM_DELETE_WINDOW:
					print(f"loop clintmess; win: {e.window}")			
	
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
