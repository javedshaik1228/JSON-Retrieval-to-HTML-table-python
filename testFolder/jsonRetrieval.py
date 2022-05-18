import os, sys, json, pprint
import string
import re
from tkinter.messagebox import RETRY

import requests
from jsonToHtmlTable import writeTable

def main():

    #_url = "http://test.webservices.1a.amadeus.net:25050/1ASIHOSJSONU/TDCRET/hotels-descriptive-content/property/retrieve-partial"

    if(len(sys.argv) == 4):
        propertyCode = sys.argv[1]
        getLongText = sys.argv[2]
        phase = sys.argv[3]
    else:
        return

    SAPID = getSAP_ID(phase)

    _url = "http://test.webservices.1a.amadeus.net:25050/" + SAPID + "/TDCRET/hotels-descriptive-content/property/retrieve-partial"

    BODY =  {"propertyCodes":[propertyCode] ,"parameters":{"getLongDescription": getLongText}}

    r = requests.post(_url, json = BODY)

    retrieved_data =  r.text

    if checkForError(retrieved_data, phase): return

    retrieved_data = json.loads(retrieved_data)         #convert response to json (dict)
    css = "class='bordered-table'"

    htmlcode = "<table " + css +">"
    htmlcode += writeTable(retrieved_data['propertiesList'][0], True)
    htmlcode += "<table style = 'width:100%' ><tr class = 'emptyrow'><td>&nbsp;</td></tr>" 
    #an empty table row just to fill the bottom line of table, since border-bottom is hidden for rest of the table.
    htmlcode += "</table>"
    print(htmlcode)

def getSAP_ID(phase):
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

if __name__ == "__main__":
    main()