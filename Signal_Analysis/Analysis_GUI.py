# coding = utf-8
########################################################################################
#########pyqt界面
###################################################################################
import re
import sys
 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from pip import main
import redis
import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from scipy.fftpack import fft,ifft, hilbert
# from pyts.approximation import PiecewiseAggregateApproximation
import threading
from scipy.io import loadmat,savemat
import time
 
from PyQt5.QtCore import QObject,QRect,QTimer
strList = []
strList01 = []
strList02 = []
strList03 = []
strList04 = []

r = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)

def predictResultPop():
    result = r.rpop("predictResult-0-0")
    return result


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 30, 200, 500))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.InitButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.InitButton.setMinimumSize(QtCore.QSize(0, 48))
        self.InitButton.setObjectName("InitButton")
        self.horizontalLayout.addWidget(self.InitButton)
        self.StartButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.StartButton.setMinimumSize(QtCore.QSize(0, 48))
        self.StartButton.setObjectName("StartButton")
        self.horizontalLayout.addWidget(self.StartButton)
        self.StopButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.StopButton.setMinimumSize(QtCore.QSize(0, 48))
        self.StopButton.setObjectName("StopButton")
        self.horizontalLayout.addWidget(self.StopButton)
        self.InitDiagnosisButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.InitDiagnosisButton.setMinimumSize(QtCore.QSize(0, 48))
        self.InitDiagnosisButton.setObjectName("InitDiagnosisButton")
        self.horizontalLayout.addWidget(self.InitDiagnosisButton)
        self.StartDiagnosisButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.StartDiagnosisButton.setMinimumSize(QtCore.QSize(0, 48))
        self.StartDiagnosisButton.setObjectName("StartDiagnosisButton")
        self.horizontalLayout.addWidget(self.StartDiagnosisButton)
        self.StopDiagnosisButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.StopDiagnosisButton.setMinimumSize(QtCore.QSize(0, 48))
        self.StopDiagnosisButton.setObjectName("StopDiagnosisButton")
        self.horizontalLayout.addWidget(self.StopDiagnosisButton)





        # self.horizontalLayoutWidget_1 = QtWidgets.QWidget(self.centralwidget)
        # self.horizontalLayoutWidget_1.setGeometry(QtCore.QRect(150, 40, 400, 180))
        # self.horizontalLayoutWidget_1.setObjectName("horizontalLayoutWidget")
        # self.horizontalLayout_1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_1)
        # self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        # self.TemplateButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_1)
        # self.TemplateButton.setMinimumSize(QtCore.QSize(0, 48))
        # self.TemplateButton.setObjectName("TemplateButton")
        # self.horizontalLayout_1.addWidget(self.TemplateButton)
        




        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(300, 80, 800, 400))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_2.addWidget(self.plainTextEdit)
        self.plainTextEdit2 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit2.setObjectName("plainTextEdit2")
        self.horizontalLayout_2.addWidget(self.plainTextEdit2)
        self.plainTextEdit3 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit2.setObjectName("plainTextEdit3")
        self.horizontalLayout_2.addWidget(self.plainTextEdit3)
        self.plainTextEdit4 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit4.setObjectName("plainTextEdit4")
        self.horizontalLayout_2.addWidget(self.plainTextEdit4)
        self.plainTextEdit5 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit5.setObjectName("plainTextEdit5")
        self.horizontalLayout_2.addWidget(self.plainTextEdit5)
        MainWindow.setCentralWidget(self.centralwidget)
 
        self.retranslateUi(MainWindow)
        self.InitButton.clicked.connect(self.InitConnect)
        self.StopButton.clicked.connect(self.StopAnalysis)
        self.StartButton.clicked.connect(self.star)#self.onPresse
        self.InitDiagnosisButton.clicked.connect(self.DiagnosisInit)
        self.StartDiagnosisButton.clicked.connect(self.BeginDiagnosis)
        self.StopDiagnosisButton.clicked.connect(self.ShutDownDiagnosis)
        # self.TemplateButton.clicked.connect(self.template)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #实例化定时器 写在主窗口里面
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.a)

        self.timerDiagnosis = QTimer(MainWindow)
        self.timerDiagnosis.timeout.connect(self.b)
        r.set("DiagnosisStatus",0)


    def a(self):
        if(len(strList)==0 or len(strList01)==0 or len(strList02)==0 or len(strList03)==0):
            return
        else:
            gotStr0 = strList.pop(0)
            gotStr1 = strList01.pop(0)
            gotStr2 = strList02.pop(0)
            gotStr3 = strList03.pop(0)
            self.plainTextEdit.appendPlainText(gotStr0)
            self.plainTextEdit2.appendPlainText(gotStr1)
            self.plainTextEdit3.appendPlainText(gotStr2)
            self.plainTextEdit4.appendPlainText(gotStr3)

    def b(self):
        if(len(strList04)==0):
            return
        else:
            gotStr4 = strList04.pop(0)
            self.plainTextEdit5.appendPlainText(gotStr4)

    def star(self):
    	#把定时器写在主窗口里面 之前再次调用是因为写在了按钮事件里面
    	#这样就不会出现再打开一个定时器 而是一直循环调用这个定时器
    	#执行另外一个函数或者按钮链接两个槽一个启动这个定时器
    	#一个用来执行请求参数 每次刷新就重新获取请求返回的参数(这个是不固定的)所以每次都要调用一下
        #写在主窗口也可以 再次start是重新启动
        #注意这里是start不是startTimer
        self.timer.start(1000)

 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "振动信号检测程序"))
        self.StartButton.setText(_translate("MainWindow", "开始故障监测"))
        self.StopButton.setText(_translate("MainWindow", "停止故障监测"))
        self.InitButton.setText(_translate("MainWindow", "监测初始化连接"))
        self.InitDiagnosisButton.setText(_translate("MainWindow","诊断初始化连接"))
        self.StartDiagnosisButton.setText(_translate("MainWindow", "开始故障诊断"))
        self.StopDiagnosisButton.setText(_translate("MainWindow", "停止故障诊断"))
        # self.TemplateButton.setText(_translate("MainWindow","模板数据采集"))
        # self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        # self.pushButton.setText(_translate("MainWindow", "PushButton"))
 
    def InitConnect(self,checked): #初始化连接
        # self.plainTextEdit.appendPlainText(
        #     '按钮被释放')
        
        # str = '1111111111111111111'
        # self.SetEdit(str)

        # gotStr = strList.pop(0)

        # self.SetSampleStatus(True)

        self.plainTextEdit.clear()
        self.plainTextEdit2.clear()
        self.plainTextEdit3.clear()
        self.plainTextEdit4.clear()

        strList.clear()
        strList01.clear()
        strList02.clear()
        strList03.clear()
        
        self.thread_0 = myThread(channelCode= '0-0' , workCondition= "3000rpm-560kw-0103")
        self.thread_0.SetSampleStatus(True)
        self.thread_1 = myThread(channelCode= '0-1' , workCondition= "3000rpm-560kw-0103")
        self.thread_1.SetSampleStatus(True)
        self.thread_2 = myThread(channelCode= '0-2' , workCondition= "3000rpm-560kw-0103")
        self.thread_2.SetSampleStatus(True)
        self.thread_3 = myThread(channelCode= '0-3' , workCondition= "3000rpm-560kw-0103")
        self.thread_3.SetSampleStatus(True)


        # thread_1 = myThread("0-1")
        # thread_2 = myThread("0-2")
        # thread_3 = myThread("0-3")

        self.thread_0.start()
        self.thread_1.start()
        self.thread_2.start()
        self.thread_3.start()
        # self.thread_0.join()
        # thread_1.join()
        # thread_2.join()
        # thread_3.join()
 
    def StopAnalysis(self, checked):
        # threading.Thread._Thread__stop(self.thread_0)
        self.thread_0.SetSampleStatus(False)
        self.thread_1.SetSampleStatus(False)
        self.thread_2.SetSampleStatus(False)
        self.thread_3.SetSampleStatus(False)
        self.timer.stop()
    
    def Template(self,checked):
        pass
        
    def DiagnosisInit(self,checked):
        r.set("DiagnosisStatus",1)
        self.plainTextEdit5.clear()
        strList04.clear()
        self.thread_4 = diagnosisThread(channelCode= '0-0' , workCondition= "3000rpm-560kw-0103")
        self.thread_4.setDiagnosisStatus(True)
        self.thread_4.start()

    def BeginDiagnosis(self,checked):
        
        self.timerDiagnosis.start(1000)

    
    def ShutDownDiagnosis(self,checked):
         r.set("DiagnosisStatus",0)
         self.thread_4.setDiagnosisStatus(False)
         self.timerDiagnosis.stop()

    def SetEdit(self,str):
        self.plainTextEdit.appendPlainText(str)
        

