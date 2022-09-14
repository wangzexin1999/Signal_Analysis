from pip import main
import redis
import redis
import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import pandas as pd
from scipy.fftpack import fft,ifft, hilbert
# from pyts.approximation import PiecewiseAggregateApproximation
import pylab
import threading
from scipy.io import loadmat,savemat
from PIL import Image
import util
import GetTemplateData
from Monitor import Monitor
########################################################################################
#########实时信号监测
###################################################################################



#######################时域信号(有量纲)分析#######################################
def MonitorTimeDomainSignal(Work_Condition, channelCode,path):
    r = util.RedisConnect(6379,'localhost')
    template_stat_mean,template_stat_var,template_stat_std,template_stat_rms,template_stat_fengfengzhi = GetTemplateData.get_dimensional_Template_data(path)
    signal_num = 1
    while(True):
        # every_data = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
        every_data_all = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])
        data_workCondition = list(every_data_all.keys())[0]#工况信息
        print("当前检测的数据为时域有量纲-工况：{}-通道：{}".format(Work_Condition,channelCode))
        every_data = every_data_all[data_workCondition]
        everyPuXianDict = util.get_amplitude(every_data)
        amplitudeList = []
        for puxian in everyPuXianDict.items():
            amplitudeList.append(puxian[1])
        amplitudeList = np.array(amplitudeList)
        puxian_mean = amplitudeList.mean()
        puxian_var = amplitudeList.var()
        puxian_std = amplitudeList.std()
        puxian_rms = np.sqrt(pow(puxian_mean, 2) + pow(puxian_std, 2))
        puxian_fengfengzhi = max(amplitudeList) - min(amplitudeList)

        mean_difference = abs(puxian_mean - template_stat_mean)
        var_difference = abs(puxian_var - template_stat_var)
        std_difference = abs(puxian_std - template_stat_std)
        rms_difference = abs(puxian_rms - template_stat_rms)
        fengfengzhi_difference = abs(puxian_fengfengzhi - template_stat_fengfengzhi)

        # print(mean_difference,var_difference,std_difference,rms_difference,fengfengzhi_difference)
        if (mean_difference > 0.6 or var_difference > 16 or  std_difference > 1.25 or rms_difference > 1.2 or fengfengzhi_difference > 23.5):
            print("第{}组数据分析完成,结果为异常".format(signal_num))
            monitorResult = 1
        else:
            print("第{}组数据分析完成,结果为正常".format(signal_num))
            monitorResult = 0
        r.lpush("MonitorResult",monitorResult)
        signal_num += 1


