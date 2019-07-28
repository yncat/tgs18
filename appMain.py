# -*- coding: utf-8 -*-
# TGS19 main implementation
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal
import bgtsound
import buildSettings
import window
import world
class Application(window.SingletonWindow):
	"""
	The game's main application class.

	Instantiate this class, call initialize method, then call run method to start the application. Other methods are internally used and should not be called from outside of the class.
	"""
	def __init__(self):
		super().__init__()
	def initialize(self):
		super().initialize(1200, 800, buildSettings.GAME_NAME+" ("+str(buildSettings.GAME_VERSION)+")")
		openal.oalGetListener().set_gain(8)
		self.pointSample=bgtsound.sample("fx/point.ogg")


	def run(self):
		s=self.getScreenSize()
		self.setMousePos(s[0]/2,s[1]/2)
		w=world.World()
		while(True):
			self.frameUpdate()
			w.frameUpdate()
			if self.keyPressed(window.K_ESCAPE): break
		self.exit()

	def exit(self):
		openal.oalQuit()
