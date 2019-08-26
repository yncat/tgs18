# -*- coding: utf-8 -*-
# TGS19 background ambience handling
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import bgtsound

class Background(object):
	"""Background ambience can be slided louder / quieter."""
	def __init__(self):
		s=bgtsound.sound()
		s.stream("fx/background.ogg")
		self.initial_volume=0
		s.volume=self.initial_volume
		self.sound=s

	def play(self):
		self.sound.play_looped()

	def change(self,volume,time):
		self.sound.slideVolume(volume,time)
