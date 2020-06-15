import os
import numpy as np
np.random.seed(1337)
import json
import argparse
import cPickle as pickle

from keras.models import Sequential, model_from_json
from keras.optimizers import Adam

from modeldump import ModelDump

def parse():
    """
    Parse arguments
    """
    
    parser = argparse.ArgumentParser(description='This is a simple script to dump Keras model into simple format suitable for porting into pure C++ model')

    parser.add_argument('-t', '--training_reruns', help="Number of training reruns", type=int, required=True)
    parser.add_argument('-p', '--pairs', help="Number of pairs of particles", type=int, required=True)
    parser.add_argument('-b', '--model_base_dir', help="Model base directory", type=str, required=True)
    parser.add_argument('-m', '--model_dir', help="Model directory", type=str,required=True)
    parser.add_argument('-o', '--out_dir', help="Output directory in which others will be created", type=str,required=True)
    parser.add_argument('-v', '--verbose', help="Verbose", type=bool, required=False)
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse()

    for i in range(args.training_reruns):
        print ('Working on training run {}'.format(i))
        mod_dir = args.model_base_dir + args.model_dir + '_{}/'.format(i)
        output = args.out_dir + '_{}/'.format(i)
        if not os.path.exists(output):
            os.mkdir(output)

        for pair in range(args.pairs):
            pair_dir = mod_dir + "pair_0.02_{}/".format(pair)
            pair_out_dir = output + "pair_0.02_{}/".format(pair)
            if not os.path.exists(pair_out_dir):
                os.mkdir(pair_out_dir)

            print ('Reading data from {}'.format(pair_dir))
            print ('Saving data to {}'.format(pair_out_dir))

            model_dump = ModelDump(pair_dir + '/model_arch.json', pair_dir + '/model_weights.h5', pair_out_dir + '/model.nnet', init=True)
        
            print ('################# Converting metadata #################')
            pickle_out = open(pair_dir+ "/dataset_metadata.pickle","rb")
            metadata = pickle.load(pickle_out)
            pickle_out.close()

            with open(pair_out_dir + '/dataset_metadata.dat', 'w') as fin:
                for idx, i in enumerate(metadata['x_mean']):
                    if idx == len(metadata['x_mean'])-1:
                        fin.write(str(i) + "\n")
                    else:
                        fin.write(str(i) + " ")
                for idx, i in enumerate(metadata['x_std']):
                    if idx == len(metadata['x_std'])-1:
                        fin.write(str(i) + "\n")
                    else:
                        fin.write(str(i) + " ")
                fin.write(str(metadata['y_mean']) + "\n")
                fin.write(str(metadata['y_std']) + "\n")

        cut_dir = mod_dir + "cut_0.02/"
        cut_out_dir = output + "cut_0.02/"
        if not os.path.exists(cut_out_dir):
                os.mkdir(cut_out_dir)

        print ('Reading data from {}'.format(cut_dir))
        print ('Saving data to {}'.format(cut_out_dir))

        model_dump = ModelDump(cut_dir + '/model_arch.json', cut_dir + '/model_weights.h5', cut_out_dir + '/model.nnet', init=True)
        
        print ('################# Converting metadata #################')
        pickle_out = open(cut_dir+ "/dataset_metadata.pickle","rb")
        metadata = pickle.load(pickle_out)
        pickle_out.close()

        with open(cut_out_dir + '/dataset_metadata.dat', 'w') as fin:
            for idx, i in enumerate(metadata['x_mean']):
                if idx == len(metadata['x_mean'])-1:
                    fin.write(str(i) + "\n")
                else:
                    fin.write(str(i) + " ")
            for idx, i in enumerate(metadata['x_std']):
                if idx == len(metadata['x_std'])-1:
                    fin.write(str(i) + "\n")
                else:
                    fin.write(str(i) + " ")
            fin.write(str(metadata['y_mean']) + "\n")
            fin.write(str(metadata['y_std']) + "\n")

