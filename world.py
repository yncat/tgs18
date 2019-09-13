# -*- coding: utf-8 -*-
# TGS19 game world
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import random
import background
import bgtsound
import openal
import enemies
import globalVars
import player
import window

AMB_VOLUME_STEP=6
CLEAR_SOUNDS_NUM=36
TIME_LIMIT=90
INITIAL_SPAWN_TIME=5000

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
		self.endTimer=window.Timer()
		self.time_count=0
		self.force_game_over=False
		self.current_spawn_time=INITIAL_SPAWN_TIME
		self.firstKilled=False
		self.firstSpawned=False

	def terminate(self):
		if self.background: self.background.terminate()
		self.background=None

	def frameUpdate(self):
		if self.endTimer.elapsed>=1000: self._processTime()
		for elem in self.enemies[:]:
			if elem is not None and elem.stat==enemies.DEAD:
				self.enemies.remove(elem)
				self._addPoint()
			if elem is not None: elem.frameUpdate()
		#end enemies update
		if self.spawnTimer.elapsed>=self.current_spawn_time:
			self.spawnTimer.restart()
			self.spawnEnemy()
			s=10000-(self.getScore()*1500)
			if s<3000: s=3000
			s+=random.randint(-2000,2000)
			self.current_spawn_time=s
		#end spawn
		self.player.frameUpdate()
		for elem in self.enemies: elem.frameUpdate()

	def _processTime(self):
		self.time_count+=1
		if self.time_count==TIME_LIMIT:
			self.force_game_over=True
			return
		#end time up
		if self.time_count>=TIME_LIMIT-10: bgtsound.playOneShot(globalVars.app.countSample,vol=-10)
		self.endTimer.restart()

	def getScore(self):
		return self.score

	def spawnEnemy(self):
		if self.firstSpawned and not self.firstKilled: return
		e=enemies.Mosquito(self)
		self.enemies.append(e)
		self.background.changeVolume(AMB_VOLUME_STEP*-1)
		if not self.firstSpawned:
			self.firstSpawned=True
			e.setDistance(2)
			e.setMoveInterval(100)
			e.setApproachFacter(0)

	def getGameover(self):
		return self.player.getWeaponCapacity() ==0 or self.force_game_over is True

	def clear(self):
		self.player.delete()
		for elem in self.enemies:
			elem.delete()
		#end delete
		self.enemies=[]

	def _addPoint(self):
		s=CLEAR_SOUNDS_NUM-1 if self.score>=CLEAR_SOUNDS_NUM else self.score
		bgtsound.playOneShot(globalVars.app.clearSample[s])
		self.score+=1
		self.background.changeVolume(AMB_VOLUME_STEP)
		if not self.firstKilled:
			self.firstKilled=True
			self.spawnTimer.restart()
			self.current_spawn_time=3000

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
