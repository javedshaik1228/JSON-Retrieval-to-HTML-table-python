#!/usr/bin/env python
import os, sys, json, pprint
import string
import re
from unittest.mock import NonCallableMagicMock

import requests


def main():

    if(len(sys.argv) == 3):
        propertyCode = sys.argv[1]
        phaseCode = sys.argv[2]
        #Todo: add functionality to get long description . getLongText = sys.argv[3]
    else:
        return

    SAPID = getSAPID(phaseCode)

    if(phaseCode == "PRD"): 
        _url = "[host for PRD phase]" + SAPID + "/TDCRET/hotels-descriptive-content/property/retrieve-partial"
    else:        
        _url = "http://test.webservices.1a.amadeus.net:25050/" + SAPID + "/TDCRET/hotels-descriptive-content/property/retrieve-partial"

    BODY =  {"propertyCodes":[propertyCode] ,"parameters":{"getLongDescription": False}}

    r = requests.post(_url, json = BODY)

    retrievedData =  r.text

     #check for errors in the received response
    if checkForError(retrievedData, phaseCode): return    

    #convert response to json (dict)
    retrievedData = json.loads(retrievedData)         
    css = "class='bordered-table'"

    # htmlcode = '<div class="accordian">'
    # htmlcode += writeFirstLevel(retrievedData['propertiesList'][0])
    # htmlcode += '</div>'

    # Opening JSON file
    f = open('test.json')
  
    data = json.load(f)


    htmlcode = '</pre><div class="tree">'
    htmlcode += writeTree(retrievedData['propertiesList'][0])
    # htmlcode += writeTree(data)
    htmlcode += '</div>'

    print(htmlcode)

def getSAPID(phase):
    if(phase == "PDT"):
        SAPID = "1ASIHOSJSON"
    elif(phase == "UAT"):
        SAPID = "1ASIHOSJSONU"
    elif(phase == "FVT"):
        SAPID = "1ASIHOSJSONF"
    elif(phase == "PRD"):
        SAPID = ""
    return SAPID

def checkForError(r, phase):
    if ("errorList" in r):
        print(r + " \nIn the env: " + phase)
        return True
    return False


css = "class='bordered-table'"

"""
    If var is dictionary type, then iterate each key and value, if list type, iterate through each item
    1. Check if the value in key:value pair (only if var is dict) is not nested (not a dict or list type). If not nested, then print in the form of table row.
    2. Else, check if its in first level of json structure. if yes, insert another table 
            (This is to make sure that the table spans whole page and doesnt leave whitespace because of nested structure) 
    3. insert new table data with rowspan attr, with no. of rowspan count = the depth of dictionary/ list.
    4. Recursive calling of writeTable function with isFirstLevel as false.
"""

#is first level
def writeFirstLevel(rData):
    html = ""
    if(type(rData) == dict):     
        for key,value in rData.items():         
            html += insertCard(key,  value)          #new card for each key
    elif(type(rData) == list):
        print(len(rData))    
        for _item in rData:
            html += insertCard(key = _item)                #new card for each item
    return html


#not in 1st level
def writeTable(var):
    html = ""
    if(type(var) == dict):     
        for key,value in var.items():
            if(valueIsNotNested(value)):
                html += writePair(key, value)
            else:
                html += "<td class='hcd_td'  rowspan=" + str(getDepth(value)) +">" + str(key) + "</td>"
                html += writeTable(value)

    elif(type(var) == list):    
        for _item in var:
            if(type(_item) == dict):
                html += writeTable(_item)
            elif type(_item) == list:
                html += "<td class='hcd_td' rowspan=" + str(getDepth(_item)) +">" + str(_item) + "</td>"
                html += writeTable(_item)
            else:
                html += "<td class='hcd_td'>" + str(_item) + "</td></tr><tr class = 'hcd_tr'>"
    return html

#for each key in 1st level, enter a new table card
def insertCard(key, value = None):                  
    htmlcard = '<div class="card">' 
    htmlcard += '<div class="card-header">' 
    #function overloading
    if value is not None:
        htmlcard += '<h3>' + getTitle(key) + '</h3> <span class="fa fa-minus"> </span> </div>'
        htmlcard += '<div class="card-body active"> <table ' + css + '>'
        htmlcard += writeTable({key: value})

    #If value is none, then list type
    else:
        _item = key     
        htmlcard += '<h3>' + getTitle(_item) + '</h3> <span class="fa fa-minus"> </span> </div>'
        htmlcard += '<div class="card-body active"> <table ' + css + '>'
        htmlcard += writeTable([_item])
    
    htmlcard += '</table> </div> </div>'
    return htmlcard


#todo
def getTitle(var):
    title = str(var)
    return title

#write the pair as in the form of table data
def writePair(key, value):                      

    if (key == "url"):                                                      #for url values, insert anchor tags
        html = "<td class='hcd_td'>" + str(key) +"</td> <td class='hcd_td'> <a href="+ str(value) +">" + str(value) +  "</a> </td></tr><tr class = 'hcd_tr'>"
    else:
        html = "<td class='hcd_td'>" + str(key) +"</td> <td class='hcd_td'>" + str(value) + "</td></tr><tr class = 'hcd_tr'>"
    return html

def valueIsNotNested(value):
    if(type(value) == list or type(value) == dict):
        return False
    else:
        return True 

#get depth of nested data types
def getDepth(var):                             
    cnt = 0
    if(type(var) == dict):
        for key,value in var.items():
            if valueIsNotNested(value):
                cnt += 1           
            else:
                cnt += getDepth(value)  
    elif(type(var) == list):
        for _item in var:
            if valueIsNotNested(_item):
                cnt += 1           
            else:
                cnt += getDepth(_item)  
    return cnt


"Tree structure"
def writeTree(rData):
    html = ""
    if(type(rData) == dict):
        for key,value in rData.items():
            html += insertNode(key, value)
    return html

def insertNode(key, value = None):
    if value is not None:
        htmlNode = "<div class = 'node'>"
        htmlNode +=  getTitle(key) + '</div>'
        htmlNode += '<div class = "node-body active"> <ul>'
        htmlNode += nodeBody(value)
        htmlNode += '</ul></div>'
    else:
        htmlNode = nodeBody(key)
        htmlNode += '</ul></div>'
    return htmlNode

def nodeBody(value):
    htmlNode = ""
    if(type(value) == dict):
        for keys,values in value.items():
            if(valueIsNotNested(values)):
                htmlNode += '<li>' + str(keys) + ' : ' + str(values) + '</li>'
            elif(type(values) == dict):
                htmlNode += insertNode(keys, values)
            elif(type(values) == list):
                htmlNode += "<div class = 'node'>"
                htmlNode +=   getTitle(keys) + '</div>'
                htmlNode += '<div class = "node-body active"> <ul>'
                htmlNode += insertNode(values)

    elif(type(value) == list):
        for _items in value:
            if(valueIsNotNested(_items)):
                htmlNode += '<li>' + str(_items) + '</li>'
            else:
                htmlNode += "<div class = 'node'> </div>"
                htmlNode += '<div class = "node-body active"> <ul>'
                htmlNode += insertNode(_items)
    else:
        htmlNode += '<li>' + str(value) + '</li>'
    return htmlNode
    


if __name__ == "__main__":
    main()