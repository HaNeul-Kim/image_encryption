#!/usr/bin/env python
#-*-coding:utf-8-*-

import numpy as np

class ImageUtils:

# コンストラクタ
    def __init__(self):
        return

# n x nで分割した2進イメージをzigzagの順で長さn^2の列にする
    def arrange_cell_in_line(self, cell, n):
        arranged = np.copy(cell)
        arranged = np.reshape(arranged, (n * n, 8))
        count = 0
        l1 = 0
        l2 = 0
        
# zigzagの順番をつくる
        while l1 + l2 < n + n - 1:
            arranged[count,] = np.copy(cell[l1, l2,])
            if (l1 == 0 or l1 == n - 1) and l2 % 2 == 0:
                l2 += 1
            elif (l2 == 0 or l2 == n - 1) and l1 % 2 == 1:
                l1 += 1
            elif (l1 + l2) % 2 == 1:
                l1 += 1
                l2 -= 1
            elif (l1 + l2) % 2 == 0:
                l1 -= 1
                l2 += 1
            count += 1
        return arranged

# n^2のimgをn x nイメージに直す(zigzagのやつを正方形に戻す)
    def arrange_cell_in_square(self, bin_img, n):
        img_ = np.copy(bin_img)
        img_ = np.reshape(img_, (n, n, 8))
        c= 0
        k1 = 0
        k2 = 0
        while k1 + k2 < n + n - 1:
            img_[k1, k2,] = np.copy(bin_img[c,])
            if (k1 == 0 or k1 == n - 1) and k2 % 2 == 0:
                k2 += 1
            elif (k2 == 0 or k2 == n - 1) and k1 % 2 == 1:
                k1 += 1
            elif (k1 + k2) % 2 == 1:
                k1 += 1
                k2 -= 1
            elif (k1 + k2) % 2 == 0:
                k1 -= 1
                k2 += 1
            c += 1
        return img_

