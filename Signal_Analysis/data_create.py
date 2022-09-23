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
from scipy.io import loadmat,savemat
from PIL import Image


r = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)

dataList = []
#原数据
def readfile(filename):    
    dataNum = 0
    max = 0
    with open(filename,"r") as f:
        for line in f.readlines():
            linestr = line.strip('\n')
            dataList.append(float(linestr))
            dataNum += 1
            if linestr >= str(max):
                max = linestr
            # if dataNum >=1024 :
            #     break
    return dataList, dataNum, max
signal,all_lenght,m=readfile("0A6E63CD-7AA4-4520-8108-F4D36A1D5711-0-1.txt")


#######################创建文件夹#############################################
for i in range (4):
    random_start = 0
    for j in range (10):
        # random_start = np.random.randint(low=0, high=(all_lenght - 2 * 20000))
        dataListcos = signal[random_start:random_start + 20000]
        random_start+=20000
        if len(dataListcos) != 20000:
            print("点数不足20000，break")
            break
        jsondata = {"5300rpm-320kw-1229":dataListcos}
        json_str = json.dumps(jsondata)
        channelCode = 'redisCollectionData-0-' + str(i)
        r.lpush(channelCode,json_str)

