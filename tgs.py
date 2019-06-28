# -*- coding: utf-8 -*-
# TGS19 bootstrap
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>

import openal 
import appMain
import helper
import globalVars

def main():
	helper.InstallOpenAl()
	app=appMain.Application()
	globalVars.app=app
	app.initialize()
	app.run()
#global schope
if __name__ == "__main__": main()