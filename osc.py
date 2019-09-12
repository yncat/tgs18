# -*- coding: utf-8 -*-
# TGS19 OSC receiver
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import threading

PORT=12000
IP="127.0.0.1"
X_BOUNDARY=0.5
Z_BOUNDARY=0.5

class Controller(object):
	def __init__(self):
		self.dispatcher = Dispatcher()
		self.dispatcher.map("/realsense*",self._onMessageReceived)
		self.server = osc_server.ThreadingOSCUDPServer((IP, PORT), self.dispatcher)
		self.raw=(0.0,0.0,0.0)
		self.offset=[0.0,0.0,0.0]
		self.distance_cach=(0.0,0.0,0.0)
		self.thread=threading.Thread(target=self._thread)
		self.thread.setDaemon(True)
		self.thread.start()

	def cleanup(self):
		self.server.shutdown()
		self.thread.join()

	def getPosition2d(self):
		r=[self.raw[0]-self.offset[0],self.raw[2]-self.offset[2]]
		if r[0]>=X_BOUNDARY:
			r[0]=X_BOUNDARY
			self.setCustomOffset2d(X_BOUNDARY,None)
		if r[0]<=X_BOUNDARY*-1:
			r[0]=X_BOUNDARY*-1
			self.setCustomOffset2d(X_BOUNDARY*-1,None)
		if r[1]>=Z_BOUNDARY:
			r[1]=Z_BOUNDARY
			self.setCustomOffset2d(None,Z_BOUNDARY)
		if r[1]<=Z_BOUNDARY*-1:
			r[1]=Z_BOUNDARY*-1
			self.setCustomOffset2d(None,Z_BOUNDARY*-1)
		#end adjusting
		return r

	def getDistance2d(self):
		r=[self.raw[0]-self.distance_cach[0],self.raw[2]-self.distance_cach[2]]
		self.distance_cach=(self.raw[0],self.raw[1],self.raw[2])
		return r

	def recalibrate(self):
		self.offset=[self.raw[0],self.raw[1],self.raw[2]]

	def _onMessageReceived(self,unused_address, x, y, z,qw,qx,qy,qz):
		self.raw=(x,y,z)
		self.distance_cach=(0.0,0.0,0.0)

	def setCustomOffset2d(self,x,z):
		if x is not None: self.offset[0]=self.raw[0]-x
		if z is not None: self.offset[2]=self.raw[2]-z

	def _thread(self):
		print("server")
		self.server.serve_forever()
