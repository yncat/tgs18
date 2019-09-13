# -*- coding: utf-8 -*-
# TGS19 main implementation
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import datetime
import glob
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
		self.countSample=bgtsound.sample("fx/count_new.ogg")
		self.gameoverSample=bgtsound.sample("fx/gameover.ogg")
		self.needleSample=[]
		for i in range(3):
			self.needleSample.append(bgtsound.sample("fx/attack%d.ogg" % (i+1)))
		#end needle load
		self.clearSample=[]
		for elem in glob.glob("fx/clears/*.ogg"):
			self.clearSample.append(bgtsound.sample(elem))
		#end clear sample loading
		self.world=None
		self.oscController=osc.Controller()


	def run(self):
		s=self.getScreenSize()
		self.setMousePos(s[0]/2,s[1]/2)
		self.homeSound=bgtsound.sound()
		self.homeSound.stream("fx/home.ogg")
		while(True):
			self.homeSound.play_looped()
			self.frameUpdate()
			if self.keyPressed(window.K_KP0) or self.keyPressed(window.K_0):
				self.oscController.recalibrate()
				self.say("センサー準備完了")
			#end recalibration
			if self.keyPressed(window.K_RETURN) or self.keyPressed(window.K_KP_ENTER): self.play()
			if self.keyPressed(window.K_ESCAPE): break

	def play(self):
		self.homeSound.stop()
		self.say("start!")
		w=world.World()
		self.world=w
		while(True):
			self.frameUpdate()
			w.frameUpdate()
			if self.keyPressed(window.K_KP0) or self.keyPressed(window.K_0): self.oscController.recalibrate()
			if w.getGameover(): break
			if self.keyPressed(window.K_ESCAPE) or self.keyPressed(window.K_KP9): break
		#end game loop
		bgtsound.playOneShot(self.gameoverSample,vol=-15)
		w.clear()
		w.terminate()
		self.wait(3000)
		s="ゲームオーバー! あなたは、%d匹の蚊をやっつけて、%d回、蚊に刺されました。" % (w.getScore(), w.getAttacked())
		self.say(s)
		f=open("game_log.txt","a")
		f.write("%s: kill %d, damage %d.\n" % (datetime.datetime.now(),w.getScore(), w.getAttacked()))
		f.close()
		
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