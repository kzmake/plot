#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np
from multiprocessing import Pool
from pic import path, profile, file, omake

## CUI
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

ORIGIN = 'lower'
INTERPOLATION = 'spline36'
C_MAX = 0.01
C_MIN = -C_MAX
#C_MAP = omake.generate_cmap(['blue', '#222222', 'red'])
C_MAP = plt.cm.seismic

def parse():
    parser = argparse.ArgumentParser(
            description='fieldデータから2dのカラーコンタをつくるやーつ'
            )
    # 必須
    
    # 任意
    parser.add_argument('-cmax', type=int)
    parser.add_argument('-cmin', type=int)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    
    return parser.parse_args()

def load(file_path):
    print(file_path)
    d = np.loadtxt(file_path, delimiter='\t').reshape(profile.TIMESTEP_MAX+1, 4)[:,1:]
    v = d[:, 0] + d[:, 1] + d[:, 2] 
    return d

def load_r(file_path):
    print(file_path)
    d = np.loadtxt(file_path, delimiter='\t').reshape(profile.TIMESTEP_MAX+1, 2)[:,1:]
    v = d[:, 0] 
    return v

def save(file_path, fig):
    fig.savefig(file_path, bbox_inches='tight', transparent=True)
    #plt.savefig(file_path), bbox_inches='tight', transparent=True)

def main():

    x = np.array([i for i in range(profile.TIMESTEP_MAX + 1)])
    #eles = setup_data(file_in('eles_k'))
    #ions = setup_data(file_in('ions_k'))
    #eles = load_r(file.input('energy_eles_r.txt'))
    #ions = load_r(file.input('energy_ions_r.txt'))
    #f_b = load(file.input('energy_f_b.txt'))
    f_e = load(file.input('energy_f_e.txt'))

    t0 = f_e[1000, 0] + f_e[1000, 1] + f_e[1000, 2]
    #t0 = f_b[0] + f_e[0]
    f_e[:, 0] /= t0
    f_e[:, 1] /= t0
    f_e[:, 2] /= t0

    f_e[:, 1] += f_e[:, 2]
    f_e[:, 0] += f_e[:, 1]


    plt.fill_between(x, 0, f_e[:,2], facecolor='red', label='Ex', alpha=0.3)
    plt.fill_between(x, f_e[:,2], f_e[:,1], facecolor='cyan', label='Ey', alpha=0.3)
    plt.fill_between(x, f_e[:,1], f_e[:,0], facecolor='green', label='Ez', alpha=0.3)

    plt.legend()
    
    plt.savefig(file.output('energy_f_e'), bbox_inches='tight', transparent=True)

    plt.xlim(0, 2000)

    plt.savefig(file.output('energy_f_e_xlim2000'), bbox_inches='tight', transparent=True)

    plt.xlim(0, profile.TIMESTEP_MAX)

    plt.yscale("log")

    plt.savefig(file.output('energy_f_e_log'), bbox_inches='tight', transparent=True)

    plt.clf()
    
if __name__ == '__main__':
    main()
