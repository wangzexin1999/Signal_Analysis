# BUG日志
**1.Monitor类**
**多线程保存图像有问题**
1. 需要使用init这个类初始化第几个channel和workCondition，为了多线程做准备
2. redis的brpop命令在多线程情况下，出现数据给不足的情况,
3. bug已经解决，bug由redis某些祯数据不足20000长度引起，不是多线程问题