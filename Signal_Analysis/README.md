**1.Monitor类**

1. 需要使用init这个类初始化第几个channel和workCondition，为了多线程做准备
2. redis的brpop命令在多线程情况下，出现数据给不足的情况,