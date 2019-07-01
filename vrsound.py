# -*- coding: utf-8 -*-
# TGS19 3D sound wrapper for multiple audio backends
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal

def load(path): return OpenAlSource(path)

class OpenAlSource(object):
	def __init__(self,path):
		self.handle=openal.oalOpen(path)

	def play(self):
		self.handle.play()

	def stop(self):
		self.handle.stop()

	def setLooping(self,lp):
		self.handle.set_looping(lp)

	def setPosition(self,pos):
		self.handle.set_position(pos)

	def setPitch(self,pitch):
		self.handle.set_pitch(pitch)

	def setGain(self,gain):
		self.handle.set_gain(gain)
