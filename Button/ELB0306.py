#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
响应按钮
"""

import RPi.GPIO as GPIO
import time


class Buttons():
    # 设置引脚编码模式
    gpioMode = GPIO.BCM
    # 检测电平是上升还是下降 GPIO.PUD_UP / GPIO.PUD_DOWN：
    pudMode = GPIO.PUD_UP
    # 0 视为按下还是 1 视为按下
    isDownVal: int = 0
    # 按键时可能有电平抖动，进行几次重复验证
    chkDownTimes: int = 2
    # 每次重复验证间隔多久
    chkDownTime: float = 0.05
    # 设置按键引脚编码列表
    keys = [20]

    # 以下不要修改
    keysLen = 0
    keyIsDown = []
    keyChkDown = []

    def __init__(self):
        GPIO.setmode(self.gpioMode)  # 设置引脚编码模式
        for key in self.keys:
            GPIO.setup(key, GPIO.IN, self.pudMode)  # 初始化引脚为输入模式
            self.keyIsDown.append(0)  # 初始化按键状态数组
            self.keyChkDown.append(True)  # 初始化按键状态数组
            self.keysLen += 1

    def chkButtons(self):
        for t in range(self.chkDownTimes): # 按键时可能有电平抖动多验证几次
            time.sleep(self.chkDownTime) # 每次验证间隔时间
            for i in range(self.keysLen):
                key: int = self.keys[i]
                keyM: int = self.keyIsDown[i]
                chkDown: bool = self.keyChkDown[i]
                inputVal = GPIO.input(key)
                if (chkDown == True and inputVal == self.isDownVal):
                    keyM += 1
                    if keyM == self.chkDownTimes:
                        print("KEY " + str(i) + " DOWN")
                        self.keyChkDown[i] = False
                    self.keyIsDown[i] = keyM
                elif (chkDown == False and inputVal != self.isDownVal):
                    keyM -= 1
                    if keyM == 0:
                        print("KEY " + str(i) + " UP")
                        self.keyChkDown[i] = True
                    self.keyIsDown[i] = keyM

try:
    btn = Buttons()
    while True:
        time.sleep(0.05)
        btn.chkButtons()
except KeyboardInterrupt:
    print("Exit...")
    GPIO.cleanup()
