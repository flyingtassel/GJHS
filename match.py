import os
import os.path

# class match(object):
#       #初始化头
#     def __init__(self):
#         pass

def finddifs(path='E:\zxcsdownloads'):
    dirs=[]
    dirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]
    rars=[]
    covers=[]
    for d in dirs:
        for y in [x for x in os.listdir(os.path.join(
                path, d)) if os.path.splitext(x)[1] != '.rar']:
            covers.append(y.split('.')[0])

        for y in [x for x in os.listdir(os.path.join(
                path, d)) if os.path.splitext(x)[1] == '.rar']:
            rars.append(y.split('[')[0])
    dif1 = list(set(covers).difference(set(rars)))
    dif1.sort()
    dif2 = list(set(rars).difference(set(covers)))
    dif2.sort()
    print("covers count:", len(covers),
            "||files count:", len(rars))
            
    print("dif1 covers-->rars: ", dif1, "count : ", len(dif1))
    print("dif2 rars-->covers: ", dif2, "count : ", len(dif2))
    return dif1,dif2

# def findtest():
#     covers=[]
#     rars=[]
#     for r,rt,rtx in os.walk('D:\git\zxcs8\downloads'):        
#         for files in rtx:
#             if os.path.splitext(files)=='.jpg':
#                 covers.append(files)
#             elif os.path.splitext(files) == '.rar':
#                 rars.append(files)
#     return print(covers)


# findtest()
finddifs()

