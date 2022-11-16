#取txt文件 的若干行到另一个txt
f1 = open(r'C:/Users/xinnnn/Desktop/qttest/datasetForQT/captureDataSet/normal-3.txt','rb')
f2= open(r'C:/Users/xinnnn/Desktop/qttest/datasetForQT/captureDataSet/normalBangNormal-3.txt','ab')

i=0
while True:
    line = f1.readline()
    i+=1
    if i<=60000:
        f2.write(line)
    if i>60000:
        break