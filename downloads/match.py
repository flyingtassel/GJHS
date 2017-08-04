import os
import os.path

def findcovers(path='./downloads'):
    dirs=[]
    dirs = [x for x in os.listdir( path ) if os.path.isdir(os.path.join(path,x))]

    covers=[]
    for d in dirs:
        for y in [x for x in os.listdir(os.path.join(
                path, d)) if os.path.splitext(x)[1] == '.jpg']:
            covers.append(y.split('.')[0])


    return covers


def findrars(path='./downloads'):
    dirs = []
    dirs = [x for x in os.listdir(
        path) if os.path.isdir(os.path.join(path, x))]

    rars = []
    for d in dirs:
        for y in [x for x in os.listdir(os.path.join(
                path, d)) if os.path.splitext(x)[1] == '.rar']:
            rars.append(y.split('[')[0])

    return rars

def findtest():
    covers=[]
    rars=[]
    for r,rt,rtx in os.walk('D:\git\zxcs8\downloads'):        
        for files in rtx:
            if os.path.splitext(files)=='.jpg':
                covers.append(files)
            elif os.path.splitext(files) == '.rar':
                rars.append(files)
    return print(covers)

findcovers()
findrars()
findtest()
