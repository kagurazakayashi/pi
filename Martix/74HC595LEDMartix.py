#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
LED 8*8 全彩点阵屏
74HC595D 移位寄存器 x4
"""
import RPi.GPIO
# pip3 install wiringpi (https://github.com/WiringPi/WiringPi-Python)
import wiringpi
import time


class Martix():
    # 接線
    # Pi          Martix
    # 5V          <-> VCC
    # SPISCLK     <-> CLK
    # CE0(SPICS0) <-> CE
    # SPIMOSI     <-> MOSI
    # GND         <-> GND
    # 可能需要先启动 SPI 功能
    # sudo raspi-config
    # Interface Options -> SPI -> yes -> The SPI interface is enabled

    # <設定>
    SPIchannel = 0  # CE0 / CE1
    SPIspeed = 500000  # 最大时钟速度 Hz
    # </設定>

    def __init__(self):
        # 打开 SPI 设备， 0 为 /dev/spi-decv0.0
        wiringpi.wiringPiSetupGpio()
        wiringpi.wiringPiSPISetup(self.SPIchannel, self.SPIspeed)

    def clear(self):
        wiringpi.wiringPiSPIDataRW(self.SPIchannel, bytes([0]))

    def test(self):
        while True:
            heart = [0x00, 0x66, 0xFF, 0xFF, 0xFF, 0x7E, 0x3C, 0x18]
            j: int = 0
            for nowHeart in heart:
                data = [nowHeart, 0xFF, 0xFF, 0x01 << j]
                print(data)
                wiringpi.wiringPiSPIDataRW(self.SPIchannel, bytes(data))
                time.sleep(1)
                j = j + 1


martix = Martix()
martix.test()
# martix.clear()
