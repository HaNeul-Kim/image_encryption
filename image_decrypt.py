#!/usr/bin/env python
#-*-coding:utf-8-*-

import cv2
import numpy as np
import random
import copy

loaded_img = cv2.imread('./encrypted_00137606_4.png', cv2.IMREAD_GRAYSCALE)
img = np.zeros(loaded_img.shape, np.uint8)
img[:,:]=loaded_img
original_shape = loaded_img.shape
imgH = original_shape[0]
imgW = original_shape[1]
KEY = "e5 da 75 0b 4c 1f 78 d3 28 ea 25 e6 b1 5c f9 43"

#split given key string
def split_key_in_int(string_key):
    key = string_key.split()
    key_int = []
    for x in key:
        x = '0x'+x
        x = int(x, 16)
        key_int.append(x)
    return key_int

def generate_random_seeds(key_arr):
    seeds = []
    for i in range(1,5):
        seed = 0
        for j in range(0, 4):
            seed += key_arr[4 * i - 3 + j - 1]
        seeds.append(seed)
    return seeds

#n x nで分割した2進イメージをzigzagの順で長さn^2の列にする
def arrange_cell_in_line(cell, n):
    arranged = np.copy(cell)
    arranged = np.reshape(arranged, (n * n, 8))
    count = 0
    l1 = 0
    l2 = 0
    #zigzagの順番をつくる
    while l1 + l2 < n + n - 1:
        arranged[count,] = cell[l1, l2,]
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

#n^2のimgをn x nイメージに直す(zigzagのやつを正方形に戻す)
def arrange_cell_in_square(bin_img, n):
    img_ = np.copy(bin_img)
    img_ = np.reshape(img_, (n, n, 8))
    c= 0
    k1 = 0
    k2 = 0
    while k1 + k2 < n + n - 1:
        img_[k1, k2,] = bin_img[c,]
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

def binary_swap(array, i, j):
    array[i], array[j] = array[j], array[i]
    return array

def swap_position(char, g):
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

def cross(gene1, gene2, mask):
    child1 = gene1
    child2 = gene2
    for m2 in range(0, mask.shape[0]):
        tmp = np.copy(child1)
        if mask[m2] == 1:
            child1[m2] = np.copy(child2[m2])
            child2[m2] = np.copy(tmp[m2])
    return child1, child2

def mutation(gene_, subkey, i):
    swap_pos1 = swap_position(subkey[0], i)
    swap_pos2 = swap_position(subkey[1], i)
    gene = gene_
    gene = binary_swap(gene, swap_pos2[0], swap_pos2[1])
    gene = binary_swap(gene, swap_pos1[0], swap_pos1[1])
    return gene

def reverse_initiate(img_, seeds, m_, s_):
    img_ = np.unpackbits(img_, axis = 1)
    img_ = np.transpose(img_)
    shape = img_.shape
    m = m_
    s = s_
    for i in range(0,4):
        random.seed(seeds[3 - i])
        n = m * s
        random_list = range(n)
        random_list = random.sample(random_list, len(random_list))
        copied_img = np.copy(img_)

        w = shape[0]
        h = shape[1]
        q = w // n
        r = h // n
#swap columns　in each block
        for j in range(0, q):
            for k in range(0, r):
                copied_img[n*j:n*(j + 1), n*k:n*(k + 1)] = np.copy(np.transpose(img_[n*j:n*(j + 1), n*k:n*(k + 1)]))

        img_ = np.copy(copied_img)

        for j in range(0, n):
            for k in range(0, q):
                if n * k + j < w and n * k + random_list[j] < w:
                    copied_img[n * k + random_list[j]] = np.copy(img_[n * k + j])

        m = m - 1
        img_ = np.copy(copied_img)
    img_ = np.transpose(img_)
    img_ = np.packbits(img_, axis = 1)
    return img_

#recombi = np.transpose(recombi)
#recombi = np.packbits(recombi, axis = 1)

#逆cross, 逆mutation:確認済み
def execute_reverse_ga(keys_int, img, n_):
    keys = np.array(key_int, dtype = np.uint8)
    keys = np.unpackbits(keys, axis = 0)
    keys = np.reshape(keys, (16, 8))
    n = n_
    for i in range(0, 4):
        q = imgH // n
        r = imgW // n
        for i1 in range(0, q):
            for i2 in range(0, r):
                cell = np.copy(img[n*i2 : n * (i2 + 1), n * i1: n*(i1 + 1)])
                cell = np.unpackbits(cell, axis = 1)
                cell = np.reshape(cell, (n, n, 8))
                arranged_cell = arrange_cell_in_line(cell, n)
#arranged_cellの中で、マスクを使ってcrossを行う
                for m_ in range(0, keys.shape[0]):
                    for m in range(0, arranged_cell.shape[0] // 2):
#mutation   
                        arranged_cell[m * 2 + 1,] = mutation(arranged_cell[m * 2 + 1,], key[keys.shape[0] - 1 - m_], 3 - i)
                        arranged_cell[m * 2,] = mutation(arranged_cell[m * 2,], key[keys.shape[0] - 1 - m_], 3 - i)
#cross      
                        arranged_cell[m * 2,], arranged_cell[m * 2 + 1,] = cross(arranged_cell[m * 2,], arranged_cell[m * 2 + 1,], keys[keys.shape[0] - 1 - m_,])

#zigzagの順番を元に戻す
                cell = arrange_cell_in_square(arranged_cell, n)
                cell = np.reshape(cell, (n, n * 8))
                cell = np.packbits(cell, axis = 1)
                img[n*i2 : n * (i2 + 1), n * i1: n*(i1 + 1)] = np.copy(cell)

            #mutationを行う
        print(i + 1, " generation finished")
        n = n - 8
    return img

if __name__=='__main__':
#random seed
    key = KEY.split()
    key_int = split_key_in_int(KEY)
    seeds = generate_random_seeds(key_int)
    img = execute_reverse_ga(key_int, img, 40)
    img = reverse_initiate(img, seeds, 6, 8)
    cv2.imshow('image', img)
    #cv2.imshow('image', copied_img)
    k = cv2.waitKey(0)
    if k == ord('q'):
        cv2.destroyAllWindows()
    elif k == ord('s'):
        cv2.imwrite('decrypted_correct.png', img)
        cv2.destroyAllWindows()
