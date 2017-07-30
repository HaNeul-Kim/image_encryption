#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
import os
import cv2
import numpy as np
import random
import copy

from ga_tools import GATools
from image_utils import ImageUtils
from key_utils import KeyUtils
from encrypter import Encrypter
from decrypter import Decrypter

# TODO: argparseの追加
"""
argparseの内容
- encrypt/decryptの設定
- keyの設定
- 画像ファイルパスの設定
- 出力パスの設定(defaultを設ける)
"""

if __name__=='__main__':

# 各種設定
    parser = argparse.ArgumentParser(description = 'execute encryption/decryption for a grayscale image')
    parser.add_argument('-e', '--encrypt', help='encryption mode', action="store_true")
    parser.add_argument('-d', '--decrypt', help='decryption mode', action="store_true")
    parser.add_argument('--key', nargs='?', default="e5 da 75 0b 4c 1f 78 d3 28 ea 25 e6 b1 5c f9 43", help='32-digit hexadecimal encryption key')
    parser.add_argument('--input', help='image file path')
    args = parser.parse_args()
    
    ga = GATools()
    k = KeyUtils()
    e = Encrypter()
    d = Decrypter()
    #loaded_img = cv2.imread('./test_image/00137606.jpg', cv2.IMREAD_GRAYSCALE)
    #loaded_img = cv2.imread('./encrypted_00137606_4.png', cv2.IMREAD_GRAYSCALE)
    loaded_img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    img = np.zeros(loaded_img.shape, np.uint8)
    img[:,:]=loaded_img
    original_shape = loaded_img.shape
    imgH = original_shape[0]
    imgW = original_shape[1]
    KEY = args.key

    if args.encrypt:
#image recombination
        img = ga.image_recombination(img)
# initial genes
        img = e.initiate(img, KEY, 3, 8)
#cross and mutation
#16進数のキーを2桁ずつ区切って2進数にし、それぞれをcross/mutation用のキーとして用いる
        img = e.execute_ga(KEY, img, 16)

    elif args.decrypt:
        img = d.execute_reverse_ga(KEY, img, 40)
        img = d.reverse_initiate(img, KEY, 6, 8)

    cv2.imshow('image', img)
    #cv2.imshow('image', copied_img)
    k = cv2.waitKey(0)
    if k == ord('q'):
        cv2.destroyAllWindows()
    elif k == ord('s'):
        file_name = os.path.basename(args.input)
        file_name_noext = os.path.splitext(file_name)[0]
        if args.encrypt:
            e_dir = './encrypted'
            if not os.path.exists(e_dir):
                os.mkdir(e_dir)
            file_str = []
            file_str.append(e_dir)
            file_str.append('/')
            file_str.append(file_name_noext)
            file_str.append('_encrypted.png')
            save_file = ''.join(file_str)
            cv2.imwrite(save_file, img)
        
        elif args.decrypt:
            d_dir = './decrypted'
            if not os.path.exists(d_dir):
                os.mkdir(d_dir)
            file_str = []
            file_str.append(d_dir)
            file_str.append('/')
            file_str.append(file_name_noext)
            file_str.append('_decrypted.png')
            save_file = ''.join(file_str)
            cv2.imwrite(save_file, img)

        cv2.destroyAllWindows()
