#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
LED交通信号灯模块 5V 红绿灯发光模块
"""

import GPIO as GPIO
import time


class RYGLED():

    # <設定>
    # 設定燈的 GPIO 介面 [紅,黃,綠]
    LED: list = [25, 24, 23]
    # 陰極陽極設定
    POL: bool = False
    # </設定>

    # 設定 GPIO 編號模式
    GPIO.setmode(GPIO.BCM)
    # 設定用作輸出的每個通道
    for n in LED:
        GPIO.setup(n, GPIO.OUT)

    def autoNot(self, val: bool) -> bool:
        """ 陰極陽極切換
        @param  {bool} val 是否應該為點亮狀態
        @return {bool} 實際應該傳送的布林值
        """
        if self.POL:
            return not val
        else:
            return val

    def int2bool(num: int) -> bool:
        """ 將數字轉換為布林值
        @param {int} 原數字
        @return {bool} 布林值
        """
        if num > 0:
            return True
        return False

    def light(self, switch: int):
        """ 點亮一個或多個燈
        @param {int} switch 設定每個燈的狀態
        3位數，分別為 [紅,黃,綠] ，0為不顯示，1為顯示。例如：
        100紅 10黃 1綠 110黃紅 11黃綠
        """
        if switch > 999:
            switch = 111
        elif switch < 0:
            switch = 0
        r: int = int(switch / 100)
        y: int = int(switch % 100 / 10)
        g: int = int(switch % 10)
        i: int = 0
        GPIO.output(self.LED, self.autoNot(False))  # for n in LED
        for isLight in [r, y, g]:
            gpio: int = self.LED[i]
            GPIO.output(gpio, self.autoNot(isLight))
            i += 1

    def lightOne(self, open: int):
        """ 点亮一个灯，其他灯熄灭
        @param {int} open -1紅 0黃 1綠
        """
        if open > 1:
            open = 1
        elif open < -1:
            open = -1
        switch: int = open + 1
        GPIO.output(self.LED, self.autoNot(False))  # for n in LED
        gpio: int = self.LED[switch]
        GPIO.output(gpio, self.autoNot(True))  # for n in LED


# 使用示例（灯依次动画开关）：
try:
    while True:
        ryg = RYGLED()
        ani = [1, 11, 111, 110, 100, 0]
        for light in ani:
            ryg.light(light)
            time.sleep(1)
except KeyboardInterrupt:
    print("Exit...")
    GPIO.cleanup()
