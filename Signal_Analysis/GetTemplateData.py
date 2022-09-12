from pip import main
import redis
import redis
import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import os
from scipy.fftpack import fft,ifft, hilbert
# from pyts.approximation import PiecewiseAggregateApproximation
import pylab
import threading
from scipy.io import loadmat,savemat
from PIL import Image
import util
########################################################################################
#########读取json
###################################################################################




#######################读取时域有量纲信息json#######################################
#############################################################################
def get_dimensional_Template_data(path):
    template_skewness = []
    template_kurtosis = []
    template_boxing = []
    template_fengzhi = []
    template_maichong = []
    for root , dirs , files  in os.walk(path):
        for json_file in files:
            json_path = path + '/' + json_file
            with open(json_path) as fr:
                json_data = json.load(fr)
                template_skewness.append(json_data['mean'])
                template_kurtosis.append(json_data['var'])
                template_boxing.append(json_data['std'])
                template_fengzhi.append(json_data['rms'])
                template_maichong.append(json_data['fengfengzhi'])
    template_stat_mean = np.array(template_skewness).mean()
    template_stat_var = np.array(template_kurtosis).mean()
    template_stat_std = np.array(template_boxing).mean()
    template_stat_rms = np.array(template_fengzhi).mean()
    template_stat_fengfengzhi = np.array(template_maichong).mean()

    return template_stat_mean,template_stat_var,template_stat_std,template_stat_rms,template_stat_fengfengzhi

#######################读取时域无量纲信息json#######################################
def get_nondimensional_Template_data(path):
    template_skewness = []
    template_kurtosis = []
    template_boxing = []
    template_fengzhi = []
    template_maichong = []
    template_yudu = []
    for root , dirs , files  in os.walk(path):
        for json_file in files:
            json_path = path + '/' + json_file
            with open(json_path) as fr:
                json_data = json.load(fr)
                template_skewness.append(json_data['skewness'])
                template_kurtosis.append(json_data['kurtosis'])
                template_boxing.append(json_data['boxing'])
                template_fengzhi.append(json_data['fengzhi'])
                template_maichong.append(json_data['maichong'])
                template_yudu.append(json_data['yudu'])
    template_stat_skewness = np.array(template_skewness).mean()
    template_stat_kurtosis = np.array(template_kurtosis).mean()
    template_stat_boxing = np.array(template_boxing).mean()
    template_stat_fengzhi = np.array(template_fengzhi).mean()
    template_stat_maichong = np.array(template_maichong).mean()
    template_stat_yudu = np.array(template_yudu).mean()
    return template_stat_skewness,template_stat_kurtosis,template_stat_boxing,template_stat_fengzhi,template_stat_maichong,template_stat_yudu


#######################读取feature json#######################################
def get_feature_template_data(path):
    time_feature = []
    frequent_feature = []
    simple_feature = []
    for root , dirs , files  in os.walk(path):
        for json_file in files:
            json_path = path + '/' + json_file
            with open(json_path) as fr:
                json_data = json.load(fr)
                time_feature.append(json_data['timeDomain'])
                frequent_feature.append(json_data['frequencyDomain'])
                simple_feature.append(json_data['simple'])
    
    res_time = np.array(time_feature)
    res_frequent = np.array(frequent_feature)
    res_simple = np.array(simple_feature)
    
    #列均值
    time_mean = np.mean(res_time,axis=0) 
    frequent_mean = np.mean(res_frequent,axis=0)
    simple_mean = np.mean(res_simple,axis=0)

    return time_mean,frequent_mean,simple_mean