#! /usr/bin/env python3
import os
import json
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def index():
    path = "/home/shiyanlou/files"
    content = ""
    for s in os.listdir(path):
        newDir=os.path.join(path,s)
        with open(newDir,"r") as myfile:
            dict1 = json.load(myfile)
            content += dict1["title"]+"\n"
            print(dict1["title"])
    return content

@app.route("/files/<filename>")
def files(filename):
    path = "/home/shiyanlou/files/"
    content = ""
    dict1 = {}
    if filename == "helloworld" or filename == "helloshiyanlou":
        print("I am here ...")
        with open(path+filename+".json") as myfile:
            dict1 = json.load(myfile)
            for k1,v in dict1.items():
                content += k1 +" : " + v 
        return content
    else:
        return render_template("404.html")







if __name__ == "__main__":
    index()
