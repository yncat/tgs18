# -*- coding: utf-8 -*-
# TGS19 helper functions
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>

import os
import shutil
import winpaths
import platform_utils.paths as paths

def InstallOpenAl():
	if paths.is_windows:
		_installOpenAlWin()

def _installOpenAlWin():
	appdata=winpaths.get_appdata()
	if not os.path.isfile(appdata+"\\alsoft.ini"): shutil.copyfile("other\\alsoft.ini",appdata+"\\alsoft.ini")
	fld=paths.app_data_path('openal')
	if not os.path.isfile(fld+"\\hrtf\\default-44100.mhr"):
		paths.ensure_path(fld+"\\hrtf")
		shutil.copyfile("other\\default-44100.mhr",fld+"\\hrtf\\default-44100.mhr")


