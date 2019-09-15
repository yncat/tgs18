# -*- coding: utf-8 -*-
# TGS19 weapons
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import globalVars
import vrsound
import window

"""This module will contain weapons that can kill mosquitoes. I don't come up with anything except spray though."""

DEFAULT_SPRAY_CAPACITY=700
class Spray(object):
	"""A spray can that contains poisonus substance."""
	def __init__(self,world):
		self.world=world
		self.capacity=700
		self._calcCrossfadePoints()
		self.active=False
		self.loopTimer=window.Timer()
		self.looping=False
		self.startSound=[vrsound.load("fx/spray2start.ogg"), vrsound.load("fx/spray1start.ogg"), vrsound.load("fx/spray0start.ogg")]
		self.loopSound=[vrsound.load("fx/spray2loop.ogg"), vrsound.load("fx/spray1loop.ogg"), vrsound.load("fx/spray0loop.ogg")]
		for elem in self.loopSound:
			elem.setLooping(True)
		#end set looping
		self.stopSound=[vrsound.load("fx/spray2end.ogg"), vrsound.load("fx/spray1end.ogg"), vrsound.load("fx/spray0end.ogg")]
		self.emptySound=vrsound.load("fx/spray1end.ogg")
		self.resetSound=vrsound.load("fx/reset.ogg")
		self.x=0
		self.z=0
		self.attackTimer=window.Timer()
		self.gains=(0.0, 0.0, 0.0)
		self.gotEmpty=False
		self.afterEmptyTimer=window.Timer()
		self.paused=False

	def frameUpdate(self,dist,direct=False):
		if globalVars.app.keyPressed(window.K_q): globalVars.app.say("%d %d" % (self.x, self.z))
		if self.gotEmpty and self.afterEmptyTimer.elapsed>=3000:
			self.gotEmpty=False
			self.capacity=0
		#end 23 seconds of silence after getting empty
		self.move(dist,direct)
		if self.active is True and self.looping is False and self.loopTimer.elapsed>80: self._loop()
		if self.active and self.attackTimer.elapsed>=50: self._attack()

	def getCapacity(self):
		return self.capacity

	def _calcCrossfadePoints(self):
		self.crossfadePoints=[
			int((self.capacity/2)+25),
			int((self.capacity/2)-25),
			int((self.capacity/8)+25),
			int((self.capacity/8)-25),
		]

	def _attack(self):
		if self.capacity ==1:
			self.untrigger()
			self.gotEmpty=True
			self.afterEmptyTimer.restart()
			return
		#end got empty
		self._updateGains()
		self.capacity-=1
		for elem in self.world.enemies:
			d=elem.getDistance(self.x,self.z)
			if d<=3.0:
				elem.damage(10-(d*3.0))
		#end for
		self.attackTimer.restart()

	def _loop(self):
		self.looping=True
		self._playSound(self.loopSound)

	def trigger(self):
		if self.capacity<=0:
			self.emptySound.play()
			return
		#end empty
		self._updateGains()
		self._playSound(self.startSound)
		for elem in self.stopSound:
			elem.stop()
		#end stop stop sounds
		self.looping=False
		self.loopTimer.restart()
		self.active=True

	def untrigger(self):
		if self.active is not True: return
		self._playSound(self.stopSound)
		for elem in self.loopSound:
			elem.stop()
		#end stop loop sounds
		for elem in self.startSound:
			elem.stop()
		#end stop start sounds
		self.active=False

	def move(self,dist,direct=False):
		if direct:
			#print("update %s" % str(dist))
			self.x=dist[0]*10
			self.z=dist[1]*10
			if globalVars.app.keyPressed(window.K_w): globalVars.app.say("update %f %f" % (self.x, self.z))
		else:
			self.x+=dist[0]/200
			self.z+=dist[1]/200
		#end direct or not direct
		if self.x>3.0: self.x=3.0
		if self.x<-3.0: self.x=-3.0
		if self.z>3.0: self.z=3.0
		if self.z<-3.0: self.z=-3.0
		self.updatePosition()

	def updatePosition(self):
		for i in range(len(self.loopSound)):
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
		if self.capacity>self.crossfadePoints[0]: return (1.0,0.0,0.0)
		if self.capacity>self.crossfadePoints[1]: return (1.0-((self.crossfadePoints[0]-self.capacity)*0.02), (self.crossfadePoints[0]-self.capacity)*0.02, 0.0)
		if self.capacity>self.crossfadePoints[2]: return (0.0,1.0,0.0)
		if self.capacity>self.crossfadePoints[3]: return (0.0, 1.0-((self.crossfadePoints[2]-self.capacity)*0.02), (self.crossfadePoints[2]-self.capacity)*0.02)
		return (0.0, 0.0, 1.0)

	def _playSound(self,s):
		for i in range(len(s)):
			s[i].play()
		#end for
	#end _playSound

	def delete(self):
		for i in range(len(self.loopSound)):
			self.startSound[i].stop()
			self.loopSound[i].stop()
			self.stopSound[i].stop()
		#end stop
		self.startSound=None
		self.loopSound=None
		self.stopSound=None

	def setPaused(self,p):
		if p==self.paused: return
		self.paused=p
		for i in range(len(self.loopSound)):
			self.startSound[i].setPaused(p)
			self.loopSound[i].setPaused(p)
			self.stopSound[i].setPaused(p)
		#end stop
		self.loopTimer.setPaused(p)
		self.attackTimer.setPaused(p)
		self.afterEmptyTimer.setPaused(p)

	def resetPosition(self):
		self.resetSound.play()
		self.x=0
		self.z=0
