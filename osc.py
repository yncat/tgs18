# -*- coding: utf-8 -*-
# TGS19 OSC receiver
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import threading

PORT=12000
IP="127.0.0.1"

class Controller(object):
	def __init__(self):
		self.dispatcher = Dispatcher()
		self.dispatcher.map("/realsense*",self._onMessageReceived)
		self.server = osc_server.ThreadingOSCUDPServer((IP, PORT), self.dispatcher)
		self.raw=(0.0,0.0,0.0)
		self.offset=(0.0,0.0,0.0)
		self.distance_cach=(0.0,0.0,0.0)
		self.thread=threading.Thread(target=self._thread)
		self.thread.setDaemon(True)
		self.thread.start()

	def cleanup(self):
		self.server.shutdown()
		self.thread.join()

	def getPosition2d(self):
		return (self.raw[0]-self.offset[0],self.raw[2]-self.offset[2])

	def getDistance2d(self):
		r=(self.raw[0]-self.distance_cach[0],self.raw[2]-self.distance_cach[2])
		self.distance_cach=(self.raw[0],self.raw[1],self.raw[2])
		return r

	def recalibrate(self):
		self.offset=(self.raw[0],self.raw[1],self.raw[2])

	def _onMessageReceived(self,unused_address, x, y, z,qw,qx,qy,qz):
		print("%d %d %d" % (x,y,z))
		self.raw=(x,y,z)
		self.distance_cach=(0.0,0.0,0.0)

	def _thread(self):
		print("server")
		self.server.serve_forever()
