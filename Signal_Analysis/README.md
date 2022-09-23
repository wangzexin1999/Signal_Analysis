**1.Monitor类**

1. 需要使用init这个类初始化第几个channel和workCondition，为了多线程做准备
2. redis的brpop命令在多线程情况下，出现数据给不足的情况,

**2.Analysis_GUI**

带有pyqt界面，定时器实时刷新结果。


**3.util文件**
工具文件，里面是一些工具函数


**4.data_create文件**
往redis里存入数据，正常流程是数据从前端采集进入redis，为了模拟这一过程，将数据从txt读入并存入redis里。

**5.GetNormalSignalTemplate**
获取信号模板，参数TemplateSize是获取多少帧信号做模板，将信号经过预处理，保存成
    1.时域统计值
    2.频域谱线幅值（10000个） //暂时谱线不用模板对比，采用计算方差，计算方差对比功能在Monitor类里
    3.时频域STFT图像         //时频域对比暂时不采用

**6.GetTemplateData**
读取从“GetNormalSignalTemplate.py”中获取的模板，模板只需要获取一次，对于已经获取的模板直接读取json文件就可以。

**7.MonitorSignal**
一帧一帧读取信号，并提取特征，与GetTemplateData.py所读取的模板信息做对比（目前只写了时域统计值对比的方式，频域采用谱线方差的方式，
时频域暂定）

