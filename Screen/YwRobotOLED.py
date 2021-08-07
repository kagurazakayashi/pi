# GND <-> GND
# 5V <-> 5V
# SDA <-> SDA1
# SCL <-> SCL1

# sudo apt-get install i2c-tools
# sudo apt-get install python-smbus
# sudo i2cdetect -l
# sudo i2cdetect -y 1
# pip3 install board adafruit_ssd1306 adafruit-circuitpython-ssd1306 adafruit-blinka RPI.GPIO

from board import SCL, SDA
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(SCL, SDA)

# 创建设备类，设置屏幕尺寸、协议、地址
# I2C 地址用 sudo i2cdetect -y 1 查
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 填充整个屏幕为空，清空屏幕
display.fill(0)
display.show()

# 设置某个像素的显示（X，Y，是否亮）
display.pixel(0, 0, 1)
display.show()

# 显示英数文字:

# 创建用于绘图的空白图像， 1是 1位图
width = display.width
height = display.height
image = Image.new("1", (width, height))
# 获取绘图对象以在图像上绘制
draw = ImageDraw.Draw(image)
# 绘制一个全屏长方形，全黑
draw.rectangle((0, 0, width, height), outline=0, fill=0)
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
display.image(image)
display.show()