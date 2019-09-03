# -*- coding: utf-8 -*-
# TGS19 main implementation
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import openal
import bgtsound
import buildSettings
import dialog
import osc
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
		self.gameoverSample=bgtsound.sample("fx/gameover.ogg")
		self.needleSample=bgtsound.sample("fx/needle.ogg")
		self.world=None
		self.oscController=osc.Controller()


	def run(self):
		s=self.getScreenSize()
		self.setMousePos(s[0]/2,s[1]/2)
		self.oscController.recalibrate()
		self._waitForReturn()
		p=self.oscController.getPosition2d()
		print(p)
		self.oscController.recalibrate()
		self.say("start!")
		w=world.World()
		self.world=w
		while(True):
			self.frameUpdate()
			w.frameUpdate()
			if w.getGameover(): break
			if self.keyPressed(window.K_ESCAPE): break
		#end game loop
		bgtsound.playOneShot(self.gameoverSample)
		w.clear()
		w.terminate()
		self.wait(3000)
		dialog.dialog("結果", "今回の特典は、%dでした。" % w.getScore())
		self.exit()

	def onExit(self):
		if self.world: self.world.terminate()
		self.oscController.cleanup()
		openal.oalQuit()
		return True

	def _waitForReturn(self):
			self.say("Press enter to continue")
			while(True):
				self.frameUpdate()
				if self.keyPressed(window.K_RETURN): break

	def getOscController(self):
		return self.oscController