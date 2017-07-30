#!/usr/bin/env python
#-*-coding:utf-8-*-

import numpy as np

class KeyUtils:

# コンストラクタ
    def __init__(self):
        return

# keyを2文字ずつ切る
    def split_key_in_int(self, string_key):
        key = string_key.split()
        key_int = []
        for x in key:
            x = '0x'+x
            x = int(x, 16)
            key_int.append(x)
        return key_int

# keyから4つのrandom seedを生成する
    def generate_random_seeds(self, string_key):
        key_arr = self.split_key_in_int(string_key)
        seeds = []
        for i in range(1,5):
            seed = 0
            for j in range(0, 4):
                seed += key_arr[4 * i - 3 + j - 1]
            seeds.append(seed)
        return seeds
        
    def generate_binary_key(self, string_key):
        keys_int = self.split_key_in_int(string_key)
        keys = np.array(keys_int, dtype = np.uint8)
        keys = np.unpackbits(keys, axis = 0)
        keys = np.reshape(keys, (16, 8))
        return keys
