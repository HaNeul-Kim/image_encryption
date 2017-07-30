#!/usr/bin/env python
#-*-coding:utf-8-*-

class Swap:

# コンストラクタ
    def __init__(self):
        return

# binary nparrayの、指定した箇所を互換する
    def binary_swap(self, array, i, j):
        array[i], array[j] = array[j], array[i]
        return array

# 鍵のchar(0~9, A~E)と世代数から突然変異する位置を求める
# g:世代数
    def swap_position(self, char, g):
        char = int(char, 16)
        pos1 = char % 4
        pos2 = 0
        if char < 4:
            pos2 = g + 4
        elif char < 8:
            pos2 = (g + 1) % 4 + 4
        elif char < 12:
            pos2 = (g + 2) % 4 + 4
        elif char < 16:
            pos2 = (g + 3) % 4 + 4
        return [pos1, pos2]
