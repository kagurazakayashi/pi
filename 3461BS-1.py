#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
3461BS-1 數碼管顯示
持續掃描顯示，可輸入字串來更新顯示，如 "1234" "12.34" "A.1.2.3" "[1.2]" 等等
"""


import RPi.GPIO
import time
import threading


class DigitalTubeShow(threading.Thread):

    # 接線圖
    #   數字 GPIO 埠: 1-7 和 小數點 DP
    #   共陽/共陰 GPIO 埠: A-D
    #
    #   A  1  6  B  C  2  接
    #   x  x  x  x  x  x  線
    #
    #    111    數碼管
    #   6   2   單獨數字中
    #   6   2   每個管的
    #    777    編號
    #   5   3
    #   5   3
    #    444  DP
    #
    #   x  x  x  x  x  x  接
    #   5  4  DP 3  7  D  線

    # <設定>
    # 設定數字 GPIO 埠 [#1,#2,#3,#4,#5,#6,#7,DP]
    LED: list = [4, 27, 26, 13, 6, 17, 22, 19]
    # 設定共陽/共陰 GPIO 埠 [#A,#B,#C,#D]
    DIG: list = [12, 16, 20, 21]
    # 陰極陽極設定
    POL: bool = True
    # 重新整理時間
    FPS = 120
    # 上次顯示的字串
    last: str = ""
    # 本次顯示的字串，執行緒執行中可以隨時更新 text 屬性來更新字串
    text: str = ""
    # </設定>

    # 設定模式 GPIO 編號模式
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    # 設定用作輸入或輸出的每個通道
    for n in LED:
        RPi.GPIO.setup(n, RPi.GPIO.OUT)
    for n in DIG:
        RPi.GPIO.setup(n, RPi.GPIO.OUT)
    # 四個數字輪流顯示完作為一幀
    digSleep: float = 1 / (FPS * len(DIG))
    digLen: int = len(DIG)
    # 是否正在執行，設定為否則在本輪更新顯示後退出
    running: bool = False

    # 數字資料庫 [#1,#2,#3,#4,#5,#6,#7,DP]
    DAT: dict = {
        #    [ #1  ,  #2  ,  #3  ,  #4  ,  #5  ,  #6  ,  #7  ]
        ' ': [False, False, False, False, False, False, False],
        '0': [True,  True,  True,  True,  True,  True,  False],
        '1': [False, True,  True,  False, False, False, False],
        '2': [True,  True,  False, True,  True,  False, True],
        '3': [True,  True,  True,  True,  False, False, True],
        '4': [False, True,  True,  False, False, True,  True],
        '5': [True,  False, True,  True,  False, True,  True],
        '6': [True,  False, True,  True,  True,  True,  True],
        '7': [True,  True,  True,  False, False, False, False],
        '8': [True,  True,  True,  True,  True,  True,  True],
        '9': [True,  True,  True,  True,  False, True,  True],
        'A': [True,  True,  True,  False, True,  True,  True],
        'C': [True,  False, False, True,  True,  True,  False],
        'E': [True,  False, False, True,  True,  True,  False],
        'F': [True,  False, False, False, True,  True,  True],
        'H': [False, True,  True,  False, True,  True,  True],
        'I': [False, False, False, False, True,  True,  False],
        'J': [False, True,  True,  True,  True,  False, False],
        'L': [False, False, False, True,  True,  True,  False],
        'N': [False, False, True,  False, True,  False, True],
        'O': [True,  True,  True,  True,  True,  True,  False],
        'P': [True,  True,  False, False, True,  True,  True],
        'Q': [True,  True,  True,  False, False, True,  True],
        'S': [True,  False, True,  True,  False, True,  True],
        'U': [False, True,  True,  True,  True,  True,  False],
        'X': [False, True,  True,  False, True,  True,  True],
        'Y': [False, True,  True,  True,  False, True,  True],
        '-': [False, False, False, False, False, False, True],
        '_': [False, False, False, True,  False, False, False],
        '[': [True,  False, False, True,  True,  True,  False],
        ']': [True,  True,  True,  True,  False, False, False],
        '?': [True,  True,  False, False, True,  False, True],
        ',': [False, False, True,  True,  False, False, False],
        '>': [False, False, False, False, True,  True,  True],
        '<': [False, True,  True,  False, False, False, True],
        '^': [True,  True,  False, False, False, True,  False],
        '"': [False, True,  False, False, False, True,  False],
        "'": [False, False, False, False, False, True,  False],
    }

    def __init__(self):
        threading.Thread.__init__(self)
        # 設定 GPIO 引腳的輸出狀態
        self.cleanAll()

    def autoNot(self, val: bool) -> bool:
        """ 陰極陽極切換
        @param  {bool} val 是否應該為點亮狀態
        @return {bool} 實際應該傳送的布林值
        """
        if self.POL:
            return not val
        else:
            return val

    def showChar(self, group: int, char: str, dot=False) -> bool:
        """ 顯示某個字元
        @param {int}  group 數字序號
        @param {str}  char  要顯示的字元
        @param {bool} dot   顯示小數點
        """
        # 檢查是否在範圍內
        if char not in self.DAT:
            print('E/无法显示字符 ' + char)
            return False
        if group > self.digLen - 1:
            print('E/无效的数字位置 ' + str(group))
            return False
        # 設定 GPIO 引腳的輸出狀態，先清空每個數字顯示
        RPi.GPIO.output(self.DIG, self.autoNot(True))  # for n in DIG
        # 設定單個數字中的每個 LED 燈狀態
        selectCharArr: list[bool] = self.DAT[char]
        i: int = 0
        for ledStatus in selectCharArr:
            gpioId: int = self.LED[i]
            # print("设置第 " + str(group) + " 个数字（预期为 " + char + " ）中的第 " + str(i) + " 个LED（GPIO " + str(gpioId) + " ）状态为", autoNot(ledStatus))
            RPi.GPIO.output(gpioId, self.autoNot(ledStatus))
            i += 1
        RPi.GPIO.output(self.LED[-1], self.autoNot(dot))
        # 為選定數字的共陰/陽提供訊號，顯示這個數字
        selectGroup: int = self.DIG[group]
        RPi.GPIO.output(selectGroup, self.autoNot(False))
        # 程式休眠
        time.sleep(self.digSleep)
        return True

    def showString(self, displayStr: str) -> bool:
        """ 顯示字串
        例如： "1234" "12.34" "A.1.2.3" "[1.2]"
        @param {str} displayStr 顯示字串
        """
        # 分別檢查檢查無 . 的長度和 . 的長度
        noDotStr: str = displayStr.replace(".", "")
        noDotStrLen: int = len(noDotStr)
        if noDotStrLen > self.digLen or displayStr.count(".") > 4:
            print('E/不能显示超长字符串 ' + displayStr)
            return False
        # 不足位數在前面補空白
        elif noDotStrLen < self.digLen:
            displayStr = (" " * (self.digLen - noDotStrLen)) + displayStr
        # 逐個字進行解析
        strLen: str = len(displayStr)
        i: int = 0
        j: int = 0
        for char in displayStr:
            # 如果是 . 則因為已經在上一邊迴圈處理，不再處理
            if char == ".":
                i += 1
                continue
            # 檢查上一個字元
            prevChar: str = ""
            prevI = i - 1
            if prevI > 0:
                prevChar = displayStr[prevI]
                # 檢查無法顯示的連續 .
                if prevChar == "." and char == ".":
                    print('E/小数点使用不正确 ' + displayStr)
                    return False
            # 檢查下一個字元
            nextChar: str = ""
            nextI = i + 1
            dot = False
            if nextI < strLen:
                nextChar = displayStr[nextI]
                # 如果下一個字元是 . 則隨字元傳送 . 的狀態
                if nextChar == ".":
                    dot = True
            if self.showChar(j, char, dot) == False:
                return False
            j += 1
            i += 1
        return True

    def cleanAll(self):
        """清空所有顯示"""
        RPi.GPIO.output(self.DIG, self.autoNot(True))  # for n in DIG

    def run(self):
        """開始顯示"""
        self.running = True
        # 如果純執行輸出的話會變成 1,22,333,4444 ，需要掃描重新整理，依次顯示每個數字，只要顯示速度夠快，視覺殘留就能保持顯示
        while self.running:
            # 開始顯示 text 屬性字串，並在輸入資料不正確時恢復為上一個資料
            if self.showString(self.text):
                if self.last != self.text:
                    self.last = self.text
            elif self.text != self.last:
                    self.text = self.last
        print("Exit DigitalTubeShow...")


# 使用示例：
# tubeShow = DigitalTubeShow()
# tubeShow.start()
# startTime = time.time()
# try:
#     while True:
#         nowTime = time.time()
#         countTime = nowTime - startTime
#         tubeShow.text = str(int(countTime))
#         print(tubeShow.text)
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Exit...")
#     # 等待執行緒結束
#     tubeShow.running = False
#     tubeShow.join()
#     print("Cleanup...")
#     RPi.GPIO.cleanup()