#rpm转速 kw功率 
class SpectrumBuilder():
    def __init__(self,ChannelCode,workCondition):
        self.ChannelCode = ChannelCode
        self.workCondition = workCondition
        self.m_ui = Ui_MainWindow()
    # def predictPop(self):
    #     r.rpop("predicResult-0-0")

    def SetStatus(self,status):
        self.m_status = status

    def SetDiagnosisStatus(self,diagnosisStatus):
        self.m_diagnosisStatus = diagnosisStatus

    def WriteEveryData(self,every_data):
        json_data = {"CollectionData":every_data}
        json_str = json.dumps(json_data)
        return json_str
    
    def get_puxian(self,single_data):
        puxian = {}
        for i in range(len(single_data)):
            if single_data[i] > 25:
                x_point = "x_axis: " + str(i)
                puxian[x_point] = float(single_data[i])
        return puxian   

    #获取最大的三个谱线
    def FindMax3Puxian(self,ls): # 快速获取list中最大的三个元素
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

    #计算总值
    def TotalValue(self,single_data):
        totalsum = 0
        for i in range(len(single_data)):
            totalsum += single_data[i]
        return totalsum

    def timeToFFT(self,single_data):
        dataLength = len(single_data)
        a = np.tile(single_data,2)
        fft_y=fft(a) 
        fft_y[0] = 0
        fft_y = np.resize(fft_y,dataLength)
        x = np.linspace(0, dataLength, dataLength,endpoint=True)
        fft_array = fft_y.reshape(-1)
        fftTransformdata = abs(fft_array).tolist()
        return fftTransformdata

    def which_channel(self,channelCode):
        if(channelCode == '0-0'):
            return strList
        elif(channelCode == '0-1'):
            return strList01
        elif(channelCode == '0-2'):
            return strList02
        elif(channelCode == '0-3'):
            return strList03

    #######################获取幅值#############################################
    #############################################################################
    def get_amplitude(self,single_data):
        amplitude = {}
        for i in range(len(single_data)):
            x_point = "x_axis: " + str(i)
            amplitude[x_point] = float(single_data[i])
        return amplitude
        
    def Normalization(self,fftdata):
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

    def get_plot(self,fft_data,path):
        plt.plot(fft_data)
        plt.savefig(path)

    #######################创建文件夹#############################################
    #############################################################################
    def make_dir(self,domain,work_condition,channelCode):
        source_path = "C:/wangzexin/Graduation/Signal_Analysis/pinpu_json"
        if os.path.exists(source_path+'/'+domain+'/'+work_condition+'/'+channelCode):
            isExist = True
            # print(work_condition+'文件夹已存在')
            print("开始分析")
            # self.m_ui.SetEdit("开始分析")
        else:
            os.makedirs(source_path+'/'+domain+'/'+ work_condition+'/'+channelCode)
            isExist = False
        return isExist

    #######################读取频域信息json#######################################
    #############################################################################
    def get_FrequentDomain_Template_data(self,path):
        template_mean = []
        template_var = []
        template_std = []
        template_rms = []
        template_fengfengzhi = []
        template_totalvalue = []
        firstMax = []
        secondMax = []
        thirdMax = []
        for root , dirs , files  in os.walk(path):
            for json_file in files:
                json_path = path + '/' + json_file
                with open(json_path) as fr:
                    json_data = json.load(fr)
                    # template_mean.append(json_data['mean'])
                    # template_var.append(json_data['var'])
                    # template_std.append(json_data['std'])
                    # template_rms.append(json_data['rms'])
                    # template_fengfengzhi.append(json_data['fengfengzhi'])
                    template_totalvalue.append(json_data['totalvalue'])
                    firstMax.append(json_data['FirstMax'])
                    secondMax.append(json_data['SecondMax'])
                    thirdMax.append(json_data['ThirdMax'])

        # template_stat_mean = np.array(template_mean).mean()
        # template_stat_var = np.array(template_var).mean()
        # template_stat_std = np.array(template_std).mean()
        # template_stat_rms = np.array(template_rms).mean()
        # template_stat_fengfengzhi = np.array(template_fengfengzhi).mean()

        max_firstmax = np.array(firstMax).max()
        max_secondmax = np.array(secondMax).max()
        max_thirdmax = np.array(thirdMax).max()
        max_totalvalue = np.array(template_totalvalue).max()

        return max_firstmax,max_secondmax,max_thirdmax,max_totalvalue

        #######################获取频域信息模板#######################################
        #############################################################################
    def GetNormalFrequentDomainSignalTemplate(self , TemplateSize , Work_Condition):
        self.TemplateSize = TemplateSize
        template_mean = []
        template_var = []
        template_std = []
        template_rms = []
        template_fengfengzhi = []
        isExist = self.make_dir('Frequent_Domain',Work_Condition , self.ChannelCode)
        if(isExist == False):
            r = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)
            for i in range(TemplateSize):
                # every_data = json.loads(r.brpop("redisCollectionData-"+ self.ChannelCode)[1])['redisCollectionData']
                every_data_all = json.loads(r.brpop("redisCollectionData-"+ self.ChannelCode)[1])
                data_workCondition = list(every_data_all.keys())[0]#工况信息
                print("当前记录的模板数据为---频域---工况：{}---通道：{}".format(Work_Condition,self.ChannelCode))
                # self.m_ui.plainTextEdit.appendPlainText("当前记录的模板数据为---时域---工况：{}---通道：{}".format(Work_Condition,self.ChannelCode))
                every_data = every_data_all[data_workCondition]
                every_data = self.timeToFFT(every_data)
                firstData,secondData,thirdData,firIndex,secIndex,thiIndex = self.FindMax3Puxian(every_data)
                everyPuXianDict = self.get_amplitude(every_data)
                amplitudeList = []
                for puxian in everyPuXianDict.items():
                    amplitudeList.append(puxian[1])
                amplitudeList = np.array(amplitudeList)
                amplitude_mean = amplitudeList.mean()
                amplitude_var = amplitudeList.var()#方差
                amplitude_std = amplitudeList.std()#标准差
                amplitude_rms = np.sqrt(pow(amplitude_mean, 2) + pow(amplitude_std, 2))#均方根
                amplitude_fengfengzhi = max(amplitudeList) - min(amplitudeList)
                amplitude_totalValue = self.TotalValue(every_data)
                pinpuStatisticDict = {}
                pinpuStatisticDict['FirstMax'] = firstData
                pinpuStatisticDict['FirstMaxIndex'] = firIndex
                pinpuStatisticDict['SecondMax'] = secondData
                pinpuStatisticDict['SecondMaxIndex'] = secIndex
                pinpuStatisticDict['ThirdMax'] = thirdData
                pinpuStatisticDict['ThirdMaxIndex'] = thiIndex
                
                pinpuStatisticDict['mean'] = amplitude_mean
                pinpuStatisticDict['var'] = amplitude_var
                pinpuStatisticDict['std'] = amplitude_std
                pinpuStatisticDict['rms'] = amplitude_rms
                pinpuStatisticDict['totalvalue'] = amplitude_totalValue

                template_mean.append(amplitude_mean)
                template_var.append(amplitude_var)
                template_std.append(amplitude_std)
                template_rms.append(amplitude_rms)
                template_fengfengzhi.append(amplitude_fengfengzhi)
                with open("C:/wangzexin/Graduation/Signal_Analysis/pinpu_json/Frequent_Domain/{}/{}/Channel-{}_WorkCondition-{}_TemplateNum-{}.json".format(Work_Condition,self.ChannelCode,self.ChannelCode,Work_Condition,str(i)),"w") as f:
                    json.dump(pinpuStatisticDict,f)
                    f.close()
                print("已记录的模板样本量: {}".format(i+1))
                # self.m_ui.plainTextEdit.appendPlainText("已记录的模板样本量: {}".format(i+1))
            
                # plt.plot(time_data)
                # plt.savefig("/home/wangzexin/Graduation/wdcnn_project/pinpu/{}pinpu--time--{}.png".format(self.ChannelCode,str(i)))

            print("模板样本记录完成，共{}组样本".format(TemplateSize))
            # self.m_ui.plainTextEdit.appendPlainText("模板样本记录完成，共{}组样本".format(TemplateSize))

        # mean_mean = np.array(template_mean).mean()
        # var_mean = np.array(template_var).mean()
        # std_mean = np.array(template_std).mean()
        # rms_mean = np.array(template_rms).mean()
        # fengfengzhi_mean = np.array(template_fengfengzhi).mean()

        # self.tem_mean = mean_mean
        # self.tem_var = var_mean
        # self.tem_std = std_mean
        # self.tem_rms = rms_mean
        # self.tem_fengfengzhi = fengfengzhi_mean

        # return mean_mean, var_mean, std_mean, rms_mean, fengfengzhi_mean


        #######################频域信号分析#######################################
        #############################################################################
    def MonitorFrequentDomainSignal(self , Work_Condition):
        r = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)
        path = "C:/wangzexin/Graduation/Signal_Analysis/pinpu_json/Frequent_Domain"+'/'+ Work_Condition + '/'+ self.ChannelCode
        max_firstmax,max_secondmax,max_thirdmax,max_totalvalue = self.get_FrequentDomain_Template_data(path)
        thisList = self.which_channel(self.ChannelCode)
        strFirst = "当前检测的数据为数据为-工况：{}-通道：{}".format(Work_Condition,self.ChannelCode)
        thisList.append(strFirst)
        signal_num = 0
        while(self.m_status):
            # every_data = json.loads(r.brpop("redisCollectionData-"+ self.ChannelCode)[1])['redisCollectionData']
            every_data_all = json.loads(r.brpop("redisCollectionData-"+ self.ChannelCode)[1])
            data_workCondition = list(every_data_all.keys())[0]#工况信息
            print("当前检测的数据为数据为-工况：{}-通道：{}".format(Work_Condition,self.ChannelCode))
            every_data = every_data_all[data_workCondition]
            every_data = self.timeToFFT(every_data)
            everyPuXianDict = self.get_amplitude(every_data)
            maxFirst,maxSecond,maxThird,maxFirstIndex,maxSecondIndex,maxThirdIndex = self.FindMax3Puxian(every_data)
            totalValue = self.TotalValue(every_data)
            amplitudeList = []
            for puxian in everyPuXianDict.items():
                amplitudeList.append(puxian[1])
            amplitudeList = np.array(amplitudeList)
            puxian_mean = amplitudeList.mean()
            puxian_var = amplitudeList.var()
            puxian_std = amplitudeList.std()
            puxian_rms = np.sqrt(pow(puxian_mean, 2) + pow(puxian_std, 2))
            puxian_fengfengzhi = max(amplitudeList) - min(amplitudeList)

            totalWeight = round((totalValue/max_totalvalue),2)
            firstMaxWeight = round((maxFirst/max_firstmax),2)
            secondMaxWeight = round((maxSecond/max_secondmax),2)
            thirdMaxWeight = round((max_thirdmax/max_thirdmax),2)
            # mean_difference = abs(puxian_mean - template_stat_mean)
            # var_difference = abs(puxian_var - template_stat_var)
            # std_difference = abs(puxian_std - template_stat_std)
            # rms_difference = abs(puxian_rms - template_stat_rms)
            # fengfengzhi_difference = abs(puxian_fengfengzhi - template_stat_fengfengzhi)

            # print(mean_difference,var_difference,std_difference,rms_difference,fengfengzhi_difference)
            # if (mean_difference > 40 or var_difference > 200 or  std_difference > 10 or rms_difference > 110 or fengfengzhi_difference > 0):
            #     print("第{}组数据分析完成,结果为异常".format(signal_num))
            #     strSecond = "第{}组数据分析完成,结果为异常".format(signal_num)
                
            # else:
            #     print("第{}组数据分析完成,结果为正常".format(signal_num))
            #     strSecond = "第{}组数据分析完成,结果为正常".format(signal_num)
            strSecond = "第{}组数据:峰值比重：{},总值比重: {}".format(signal_num+1,firstMaxWeight,totalWeight)
            thisList.append(strSecond)
            signal_num += 1
            time.sleep(1)
    
    def faultDiagnosis(self):
        strList04.append("开始故障诊断-工况：{}".format(self.workCondition))
        
        while(self.m_diagnosisStatus):
            result = predictResultPop()
            strList04.append("故障类型为{}".format(result))
            time.sleep(1)

