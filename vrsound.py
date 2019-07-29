# -*- coding: utf-8 -*-
# TGS19 3D sound wrapper for multiple audio backends
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal

def load(path): return OpenAlSource(path)

class OpenAlSource(object):
	def __init__(self,path):
		self.handle=openal.oalOpen(path)
		self.paused=False

	def play(self):
		if self.paused: self.paused=False
		self.handle.play()

	def stop(self):
		if self.paused: self.paused=False
		self.handle.stop()

	def setPaused(self,p):
		if p==self.paused: return
		if p is True and self.getPlayState() is False: return
		self.paused=p
		if p is True:
			self.handle.pause()
		else:
			self.handle.play()

	def setLooping(self,lp):
		self.handle.set_looping(lp)

	def setPosition(self,pos):
		self.handle.set_position(pos)

	def setPitch(self,pitch):
		self.handle.set_pitch(pitch)

	def setGain(self,gain):
		self.handle.set_gain(gain)

	def getPlayState(self):
		return self.handle.get_state()==openal.AL_PLAYING

