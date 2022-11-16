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
import ast

r = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)

channelCode = "0"

count = 0
while True:
    every_data_all = json.loads(r.blpop("redisCollectionData-0")[1])
    data_workCondition = list(every_data_all.keys())[0]#工况信息
    every_data = every_data_all[data_workCondition]
    print(len(every_data))
    count+=1
    print(count)

