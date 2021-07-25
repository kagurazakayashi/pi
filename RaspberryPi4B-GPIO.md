# 树莓派4B GPIO引脚对照表

- | GPIO引脚用途 | wiringPi 编码 | BCM 编码 | 功能名 | 物理引脚 BOARD 编码 | ...

|    GPIO   | wPi | BCM |   NAME  | Ph |\|| Ph |  NAME   | BCM | wPi |   GPIO    |
|  -------: | --: | --: | ------: | :- |--| -: | :------ | :-- | :-- | :-------- |
|           |     |     |    3.3V |  1 |\||  2 | 5V      |     |     |           |
|      SDA1 |   8 |   2 |   SDA.1 |  3 |\||  4 | 5V      |     |     |           |
|      SCL1 |   9 |   3 |   SCL.1 |  5 |\||  6 | GND     |     |     |           |
| GPIO_GCLK |   7 |   4 |  GPIO.7 |  7 |\||  8 | TXD     | 14  | 15  | TXD0      |
|           |     |     |     GND |  9 |\|| 10 | RXD     | 15  | 16  | RXD0      |
| GPIO_GEN0 |   0 |  17 |  GPIO.0 | 11 |\|| 12 | GPIO.1  | 18  | 1   | GPIO_GEN1 |
| GPIO_GEN2 |   2 |  27 |  GPIO.2 | 13 |\|| 14 | GND     |     |     |           |
| GPIO_GEN3 |   3 |  22 |  GPIO.3 | 15 |\|| 16 | GPIO.4  | 23  | 4   | GPIO_GEN4 |
|           |     |     |    3.3V | 17 |\|| 18 | GPIO.5  | 24  | 5   | GPIO_GEN5 |
|  SPI_MOSI |  12 |  10 |    MOSI | 19 |\|| 20 | GND     |     |     |           |
|  SPI_MISO |  13 |   9 |    MISO | 21 |\|| 22 | GPIO.6  | 25  | 6   | GPIO_GEN6 |
|  SPI_SCLK |  14 |  11 |    SCLK | 23 |\|| 24 | CE0     | 8   | 10  | SPI_CE0_N |
|           |     |     |     GND | 25 |\|| 26 | CE1     | 7   | 11  | SPI_CE1_N |
|     ID_SD |  30 |   0 |   SDA.0 | 27 |\|| 28 | SCL.0   | 1   | 31  | ID_SC     |
|           |  21 |   5 | GPIO.21 | 29 |\|| 30 | GND     |     |     |           |
|           |  22 |   6 | GPIO.22 | 31 |\|| 32 | GPIO.26 | 12  | 26  |           |
|           |  23 |  13 | GPIO.23 | 33 |\|| 34 | GND     |     |     |           |
|           |  24 |  19 | GPIO.24 | 35 |\|| 36 | GPIO.27 | 16  | 27  |           |
|           |  25 |  26 | GPIO.25 | 37 |\|| 38 | GPIO.28 | 20  | 28  |           |
|           |     |     |     GND | 39 |\|| 40 | GPIO.29 | 21  | 29  |           |

# gpio readall / Pi 4B

