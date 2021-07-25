#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
3461BS-1 數碼管實時顯示 CPU 溫度
"""
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
from NixieTube3461BS1 import NixieTube
import RPi.GPIO
import time
import threading

tubeShow = NixieTube()
tubeShow.start()
startTime = time.time()
try:
    while True:
        f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
        text:str = f.read()
        f.close()
        temp:float = int(text) / 1000
        tempstr:str = str(temp)
        tempshow:str = ""
        for char in tempstr:
            tempshow += char
            noDotStr: str = tempshow.replace(".", "")
            if len(noDotStr) == 4:
                break
        while True:
            noDotStr: str = tempshow.replace(".", "")
            if len(noDotStr) == 4:
                break
            tempshow = " " + tempshow
        tubeShow.text = tempshow
        time.sleep(1)
except KeyboardInterrupt:
    print("Exit...")
    # 等待執行緒結束
    tubeShow.running = False
    tubeShow.join()
    print("Cleanup...")
    RPi.GPIO.cleanup()