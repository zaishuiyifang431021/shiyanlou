#! /usr/bin/env python3
import sys
import datetime
import csv
import getopt
from configparser import ConfigParser
from multiprocessing import Process
from multiprocessing import Pipe


f1 = ""
f2 = ""
f3 = ""
conn1 , conn2 = Pipe()
conn3 , conn4 = Pipe()
conn5 , conn6 = Pipe()
conn7 , conn8 = Pipe()
process = Process()


dict1 = {}  # test.cfg
dict2 = {}  # user.csv

gh = 0
sqgz = 0
sbje = 0
gsje = 0
shgz = 0
gz = 0

# read config file to dict
def read_init():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "C:c:d:o:",["help","C=","c="])
        city = ""
        for opt, arg in opts:
            print(":::::!!!!opt?{}?arg: {}".format(opt,arg))
            if "-C" == opt:
                print ("-C ???????{} ".format(arg))
                city = arg

            elif "-c" == opt:
                print("-c ???????{} ".format(arg))
                config = ConfigParser()
                config.read(arg, encoding='UTF-8')
                list1 = config.items(city)
                for ii in list1 :
                    dict1[ii[0].strip()] = ii[1].strip()
                print("?????????? dict1: {}".format(dict1))
            elif '-d' == opt:
                print("-d ???????{} ".format(arg))
                with open(arg) as myfile:
                    data1 = list(csv.reader(myfile))
                       # print(data1)
                    for d in data1:
                        dict2[d[0].strip()] = d[1].strip()
                print("user.csv ?? dict2 : {}".format(dict2))
            elif '-o' == opt:
                print("-o ???????{} ".format(arg))
                conn7.send(arg)
        conn1.send(dict1)
        conn3.send(dict2)
    except getopt.GetoptError as e:
        print("????????????? calculator.py -C cityname -c configfile -d userdata -o resultdata")
        print(e)


def sbjejs(gz,dict1):

    sbjs = 0
    JiShuL = float(dict1["JiShuL".lower()])
    JiShuH = float(dict1["JiShuH".lower()])
    YangLao = float(dict1["YangLao".lower()])
    YiLiao = float(dict1["YiLiao".lower()])
    ShiYe = float(dict1["ShiYe".lower()])
    GongShang = float(dict1["GongShang".lower()])
    ShengYu = float(dict1["ShengYu".lower()])
    GongJiJin = float(dict1["GongJiJin".lower()])
    gz = float(gz)

    # print(dict1)
    if gz <= JiShuL:
        sbjs = JiShuL
    elif JiShuL < gz <= JiShuH:
        sbjs = gz
    elif gz > JiShuH:
        sbjs = JiShuH
    # print("sbjs ? {}".format(sbjs))
    sbje = sbjs * (YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin)
    print("sbjejs()....sbje: {}".format(sbje))
    return  sbje


def gsjejs(gz, sbje):
    yjssde = 0
    # ns = 0
    sl = 0
    sskcs = 0
    wxyj = 0.165
    print("gsjejs()&&**&& sbje:{}".format(sbje))
    try:
        gz = float(gz)
    except Exception as e:
        print("Parameter Error")
        print(e)
    yjssde = gz - float(sbje) - 5000
    if yjssde < 0:
        yjssde = 0
        sl = 0.00
        sskcs = 0
    elif 0 < yjssde <= 3000:
        sl = 0.03
        sskcs = 0
    elif 3000 < yjssde <= 12000:
        sl = 0.1
        sskcs = 210
    elif 12000 < yjssde <= 25000:
        sl = 0.2
        sskcs = 1410
    elif 25000 < yjssde <= 35000:
        sl = 0.25
        sskcs = 2660
    elif 35000 < yjssde <= 55000:
        sl = 0.3
        sskcs = 4410
    elif 5500 < yjssde <= 80000:
        sl = 0.35
        sskcs = 7160
    elif 80000 < yjssde:
        sl = 0.45
        sskcs = 15160

    gsje = yjssde * sl - sskcs
    if gsje < 0:
        gsje = 0
    # print("{:.2f}".format(gsje))
    print("geshui jin e wei :{}".format(gsje))
    return  gsje


def jszhgz():
    data = []
    dict2 = conn4.recv()
    dict1 = conn2.recv()
    print("dict1: {}, dict2: {}".format(dict1,dict2))
    # dict2 = {'101': '5000.00', '203': '6500.00', '309': '15000.00'}
    for mr in dict2.items():


        sbje = sbjejs(mr[1],dict1)

        # 2???????
        gsje = gsjejs(mr[1], sbje)

        # 3) ????
        shgz = float(mr[1]) - sbje - gsje


        str1 = "{},{:.2f},{:.2f},{:.2f},{:.2f},{}".format(mr[0], float(mr[1]), sbje, gsje, shgz,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data.append(str1)
    print("data?{}".format(data))
    conn5.send(data)

#???????????
# ??, ????, ????, ????, ????
# def write_file(self,filename,gh,sqgz,sbje,gsje,shgz):
def write_file():
    # filename = conn8.recv()
    data = conn6.recv()
    filename = conn8.recv()

    with open(filename,"w",newline='') as myfile:
        for ii in data:
            myfile.write(ii+"\n")


if __name__ == "__main__":
    #read_init()
    #jszhgz()
    #write_file()
    p1 = Process(target=read_init)
    p1.start()
    p2 = Process(target=jszhgz)
    p2.start()
    p3 = Process(target=write_file)
    p3.start()

