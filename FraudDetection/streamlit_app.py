# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 11:07:52 2022

@author: Chimaobi Okite
"""

import streamlit as st
import pandas as pd
import pickle
from datetime import time

##load the training model
pickle_in = open(r"C:\Users\lenovo\Documents\Machine_Learning\Deployments\classifier.pkl", 'rb') 
classifier = pickle.load(pickle_in)

def main():
    
    st.title('Anomaly Detection In Cellular Networks Demo')
    
    t = st.time_input('Enter time of observation', time(8, 45))
    t = str(t)
    Time = t[: -3]
    
    cellNum = st.slider('Set Cell Number',0,10,2,1)
    base = st.radio('Enter Base name', ('A','B','C','U','W','V'), 0)
    
    PRBUsageUL	= st.slider('Percentage PRB uplink', 0.0, 100.0, 0.01)
    PRBUsageDL	= st.slider('Percentage PRB downlink', 0.0, 100.0, 0.01)
    
    meanThr_DL	= st.slider('Mean Traffic Carried downlink',  0.0, 20.0, 0.01)
    meanThr_UL	= st.slider('Mean Traffic Carried uplink' , 0.0, 20.0, 0.01)
    
    maxThr_DL	= st.slider('Maximum Traffic Carried downlink',  0.0, 200.0, 0.01)
    maxThr_UL	= st.slider('Maximum Traffic Carried uplink',  0.0, 200.0, 0.01)
    
    meanUE_DL = st.slider('Average Number Of User Equipment Active downlink', 0.0, 5.0, 0.01)
    meanUE_UL = st.slider('Average Number Of User Equipment Active Uplink',  0.0, 5.0, 0.01)
    
    maxUE_DL = st.slider('Maximum Number Of User Equipment Active downlink', 0, 20, 1)
    maxUE_UL = st.slider('Maximum Number Of User Equipment Active Uplink', 0, 20, 1)
    
    maxUE_ULDL = maxUE_DL + maxUE_UL
    data = pd.DataFrame({'Time': Time, 'PRBUsageUL': PRBUsageUL, 'PRBUsageDL': PRBUsageDL,
                         'meanThr_DL': meanThr_DL, 'meanThr_UL':meanThr_UL,
                         'maxThr_DL':maxThr_DL, 'maxThr_UL':maxThr_UL,
                         'meanUE_DL':meanUE_DL, 'meanUE_UL':meanUE_UL,
                         'maxUE_DL':maxUE_DL, 'maxUE_UL':maxUE_UL, 
                         'maxUE_UL+DL': maxUE_ULDL,'hour':0,
                         'minute': 0,'cell_code':0,
                         'BaseName_A':0,'BaseName_B':0, 
                         'BaseName_C':0, 'BaseName_U':0, 'BaseName_V':0,
                         'BaseName_W':0}, index=[0])
    
    
    if st.button("Predict"):
        result = process(data, cellNum, base)
        if result == 0:
            st.success('0 (normal): The current activity of this cell corresponds to normal behavior')
        else: 
            st.success('1 (usual): current activity slightly differs from the behavior usually observed for this time of the day')
        

def process(data, cellNum, base,):
  data[['maxUE_UL', 'maxUE_DL', 'maxUE_UL+DL']] = data[['maxUE_UL', 'maxUE_DL', 'maxUE_UL+DL']].fillna(0)
  data['maxUE_UL+DL'] = data['maxUE_UL+DL'].replace(to_replace= '#¡VALOR!', value = 0)
  data['maxUE_UL+DL'] = data['maxUE_UL+DL'].apply(lambda x: int(x))
  data['hour'] = data['Time'].map(lambda x : int(x[0:x.index(':')]))
  data['minute'] = data['Time'].map(lambda x : int(x[x.index(':') + 1:]))
  data['cell_code'] = cellNum
  data = data.drop(['Time'], axis = 1)
  data['BaseName_' + base] = 1

  prediction = classifier.predict(data)
  
  return prediction


if __name__=='__main__': 
    main()

