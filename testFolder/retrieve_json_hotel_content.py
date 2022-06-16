#!/usr/bin/env python
import os, sys, json, pprint
import string
import re

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


    #empty tables just to fill the top and botom line of table, since border-top, border-bottom is hidden for rest of the table to prevent border merging.
    htmlcode = "<table class = 'emptytable-top' ><tr class = 'hcd_tr'><td>&nbsp;</td></tr> </table>" 

    htmlcode += "<table " + css +">"
    htmlcode += writeTable(retrievedData['propertiesList'][0], True)
    
    htmlcode += "<table class = 'emptytable-bottom'><tr class = 'hcd_tr'><td>&nbsp;</td></tr> </table>" 

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


def writeTable(var, isFirstLevel):
    html = ""
    if(type(var) == dict):     
        for key,value in var.items():
            if(valueIsNotNested(value)):
                html += writePair(key, value)
            else:
                html += checkFirstLevel(isFirstLevel)
                html += "<td class='hcd_td'  rowspan=" + str(getDepth(value)) +">" + str(key) + "</td>"
                html += writeTable(value, False)

    elif(type(var) == list):    
        for _item in var:
            if(type(_item) == dict):
                html += checkFirstLevel(isFirstLevel)
                html += writeTable(_item , False)
            elif type(_item) == list:
                html += checkFirstLevel(isFirstLevel)
                html += "<td class='hcd_td' rowspan=" + str(getDepth(_item)) +">" + str(_item) + "</td>"
                html += writeTable(_item , False)
            else:
                html += "<td class='hcd_td'>" + str(_item) + "</td></tr><tr class = 'hcd_tr'>"
    return html

#for each key in 1st level, enter a new table
def checkFirstLevel(isFirstLevel):            
    if(isFirstLevel):
        return "<table " + css +">"
    return ""

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


if __name__ == "__main__":
    main()