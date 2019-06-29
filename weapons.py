# -*- coding: utf-8 -*-
# TGS19 weapons
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import vrsound
import window

"""This module will contain weapons that can kill mosquitoes. I don't come up with anything except spray though."""

class Spray(object):
	"""A spray can that contains poisonus substance."""
	def __init__(self):
		self.capacity=30
		self.active=False
		self.loopTimer=window.Timer()
		self.looping=False
		self.startSound=vrsound.load("fx/ss.ogg")
		self.loopSound=vrsound.load("fx/sl.ogg")
		self.loopSound.setLooping(True)
		self.stopSound=vrsound.load("fx/se.ogg")

	def frameUpdate(self):
		if self.active is True and self.looping is False and self.loopTimer.elapsed>80: self._loop()

	def _loop(self):
		self.looping=True
		self.loopSound.play()

	def trigger(self):
		self.startSound.play()
		self.stopSound.stop()
		self.looping=False
		self.loopTimer.restart()
		self.active=True

	def untrigger(self):
		self.stopSound.play()
		self.loopSound.stop()
		self.startSound.stop()
		self.active=False
