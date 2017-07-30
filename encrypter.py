#!/usr/bin/env python
#-*-coding:utf-8-*-

import numpy as np
import random
import copy

from image_utils import ImageUtils
from key_utils import KeyUtils
from ga_tools import GATools

class Encrypter:

# コンストラクタ
    def __init__(self):
        self.iu = ImageUtils()
        self.ku = KeyUtils()
        self.ga = GATools()
        
# 初期遺伝子を作る:recombinationしたグレースケールイメージを入れる((128*N) x (128*N)のサイズ)
    #seeds:暗号化キーから生成された4つのrandom seedの配列
    #m, s: 論文にあるMとSのこと
    def initiate(self, img_, key, m_, s_):
        seeds = self.ku.generate_random_seeds(key)
        img_ = np.unpackbits(img_, axis = 1)
        img_ = np.transpose(img_)
        shape = img_.shape
        m = m_
        s = s_
        for i in range(0,4):
            random.seed(seeds[i])
            n = m * s
            random_list = range(n)
            random_list = random.sample(random_list, len(random_list))
            copied_img = np.copy(img_)
            w = shape[0]
            h = shape[1]
            q = w // n
            r = h // n

# swap columns　in each block
            for j in range(0, n):
                for k in range(0, q):
                    if n * k + j < w and n * k + random_list[j] < w:
                        copied_img[n * k + j] = np.copy(img_[n * k + random_list[j]])
            img_ = np.copy(copied_img)

            for j in range(0, q):
                for k in range(0, r):
                    copied_img[n*j:n*(j + 1), n*k:n*(k + 1)] = np.copy(np.transpose(img_[n*j:n*(j + 1), n*k:n*(k + 1)]))
            m = m + 1
            img_ = np.copy(copied_img)
        img_ = np.transpose(img_)
        img_ = np.packbits(img_, axis = 1)
        return img_

# GAの実行(暗号化)        
    def execute_ga(self, key, img, n_):
        keys = self.ku.generate_binary_key(key)
        key_ = key.split()
        imgH = img.shape[0]
        imgW = img.shape[1]
        n = n_
        for i in range(0, 4):
            q = imgH // n
            r = imgW // n
            for i1 in range(0, q):
                for i2 in range(0, r):
                    cell = np.copy(img[n*i2 : n * (i2 + 1), n * i1: n*(i1 + 1)])
                    cell = np.unpackbits(cell, axis = 1)
                    cell = np.reshape(cell, (n, n, 8))
                    arranged_cell = self.iu.arrange_cell_in_line(cell, n)
# arranged_cellの中で、マスクを使ってcrossを行う
                    for m_ in range(0, keys.shape[0]):
                        for m in range(0, arranged_cell.shape[0] // 2):
# cross      
                            arranged_cell[m * 2,], arranged_cell[m * 2 + 1,] = self.ga.cross(arranged_cell[m * 2,], arranged_cell[m * 2 + 1,], keys[m_,])
# mutation   
                            arranged_cell[m * 2,] = self.ga.mutation(arranged_cell[m * 2,], key_[m_], i)
                            arranged_cell[m * 2 + 1,] = self.ga.mutation(arranged_cell[m * 2 + 1,], key_[m_], i)

# zigzagの順番を元に戻す
                    cell = self.iu.arrange_cell_in_square(arranged_cell, n)
                    cell = np.reshape(cell, (n, n * 8))
                    cell = np.packbits(cell, axis = 1)
                    img[n*i2 : n * (i2 + 1), n * i1: n*(i1 + 1)] = np.copy(cell)

# mutationを行う
            print(i + 1, " generation finished")
            n = n + 8
        return img
