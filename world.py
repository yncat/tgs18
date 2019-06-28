# -*- coding: utf-8 -*-
# TGS19 game world
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal
import enemies
import player

class World(object):
	"""This object represents a game world."""
	def __init__(self):
		self.enemies=[]
		self.player=player.Player()

	def frameUpdate(self):
		pass
