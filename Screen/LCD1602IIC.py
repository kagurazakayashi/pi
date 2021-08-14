# GND <-> GND
# VCC <-> 5V
# SDA <-> SDA1
# SCL <-> SCL1

# sudo apt-get install i2c-tools
# sudo apt-get install python-smbus
# sudo i2cdetect -l
# sudo i2cdetect -y 1

# pip3 install logx

import time
import LCD1602 as LCD # wget https://raw.githubusercontent.com/dengzii/RespberryPi/master/LCD1602_IIC/LCD1602.py

# 初始化 LCD 驱动库
LCD.init_lcd()
# 显示字符串（第几个字符，第几行，字符串）
LCD.print_lcd(0, 0, '1234567890123456')
LCD.print_lcd(3, 1, 'LINE 2')
# 背光开关 0/1
LCD.turn_light(1)
# 显示时间
while True:
    now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
    LCD.print_lcd(1, 1, now)
    time.sleep(0.5)
