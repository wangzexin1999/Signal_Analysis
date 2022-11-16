from pip import main
import redis
import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import os
from scipy.fftpack import fft,ifft, hilbert
import pylab
import threading
from scipy.io import loadmat,savemat
from PIL import Image


#全局的路径
global gl_source_path 
gl_source_path = "D:\QT_backward\Signal_Analysis\qt"


############redis操作########################################################
def RedisConnect(port,host ='localhost'):
    connect = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)
    return connect

def RedisLpush(redisConect,key,value):
    redisConect.lpush(key,value)

#时域操作

############获取时域幅值#############################################
def get_amplitude(single_data):
    amplitude = {}
    for i in range(len(single_data)):
        x_point = "x_axis: " + str(i)
        amplitude[x_point] = float(single_data[i])
    return amplitude

###########获取频域谱线#############################################
def get_puxian(single_data):
    puxian = {}
    for i in range(len(single_data)):
        if single_data[i] > 25:
            x_point = "x_axis: " + str(i)
            puxian[x_point] = float(single_data[i])
    return puxian 

############归一化#############################################
def Normalization(fftdata):
    ymax = 255
    ymin = 0
    xmax = max(fftdata)
    xmin = min(fftdata)
    fftdata_nor = []
    if xmax == xmin:
        return fftdata
    for i in range(len(fftdata)):
        fftdata_nor.append(round(((ymax - ymin) * (fftdata[i] - xmin) / (xmax - xmin)) + ymin))

    # MaxPoint = max(fftdata)
    # minPoint = min(fftdata)
    # distance = MaxPoint - minPoint
    # fftdata_nor = []
    # for i in range (len(fftdata)):
    #     fftdata_temp = (fftdata[i] - minPoint)/distance
    #     fftdata_nor.append(fftdata_temp)
    return fftdata_nor

def NormalizationZero(fftdata):
    MaxPoint = max(fftdata)
    minPoint = min(fftdata)
    distance = MaxPoint - minPoint
    fftdata_nor = []
    for i in range (len(fftdata)):
        fftdata_temp = (fftdata[i] - minPoint)/distance
        fftdata_nor.append(fftdata_temp)
    return fftdata_nor
    


#######################创建文件夹#############################################
def make_dir(domain,work_condition,channelCode):

    source_path = gl_source_path+ "/TemplateFile"
    made_dir = source_path+'//'+work_condition+'/'+domain+'/'+channelCode
    if os.path.exists(source_path+'/'+work_condition+'/'+domain+'/'+channelCode):
        isExist = True
        print(work_condition+'文件夹已存在')
    else:
        os.makedirs(source_path+'/'+work_condition+'/'+domain+'/'+channelCode)
        isExist = False
    return isExist , made_dir

#######################获取最大的三个谱线#############################################
def FindMax3Puxian(ls): # 快速获取list中最大的三个元素
    max1, max2, max3 = None, None, None
    for num in ls:
        if max1 is None or max1 < num:
            max1, num = num, max1
        if num is None:
            continue
        if max2 is None or num > max2:
            max2, num = num, max2
        if num is None:
            continue
        if max3 is None or num > max3:
            max3 = num
    max1Index = ls.index(max1)
    max2Index = ls.index(max2)
    max3Index = ls.index(max3)
    return max1, max2, max3,max1Index,max2Index,max3Index

#######################计算总值#############################################
def TotalValue(single_data):
    totalsum = 0
    for i in range(len(single_data)):
        totalsum += single_data[i]
    return totalsum

#######################时域转频域#############################################
def timeToFFT(single_data):
    dataLength = len(single_data)
    a = np.tile(single_data,2)
    fft_y=fft(a) 
    fft_y[0] = 0
    fft_y = np.resize(fft_y,dataLength)
    x = np.linspace(0, dataLength, dataLength,endpoint=True)
    fft_array = fft_y.reshape(-1)
    fftTransformdata = abs(fft_array).tolist()
    return fftTransformdata

#######################计算与模板的差异#############################################
#后期可以设定阈值
def count_difference(template,real):
    N= len(template)
    strange = []
    for i in range(N):
        if(abs(template[i] - real[i])/template[i]>0.85):
            strange.append(i)
        # print(abs(template[i] - real[i])/template[i])
    return strange

#######################获取时域-频域信息-江德宏#############################################
def feature_extra(timeDomainData,sampleRate=20000):
    reslut={}
    N = len(timeDomainData) #采样个数
    # 时域特征
    F1 = sum(timeDomainData) / N
    F2 = (sum([ (index - F1)**2  for index in timeDomainData])/(N-1))**0.5
    F3 = (np.sum(np.power(np.abs(timeDomainData),0.5))/N)**2 #F3与原公式有点不一样，原公式不求绝对值，但是信号有负数
    F4 = (np.sum(np.power(timeDomainData,2))/N)**0.5
    F5 = np.max(np.abs(timeDomainData))
    F6 = np.sum(np.power(timeDomainData-F1,3))/((N-1)*F2**3)
    F7 = np.sum((timeDomainData-F1)**4)/((N-1)*(F2**4))
    F8 = F5 /F4
    F9 =F5/F3
    F10 =F4/(1/N*np.sum(np.abs(timeDomainData)))
    F11 = F10/F4 * F5


    #计算单边谱,因为双边谱完全是对称的
    fft_data = fft(timeDomainData)
    fft_amp = np.array(np.abs(fft_data)/N*2)[0:int(N/2)] #s(k)
    fft_amp[0] *= 0.5
    #绘制频率轴
    list = np.array(range(0, int(N/2)))
    freq = sampleRate*list/N #f(k)
    #频域特征
    K = list.size   #谱线数
    F12 = np.sum(fft_amp)/K
    F13 = np.sum((fft_amp-F12)**2)/(K-1)
    F14 = np.sum((fft_amp-F12)**3)/(K*(F13**2))
    F15 = np.sum((fft_amp-F12)**4)/(K*(F13**2))
    F16 = np.sum((fft_amp*freq))/(F12*K)
    F17 = (np.sum((freq - F16)**2 * fft_amp)/K)**0.5

    temp = np.sum(freq**2 * fft_amp)
    F18 = (temp/(F12*K))**0.5
    F19 = (np.sum(freq**4 * fft_amp)/temp)**0.5
    F20 = temp /((F12*K)**0.5 * F19*temp**0.5)
    F21 = F17 / F16
    F22 = np.sum((freq-F16)**3 * fft_amp)/(K*F17**3)
    F23 = np.sum((freq-F16)**4 * fft_amp)/(K * F17**4)
    # F24 = np.sum((freq - F16)**0.5 * fft_amp)/(K* F17**0.5) #开方也出现错误

    #简单统计值
    efficient = np.sum(fft_amp)
    rms = np.mean(fft_amp**2)**0.5
    reslut['timeDomain']=[F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11]
    reslut['frequencyDomain'] = [F12,F13,F14,F15,F16,F17,F18,F19,F20,F21,F22,F23]
    reslut['simple'] = [efficient,rms]
    return reslut


