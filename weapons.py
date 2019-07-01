# -*- coding: utf-8 -*-
# TGS19 weapons
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import globalVars
import vrsound
import window

"""This module will contain weapons that can kill mosquitoes. I don't come up with anything except spray though."""

class Spray(object):
	"""A spray can that contains poisonus substance."""
	def __init__(self,world):
		self.world=world
		self.capacity=30
		self.active=False
		self.loopTimer=window.Timer()
		self.looping=False
		self.startSound=vrsound.load("fx/ss.ogg")
		self.loopSound=vrsound.load("fx/sl.ogg")
		self.loopSound.setLooping(True)
		self.stopSound=vrsound.load("fx/se.ogg")
		self.x=0
		self.z=0
		self.attackTimer=window.Timer()

	def frameUpdate(self,dist):
		self.move(dist)
		if self.active is True and self.looping is False and self.loopTimer.elapsed>80: self._loop()
		if self.active and self.attackTimer.elapsed>=50: self._attack()

	def _attack(self):
		for elem in self.world.enemies:
			d=elem.getDistance(self.x,self.z)
			if d<=1:
				elem.damage(10-(d*10))
		#end for
		self.attackTimer.restart()

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

	def move(self,dist):
		self.x+=dist[0]/200
		self.z+=dist[1]/200
		self.updatePosition()

	def updatePosition(self):
		self.startSound.setPosition((self.x,0,self.z))
		self.loopSound.setPosition((self.x,0,self.z))
		self.stopSound.setPosition((self.x,0,self.z))
