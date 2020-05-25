import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import train_test_split
from keras import metrics
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from sklearn.preprocessing import normalize, MinMaxScaler
import keras.backend as K
import matplotlib.pyplot as plt
import time



class Model:
    
    def __init__(self, input_size, momenta, labels, all_jets = False, all_legs = False):
        '''
        :param input_size: the flattened input dim for the model
            e.g. 3 jets has input_dim of (3-1)*4=8
        :param momenta: input momenta in NJET format (i.e. [num points, num jets, 4])
        :param labels: labels
        '''
        self.input_size = input_size
        self.momenta = momenta
        self.labels = labels
        self.all_jets = all_jets
        self.all_legs = all_legs
    
    def standardise(self, data):
        '''standardise data
        :param data: an array over which to standardise (this array may be a variable column) 
        '''
        array = np.array(data)
        mean = np.mean(array)
        std = np.std(array)
        standard = (array-mean)/(std)
        return mean, std, standard
        
    def root_mean_squared_error(self, y_true, y_pred):
        'custom loss functoin RMSE'
        return K.sqrt(K.mean(K.square(y_pred - y_true)))
    
    def process_training_data(self, random_state=42, **kwargs):
        '''
        trainind data must be standardised and split for training and validation
        **kwargs can take on:
        :param moms: the PS points in format [no_PS_points, points, 4]
        :param labs: ground truth labels of squared matrix elements
        '''
        moms = kwargs.get('moms', self.momenta)
        labs = kwargs.get('labs', self.labels)

        if self.all_legs == True:
            momenta = np.array(moms)
        elif self.all_jets == True:
            momenta = np.array(moms)[:,2:,:] #include all outgoing jets
        else:
            momenta = np.array(moms)[:,3:,:] #pick out all but one jet
            
        labels = np.array(labs)
        
        x_standard = momenta.reshape(-1,4).copy() #shape for standardising each momentum element
        self.x_mean = np.zeros(4)
        self.x_std = np.zeros(4)
        
        self.x_mean[0],self.x_std[0],x_standard[:,0] = self.standardise(momenta.reshape(-1,4)[:,0])
        self.x_mean[1],self.x_std[1],x_standard[:,1] = self.standardise(momenta.reshape(-1,4)[:,1])
        self.x_mean[2],self.x_std[2],x_standard[:,2] = self.standardise(momenta.reshape(-1,4)[:,2])
        self.x_mean[3],self.x_std[3],x_standard[:,3] = self.standardise(momenta.reshape(-1,4)[:,3])
        
        x_standard = x_standard.reshape(-1,self.input_size) #shape for passing into network
        
        self.y_mean, self.y_std, y_standard = self.standardise(labels)
        
        X_train, X_test, y_train, y_test = train_test_split(x_standard, y_standard, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test, self.x_mean, self.x_std, self.y_mean, self.y_std   
    
    def baseline_model(self, layers, lr=0.001):
        'define and compile model'
        # create model
        # at some point can use new Keras tuning feature for optimising this model
        model = Sequential()
        model.add(Dense(layers[0], input_dim=(self.input_size), activation='tanh'))
        model.add(Dense(layers[1], activation='tanh'))
        model.add(Dense(layers[2], activation='tanh'))
        model.add(Dense(1))
        # Compile model
        model.compile(optimizer = Adam(lr=lr, beta_1=0.9, beta_2=0.999, amsgrad=False), loss = 'mean_squared_error')
        
        return model
    
    def fit(self, layers=[32,16,8], epochs=10000, lr=0.001, **kwargs):
        '''
        fit model
        :param layers: an array of lengeth 3 providing the number of hidden nodes in the three layers
        '''
        random_state = kwargs.get('random_state', 42)
        
        if len(layers) != 3:
            raise Exception('the number of layers to be defined is 3, you have defined len(layers) layers')
    
        X_train, X_test, y_train, y_test,_,_,_,_ = self.process_training_data(random_state = random_state)
        print (X_train.shape)
        
        self.model = self.baseline_model(layers=layers, lr=lr)
        ES = EarlyStopping(monitor='val_loss', min_delta=0, patience=100, verbose=0, restore_best_weights=True)
        
        self.model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test),callbacks=[ES], batch_size=512)
        
        return self.model, self.x_mean, self.x_std, self.y_mean, self.y_std
        
    def standardise_test(self, data, mean, std):
        array = np.array(data)
        standard = (array-mean)/(std)
        return standard
        
    def process_testing_data(self, moms, **kwargs):
        '''
        **kwargs can take on:
        :param x_mean, x_std, y_mean, y_std: mean and std of x and y values if not (properly) provided by class e.g. if using a pretrained model with known mean and std
        '''
            
        labs = kwargs.get('labs', None)
        if self.all_legs == True:
            momenta = np.array(moms)
        elif self.all_jets == True:
            momenta = np.array(moms)[:,2:,:] #include all outgoing jets
        else:
            momenta = np.array(moms)[:,3:,:] #pick out all but one jet

        y_mean = kwargs.get('y_mean', self.y_mean)
        
        print_y = kwargs.get('print_y', True)
        if print_y == True:
            print ('Using y_mean of {} instead of {}'.format(y_mean, self.y_mean))
        y_std = kwargs.get('y_std', self.y_std)
        x_mean = kwargs.get('x_mean', self.x_mean)
        x_std = kwargs.get('x_std', self.x_std)
        
        if labs is not None:
            labels = np.array(labs)
        
        x_standard = momenta.reshape(-1,4).copy() #shape for standardising each momentum element
        
        x_standard[:,0] = self.standardise_test(momenta.reshape(-1,4)[:,0],x_mean[0],x_std[0])
        x_standard[:,1] = self.standardise_test(momenta.reshape(-1,4)[:,1],x_mean[1],x_std[1])
        x_standard[:,2] = self.standardise_test(momenta.reshape(-1,4)[:,2],x_mean[2],x_std[2])
        x_standard[:,3] = self.standardise_test(momenta.reshape(-1,4)[:,3],x_mean[3],x_std[3])
        
        x_standard = x_standard.reshape(-1,self.input_size) #shape for passing into network
        
        if labs is not None:
            y_standard = self.standardise_test(labels,y_mean,y_std)
            return x_standard, y_standard
        
        else:
            return x_standard
    
    def destandardise(self, data, mean, std):
        'destandardise array for inference and comparison'
        array = np.array(data)
        return (array*std) + mean
    
    def destandardise_data(self, y_pred, x_pred=None, **kwargs):
        '''
        destandardise any standardised data
        :param y_pred: squared matrix element values
        :param x_pred: optional parameter of momenta values to be destandardised
        **kwargs can take on:
        :param x_mean, x_std, y_mean, y_std: mean and std of x and y values if not (properly) provided by class e.g. if using a pretrained model with known mean and std
        
        note: when initialising the class with the data used to train a pretrained model, the standardised data will be the same as used in training if the dataset is loaded and passed correctly as the mean and std is independent of the data splitting
        '''
        
        y_mean = kwargs.get('y_mean', self.y_mean)
        y_std = kwargs.get('y_std', self.y_std)
        x_mean = kwargs.get('x_mean', self.x_mean)
        x_std = kwargs.get('x_std', self.x_std)
        
        
        y_destandard = self.destandardise(y_pred,y_mean,y_std)
        
        if x_pred is not None:
            x_pred = x_pred.reshape(-1,4)
            x_destandard = x_pred.copy()
            
            x_destandard[:,0] = self.destandardise(x_pred[:,0],x_mean[0],x_std[0])
            x_destandard[:,1] = self.destandardise(x_pred[:,1],x_mean[1],x_std[1])
            x_destandard[:,2] = self.destandardise(x_pred[:,2],x_mean[2],x_std[2])
            x_destandard[:,3] = self.destandardise(x_pred[:,3],x_mean[3],x_std[3])
            
            x_destandard = x_destandard.reshape(-1,int((self.input_size)/4),4)
            
            return x_destandard, y_destandard
        
        else:
            return y_destandard
        
        
        
        
        
        
       
    
