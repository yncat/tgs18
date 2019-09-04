# -*- coding: utf-8 -*-
# TGS19 background ambience handling
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import threading
import time
import bgtsound

STEP_VALUE=2

class Background(object):
	"""Background ambience can be slided louder / quieter."""
	def __init__(self):
		s=bgtsound.sound()
		s.stream("fx/background2.ogg")
		self.volume=0
		s.volume=self.volume
		self.sound=s
		self.thread=threading.Thread(target=self._thread)
		self.thread.setDaemon(True)
		self.thread_exit=False

	def play(self):
		self.sound.play_looped()
		self.thread.start()

	def terminate(self):
		self.sound.stop()
		self.thread_exit=True
		self.thread.join()
		self.thread=None

	def changeVolume(self,volume):
		"""本来の最小値と最大値は-100 0 だが、値としてはそれ以上まで上げられる。計算の際に丸め込みが起きる。同じ数だけ下げて上げると元に戻るようにするための処置。クリッピングしちゃうと、55回下げたら50回のアップで最大になってしまうので。"""
		v=self.volume+volume
		self.volume=v

	def _thread(self):
		while(True):
			if self.thread_exit is True: break
			time.sleep(0.1)
			v=self.sound.volume
			vtarget=self.volume
			if vtarget<-100: vtarget=100
			if vtarget>0:vtarget=0
			if v==vtarget: continue
			if abs(v-vtarget)<STEP_VALUE:
				self.sound.volume=vtarget
				continue
			#end ステップ感覚以下丸め込み
			self.sound.volume=v+STEP_VALUE if v<vtarget else v-STEP_VALUE
		#end thread loop
	#end _thread
