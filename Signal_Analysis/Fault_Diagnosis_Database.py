import redis
import numpy as np
import json
from scipy.fftpack import fft
from  scipy.signal import stft
import matplotlib.pyplot as plt
import os
import util
import math
'''
1.新建一个文件夹“fault_diagosis_datasets”
2.里面两个文件夹fault_dataset_source和fault_dataset_output
3.把数据集都放在fault_dataset_source
4.fault_dataset_output这里是生成的STFT图片,有一些文件夹需要手动创建,看报错缺文件夹自己就建一个。

'''
class Fault_Diagnosis_Database:
    def __init__(self):
        self.source_path = 'C:\\wangzexin\\Graduation\\fault_diagosis_datasets\\fault_dataset_source'
        self.output_path = 'C:\\wangzexin\\Graduation\\fault_diagosis_datasets\\fault_dataset_output'
        self.data_length = 20000#数据长度暂定
        self.dataset_name = 'Dongan'
        self.output_domain = 'TimeFrequent'
        self.sample_num = 100
    
    def create_dongan_datasets(self):
        '''
        处理东安数据集
        '''
        dataset_name = 'Dongan'
        fault_name = 'normal' #故障文件名
        workcondition = '0hp-70%rpm'
        s_path = self.source_path + '\\'+dataset_name+'\\'+fault_name+'\\'+workcondition
        o_path = self.output_path + '\\'+dataset_name+'\\'+fault_name+'\\'+workcondition
        if not os.path.exists(o_path):
            os.mkdir(o_path)
        for root,dirs,files in os.walk(s_path):
            for file in files:
                if(file.split('.',1)[1]=='txt'):
                    p_input = os.path.join(s_path,file)
                    p_output = os.path.join(o_path, file.split('.')[0])
                    if not os.path.exists(p_output):
                        os.mkdir(p_output)
                    slice_data,datanum,datamax = util.readfile(p_input)
                    os.chdir(p_output)
                    for i in range(self.sample_num):
                        random_start = np.random.randint(low=0, high=(datanum - 2 * self.data_length))
                        dataListcos = slice_data[random_start:random_start + self.data_length]
                        data_stft = util.GetFrequencyFeature4(dataListcos, self.data_length/2)
                        plt.imsave('fft{}.jpg'.format(i),data_stft)
                    print('done!')
    
    def create_cwru_datasets(self):
        '''
        处理CWRU数据集
        '''
        dataset_name = 'CWRU'
        load_name = '0HP' #负载名
        s_path = self.source_path + "\\"+ dataset_name + "\\" + load_name
        o_path = self.output_path+ "\\" + dataset_name + "\\" + load_name
        if not os.path.exists(o_path):
            os.mkdir(o_path)
        data_dict = util.capture(s_path)
        data_keys = data_dict.keys()
        for i in data_keys:
            fault_condition,ext = os.path.splitext(i)
            slice_data = data_dict[i]
            all_lenght = len(slice_data)
            p_output = os.path.join(o_path,fault_condition)
            if not os.path.exists(p_output):
                os.makedirs(p_output)
            os.chdir(p_output)
            for i in range(self.sample_num):
                random_start = np.random.randint(low=0, high=(all_lenght - 2 * self.data_length))
                dataListcos = slice_data[random_start:random_start + self.data_length]
                data_stft = util.GetFrequencyFeature4(dataListcos, self.data_length/2)
                plt.imsave('fft{}.jpg'.format(i),data_stft)
            print("done!")

    def create_Ottawa_datasets(self):
        '''
        处理渥太华数据集
        '''
        dataset_name = 'Ottawa'
        fault_condition = 'Health_Accelerate'
        s_path = self.source_path + "\\"+ dataset_name + "\\" + fault_condition
        o_path = self.output_path+ "\\" + dataset_name + "\\" + fault_condition
        if not os.path.exists(o_path):
            os.mkdir(o_path)
        data_dict_channel1, data_dict_channel2= util.capture_Ottawa(s_path)
        data_keys = data_dict_channel1.keys()
        for i in data_keys:
            work_condition,ext = os.path.splitext(i)
            slice_data_channel1 = data_dict_channel1[i]
            slice_data_channel2 = data_dict_channel2[i]
            all_lenght_channel1 = len(slice_data_channel1)
            all_lenght_channel2 = len(slice_data_channel2)
            p_output = os.path.join(o_path,work_condition)
            if not os.path.exists(p_output):
                os.makedirs(p_output)
            os.chdir(p_output)
            p_channel1 = os.path.join(p_output,'channel1')
            if not os.path.exists(p_channel1):
                os.makedirs(p_channel1)
            p_channel2 = os.path.join(p_output,'channel2')
            if not os.path.exists(p_channel2):
                os.makedirs(p_channel2)
            os.chdir(p_channel1)
            for i in range(self.sample_num):
                random_start = np.random.randint(low=0, high=(all_lenght_channel1 - 2 * self.data_length))
                dataListcos = slice_data_channel1[random_start:random_start + self.data_length]
                data_stft = util.GetFrequencyFeature4(dataListcos, self.data_length/2)
                plt.imsave('fft{}.jpg'.format(i),data_stft)
            os.chdir(p_channel2)
            for i in range(self.sample_num):
                random_start = np.random.randint(low=0, high=(all_lenght_channel2 - 2 * self.data_length))
                dataListcos = slice_data_channel2[random_start:random_start + self.data_length]
                data_stft = util.GetFrequencyFeature4(dataListcos, self.data_length/2)
                plt.imsave('fft{}.jpg'.format(i),data_stft)
            print("done!")

    def create_XJTU_datasets(self):
        '''
        处理西安交大变速数据集
        '''
        dataset_name = 'XJTU_VS'
        fault_condition = 'IF_1'
        s_path = self.source_path + "\\"+ dataset_name + "\\" + fault_condition
        o_path = self.output_path+ "\\" + dataset_name + "\\" + fault_condition
        if not os.path.exists(o_path):
            os.mkdir(o_path)
        for root,dirs,files in os.walk(s_path):
            for file in files:
                work_condition,ext = os.path.splitext(file)
                p_input = os.path.join(s_path,file)
                slice_data,datanum = util.readfile_XJTU(p_input)
                if(datanum>=self.data_length*2):
                    p_output = os.path.join(o_path,work_condition)
                    if not os.path.exists(p_output):
                        os.mkdir(p_output)
                    os.chdir(p_output)
                    for i in range(self.sample_num):
                        random_start = np.random.randint(low=0, high=(datanum - self.data_length))
                        dataListcos = slice_data[random_start:random_start + self.data_length]
                        data_stft = util.GetFrequencyFeature4(dataListcos, self.data_length/2)
                        plt.imsave('fft{}.jpg'.format(i),data_stft)
                print('done!')

if __name__ == '__main__':
    database1 = Fault_Diagnosis_Database()
    # database1.create_dongan_datasets()
    # database1.create_cwru_datasets()
    # database1.create_Ottawa_datasets()
    database1.create_XJTU_datasets()





