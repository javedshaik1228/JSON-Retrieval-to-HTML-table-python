
def writeTable(var):
    html = ""
    if(type(var) == dict):     
        for key,value in var.items():
            if(valueIsNotNested(value)):
                html += writePair(key, value)
            else:
                html += "<td rowspan=" + str(get_depth(value)) +">" + str(key) + "</td>"
                html += writeTable(value)
    elif(type(var) == list):    
        for _item in var:
            if(type(_item) == dict):
                html += writeTable(_item)
            elif type(_item) == list:
                html += "<td rowspan=" + str(get_depth(_item)) +">" + str(_item) + "</td>"
                html += writeTable(_item)
            else:
                html += "<td>" + str(_item) + "</td></tr><tr>"
    return html

def writePair(key, value):
    if (key == "url"):
        html = "<td>" + str(key) +"</td> <td> <a href="+ str(value) +">" + str(value) +  "</a> </td></tr><tr>"
    else:
        html = "<td>" + str(key) +"</td> <td>" + str(value) + "</td></tr><tr>"
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