#######################时域信号(无量纲)分析#######################################
def MonitorNondimentionalTimeDomainSignal(Work_Condition, channelCode,path):
    r = util.RedisConnect(6379,'localhost')
    template_stat_skewness,template_stat_kurtosis,template_stat_boxing,template_stat_fengzhi,template_stat_maichong,template_stat_yudu = GetTemplateData.get_nondimensional_Template_data(path)
    signal_num = 1
    while(True):
        # every_data = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
        every_data_all = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])
        data_workCondition = list(every_data_all.keys())[0]#工况信息
        print("当前检测的数据为时域无量纲-工况：{}-通道：{}".format(Work_Condition,channelCode))
        every_data = every_data_all[data_workCondition]
        everyPuXianDict = util.get_amplitude(every_data)
        amplitudeList = []
        for puxian in everyPuXianDict.items():
            amplitudeList.append(puxian[1])
        amplitudeList = np.array(amplitudeList)
        puxian_mean = amplitudeList.mean()
        puxian_var = amplitudeList.var()
        puxian_std = amplitudeList.std()
        puxian_rms = np.sqrt(pow(puxian_mean, 2) + pow(puxian_std, 2))
        puxian_fengfengzhi = max(amplitudeList) - min(amplitudeList)
        amplitude_series = pd.Series(amplitudeList)
        puxian_skewness = amplitude_series.skew()#偏度
        puxian_kurtosis = amplitude_series.kurt()#峭度
        sum1=0
        for j in range(len(amplitudeList)):
            sum1+=math.sqrt(abs(amplitudeList[j]))
        #波形因子
        puxian_boxing=puxian_rms / (abs(amplitudeList).mean())
        #峰值因子
        puxian_fengzhi=(max(amplitudeList)) / puxian_rms
        #脉冲因子
        puxian_maichong=(max(amplitudeList)) / (abs(amplitudeList).mean())
        #裕度因子
        puxian_yudu=(max(amplitudeList)) / pow((sum1/(20000)),2)

        skewness_difference = abs(puxian_skewness - template_stat_skewness)
        kurtosis_difference = abs(puxian_kurtosis - template_stat_kurtosis)
        boxing_difference = abs(puxian_boxing - template_stat_boxing)
        fengzhi_difference = abs(puxian_fengzhi - template_stat_fengzhi)
        maichong_difference = abs(puxian_maichong - template_stat_maichong)
        yudu_difference = abs(puxian_yudu - template_stat_yudu)

        # print(skewness_difference,kurtosis_difference,boxing_difference,fengzhi_difference,maichong_difference,yudu_difference)
        if (skewness_difference > 0.06 or kurtosis_difference > 0.25 or  boxing_difference > 0.23 or fengzhi_difference > 0.9 or maichong_difference > 0.6 or yudu_difference > 0.7):
            print("第{}组数据分析完成,结果为异常".format(signal_num))
        else:
            print("第{}组数据分析完成,结果为正常".format(signal_num))
        signal_num += 1


#######################频域信号(有量纲)分析#######################################
def MonitorFrequentDomainSignal(Work_Condition, channelCode,path):
    r = util.RedisConnect(6379,'localhost')
    template_stat_mean,template_stat_var,template_stat_std,template_stat_rms,template_stat_fengfengzhi = GetTemplateData.get_dimensional_Template_data(path)
    signal_num = 1
    while(True):
        # every_data = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
        every_data_all = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])
        data_workCondition = list(every_data_all.keys())[0]#工况信息
        print("当前检测的数据为频域有量纲-工况：{}-通道：{}".format(Work_Condition,channelCode))
        every_data = every_data_all[data_workCondition]
        every_data = util.Normalization(every_data)
        everyPuXianDict = util.get_puxian(every_data)
        amplitudeList = []
        for puxian in everyPuXianDict.items():
            amplitudeList.append(puxian[1])
        amplitudeList = np.array(amplitudeList)
        puxian_mean = amplitudeList.mean()
        puxian_var = amplitudeList.var()
        puxian_std = amplitudeList.std()
        puxian_rms = np.sqrt(pow(puxian_mean, 2) + pow(puxian_std, 2))
        puxian_fengfengzhi = max(amplitudeList) - min(amplitudeList)

        mean_difference = abs(puxian_mean - template_stat_mean)
        var_difference = abs(puxian_var - template_stat_var)
        std_difference = abs(puxian_std - template_stat_std)
        rms_difference = abs(puxian_rms - template_stat_rms)
        fengfengzhi_difference = abs(puxian_fengfengzhi - template_stat_fengfengzhi)

        # print(mean_difference,var_difference,std_difference,rms_difference,fengfengzhi_difference)
        if (mean_difference > 5 or var_difference > 200 or  std_difference > 3 or rms_difference > 10 or fengfengzhi_difference > 0.09):
            print("第{}组数据分析完成,结果为异常".format(signal_num))
        else:
            print("第{}组数据分析完成,结果为正常".format(signal_num))
        signal_num += 1


