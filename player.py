# -*- coding: utf-8 -*-
# TGS19 player
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import globalVars
import weapons
import window

class Player(object):
	"""This object represents a player."""
	def __init__(self,world):
		self.weapon=weapons.Spray(world)
		self.paused=False

	def frameUpdate(self):
		self.weapon.frameUpdate(globalVars.app.mouseMoveDistance()*2)
		if globalVars.app.mousePressed(0) or globalVars.app.keyPressed(window.K_b): self.weapon.trigger()
		if globalVars.app.mousePressed(2): self.weapon.resetPosition()
		if globalVars.app.mouseReleased(0) or globalVars.app.keyReleased(window.K_b): self.weapon.untrigger()

	def getWeaponCapacity(self):
		return self.weapon.getCapacity()

	def delete(self):
		self.weapon.delete()
		self.weapon=None

	def setPaused(self,p):
		if p==self.paused: return
		self.paused=p
		self.weapon.setPaused(p)
