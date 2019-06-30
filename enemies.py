# -*- coding: utf-8 -*-
# TGS19 enemies
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import random
import math
import vrsound
import window

INITIAL_DISTANCE=2.0

class Mosquito(object):
	"""That damned guy. Kill em all! Exterminate!!!!!!!!!!!"""
	def __init__(self,world):
		self.world=world
		self.degrees=random.randint(0,359)
		self.distance=INITIAL_DISTANCE
		self.flying_sound=vrsound.load("fx/mosquito.ogg")
		self.flying_sound.setLooping(True)
		self.updatePosition()
		self.turn_speed=-5 if random.randint(0,1)==0 else 5
		self.approach_facter=0
		self.flying_sound.play()
		self.timer=window.Timer()
		self.hp=100

	def updatePosition(self):
		rad=math.radians(self.degrees)
		self.x=math.cos(rad)*INITIAL_DISTANCE
		self.z=math.sin(rad)*self.distance
		self.flying_sound.setPosition((self.x,0,self.z))

	def frameUpdate(self):
		if self.timer.elapsed<50: return
		self.degrees+=self.turn_speed
		if self.degrees<0: self.degrees+=360
		if self.degrees>359: self.degrees-=360
		self.distance-=self.approach_facter
		if self.distance<0.05: self.distance=0.05
		self.updatePosition()
		self.timer.restart()

	def damage(self,amount):
		self.hp-=amount
		if self.hp<0:self.hp=1
		self.flying_sound.setPitch(0.7+(self.hp*0.003))
		print("damage %s hp %s" % (amount,self.hp))

	def getDistance(self,x,z):
		_x=x-self.x
		_z=z-self.z
		return math.sqrt((_x*_x)+(_z*_z))
