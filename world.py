# -*- coding: utf-8 -*-
# TGS19 game world
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import background
import bgtsound
import openal
import enemies
import globalVars
import player
import window

class World(object):
	"""This object represents a game world."""
	def __init__(self):
		self.background=background.Background()
		self.background.play()
		self.enemies=[]
		self.player=player.Player(self)
		self.enemies.append(enemies.Mosquito(self))
		self.spawnTimer=window.Timer()
		self.score=0
		self.paused=False

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

	def setPaused(self,p):
		if p==self.paused: return
		self.paused=p
		self.player.setPaused(p)
		for elem in self.enemies:
			elem.setPaused(p)

	def _detatchEnemy(self,elem):
		self.enemies.remove(elem)