#

     
class myThread (threading.Thread):
    def __init__(self, channelCode , workCondition):
        threading.Thread.__init__(self)
        self.channelCode = channelCode
        self.workCondition = workCondition
        self.puxianObject = SpectrumBuilder(ChannelCode=self.channelCode , workCondition= self.workCondition)
    def run(self):
        print ("开始信号模板采集：通道" + self.channelCode)
        self.puxianObject.GetNormalFrequentDomainSignalTemplate(TemplateSize=10 , Work_Condition=self.workCondition)
        self.puxianObject.MonitorFrequentDomainSignal(self.workCondition)
    
    def SetSampleStatus(self, bSample):
        self.puxianObject.SetStatus(bSample)
        self.m_bSample = bSample
    
    # def Getstr(self):
    #     gotStr = strList.pop(0)
    #     return gotStr


class diagnosisThread(threading.Thread):
    def __init__(self,channelCode , workCondition):
        threading.Thread.__init__(self)
        self.channelCode = channelCode
        self.workCondition = workCondition
        self.diagnosisObject = SpectrumBuilder(ChannelCode=self.channelCode , workCondition= self.workCondition)

    def run(self):
        self.diagnosisObject.faultDiagnosis()

    def setDiagnosisStatus(self,dSample):
        self.diagnosisObject.SetDiagnosisStatus(dSample)
        self.m_dSample = dSample



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

