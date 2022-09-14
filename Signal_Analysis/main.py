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
import GetNormalSignalTemplate
import MonitorSignal


######参数设置######################

#通道0-0
template_workCondition_0 = '3000rpm-160kw-0103' #模板采集与分析的工况
tmplateSize_0 = 10

#通道0-1
template_workCondition_1 = '3000rpm-560kw-0103' #模板采集与分析的工况
tmplateSize_1 = 20

#通道0-2
template_workCondition_2 = '3000rpm-560kw-0103' #模板采集与分析的工况
tmplateSize_2 = 10


#通道0-3
template_workCondition_3 = '4000rpm-560kw-0103' #模板采集与分析的工况
tmplateSize_3 = 10




class myThread (threading.Thread):
    def __init__(self, channelCode):
        threading.Thread.__init__(self)
        self.channelCode = channelCode

    def run(self):
        print ("开始信号模板采集：通道" + self.channelCode)
        if (self.channelCode =='0-0'):
            path_0 = GetNormalSignalTemplate.get_normal_feature_template(tmplateSize_0,template_workCondition_0,self.channelCode)
            MonitorSignal.monitor_signal_feature(template_workCondition_0,self.channelCode,path_0)
        if (self.channelCode =='0-1'):
            path_1 = GetNormalSignalTemplate.GetNormalNondimentionalTimeDomainSignalTemplate(tmplateSize_1,template_workCondition_1,self.channelCode)  
            MonitorSignal.MonitorNondimensuinalTimeDomainSignal(template_workCondition_1,self.channelCode,path_1)
        if (self.channelCode =='0-2'):
            path_2 = GetNormalSignalTemplate.GetNormalFrequencyDomainSignalTemplate(tmplateSize_2,template_workCondition_2,self.channelCode)
            MonitorSignal.MonitorFrequentDomainSignal(template_workCondition_2,self.channelCode,path_2)
        if (self.channelCode =='0-3'):
            path_3 = GetNormalSignalTemplate.GetNormalNondimensionalFrequencyDomainSignalTemplate(tmplateSize_3,template_workCondition_3,self.channelCode)
            MonitorSignal.MonitorNondimentionalFrequencyDomainSignal(template_workCondition_3,self.channelCode,path_3)

if __name__ == '__main__':
    thread_0 = myThread(channelCode= '0-0')
    # thread_1 = myThread("0-1")
    # thread_2 = myThread("0-2")
    # thread_3 = myThread("0-3")

    thread_0.start()
    # thread_1.start()
    # thread_2.start()
    # thread_3.start()
    thread_0.join()
    # thread_1.join()
    # thread_2.join()
    # thread_3.join()
    MonitorSignal.monitor_frequencyDomain()