| BCM | wPi |   Name  | Mode | V | Ph |\|| Ph | V | Mode | Name    | wPi | BCM |
| --: | --: | ------: | ---: | - | :- |--| -: | - | :--- | :------ | :-- | :-- |
|     |     |    3.3v |      |   |  1 |\|| 2  |   |      | 5v      |     |     |
|   2 |   8 |   SDA.1 |   IN | 1 |  3 |\|| 4  |   |      | 5v      |     |     |
|   3 |   9 |   SCL.1 |   IN | 1 |  5 |\|| 6  |   |      | 0v      |     |     |
|   4 |   7 | GPIO. 7 |   IN | 1 |  7 |\|| 8  | 1 | IN   | TxD     | 15  | 14  |
|     |     |      0v |      |   |  9 |\|| 10 | 1 | IN   | RxD     | 16  | 15  |
|  17 |   0 | GPIO. 0 |   IN | 0 | 11 |\|| 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
|  27 |   2 | GPIO. 2 |   IN | 0 | 13 |\|| 14 |   |      | 0v      |     |     |
|  22 |   3 | GPIO. 3 |   IN | 0 | 15 |\|| 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
|     |     |    3.3v |      |   | 17 |\|| 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
|  10 |  12 |    MOSI |   IN | 0 | 19 |\|| 20 |   |      | 0v      |     |     |
|   9 |  13 |    MISO |   IN | 0 | 21 |\|| 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
|  11 |  14 |    SCLK |   IN | 0 | 23 |\|| 24 | 1 | IN   | CE0     | 10  | 8   |
|     |     |      0v |      |   | 25 |\|| 26 | 1 | IN   | CE1     | 11  | 7   |
|   0 |  30 |   SDA.0 |   IN | 1 | 27 |\|| 28 | 1 | IN   | SCL.0   | 31  | 1   |
|   5 |  21 | GPIO.21 |   IN | 1 | 29 |\|| 30 |   |      | 0v      |     |     |
|   6 |  22 | GPIO.22 |   IN | 1 | 31 |\|| 32 | 0 | IN   | GPIO.26 | 26  | 12  |
|  13 |  23 | GPIO.23 |   IN | 0 | 33 |\|| 34 |   |      | 0v      |     |     |
|  19 |  24 | GPIO.24 |   IN | 0 | 35 |\|| 36 | 0 | IN   | GPIO.27 | 27  | 16  |
|  26 |  25 | GPIO.25 |   IN | 0 | 37 |\|| 38 | 0 | IN   | GPIO.28 | 28  | 20  |
|     |     |      0v |      |   | 39 |\|| 40 | 0 | IN   | GPIO.29 | 29  | 21  |
| BCM | wPi |   Name  | Mode | V | Ph |\|| Ph | V | Mode | Name    | wPi | BCM |

# pinout

```
,--------------------------------.
| oooooooooooooooooooo J8   +======
| 1ooooooooooooooooooo  PoE |   Net
|  Wi                    1o +======
|  Fi  Pi Model 4B  V1.4 oo      |
|        ,----. +---+         +====
| |D|    |SoC | |RAM|         |USB3
| |S|    |    | |   |         +====
| |I|    `----' +---+            |
|                   |C|       +====
|                   |S|       |USB2
| pwr   |hd|   |hd| |I||A|    +====
`-| |---|m0|---|m1|----|V|-------'
```

|                     |                         |
| ------------------- | ----------------------- |
| Revision            | d03114                  |
| SoC                 | BCM2711                 |
| RAM                 | 8GB                     |
| Storage             | MicroSD                 |
| USB ports           | 4 (of which 2 USB3)     |
| Ethernet ports      | 1 (1000Mbps max. speed) |
| Wi-fi               | True                    |
| Bluetooth           | True                    |
| Camera ports (CSI)  | 1                       |
| Display ports (DSI) | 1                       |

## J8
|        |    |  |    |        |
| -----: | :- |--| -: | :----- |
|    3V3 |  1 |\|| 2  | 5V     |
|  GPIO2 |  3 |\|| 4  | 5V     |
|  GPIO3 |  5 |\|| 6  | GND    |
|  GPIO4 |  7 |\|| 8  | GPIO14 |
|    GND |  9 |\|| 10 | GPIO15 |
| GPIO17 | 11 |\|| 12 | GPIO18 |
| GPIO27 | 13 |\|| 14 | GND    |
| GPIO22 | 15 |\|| 16 | GPIO23 |
|    3V3 | 17 |\|| 18 | GPIO24 |
| GPIO10 | 19 |\|| 20 | GND    |
|  GPIO9 | 21 |\|| 22 | GPIO25 |
| GPIO11 | 23 |\|| 24 | GPIO8  |
|    GND | 25 |\|| 26 | GPIO7  |
|  GPIO0 | 27 |\|| 28 | GPIO1  |
|  GPIO5 | 29 |\|| 30 | GND    |
|  GPIO6 | 31 |\|| 32 | GPIO12 |
| GPIO13 | 33 |\|| 34 | GND    |
| GPIO19 | 35 |\|| 36 | GPIO16 |
| GPIO26 | 37 |\|| 38 | GPIO20 |
|    GND | 39 |\|| 40 | GPIO21 |

## POE
|      |   |  |   |      |
| ---- | - |--| - | ---- |
| TR01 | 1 |\|| 2 | TR00 |
| TR03 | 3 |\|| 4 | TR02 |

# 查询命令
- `gpio readall`: 对应的GPIO接口功能
  - `Oops - unable to determine board type...` 的话需要更新：
    - `cd /tmp`
    - `wget https://project-downloads.drogon.net/wiringpi-latest.deb`
    - `sudo dpkg -i wiringpi-latest.deb`
- `pinout`: 板子信息及GPIO接口信息