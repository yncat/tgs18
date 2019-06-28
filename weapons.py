# -*- coding: utf-8 -*-
# TGS19 weapons
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal

"""This module will contain weapons that can kill mosquitoes. I don't come up with anything except spray though."""

class Spray(object):
	"""A spray can that contains poisonus substance."""
	def __init__(self):
		self.capacity=30
