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
import subprocess
import time
import os
import psutil
from datetime import datetime

# 设置偏移 屏幕大小 128x64
# load_default 8*21 0,-2,8
# simsun 4*7 0,0,12
paddingLeft = 0
paddingTop = -1
lineHeight = 16
display = None
# 创建设备类，设置屏幕尺寸、协议、地址
# I2C 地址用 sudo i2cdetect -y 1 查
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
# 装载默认字体（不支持中文）
# font = ImageFont.load_default()
# 加载自定字体
font = ImageFont.truetype("/home/pi/pi/simsun.ttc", 18, encoding="unic")  # 设置字体

oldNetSpeed = {}
cpumax = 0
gpumax = 0


def clearscreen(fill=0):
    # 填充整个屏幕为空，清空屏幕
    display.fill(fill)
    display.show()


def genteststr():
    scrstr: list[str] = []
    for linei in range(0, 9):
        line: str = str(linei) + "|"
        for _ in range(0, 2):
            for rowi in range(0, 9):
                line += str(rowi)
        scrstr.append(line)
    showtext(scrstr)


def showtext(texts: list, reverse=False):
    fill0: int = 0
    fill1: int = 255
    if reverse:
        fill0 = fill1
        fill1 = 0
    # 创建用于绘图的空白图像， 1是 1位图
    width = display.width
    height = display.height
    image: Image = Image.new("1", (width, height))
    # 获取绘图对象以在图像上绘制
    draw: ImageDraw = ImageDraw.Draw(image)
    # 绘制一个全屏长方形，全黑
    draw.rectangle((0, 0, width, height), outline=0, fill=fill0)
    for linei in range(0, len(texts)):
        # 将字符绘制进去 X Y 文字 字体 填充
        draw.text((paddingLeft, paddingTop + lineHeight * linei),
                  texts[linei], font=font, fill=fill1)
    # 显示该图片
    display.image(image)
    display.show()


def printscreen(texts: list):
    print("-" * 20)
    for texti in range(0, len(texts)):
        text = str(texti) + "| " + texts[texti]
        print(text)
    print("-" * 20)


