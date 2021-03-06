import argparse
import sys
sys.path.append('./../models/')
sys.path.append('./../utils/')
sys.path.append('./../phase/')
import os

import numpy as np
import matplotlib

import matplotlib.pyplot as plt
from matplotlib import cm
import random
from matplotlib import rc
import time
import pickle
import multiprocessing
from multiprocessing import Pool

from njet_run_functions import *
from rambo_while import *
from utils import *
from model import Model

from keras.models import load_model

def generate_LO_njet(momenta, test_data):
    
    NJ_vals = []
    for i in test_data:
        vals = run_cc_test(momenta, i[1], i[2])
        NJ_vals.append(vals)
    
    # select the first test of the runs
    NJ_vals = NJ_vals[0]
    
    NJ_treevals = []
    for i in NJ_vals:
        NJ_treevals.append(i[0])
        
    return NJ_treevals 

def generate_NLO_njet(momenta, test_data, VIEW = 'NJ', k = True):
    '''
    Generates NLO virtual correction and k-factors (1-loop/born) from NJet
    :param momenta: list of 4-momenta
    :param test_data: test_data generated by run_njet(_generic)() in n3jet/utils/run_njet_functions/
    :param VIEW: 'NJ' = (1-loop*born)/born = 1-loop, 'MC' = 1-loop*born
    :param k: True returns k-factor (i.e. if VIEW = 'NJ' then returns 1-loop/born, but if 'MC' returns 1-loop)
    '''
    
    NJ_loop_vals = []
    for i in test_data:
        vals = run_generic_test(momenta, i[1], i[2], VIEW = VIEW)
        NJ_loop_vals.append(vals)
    
    # select the first test of the runs
    NJ_loop_vals = NJ_loop_vals[0][0]
        
    A0 = []
    A1_2 = []
    A1_2_error = []
    A1_1 = []
    A1_1_error = []
    A1_0 = []
    A1_0_error = []
    for i in range(len(NJ_loop_vals)):
        A0.append(NJ_loop_vals[i][0][1])
        A1_2.append(NJ_loop_vals[i][1][1])
        A1_2_error.append(NJ_loop_vals[i][1][2])
        A1_1.append(NJ_loop_vals[i][2][1])
        A1_1_error.append(NJ_loop_vals[i][2][2])
        A1_0.append(NJ_loop_vals[i][3][1])
        A1_0_error.append(NJ_loop_vals[i][3][2])
        
    NJ_treevals = np.array(A0)
    A1_0 = np.array(A1_0)

    if k == True:
        k_factor = A1_0/NJ_treevals
        return k_factor, NJ_loop_vals
    else:
        return A1_0, NJ_loop_vals
    

def generate_NLO_njet_multiprocess_1(momenta):
    test_data, ptype, order = run_njet(1)
    
    NJ_loop_vals = []
    for i in test_data:
        vals = run_generic_test([momenta], i[1], i[2])
        NJ_loop_vals.append(vals)
    
    # select the first test of the runs
    NJ_loop_vals = NJ_loop_vals[0][0]
        
    A0 = []
    A1_2 = []
    A1_2_error = []
    A1_1 = []
    A1_1_error = []
    A1_0 = []
    A1_0_error = []
    for i in range(len(NJ_loop_vals)):
        A0.append(NJ_loop_vals[i][0][1])
        A1_2.append(NJ_loop_vals[i][1][1])
        A1_2_error.append(NJ_loop_vals[i][1][2])
        A1_1.append(NJ_loop_vals[i][2][1])
        A1_1_error.append(NJ_loop_vals[i][2][2])
        A1_0.append(NJ_loop_vals[i][3][1])
        A1_0_error.append(NJ_loop_vals[i][3][2])
        
    NJ_treevals = np.array(A0)
    A1_0 = np.array(A1_0)
    k_factor = A1_0/NJ_treevals
    
    return k_factor, NJ_loop_vals

def generate_NLO_njet_multiprocess_2(momenta):
    test_data, ptype, order = run_njet(2)
    
    NJ_loop_vals = []
    for i in test_data:
        vals = run_generic_test([momenta], i[1], i[2])
        NJ_loop_vals.append(vals)
    
    # select the first test of the runs
    NJ_loop_vals = NJ_loop_vals[0][0]
        
    A0 = []
    A1_2 = []
    A1_2_error = []
    A1_1 = []
    A1_1_error = []
    A1_0 = []
    A1_0_error = []
    for i in range(len(NJ_loop_vals)):
        A0.append(NJ_loop_vals[i][0][1])
        A1_2.append(NJ_loop_vals[i][1][1])
        A1_2_error.append(NJ_loop_vals[i][1][2])
        A1_1.append(NJ_loop_vals[i][2][1])
        A1_1_error.append(NJ_loop_vals[i][2][2])
        A1_0.append(NJ_loop_vals[i][3][1])
        A1_0_error.append(NJ_loop_vals[i][3][2])
        
    NJ_treevals = np.array(A0)
    A1_0 = np.array(A1_0)
    k_factor = A1_0/NJ_treevals
    
    return k_factor, NJ_loop_vals

def generate_NLO_njet_multiprocess_3(momenta):
    test_data, ptype, order = run_njet(3)
    
    NJ_loop_vals = []
    for i in test_data:
        vals = run_generic_test([momenta], i[1], i[2])
        NJ_loop_vals.append(vals)
    
    # select the first test of the runs
    NJ_loop_vals = NJ_loop_vals[0][0]
        
    A0 = []
    A1_2 = []
    A1_2_error = []
    A1_1 = []
    A1_1_error = []
    A1_0 = []
    A1_0_error = []
    for i in range(len(NJ_loop_vals)):
        A0.append(NJ_loop_vals[i][0][1])
        A1_2.append(NJ_loop_vals[i][1][1])
        A1_2_error.append(NJ_loop_vals[i][1][2])
        A1_1.append(NJ_loop_vals[i][2][1])
        A1_1_error.append(NJ_loop_vals[i][2][2])
        A1_0.append(NJ_loop_vals[i][3][1])
        A1_0_error.append(NJ_loop_vals[i][3][2])
        
    NJ_treevals = np.array(A0)
    A1_0 = np.array(A1_0)
    k_factor = A1_0/NJ_treevals
    
    return k_factor, NJ_loop_vals
    
def multiprocess_generate_NLO_njet(momenta, n_gluon, cores):
    p = Pool(processes=cores)
    
    if n_gluon == 1:
        out = p.map(generate_NLO_njet_multiprocess_1, momenta, chunksize=len(momenta)//cores)
    if n_gluon == 2:
        out = p.map(generate_NLO_njet_multiprocess_2, momenta, chunksize=len(momenta)//cores)
    if n_gluon == 3:
        out = p.map(generate_NLO_njet_multiprocess_3, momenta, chunksize=len(momenta)//cores)
    
    
    out = np.array(out)
    
    
    k_factor, NJ_loop_vals = out[:,0], out[:,1]
    k_factor = k_factor.reshape(-1)
    NJ_loop_vals = NJ_loop_vals.reshape(-1)
    
    return k_factor, NJ_loop_vals
