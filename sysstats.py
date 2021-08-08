# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

oldNetSpeed = {}

def runcmd(cmd:str) -> str:
    return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

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
                        info["rs"] = int(lineDataArr[5]) - oldNetSpeed[ethName][0]
                elif lineDataArr[0] == "TX" and lineDataArr[1] == "packets":
                    info["tx"] = lineDataArr[5]
                    if ethName in oldNetSpeed.keys():
                        info["ts"] = int(lineDataArr[5]) - oldNetSpeed[ethName][1]
            i += 1
        ikeys = info.keys()
        if "ip4" in ikeys or "ip6" in ikeys:
            returns[ethName] = info
            oldNetSpeed[ethName] = [int(info["rx"]), int(info["tx"])]
    return returns


while True:
    # 当前 IP 地址
    iIP = runcmd("hostname -I | cut -d' ' -f1")
    # 处理器使用量百分比
    iCpuPercentage = runcmd("cat /proc/loadavg | awk '{printf \"%3d\", $1*100}'")
    # 处理器温度
    iCpuTemp = runcmd("cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"%.1f\", $1/1000}'")
    # 内存信息
    iMemArr = runcmd("free | awk 'NR==2{printf \"%d,%d,%d,%.2f\", $3,$4,$2,$3*100/$2 }'").split(',')
    iMemUsed = iMemArr[0]
    iMemFree = iMemArr[1]
    iMemTotal = iMemArr[2]
    iMemPercentage = iMemArr[3]
    # 磁盘使用
    iDiskArr = runcmd("df | awk '$NF==\"/\"{printf \"%d,%d,%d,%d\", $3,$4,$2,$5}'").split(',')
    iDiskUsed = iDiskArr[0]
    iDiskFree = iDiskArr[1]
    iDiskTotal = iDiskArr[2]
    iDiskPercentage = iDiskArr[3]

    print("IP: " + iIP)
    print("CPU: " + iCpuPercentage)
    print("CPU Temp: " + iCpuTemp)
    print("MEM: " , iMemArr)
    print("Disk: " , iDiskArr)
    print("Network: " , netspeed())
    netspeed()
    print("-" * 15)

    time.sleep(1)
