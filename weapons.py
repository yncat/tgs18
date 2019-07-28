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
		self.capacity=350
		self.active=False
		self.loopTimer=window.Timer()
		self.looping=False
		self.startSound=[vrsound.load("fx/spray2start.ogg"), vrsound.load("fx/spray1start.ogg"), vrsound.load("fx/spray0start.ogg")]
		self.loopSound=[vrsound.load("fx/spray2loop.ogg"), vrsound.load("fx/spray1loop.ogg"), vrsound.load("fx/spray0loop.ogg")]
		for elem in self.loopSound:
			elem.setLooping(True)
		#end set looping
		self.stopSound=[vrsound.load("fx/spray2end.ogg"), vrsound.load("fx/spray1end.ogg"), vrsound.load("fx/spray0end.ogg")]
		self.x=0
		self.z=0
		self.attackTimer=window.Timer()
		self.gains=(0.0, 0.0, 0.0)
	def frameUpdate(self,dist):
		self.move(dist)
		if self.active is True and self.looping is False and self.loopTimer.elapsed>80: self._loop()
		if self.active and self.attackTimer.elapsed>=50: self._attack()

	def _attack(self):
		self.capacity-=1
		for elem in self.world.enemies:
			d=elem.getDistance(self.x,self.z)
			if d<=1:
				elem.damage(10-(d*10))
		#end for
		self.attackTimer.restart()

	def _loop(self):
		self.looping=True
		self._updateGains()
		self._playSound(self.loopSound)

	def trigger(self):
		self._updateGains()
		self._playSound(self.startSound)
		for elem in self.stopSound:
			elem.stop()
		#end stop stop sounds
		self.looping=False
		self.loopTimer.restart()
		self.active=True

	def untrigger(self):
		globalVars.app.say("%d" % self.capacity)
		self._playSound(self.stopSound)
		for elem in self.loopSound:
			elem.stop()
		#end stop loop sounds
		for elem in self.startSound:
			elem.stop()
		#end stop start sounds
		self.active=False

	def move(self,dist):
		self.x+=dist[0]/200
		self.z+=dist[1]/200
		self.updatePosition()

	def updatePosition(self):
		for i in range(len(self.startSound)):
			self.startSound[i].setPosition((self.x,0,self.z))
			self.loopSound[i].setPosition((self.x,0,self.z))
			self.stopSound[i].setPosition((self.x,0,self.z))

	def _updateGains(self):
		self.gains=self._calcGains()
		for i in range(len(self.startSound)):
			self.startSound[i].setGain(self.gains[i])
		#end for
		for i in range(len(self.loopSound)):
			self.loopSound[i].setGain(self.gains[i])
		#end for
		for i in range(len(self.stopSound)):
			self.stopSound[i].setGain(self.gains[i])
		#end for

	def _calcGains(self):
		if self.capacity>325: return (1.0,0.0,0.0)
		if self.capacity>275: return (1.0-((325-self.capacity)*0.02), (275+self.capacity)*0.02, 0.0)
		if self.capacity>125: return (0.0,1.0,0.0)
		if self.capacity>75: return (0.0, 1.0-((125-self.capacity)*0.02), (75+self.capacity)*0.02)
		return (0.0, 0.0, 1.0)

	def _playSound(self,s):
		for i in range(len(s)):
			s[i].play()
		#end for
	#end _playSound
