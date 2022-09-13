import redis
import numpy as np
import json
from scipy.fftpack import fft
class Monitor:
    def __init__(self):
        # 配置redis
        self.redisHost = "localhost"
        self.redisPort = 6379
        self.redisDB = 0
        self.redisConn = redis.StrictRedis(host=self.redisHost,
                                           port=self.redisPort,
                                           db=self.redisDB,
                                           decode_responses=True)
        self.blockingReadTimeout = 1
        self.channels = ['redisCollectionData-0-' + str(index) for index in range(4)]
        self.key = '5300rpm-320kw-1229'

        self.dataLen = 20000  # 采样长度
        self.sampleLate = 20000 #采样率
        self.fequeny = self.sampleLate * np.array(range(int(self.dataLen/2)))/self.dataLen
        self.allIndex = 4
    # index 为通道
    def loadTimeDomainFromRedis(self, index: int):
        """
        index为第几个通道，从0开始。该函数自动向redis的list阻塞型队尾取数据
        """
        data = self.redisConn.brpop(self.channels[index],self.blockingReadTimeout)

        if data is None:
            return None

        jsonData = json.loads(data[1])  # 从非空队列尾部弹出数据，是RPOP的阻塞版，没有数据会等待
        timeSignal = jsonData[self.key]

        return timeSignal
    def timeDomain2FrequencyDomain(self,signal:np.ndarray):
        N = len(signal)
        N_2 = int(N/2)
        fre = np.abs(fft(signal))/N*2
        fre[0] = 0.5 * fre[0]
        return fre[0:N_2]


    def monitorFrequencyDomain(self):
        signals = []
        for index in range(10):
            signal = self.loadTimeDomainFromRedis(0)
            if signal is not None and len(signal) == 20000 :
                signals.append(signal)
            else:
                print("数据不足10祯，或者某一祯不足20000个点")
                return
        amp = [self.timeDomain2FrequencyDomain(index) for index in signals]
        amp_mean = np.mean(amp, 0)
        while True:
            val = np.sum((amp - amp_mean.reshape((1, 10000))) ** 2, axis=0) / len(signals)
            maxval = np.max(val)
            maxIndex = np.where(val == maxval) #寻找最大值下标
            if maxval >=0.01:
                print("方差大于0.01，方差为{0},，频谱为{1}".format(maxval,maxIndex))
            currentSignal = self.loadTimeDomainFromRedis(0)

            if currentSignal == None or len(currentSignal) != 20000:
                break
            currentAmp = self.timeDomain2FrequencyDomain(currentSignal)
            # 有一定可能性造成误差
            amp_mean -= amp[0]/len(amp)
            amp_mean += currentAmp/len(amp)
            del amp[0]
            amp.append(currentAmp)
        print("数据分析完毕,redis为空")

