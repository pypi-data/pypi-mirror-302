#!/usr/bin/env python3

from time import time, sleep, localtime
from gpiozero.output_devices import OutputDevice


CLK = 21
DIO = 20
# 0-9, a-z, blank, dash, star
_SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

"""
      A
     ---
  F |   | B
     -G-
  E |   | C
     ---
      D

"""


class TM1637(object):
    I2C_COMM1 = 0b01000000  # 写显存数据命令
    I2C_COMM2 = 0b11000000  # 设置地址命令
    I2C_COMM3 = 0b10000000  # 控制显示命令
    DELAY = 10/1000/1000  # 10us

    def __init__(self, clk, dio):
        self.clk = clk  # 时钟信号引脚
        self.dio = dio  # 数据输入输出引脚
        self.brightness = 0x0f  # 明亮度
        # 引脚初始化
        self.clk_pin = OutputDevice(clk)
        self.dio_pin = OutputDevice(dio)
        self.clk_pin.value = 0
        self.dio_pin.value = 0
        self.bit_delay()

    @classmethod
    def bit_delay(cls):
        sleep(cls.DELAY)

    def set_segments(self, segments, pos=0):
        # 写入命令1：写显存数据
        self.start()
        self.write_byte(self.I2C_COMM1)
        self.stop()

        # 写入命令2：设置地址，第一个数字的地址
        self.start()
        self.write_byte(self.I2C_COMM2 | pos)

        for seg in segments:
            self.write_byte(seg)
        self.stop()

        # 写入命令3：显示控制，明暗度
        self.start()
        self.write_byte(self.I2C_COMM3 | self.brightness)
        self.stop()

    def start(self):
        """ 开始条件：待确认 """
        self.dio_pin.value = 0
        self.bit_delay()
        self.clk_pin.value = 0
        self.bit_delay()

    def stop(self):
        """ 结束条件：clk为高电位，dio由低电位变为高电位 """
        self.dio_pin.value = 0
        self.bit_delay()
        self.clk_pin.value = 1
        self.bit_delay()
        self.dio_pin.value = 1
        self.bit_delay()

    def write_byte(self, b):
        # 8 Data Bits
        for i in range(8):
            # CLK low
            self.clk_pin.value = 1
            self.bit_delay()
            self.dio_pin.value = (b >> i) & 1
            self.bit_delay()

            self.clk_pin.value = 0
            self.bit_delay()

        self.clk_pin.value = 0
        self.bit_delay()
        self.clk_pin.value = 1
        self.bit_delay()
        self.clk_pin.value = 0
        self.bit_delay()

    @classmethod
    def encode_digit(cls, digit):
        """Convert a character 0-9, a-f to a segment."""
        return _SEGMENTS[digit & 0x0f]

    @classmethod
    def encode_char(cls, char):
        """Convert a character 0-9, a-z, space, dash or star to a segment."""
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36] # space
        if o == 42:
            return _SEGMENTS[38] # star/degrees
        if o == 45:
            return _SEGMENTS[37] # dash
        if o >= 65 and o <= 90:
            return _SEGMENTS[o-55] # uppercase A-Z
        if o >= 97 and o <= 122:
            return _SEGMENTS[o-87] # lowercase a-z
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48] # 0-9
        raise ValueError("Character out of range: {:d} '{:s}'".format(o, chr(o)))

    @classmethod
    def encode_string(cls, string):
        """Convert an up to 4 character length string containing 0-9, a-z,
        space, dash, star to an array of segments, matching the length of the
        source string."""
        segments = bytearray(len(string))
        for i in range(len(string)):
            segments[i] = cls.encode_char(string[i])
        return segments

    def number(self, num):
        """ 显示-999~9999的数字 """
        num = max(-999, min(num, 9999))
        string = '{0:>4d}'.format(num)
        self.set_segments(self.encode_string(string))

    def show(self, string, colon=False):
        """ 显示4位的字符串(0~9,a-z,A-Z,space,dash,star) """
        segments = self.encode_string(string)
        if len(segments) > 1 and colon:
            segments[1] |= 128
        self.set_segments(segments[:4])

    def scroll(self, string, delay=0.25):
        """ 滚动显示 """
        segments = string if isinstance(string, list) else self.encode_string(string)
        data = [0] * 8
        data[4:0] = list(segments)
        for i in range(len(segments) + 5):
            self.set_segments(data[0 + i:4 + i])
            sleep(delay)

    def clock(self):
        """ 显示时间 """
        t = localtime()
        sleep(1 - time() % 1)
        d0 = self.encode_char(t.tm_hour // 10)
        d1 = self.encode_char(t.tm_hour % 10)
        d2 = self.encode_char(t.tm_min // 10)
        d3 = self.encode_char(t.tm_min % 10)
        self.show(f'{d0}{d1}{d2}{d3}', colon=True)
        sleep(0.5)
        self.show(f'{d0}{d1}{d2}{d3}', colon=False)

    def temperature(self, num):
        if num < -9:
            self.show('lo')  # low
        elif num > 99:
            self.show('hi')  # high
        else:
            string = '{0: >2d}'.format(num)
            self.set_segments(self.encode_string(string))
        self.set_segments([_SEGMENTS[38], _SEGMENTS[12]], 2)  # degrees C


if __name__ == "__main__":
    tm = TM1637(CLK, DIO)
    tm.number(100)
    tm.number(1000)
    tm.show('1234')
    tm.show('abcd')
    tm.show('abc')
    tm.scroll('micro-blue-room')
    tm.temperature(24)  # show temperature '24*C'

    while True:
        tm.clock()
