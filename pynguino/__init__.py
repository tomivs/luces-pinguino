#! /usr/bin/python
#-*- coding: utf-8 -*- 

#Copyright (c) <2011> Yeison Nolberto Cardona Álvarez <yeison.eng@gmail.com>
#https://sites.google.com/site/yeisoneng/
#All rights reserved.

#Este módulo es distribuido bajo licencia libre, ver archivo licence.

from raiseError import PynguinoError

import os,serial
if not(os.name=='nt' or  os.name=='posix'): 
    raise PynguinoError(9)

from PinguinoProcessing import PinguinoProcessing
from PinguinoSockets import PinguinoSockets
from PinguinoLCD import PinguinoLCD
