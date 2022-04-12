#!C:\Users\shaikj\AppData\Local\Programs\Python\Python310\python.exe

from cgitb import html
from enum import Flag
from math import fabs
import os, sys, json, pprint
import re

# disbale http request warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests

from json2html import *

def main():

    _url = "https://jsonmock.hackerrank.com/api/countries"

    if(len(sys.argv) == 2):
        country = sys.argv[1]
    else:
        country = "India"

    _params = {'name':country}

    r = requests.get(_url, _params , verify= False)

    data = r.json()
    data = data['data'][0]
    data['nativeName'] = ''
    data['translations']['ja'] = ""
    data['altSpellings'] = ['alt1', 'alt2' , 'alt3' , 'alt4 ']
    #print(data)

    htmlcode = "<table>"
    htmlcode += writeHtml(data)
    htmlcode += "</table>"
    print(htmlcode)

    print("<br><br><br>")
    print("<h2>Partial Retrieval</h2>")

    f = open('test.json')
    tdc_data = json.load(f)
    htmlcode = "<table>"
    htmlcode += writeHtml(tdc_data)
    htmlcode += "</table>"
    print(htmlcode)

    print("<br><br><br>")
    print("<h2>Full Retrieval</h2>")


    f = open('test_tdc_full.json')
    tdc_data = json.load(f)
    htmlcode = "<table>"
    htmlcode += writeHtml(tdc_data)
    htmlcode += "</table>"
    print(htmlcode)




def writeHtml(jsonData):
    html = ""
    for key,value in jsonData.items():
        #print(str(key) + " " + str(value) + " type of value: " + str(type(value)))
        if(valueIsNotNested(value)):
            html += writePair(key, value)
        elif(type(value) == dict):
            html += "<td rowspan=" + str(dict_depth(value)) +">" + str(key) + "</td>"
            html += writeHtml(value)
        elif(type(value) == list):
            html += "<tr><td rowspan=" + str(len(value)  + 1) +">" + str(key) + "</td>"
            for list_value in value:
                html += "<tr><td>" + str(list_value) +"</td> </tr>"

    return html

def writePair(key, value):
    html = "<td>" + str(key) +"</td> <td>" + str(value) + "</td></tr><tr>"
    #print(html)
    return html

def valueIsNotNested(value):
    if(type(value) == list or type(value) == dict):
        return False
    else:
        return True 

def dict_depth(dic):
    cnt = 0
    for _item in dic:
        if type(dic[_item]) is dict:
            cnt += dict_depth(dic[_item])                   
        else:
            cnt += 1
    return cnt

if __name__ == "__main__":
    main()