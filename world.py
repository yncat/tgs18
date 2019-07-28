# -*- coding: utf-8 -*-
# TGS19 game world
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal
import enemies
import globalVars
import player
import window

class World(object):
	"""This object represents a game world."""
	def __init__(self):
		self.enemies=[]
		self.player=player.Player(self)
		self.enemies.append(enemies.Mosquito(self))
		self.spawnTimer=window.Timer()

	def frameUpdate(self):
		for elem in self.enemies[:]:
			if elem is not None and elem.stat==enemies.DEAD: self.enemies.remove(elem)
			if elem is not None: elem.frameUpdate()
		#end enemies update
		if self.spawnTimer.elapsed>=5000:
			self.spawnTimer.restart()
			#self.enemies.append(enemies.Mosquito(self))
		if globalVars.app.keyPressed(window.K_q): globalVars.app.say("%.2f, %.2f" % (self.enemies[0].x, self.enemies[0].z))
		self.player.frameUpdate()
		for elem in self.enemies: elem.frameUpdate()
