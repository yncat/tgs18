# -*- coding: utf-8 -*-
# TGS19 player
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal
import weapons
import window

class Player(object):
	"""This object represents a player."""
	def __init__(self):
		self.weapon=weapons.Spray()

