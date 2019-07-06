#utilex

import os
import datetime
import time
import json


def echo (p_text,p_q=0,p_fill='.'): 
    fill_format=p_fill+">"+str(p_q)+"s"
    #print(fill_format)
    print(format(p_text,fill_format))
    #print(p_text)

def list_from_file(p_filename):
    #l=[]
    l=[line.rstrip('\n') for line in open(p_filename)]
    return l



def write_to_file1(p_list,p_filename,p_mode='w'):

    f = open(p_filename,p_mode)  
    
    for item in p_list:
        f.write(item+"\n")
    f.close

def write_to_file2(p_list,p_filename,p_mode='w'):

    f = open(p_filename,p_mode)  
    
    for item in p_list:
        text=','.join(item)
        f.write(text+"\n")
    f.close


def deleteDir(dirPath):
    deleteFiles = []
    deleteDirs = []
    for root, dirs, files in os.walk(dirPath):
        for f in files:
            deleteFiles.append(os.path.join(root, f))
        for d in dirs:
            deleteDirs.append(os.path.join(root, d))
    for f in deleteFiles:
        os.remove(f)
    for d in deleteDirs:
        os.rmdir(d)
    os.rmdir(dirPath)

def fullpath(p_parent,p_child):
    return os.path.join(p_parent,p_child)

def resetDir(p_dir_name):
    if os.path.exists(p_dir_name):
        deleteDir(p_dir_name)
    os.mkdir(p_dir_name)


def change_filedate(filename, datetime_new, datetime_format, datetime_offset=0):
#filename -->  archivo a modificar la hora
#datetime_new --> nueva fecha en format string
#formato --> formato de datetime_new
#datetime_delta --> offset de la nueva cadena por default es zero horas
    dt = datetime.datetime.strptime(datetime_new,datetime_format)
    dto = dt - datetime.timedelta(hours=datetime_offset)
    to=time.mktime(dto.timetuple())
    os.utime(filename,(to,to))


def variable(p_variable,p_default="",p_json_filename="cpy.json"):
    with open(p_json_filename, 'r') as f:
        datastore = json.load(f)
    return datastore[p_variable]

def template(p_type,p_json_filename="cpy.json"):
    with open(p_json_filename, 'r') as f:
        datastore = json.load(f)
    #type_json=datastore[p_type]
    return datastore[p_type]["template"]

def content(p_type,p_content,p_json_filename="cpy.json"):
    with open(p_json_filename, 'r') as f:
        datastore = json.load(f)
    return datastore[p_type][p_content]


# retorna una lista con sus elementos stripeados
def striplist(p_l):
    return([x.strip() for x in p_l])