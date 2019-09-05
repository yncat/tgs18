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

AMB_VOLUME_STEP=6
class World(object):
	"""This object represents a game world."""
	def __init__(self):
		self.background=background.Background()
		self.background.changeVolume(-10)
		self.background.play()
		self.enemies=[]
		self.player=player.Player(self)
		self.spawnTimer=window.Timer()
		self.score=0
		self.paused=False
		self.attacked=0

	def terminate(self):
		if self.background: self.background.terminate()
		self.background=None

	def frameUpdate(self):
		for elem in self.enemies[:]:
			if elem is not None and elem.stat==enemies.DEAD:
				self.enemies.remove(elem)
				self._addPoint()
			if elem is not None: elem.frameUpdate()
		#end enemies update
		if self.spawnTimer.elapsed>=5000:
			self.spawnTimer.restart()
			self.spawnEnemy()
		#end spawn
		self.player.frameUpdate()
		for elem in self.enemies: elem.frameUpdate()

	def getScore(self):
		return self.score

	def spawnEnemy(self):
		self.enemies.append(enemies.Mosquito(self))
		self.background.changeVolume(AMB_VOLUME_STEP*-1)

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
		self.background.changeVolume(AMB_VOLUME_STEP)

	def setPaused(self,p):
		if p==self.paused: return
		self.paused=p
		self.player.setPaused(p)
		for elem in self.enemies:
			elem.setPaused(p)

	def logAttacked(self):
			self.attacked+=1

	def getAttacked(self):
		return self.attacked
	def _detatchEnemy(self,elem):
		self.enemies.remove(elem)
		self.background.changeVolume(AMB_VOLUME_STEP)
