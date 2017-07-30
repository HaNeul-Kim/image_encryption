#!/usr/bin/env python
#-*-coding:utf-8-*-

import numpy as np
import random
import copy

from swap import Swap

class GATools:
    def __init__(self):
        self.swap = Swap()

# preprocessing: image recombination
    def image_recombination(self, img):
        img_nb = np.roll(img, 1, axis = 1)
        r = np.bitwise_xor(img, img_nb)
        return r

    def cross(self, gene1, gene2, mask):
        child1 = np.copy(gene1)
        child2 = np.copy(gene2)
        for m2 in range(0, mask.shape[0]):
            tmp = np.copy(child1)
            if mask[m2] == 1:
                child1[m2] = np.copy(child2[m2])
                child2[m2] = np.copy(tmp[m2])
        return child1, child2

    def mutation(self, gene_, subkey, i):
        swap_pos1 = self.swap.swap_position(subkey[0], i)
        swap_pos2 = self.swap.swap_position(subkey[1], i)
        gene = gene_
        gene = self.swap.binary_swap(gene, swap_pos1[0], swap_pos1[1])
        gene = self.swap.binary_swap(gene, swap_pos2[0], swap_pos2[1])
        return gene
        
        
    def reverse_mutation(self, gene_, subkey, i):
        swap_pos1 = self.swap.swap_position(subkey[0], i)
        swap_pos2 = self.swap.swap_position(subkey[1], i)
        gene = gene_
        gene = self.swap.binary_swap(gene, swap_pos2[0], swap_pos2[1])
        gene = self.swap.binary_swap(gene, swap_pos1[0], swap_pos1[1])
        return gene
