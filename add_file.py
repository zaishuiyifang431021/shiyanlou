#! /usr/bin/env python3
import os

def createfile(filename,txt):
    print("creatfile start ..filename :{}".format(filename))
    if os.path.exists(filename): 
        print("file is exists ...")
    elif ".py" not in filename:
        print("cuanjian wenjian jia ...{}".format(filename))
        os.makedirs(filename)
    else:# os.path.isfile(filename):
        print("chuanjian wenjian ...{}".format(filename))
        with open(filename,"w") as myfile:
            myfile.write(txt)
    #else:
     #   print("sm louji dou meiyou zuo ")

if __name__ == "__main__":
    print("start....")
    createfile("/home/shiyanlou/syl","")
    createfile("/home/shiyanlou/syl/A","")
    createfile("/home/shiyanlou/syl/B","")
    createfile("/home/shiyanlou/syl/C","")
    createfile("/home/shiyanlou/syl/__init__.py","")
    createfile("/home/shiyanlou/syl/A/__init__.py","")
    createfile("/home/shiyanlou/syl/B/__init__.py","")
    createfile("/home/shiyanlou/syl/C/__init__.py","")
    print("end...")