def runcmd(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()


def sizestr(val: float, dot: int = 0) -> str:
    def str_of_size(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return str_of_size(integer, remainder, level)
        else:
            return integer, remainder, level

    units = [' B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = str_of_size(val, 0, 0)
    if level+1 > len(units):
        level = -1
    return ('{}.{:>01d} {}'.format(int(integer), int(remainder/100), units[level]))


def numaddzero(num, tolen=3, addchar=" ") -> str:
    multiplication: int = 1
    multiplications: list[int] = []
    for i in range(0, tolen):
        multiplications.append(multiplication)
        multiplication *= 10
    text: str = str(num)
    addlen: int = 0
    for multiplication in multiplications[::-1]:
        if multiplication == 1:
            break
        if num < multiplication:
            addlen += 1
    text = addchar * addlen + text
    return text


def straddzero(text: str, tolen=3, addchar=" ") -> str:
    strlen: int = len(text)
    if strlen >= tolen:
        return text
    difflen: int = tolen - strlen
    return addchar * difflen + text


def keepnumbers(text: str) -> str:
    nfilter: filter = filter(lambda ch: ch in '0123456789.', text)
    ntext: str = ''.join(list(nfilter))
    return ntext


def netspeed() -> list:
    ifconfig = runcmd("ifconfig")
    eths = ifconfig.split('\n\n')
    returns = {}
    for eth in eths:
        info = {}
        ethLines = eth.split('\n')
        ethName = ""
        i = 0
        for line in ethLines:
            line = line.strip()
            lineDataArr = line.split(' ')
            if i == 0:
                name = line.split(':')[0]
                ethType = name[:-1]
                if ethType != "eth" and ethType != "wlan":
                    break
                ethName = name
            elif i == 1:
                if lineDataArr[0] == "inet":
                    info["ip4"] = lineDataArr[1]
                    info["netmask"] = lineDataArr[4]
                    info["broadcast"] = lineDataArr[7]
            elif i == 2:
                if lineDataArr[0] == "inet6":
                    info["ip6"] = lineDataArr[1]
            else:
                if lineDataArr[0] == "RX" and lineDataArr[1] == "packets":
                    info["rx"] = lineDataArr[5]
                    if ethName in oldNetSpeed.keys():
                        info["rs"] = int(lineDataArr[5]) - \
                            oldNetSpeed[ethName][0]
                elif lineDataArr[0] == "TX" and lineDataArr[1] == "packets":
                    info["tx"] = lineDataArr[5]
                    if ethName in oldNetSpeed.keys():
                        info["ts"] = int(lineDataArr[5]) - \
                            oldNetSpeed[ethName][1]
            i += 1
        ikeys = info.keys()
        if "ip4" in ikeys or "ip6" in ikeys:
            returns[ethName] = info
            oldNetSpeed[ethName] = [int(info["rx"]), int(info["tx"])]
        # break # 只取首个网卡
    return returns


def p0() -> list:
    nowtime: datetime = datetime.now()
    boottime: datetime = datetime.fromtimestamp(psutil.boot_time())
    runtime: str = str(nowtime - boottime)
    runtimeArr: list[str] = runtime.split(":")
    runtime = ""
    for i in range(0, len(runtimeArr)):
        rstr: str = runtimeArr[i]
        if i == len(runtimeArr) - 1:
            rstrArr: list[str] = rstr.split(".")
            runtime += rstrArr[0]
        else:
            runtime += rstr + ":"
    osinfo = os.uname()
    return [
        "时间  " + time.strftime("%H:%M:%S", time.localtime()),
        time.strftime("%Y-%m-%d", time.localtime()).center(14),
        "运行 " + straddzero(runtime, 9),
        osinfo.nodename.center(14),
    ]


def p1() -> list:
    global cpumax, gpumax
    # 处理器使用量百分比
    icpupercentage: str = runcmd(
        "cat /proc/loadavg | awk '{printf \"%3d\", $1*100}'")
    # 处理器温度
    icputemp: float = float(runcmd(
        "cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"%.1f\", $1/1000}'"))
    if icputemp > cpumax:
        cpumax = icputemp
    # GPU温度
    igputempstr: str = runcmd("/opt/vc/bin/vcgencmd measure_temp")
    igputemp: int = int(float(keepnumbers(igputempstr)))
    if igputemp > gpumax:
        gpumax = igputemp
    # CPU频率
    iclockstr: str = runcmd("/opt/vc/bin/vcgencmd measure_clock arm")
    iclock: str = str(int(float(iclockstr.split("=")[1]) / 1000000)) + " MHz"
    # str
    return [
        "处理芯片" + numaddzero(int(icpupercentage), 4) + " %",
        "频率" + straddzero(iclock, 10),
        "CPU" + numaddzero(int(icputemp), 3) + "℃/" +
        numaddzero(int(cpumax), 3) + "℃",
        "GPU" + numaddzero(int(igputemp), 3) + "℃/" +
        numaddzero(int(gpumax), 3) + "℃",
    ]


def p2() -> list:
    # 内存信息
    imemarr: str = runcmd(
        "free | awk 'NR==2{printf \"%d,%d,%d,%.2f\", $3,$4,$2,$3*100/$2 }'").split(',')
    imemused: float = float(imemarr[0]) * 1024
    imemfree: float = float(imemarr[1]) * 1024
    imemtotal: float = float(imemarr[2]) * 1024
    imempercentage: float = float(imemarr[3])
    return [
        "运行内存 " + str(numaddzero(round(imempercentage), 3)) + " %",
        "已用 " + straddzero(sizestr(imemused), 9),
        "可用 " + straddzero(sizestr(imemfree), 9),
        "总计 " + straddzero(sizestr(imemtotal), 9)
    ]


def p3() -> list:
    # 磁盘使用
    idiskarr: str = runcmd(
        "df | awk '$NF==\"/\"{printf \"%d,%d,%d,%d\", $3,$4,$2,$5}'").split(',')
    idiskused: float = float(idiskarr[0]) * 1024
    idiskfree: float = float(idiskarr[1]) * 1024
    idisktotal: float = float(idiskarr[2]) * 1024
    idiskpercentage = int(idiskarr[3])
    return [
        "系统SD卡 " + str(numaddzero(round(idiskpercentage), 3)) + " %",
        "已用 " + straddzero(sizestr(idiskused), 9),
        "可用 " + straddzero(sizestr(idiskfree), 9),
        "总计 " + straddzero(sizestr(idisktotal), 9)
    ]


def p4() -> list:
    # 网卡
    netinfo: list = netspeed()
    netnames: list = netinfo.keys()
    if len(netnames) == 0:
        showstr: list[str] = ["没有活动网卡", "", "", ""]
        printscreen(showstr)
        showtext(showstr)
        return
    netname: str = list(netnames)[0]
    ethinfo: list = netinfo[netname]
    showstr: list[str] = ["网卡 " + netname, "", "↑ ", "↓ "]
    if "ip4" in ethinfo:
        showstr[1] = ethinfo["ip4"]
    elif "ip6" in ethinfo:
        showstr[1] = ethinfo["ip6"]
    if "ts" in ethinfo:
        showstr[2] += straddzero(sizestr(ethinfo["ts"]), 9) + "/s"
    if "rs" in ethinfo:
        showstr[3] += straddzero(sizestr(ethinfo["rs"]), 9) + "/s"
    return showstr


def run():
    clearscreen(255)
    time.sleep(1)
    while True:
        # p4()
        # time.sleep(1)
        showstr:list[str] = []
        stepsec = 3
        for i in range(1, 16):
            if i >= 1 and i <= 3:
                showstr = p0()
            elif i >= 4 and i <= 6:
                showstr = p1()
            elif i >= 7 and i <= 9:
                showstr = p2()
            elif i >= 10 and i <= 12:
                showstr = p3()
            if i >= 13 and i <= 15:
                showstr = p4()
            else:
                netspeed()
            printscreen(showstr)
            showtext(showstr)
            time.sleep(1)


try:
    run()
except KeyboardInterrupt:
    print("Exit...")
    clearscreen(255)
    time.sleep(1)
    clearscreen()
    # GPIO.cleanup()
