# -*- coding: utf-8 -*-
# TGS19 enemies
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import random
import math
import bgtsound
import globalVars
import vrsound
import window

INITIAL_DISTANCE=5.0

ACTIVE=0
DYING=1
DEAD=2

class Mosquito(object):
	"""That damned guy. Kill em all! Exterminate!!!!!!!!!!!"""
	def __init__(self,world):
		self.world=world
		self.degrees=random.randint(0,359)
		self.distance=INITIAL_DISTANCE
		self.move_interval=50
		self.flying_sound=vrsound.load("fx/mosquito2.wav")
		self.flying_sound.setLooping(True)
		self.updatePosition()
		self.turn_speed=-5 if random.randint(0,1)==0 else 5
		self.approach_facter=0.02
		self.flying_sound.play()
		self.timer=window.Timer()
		self.hp=100
		self.deathStep=9
		self.stat=ACTIVE
		self.deathTimer=window.Timer()
		self.paused=False

	def setApproachFacter(self,f):
		self.approach_facter=f

	def setMoveInterval(self,i):
		self.move_interval=i

	def setDistance(self,d):
		self.distance=d

	def updatePosition(self):
		rad=math.radians(self.degrees)
		self.x=math.cos(rad)*self.distance
		self.z=math.sin(rad)*self.distance
		self.flying_sound.setPosition((self.x,0,self.z))

	def frameUpdate(self):
		if self.stat==DEAD: return
		if self.timer.elapsed>=self.move_interval: self.move()
		if self.stat==DYING and self.deathTimer.elapsed>=30: self._kill()

	def move(self):
		if self.stat==ACTIVE and self.distance<0.1:
			self._attack()
		self.degrees+=self.turn_speed
		if self.degrees<0: self.degrees+=360
		if self.degrees>359: self.degrees-=360
		self.distance-=self.approach_facter
		if self.distance<0.05: self.distance=0.05
		self.updatePosition()
		self.timer.restart()

	def _attack(self):
		bgtsound.playOneShot(globalVars.app.needleSample[random.randint(0,2)])
		self.world.setPaused(True)
		globalVars.app.wait(700)
		self.world.logAttacked()
		self.world._detatchEnemy(self)
		self.world.setPaused(False)
		self.delete()

	def damage(self,amount):
		if self.stat!=ACTIVE: return
		self.hp-=amount
		if self.hp<0:
			self.kill()
			return
	#end kill
		self.flying_sound.setPitch(0.7+(self.hp*0.003))

	def kill(self):
		if self.stat!=ACTIVE: return
		self.stat=DYING
		self.flying_sound.setPitch(0.9)
		self.flying_sound.setGain(0.9)
		self.deathTimer.restart()

	def _kill(self):
		self.deathStep-=1
		self.flying_sound.setPitch(self.deathStep*0.1)
		self.flying_sound.setGain(self.deathStep*0.1)
		if self.deathStep==0:
			self.stat=DEAD
			return
		#end dead
		self.deathTimer.restart()

	def delete(self):
		self.flying_sound.stop()

	def getDistance(self,x,z):
		_x=x-self.x
		_z=z-self.z
		return math.sqrt((_x*_x)+(_z*_z))

	def setPaused(self,p):
		if p==self.paused: return
		self.flying_sound.setPaused(p)
		self.timer.setPaused(p)
		self.paused=p

