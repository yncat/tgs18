# -*- coding: utf-8 -*-
# TGS19 game world
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import bgtsound
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
		self.score=0

	def frameUpdate(self):
		for elem in self.enemies[:]:
			if elem is not None and elem.stat==enemies.DEAD:
				self.enemies.remove(elem)
				self._addPoint()
			if elem is not None: elem.frameUpdate()
		#end enemies update
		if self.spawnTimer.elapsed>=5000:
			self.spawnTimer.restart()
			self.enemies.append(enemies.Mosquito(self))
		if globalVars.app.keyPressed(window.K_q): globalVars.app.say("%.2f, %.2f" % (self.enemies[0].x, self.enemies[0].z))
		self.player.frameUpdate()
		for elem in self.enemies: elem.frameUpdate()

	def getScore(self):
		return self.score

	def getGameover(self):
		return self.player.getWeaponCapacity() ==0

	def clear(self):
		self.player.delete()
		for elem in self.enemies:
			elem.delete()
		#end delete
		self.enemies=[]

	def _addPoint(self):
		bgtsound.playOneShot(globalVars.app.pointSample)
		self.score+=1
