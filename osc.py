# -*- coding: utf-8 -*-
# TGS19 OSC receiver
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

PORT=12000
IP="localhost"

class Controller(object):
	def __init__(self):
		self.dispatcher = Dispatcher()
		self.dispatcher.map('/', self._onMessageReceived)
		self.server = osc_server.ThreadingOSCUDPServer((IP, PORT), self.dispatcher)Å@
		self.raw=[0.0,0.0,0.0]
		self.offset=[0.0,0.0,0.0]
		print("Server set up ")

	def getPosition(self):
		return [self.raw[0]-self.offset[0],self.raw[1]-self.offset[1],self.raw[2]-self.offset[2]]

	def recalibrate(self):
		self.offset=[self.raw[0],self.raw[1],self.raw[2]]

	def _onMessageReceived(self,unused_addr, x, y, z,qw,qx,qy,qz):
		print("OK: %02f %02f %02f" % (x,y,z))