#######################时域信号(无量纲)分析#######################################
def MonitorNondimentionalFrequencyDomainSignal(Work_Condition, channelCode,path):
    r = util.RedisConnect(6379,'localhost')
    template_stat_skewness,template_stat_kurtosis,template_stat_boxing,template_stat_fengzhi,template_stat_maichong,template_stat_yudu = GetTemplateData.get_nondimensional_Template_data(path)
    signal_num = 1
    while(True):
        # every_data = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
        every_data_all = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])
        data_workCondition = list(every_data_all.keys())[0]#工况信息
        print("当前检测的数据为数据为频域无量纲-工况：{}-通道：{}".format(Work_Condition,channelCode))
        every_data = every_data_all[data_workCondition]
        every_data = util.Normalization(every_data)
        everyPuXianDict = util.get_puxian(every_data)
        amplitudeList = []
        for puxian in everyPuXianDict.items():
            amplitudeList.append(puxian[1])
        amplitudeList = np.array(amplitudeList)
        puxian_mean = amplitudeList.mean()
        puxian_var = amplitudeList.var()
        puxian_std = amplitudeList.std()
        puxian_rms = np.sqrt(pow(puxian_mean, 2) + pow(puxian_std, 2))
        puxian_fengfengzhi = max(amplitudeList) - min(amplitudeList)
        amplitude_series = pd.Series(amplitudeList)
        puxian_skewness = amplitude_series.skew()#偏度
        puxian_kurtosis = amplitude_series.kurt()#峭度
        sum1=0
        for j in range(len(amplitudeList)):
            sum1+=math.sqrt(abs(amplitudeList[j]))
        #波形因子
        puxian_boxing=puxian_rms / (abs(amplitudeList).mean())
        #峰值因子
        puxian_fengzhi=(max(amplitudeList)) / puxian_rms
        #脉冲因子
        puxian_maichong=(max(amplitudeList)) / (abs(amplitudeList).mean())
        #裕度因子
        puxian_yudu=(max(amplitudeList)) / pow((sum1/(20000)),2)

        skewness_difference = abs(puxian_skewness - template_stat_skewness)
        kurtosis_difference = abs(puxian_kurtosis - template_stat_kurtosis)
        boxing_difference = abs(puxian_boxing - template_stat_boxing)
        fengzhi_difference = abs(puxian_fengzhi - template_stat_fengzhi)
        maichong_difference = abs(puxian_maichong - template_stat_maichong)
        yudu_difference = abs(puxian_yudu - template_stat_yudu)

        # print(skewness_difference,kurtosis_difference,boxing_difference,fengzhi_difference,maichong_difference,yudu_difference)
        if (skewness_difference > 0.06 or kurtosis_difference > 0.4 or  boxing_difference > 0.23 or fengzhi_difference > 0.1 or maichong_difference > 0.1 or yudu_difference > 0.2):
            print("第{}组数据分析完成,结果为异常".format(signal_num))
        else:
            print("第{}组数据分析完成,结果为正常".format(signal_num))
        signal_num += 1

#######################时域、频域特征分析 2022-0909#######################################
def monitor_signal_feature(Work_Condition, channelCode,path):
    r = util.RedisConnect(6379,'localhost')
    time_mean,frequent_mean,simple_mean = GetTemplateData.get_feature_template_data(path)
    signal_num = 1
    while(True):
        # every_data = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])['redisCollectionData']
        every_data_all = json.loads(r.brpop("redisCollectionData-"+ channelCode)[1])
        data_workCondition = list(every_data_all.keys())[0]#工况信息
        print("当前为特征值监测-工况：{}-通道：{}".format(Work_Condition,channelCode))
        every_data = np.array(every_data_all[data_workCondition])
        data_feature = util.feature_extra(every_data)
        strange = {}
        strange['timeDomain'] = util.count_difference(time_mean,data_feature['timeDomain'])
        strange['frequencyDomain'] = util.count_difference(frequent_mean,data_feature['frequencyDomain'])
        strange['simple'] = util.count_difference(simple_mean,data_feature['simple'])
        print(strange['timeDomain'])


def monitor_frequencyDomain():

    m = Monitor()
    m.monitorFrequencyDomain()