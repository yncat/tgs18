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

	def frameUpdate(self):
		self.weapon.frameUpdate(globalVars.app.mouseMoveDistance())
		if globalVars.app.mousePressed(0): self.weapon.trigger()
		if globalVars.app.mouseReleased(0): self.weapon.untrigger()

	def getWeaponCapacity(self):
		return self.weapon.getCapacity()
