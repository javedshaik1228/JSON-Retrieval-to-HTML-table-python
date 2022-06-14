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
                html += checkifFirstLevel(isFirstLevel)
                html += "<td class='hcd_td'  rowspan=" + str(get_depth(value)) +">" + str(key) + "</td>"
                html += writeTable(value, False)

    elif(type(var) == list):    
        for _item in var:
            if(type(_item) == dict):
                html += checkifFirstLevel(isFirstLevel)
                html += writeTable(_item , False)
            elif type(_item) == list:
                html += checkifFirstLevel(isFirstLevel)
                html += "<td class='hcd_td' rowspan=" + str(get_depth(_item)) +">" + str(_item) + "</td>"
                html += writeTable(_item , False)
            else:
                html += "<td class='hcd_td'>" + str(_item) + "</td></tr><tr class = 'hcd_tr'>"
    return html

def checkifFirstLevel(isFirstLevel):      #for each key in 1st level, enter a new table
    if(isFirstLevel):
        return "<table " + css +">"
    return ""


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

def get_depth(var):
    cnt = 0
    if(type(var) == dict):
        for key,value in var.items():
            if valueIsNotNested(value):
                cnt += 1           
            else:
                cnt += get_depth(value)  
    elif(type(var) == list):
        for _item in var:
            if valueIsNotNested(_item):
                cnt += 1           
            else:
                cnt += get_depth(_item)  
    return cnt
