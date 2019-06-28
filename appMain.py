# -*- coding: utf-8 -*-
# TGS19 main implementation
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal
import buildSettings
import window

class Application(window.SingletonWindow):
	"""
	The game's main application class.

	Instantiate this class, call initialize method, then call run method to start the application. Other methods are internally used and should not be called from outside of the class.
	"""
	def __init__(self):
		super().__init__()
	def initialize(self):
		super().initialize(640, 480, buildSettings.GAME_NAME+" ("+str(buildSettings.GAME_VERSION)+")")

	def run(self):
		while(True):
			self.frameUpdate()
			if self.keyPressed(window.K_ESCAPE): break
		self.exit()

