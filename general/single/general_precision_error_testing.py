import sys
sys.path.append('./../')
sys.path.append('./../../utils/')
sys.path.append('./../../phase/')
sys.path.append('./../../models/')
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import random
from matplotlib import rc
import time
import cPickle as pickle
import multiprocessing
import argparse

import rambo_while
from njet_run_functions import *
from model import Model
from fks_partition import *
from keras.models import load_model
from tqdm import tqdm
from fks_utils import *
#from piecewise_utils import *
from utils import *
from uniform_utils import *
import rambo_piecewise_balance as rpb
from rambo_piecewise_balance import *


parser = argparse.ArgumentParser(description='Once models have been trained using []_init_model_testing.py then this script can be used for testing, given some testing data. Note: this assumes that testing data has already been generated.')

parser.add_argument(
    '--test_mom_file',
    dest='test_mom_file',
    help='destination of testing momenta file',
    type=str,
)

parser.add_argument(
    '--test_nj_file',
    dest='test_nj_file',
    help='destination of testing NJet file',
    type=str,
)

parser.add_argument(
    '--model_base_dir',
    dest='model_base_dir',
    help='model base directory in which folders will be created',
    type=str,
)

parser.add_argument(
    '--model_dir',
    dest='model_dir',
    help='model directory which will be created on top of model_base_dir',
    type=str,
)

parser.add_argument(
    '--training_reruns',
    dest='training_reruns',
    help='number of training reruns for testing, default: 1',
    type=int,
    default=1,
)

parser.add_argument(
    '--all_legs',
    dest='all_legs',
    help='train on data from all legs, not just all jets, default: False',
    type=str,
    default='False',
)

args = parser.parse_args()
test_mom_file = args.test_mom_file
test_nj_file = args.test_nj_file
model_base_dir = args.model_base_dir
model_dir = args.model_dir
training_reruns = args.training_reruns
all_legs = args.all_legs

def file_exists(file_path):
    if os.path.exists(file_path) == True:
        pass
    else:
        raise ValueError('{} does not exist'.format(file_path))

file_exists(test_mom_file)
file_exists(test_nj_file)
file_exists(model_base_dir)
file_exists(model_base_dir + model_dir + '_0')

test_momenta = np.load(test_mom_file, allow_pickle=True)

print ('############### Momenta loaded ###############')

test_nj = np.load(test_nj_file, allow_pickle=True)

print ('############### NJet loaded ###############')

test_momenta = test_momenta.tolist()

print ('Training on {} PS points'.format(len(test_momenta)))

print ('############### Inferring on models ###############')

nlegs = len(test_momenta[0])-2

test_mom_len = len(test_momenta)

if all_legs == 'False':    
    NN = Model(nlegs*4,test_momenta,test_nj,all_jets=True)
else:
    print ('Recutting for all legs')
    test_cut_momenta, test_near_momenta, test_near_nj, test_cut_nj = cut_near_split(test_momenta, test_nj, 0.01, 0.02, all_legs=True)
    test_momenta = np.concatenate((test_cut_momenta, test_near_momenta))
    test_nj = np.concatenate((test_cut_nj, test_near_nj))
    indices = np.arange(len(test_nj))
    np.random.shuffle(indices)
    test_momenta = test_momenta[indices]
    test_nj = test_nj[indices]
    test_momenta = test_momenta.tolist()
    NN = Model((nlegs+2)*4, test_momenta, test_nj, all_legs=True)
_,_,_,_,_,_,_,_ = NN.process_training_data()

models = []
x_means = []
y_means = []
x_stds = []
y_stds = []

for i in range(training_reruns):
    print ('Working on model {}'.format(i))
    model_dir_new = model_base_dir + model_dir + '_{}/'.format(i)
    print ('Looking for directory {}'.format(model_dir_new))
    if os.path.exists(model_dir_new) == False:
        os.mkdir(model_dir_new)
        print ('Directory created')
    else:
        print ('Directory already exists')
    model = load_model(model_dir_new + 'model',custom_objects={'root_mean_squared_error':NN.root_mean_squared_error})
    models.append(model)
    
    pickle_out = open(model_dir_new + "/dataset_metadata.pickle","rb")
    metadata = pickle.load(pickle_out)
    pickle_out.close()
    
    x_means.append(metadata['x_mean'])
    y_means.append(metadata['y_mean'])
    x_stds.append(metadata['x_std'])
    y_stds.append(metadata['y_std'])
    
    
print ('############### All models loaded ###############')

#y_preds = []
for i in range(training_reruns):
    test = i
    print ('Predicting on model {}'.format(i))
    model_dir_new = model_base_dir + model_dir + '_{}/'.format(test)
    if test == 0 and all_legs == 'True':
        print ('Saving out indices for later plotting')
        np.save(model_dir_new + 'indices.npy', indices)
    x_standard = NN.process_testing_data(moms=test_momenta,x_mean=x_means[test],x_std=x_stds[test],y_mean=y_means[test],y_std=y_stds[test])
    pred = models[test].predict(x_standard)
    y_pred = NN.destandardise_data(pred.reshape(-1),x_mean=x_means[test],x_std=x_stds[test],y_mean=y_means[test],y_std=y_stds[test])
    #y_preds.append(y_pred)
    np.save(model_dir_new + '/pred_{}'.format(test_mom_len), y_pred)

print ('############### Finished ###############')
