from posixpath import dirname
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
import util

########################################################################################
#########p获取模板
###################################################################################


source_path = util.gl_source_path
#######################获取时域有量纲信息模板#######################################
def GetNormalTimeDomainSignalTemplate(TemplateSize , workCondition, channelCode):
    isExist , dirname = util.make_dir('Time_Dimain_dimensional',workCondition , channelCode)
    if(isExist == False):
        r = util.RedisConnect(6379,'localhost')
        for i in range(TemplateSize):
            # every_data = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前记录的模板数据为---时域(有量纲)---工况：{}---通道：{}".format(workCondition,channelCode))
            every_data = every_data_all[data_workCondition]
            everyPuXianDict = util.get_amplitude(every_data)
            amplitudeList = []
            for puxian in everyPuXianDict.items():
                amplitudeList.append(puxian[1])
            amplitudeList = np.array(amplitudeList)
            amplitude_mean = amplitudeList.mean()
            amplitude_var = amplitudeList.var()#方差
            amplitude_std = amplitudeList.std()#标准差
            amplitude_rms = np.sqrt(pow(amplitude_mean, 2) + pow(amplitude_std, 2))#均方根
            amplitude_fengfengzhi = max(amplitudeList) - min(amplitudeList)
            pinpuStatisticDict = {}
            pinpuStatisticDict['mean'] = amplitude_mean
            pinpuStatisticDict['var'] = amplitude_var
            pinpuStatisticDict['std'] = amplitude_std
            pinpuStatisticDict['rms'] = amplitude_rms
            pinpuStatisticDict['fengfengzhi'] = amplitude_fengfengzhi
            with open(source_path +"/TemplateFile/{}/Time_Dimain_dimensional/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(workCondition,channelCode,channelCode,workCondition,str(i)),"w") as f:
                json.dump(pinpuStatisticDict,f)
                f.close()
            print("已记录的模板样本量: {}".format(i+1))
        
            # plt.plot(time_data)
            # plt.savefig("/home/wangzexin/Graduation/wdcnn_project/pinpu/{}pinpu--time--{}.png".format(channelCode,str(i)))

        print("模板样本记录完成，共{}组样本".format(TemplateSize))

    return dirname


#######################获取时域无量纲信息模板#######################################
def GetNormalNondimensionalTimeDomainSignalTemplate(TemplateSize , workCondition, channelCode):
    isExist , dirname = util.make_dir('Time_Dimain_nondimensional',workCondition , channelCode)
    if(isExist == False):
        r = util.RedisConnect(6379,'localhost')
        for i in range(TemplateSize):
            # every_data = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前记录的模板数据为---时域(无量纲)---工况：{}---通道：{}".format(workCondition,channelCode))
            every_data = every_data_all[data_workCondition]
            everyPuXianDict = util.get_amplitude(every_data)
            amplitudeList = []
            for puxian in everyPuXianDict.items():
                amplitudeList.append(puxian[1])
            amplitudeList = np.array(amplitudeList)
            amplitude_mean = amplitudeList.mean()
            amplitude_var = amplitudeList.var()#方差
            amplitude_std = amplitudeList.std()#标准差
            amplitude_rms = np.sqrt(pow(amplitude_mean, 2) + pow(amplitude_std, 2))#均方根
            amplitude_fengfengzhi = max(amplitudeList) - min(amplitudeList)
            amplitude_series = pd.Series(amplitudeList)
            amplitude_skewness = amplitude_series.skew()#偏度
            amplitude_kurtosis = amplitude_series.kurt()#峭度
            sum=0
            for j in range(len(amplitudeList)):
                sum+=math.sqrt(abs(amplitudeList[j]))
            #波形因子
            df_boxing=amplitude_rms / (abs(amplitudeList).mean())
            #峰值因子
            df_fengzhi=(max(amplitudeList)) / amplitude_rms
            #脉冲因子
            df_maichong=(max(amplitudeList)) / (abs(amplitudeList).mean())
            #裕度因子
            df_yudu=(max(amplitudeList)) / pow((sum/(20000)),2)
            pinpuStatisticDict = {}
            pinpuStatisticDict['skewness'] = amplitude_skewness
            pinpuStatisticDict['kurtosis'] = amplitude_kurtosis
            pinpuStatisticDict['boxing'] = df_boxing
            pinpuStatisticDict['fengzhi'] = df_fengzhi
            pinpuStatisticDict['maichong'] = df_maichong
            pinpuStatisticDict['yudu'] = df_yudu
            with open(source_path+"/TemplateFile/{}/Time_Dimain_nondimensional/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(workCondition,channelCode,channelCode,workCondition,str(i)),"w") as f:
                json.dump(pinpuStatisticDict,f)
                f.close()
            print("已记录的模板样本量: {}".format(i+1))
        
            # plt.plot(time_data)
            # plt.savefig("/home/wangzexin/Graduation/wdcnn_project/pinpu/{}pinpu--time--{}.png".format(channelCode,str(i)))

        print("模板样本记录完成，共{}组样本".format(TemplateSize))

    return dirname

#######################获取频域有量纲信息模板#######################################
def GetNormalFrequencyDomainSignalTemplate(TemplateSize , workCondition, channelCode):
    isExist , dirname = util.make_dir('Frequent_Dimain_dimensional',workCondition , channelCode)
    if(isExist == False):
        r = util.RedisConnect(6379,'localhost')
        for i in range(TemplateSize):
            # every_data = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前记录的模板数据为---频域(有量纲)---工况：{}---通道：{}".format(workCondition,channelCode))
            every_data = every_data_all[data_workCondition]
            every_data = util.Normalization(every_data)
            everyPuXianDict = util.get_puxian(every_data)
            amplitudeList = []
            for puxian in everyPuXianDict.items():
                amplitudeList.append(puxian[1])
            amplitudeList = np.array(amplitudeList)
            amplitude_mean = amplitudeList.mean()
            amplitude_var = amplitudeList.var()#方差
            amplitude_std = amplitudeList.std()#标准差
            amplitude_rms = np.sqrt(pow(amplitude_mean, 2) + pow(amplitude_std, 2))#均方根
            amplitude_fengfengzhi = max(amplitudeList) - min(amplitudeList)
            pinpuStatisticDict = {}
            pinpuStatisticDict['mean'] = amplitude_mean
            pinpuStatisticDict['var'] = amplitude_var
            pinpuStatisticDict['std'] = amplitude_std
            pinpuStatisticDict['rms'] = amplitude_rms
            pinpuStatisticDict['fengfengzhi'] = amplitude_fengfengzhi
            with open(source_path+"/TemplateFile/{}/Frequent_Dimain_dimensional/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(workCondition,channelCode,channelCode,workCondition,str(i)),"w") as f:
                json.dump(pinpuStatisticDict,f)
                f.close()
            print("已记录的模板样本量: {}".format(i+1))
        
            # plt.plot(time_data)
            # plt.savefig("/home/wangzexin/Graduation/wdcnn_project/pinpu/{}pinpu--time--{}.png".format(channelCode,str(i)))

        print("模板样本记录完成，共{}组样本".format(TemplateSize))

    return dirname


#######################获取频域无量纲信息模板#######################################
def GetNormalNondimensionalFrequencyDomainSignalTemplate(TemplateSize , workCondition, channelCode):
    isExist , dirname = util.make_dir('Frequent_Dimain_nondimensional',workCondition , channelCode)
    if(isExist == False):
        r = util.RedisConnect(6379,'localhost')
        for i in range(TemplateSize):
            # every_data = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前记录的模板数据为---频域(无量纲)---工况：{}---通道：{}".format(workCondition,channelCode))
            every_data = every_data_all[data_workCondition]
            every_data = util.Normalization(every_data)
            everyPuXianDict = util.get_puxian(every_data)
            amplitudeList = []
            for puxian in everyPuXianDict.items():
                amplitudeList.append(puxian[1])
            amplitudeList = np.array(amplitudeList)
            amplitude_mean = amplitudeList.mean()
            amplitude_var = amplitudeList.var()#方差
            amplitude_std = amplitudeList.std()#标准差
            amplitude_rms = np.sqrt(pow(amplitude_mean, 2) + pow(amplitude_std, 2))#均方根
            amplitude_fengfengzhi = max(amplitudeList) - min(amplitudeList)
            amplitude_series = pd.Series(amplitudeList)
            amplitude_skewness = amplitude_series.skew()#偏度
            amplitude_kurtosis = amplitude_series.kurt()#峭度
            sum=0
            for j in range(len(amplitudeList)):
                sum+=math.sqrt(abs(amplitudeList[j]))
            #波形因子
            df_boxing=amplitude_rms / (abs(amplitudeList).mean())
            #峰值因子
            df_fengzhi=(max(amplitudeList)) / amplitude_rms
            #脉冲因子
            df_maichong=(max(amplitudeList)) / (abs(amplitudeList).mean())
            #裕度因子
            df_yudu=(max(amplitudeList)) / pow((sum/(20000)),2)
            pinpuStatisticDict = {}
            pinpuStatisticDict['skewness'] = amplitude_skewness
            pinpuStatisticDict['kurtosis'] = amplitude_kurtosis
            pinpuStatisticDict['boxing'] = df_boxing
            pinpuStatisticDict['fengzhi'] = df_fengzhi
            pinpuStatisticDict['maichong'] = df_maichong
            pinpuStatisticDict['yudu'] = df_yudu
            with open(source_path+"/TemplateFile/{}/Frequent_Dimain_nondimensional/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(workCondition,channelCode,channelCode,workCondition,str(i)),"w") as f:
                json.dump(pinpuStatisticDict,f)
                f.close()
            print("已记录的模板样本量: {}".format(i+1))
        
            # plt.plot(time_data)
            # plt.savefig("/home/wangzexin/Graduation/wdcnn_project/pinpu/{}pinpu--time--{}.png".format(channelCode,str(i)))

        print("模板样本记录完成，共{}组样本".format(TemplateSize))

    return dirname

#######################获取特征值信息模板-2022-0909#######################################
def get_normal_feature_template(TemplateSize , workCondition, channelCode):
    template_name = 'signal_feature'
    isExist , dirname = util.make_dir(template_name,workCondition , channelCode)
    if(isExist == False):
        r = util.RedisConnect(6379,'localhost')
        for i in range(TemplateSize):
            # every_data = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前记录的模板数据为工况：{}---通道：{}".format(workCondition,channelCode))
            every_data = np.array(every_data_all[data_workCondition])
            signal_feature = util.feature_extra(every_data)
            with open(source_path +"/TemplateFile/{}/{}/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(workCondition,template_name,channelCode,channelCode,workCondition,str(i)),"w") as f:
                json.dump(signal_feature,f)
                f.close()
            print("已记录的模板样本量: {}".format(i+1))
        
        print("模板样本记录完成，共{}组样本".format(TemplateSize))

    return dirname

#######################获取特征值信息模板-2022-0909#######################################
def get_normal_feature_template(TemplateSize , workCondition, channelCode):
    template_name = 'signal_feature'
    isExist , dirname = util.make_dir(template_name,workCondition , channelCode)
    if(isExist == False):
        r = util.RedisConnect(6379,'localhost')
        for i in range(TemplateSize):
            # every_data = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.blpop("redisCollectionData-"+ channelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前记录的模板数据为工况：{}---通道：{}".format(workCondition,channelCode))
            every_data = np.array(every_data_all[data_workCondition])
            signal_feature = util.feature_extra(every_data)
            with open(source_path +"/TemplateFile/{}/{}/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(workCondition,template_name,channelCode,channelCode,workCondition,str(i)),"w") as f:
                json.dump(signal_feature,f)
                f.close()
            print("已记录的模板样本量: {}".format(i+1))
        
        print("模板样本记录完成，共{}组样本".format(TemplateSize))

    return dirname