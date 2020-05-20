import pandas as pd

import keras
keras.backend.clear_session()
from keras.backend import clear_session

from keras.models import load_model
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
global graph
graph = tf.get_default_graph()

class TrajectoryPredictor():
    def __init__(self):
        #清理keras缓存
        keras.backend.clear_session()
        global model
        #self.model
        model=load_model('main/static/model/2retrain240step5flod5.h5')
        #model=load_model('C:\\Users\\season\\diploma_project\\web\\TPW-0.2\\main\\static\\model\\2retrain240step5flod5.h5')
        global nextMinModel
        nextMinModel=load_model('main/static/model/LSTM5fold5time.h5')
        #nextMinModel=load_model("C:\\Users\\season\\diploma_project\\web\\TPW-0.2\\main\\static\\model\\LSTM5fold5time.h5")
        #加载后预测一次，预防报错
        one_X = np.array([[1001.98, 22.3, 71.3, 0.69, -1.15, 0.06, 114.0504099684137, 30.597413575864977, 24.3]])
        self.scaler_max_onestep=[4.19920508e+04,2.80100006e+02,1.76169998e+02,3.23140015e+02,3.23140015e+02,1.64190002e+02,1.22058884e+02,3.27609520e+01,3.55371016e+04]
        self.scaler_min_onestep=[0.,-212.46000671,-314.23999023,-324.45999146,-179.61000061,-164.08999634,106.26604462,24.67316818,0.]
        self.scaler_max=[5251.29980,280.100006,100.000000,323.140015,167.520004,164.190002,120.041611,31.6188507,34596.1016]
        self.scaler_min=[0.0,-234.21000671,-327.67999268,-324.45999146,-171.88000488,-82.26999664,108.49158478,24.95638084,8.30000019]
        one_X = self.transfromX(one_X)
        test_y=model.predict(one_X)

    def FNoramlize(self,alist,low,high):
        delta = float(high - low)
        if delta != 0:
            for i in range(0, len(alist)):
                alist[i] = alist[i]*delta + low
        return alist

    def Normalize(self,x,max,min):
        delta= float(max-min)
        if delta !=0:
            x=(x-min)/delta
        return x

    def transfromX(self,one_X,tag="240"):
        if tag=="onestep":
            one_X = [self.Normalize(one_X[i], self.scaler_max_onestep[i], self.scaler_min_onestep[i]) for i in range(len(one_X))]
        else:
            one_X = [self.Normalize(one_X[i], self.scaler_max[i], self.scaler_min[i]) for i in range(len(one_X))]
        one_X=np.array([one_X])
        one_X = one_X.reshape((one_X.shape[0], 1,9))
        return one_X

    def makeAPrediction(self,one_X):
        one_X=self.transfromX(one_X)
        with graph.as_default():
            one_y=model.predict(one_X)
        longitudes=[one[0] for one in one_y[0][:,-3:-2]]
        longitudes=self.FNoramlize(longitudes,self.scaler_min[-3],self.scaler_max[-3])
        latitudes=[one[0] for one in one_y[0][:,-2:-1]]
        latitudes=self.FNoramlize(latitudes,self.scaler_min[-2],self.scaler_max[-2])
        altitudes=[one[0] for one in one_y[0][:,-1:]]
        altitudes=self.FNoramlize(altitudes,self.scaler_min[-1],self.scaler_max[-1])
        return longitudes,latitudes,altitudes

    def makeNextMinPrediction(self,one_X):
        one_X = self.transfromX(one_X,tag="onestep")
        print(one_X)
        global graph
        graph = tf.get_default_graph()
        with graph.as_default():
            one_y = nextMinModel.predict(one_X)
        print(one_y)
        longitudes = [one for one in one_y[:, -3:-2]]
        longitudes = self.FNoramlize(longitudes, self.scaler_min[-3], self.scaler_max[-3])
        latitudes = [one for one in one_y[:, -2:-1]]
        latitudes = self.FNoramlize(latitudes, self.scaler_min[-2], self.scaler_max[-2])
        altitudes = [one for one in one_y[:, -1:]]
        altitudes = self.FNoramlize(altitudes, self.scaler_min[-1], self.scaler_max[-1])
        return longitudes[0], latitudes[0], altitudes[0]