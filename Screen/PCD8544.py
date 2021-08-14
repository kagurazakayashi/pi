#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# sudo apt-get install python-pip python-dev build-essential
# pip3 install RPi.GPIO
# git clone https://github.com/adafruit/Adafruit_Nokia_LCD.git
# cd Adafruit_Nokia_LCD
# sudo python3 setup.py install
# pip3 install Adafruit_BBIO

import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 端口设定
SCLK = 17
DIN = 18
DC = 27
RST = 23
CS = 22
SPI_PORT = 0
SPI_DEVICE = 0

# 端口初始化
# self, dc, rst, sclk=None, din=None, cs=None, gpio=None, spi=None
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
# disp = LCD.PCD8544(dc=DC, rst=RST, sclk=SCLK, din=DIN, cs=CS, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
disp.begin(contrast=60)

# 清除屏幕
disp.clear()
disp.display()

# 创建用于绘图的空白图像， 1是 1位图
width = LCD.LCDWIDTH
height = LCD.LCDHEIGHT
image = Image.new("1", (width, height))
# 获取绘图对象以在图像上绘制
draw = ImageDraw.Draw(image)
# 绘制一个全屏长方形，全白
draw.rectangle((0,0,width, height), outline=255, fill=255)
# 装载默认字体（不支持中文）
font = ImageFont.load_default()
# 加载自定字体
# font = ImageFont.truetype("simsun.ttc", 20, encoding="unic")  # 设置字体
# 设置偏移
paddingLeft = 0
paddingTop = -2
lineHeight = 8
for i in range(0, 9):
    # 将字符绘制进去 X Y 文字 字体 填充
    draw.text((paddingLeft, paddingTop + lineHeight * i), str(i) + "|2345678901234567890", font=font, fill=255)
# 显示该图片
disp.image(image)
disp.display()
time.sleep(1)