import xlwt
import os
import re

chapterList = []
dataMap = {}

def chapterObtain( logFileDir ):
    fo = open(logFileDir)
    fileLines = fo.readlines()
    charpter = []
    for line in fileLines:
        if line.startswith(r'File['):
            charpter = []
            charpter.append(line)
            # print(charpter[0])
            continue
        if len(charpter) > 0:
            charpter.append(line)
        if line.startswith(r'     |___Moment: First['):
            global chapterList
            chapterList.append(charpter)
            # print(charpter[8])
            charpter = []
            continue
    return
def dataAnalysis(keyTup, valueList):
    if keyTup in dataMap.keys():
        v = dataMap[keyTup]
        # writeBytes
        wBytes = v[0] + valueList[0]
        # writeMegaBytes
        wMB = v[1] + valueList[1]
        # writeCount
        wCount = v[2] + valueList[2]
        # fileSyncCount
        fCount= v[3] + valueList[3]
        # writeTimeGapMin
        wtMin = float()
        if(v[4] < valueList[4]):
            wtMin = v[4]
        else:
            wtMin = valueList[4]
        # writeTimeGapMax
        wtMax = float()
        if(v[5] > valueList[5]):
            wtMax = v[5]
        else:
            wtMax = valueList[5]
        # writeTimeGapAvg
        wtAvgValue = v[6][0] + valueList[6][0]
        wtAvgValueCount = v[6][1] + valueList[6][1]
        wtAvg = [wtAvgValue, wtAvgValueCount]
        # writeTimeSpan
        # writeMomentFirst
        # writeMomentLast
        vl = [wBytes, wMB, wCount, fCount, wtMin, wtMax, wtAvg]
        # print(str(wBytes) + '    '+ str(wMB) + '   ' + str(wCount) + '   ' + str(fCount) + '   ' + str(wtMin) + '   ' + str(wtMax))
        dataMap.update({keyTup : vl})
    else:
        dataMap[keyTup] = valueList
    return

def dataFilter( charpter ):
    fileName = ''
    processName = ''
    threadName = ''
    writeBytes = int()
    writeMegaBytes = float()
    writeCount = int()
    fileSyncCount = int()
    writeTimeGapMin = float()
    writeTimeGapMax = float()
    writeTimeGapAvg = float()
    # writeTimeSpan = float()
    # writeMomentFirst = float()
    # writeMomentLast = float()

    for line in charpter:
        if line.startswith(r'File['):
            # list = line.split(':')
            # fileName = list[1].replace('[','').replace(']','').replace(',','')
            # print(line)
            # content = re.split(r'.*?\[', line)
            # dirRegex = re.compile(r'[[](.*?)[]]')
            # mo = dirRegex.search(line)
            res = re.findall(r'[n][a][m][e][:][\[](.*?)[\]]', line)
            #print(res)
            fileName = res[0]
        if line.startswith(r'  |___EXE Name'):
            res = re.findall(r'[\[](.*?)[\]]', line)
            processName = res[0]
            threadName = res[1]
            # print(processName + '       ' + threadName)
        if line.startswith(r'     |___Write'):
            res = re.findall(r'[\[](.*?)[\]]', line)
            writeBytes = int(res[0])
            writeMegaBytes = float(res[2])
            writeCount = int(res[3])
            fileSyncCount = int(res[4])
        if line.startswith(r'     |___Time Gap'):
            res = re.findall(r'[\[](.*?)[\]]', line)
            writeTimeGapMin = float(res[0].replace('ns','').replace('s',''))
            writeTimeGapMax = float(res[1].replace('ns','').replace('s',''))
            writeTimeGapAvgValue = float(res[2].replace('ns','').replace('s',''))
            writeTimeGapAvgCount = int(1)
            writeTimeGapAvg= [writeTimeGapAvgValue, writeTimeGapAvgCount]
            writeTimeSpan = float(res[3].replace('ns','').replace('s',''))
        if line.startswith(r'     |___Moment'):
            res = re.findall(r'[\[](.*?)[\]]', line)
            writeMomentFirst = float(res[0].replace('ns','').replace('s',''))
            writeMomentLast = float(res[1].replace('ns','').replace('s',''))
    
    print(fileName + '    '+ processName + '   ' + threadName +  '   '+
        str(writeBytes) + '    '+ str(writeMegaBytes) + '   ' + str(writeCount) + '   ' + str(fileSyncCount) + '   ' + str(writeTimeGapMin) + '   ' + str(writeTimeGapMax))
    keyTup = (fileName, processName, threadName)
    valueList = [writeBytes, writeMegaBytes, writeCount, fileSyncCount, writeTimeGapMin, writeTimeGapMax, writeTimeGapAvg]

    dataAnalysis(keyTup, valueList)
    return

wb = xlwt.Workbook(encoding = 'utf-8')
dir = os.getcwd()
print(dir)
dataSheet = wb.add_sheet('process_rw_analysis', cell_overwrite_ok = True)
xlname = 'Emmc_Log_Analysis.xls'

my_style_1 = xlwt.XFStyle()
font = my_style_1.font
font.bold = True
font.colour_index = 0x08
alignment = my_style_1.alignment
alignment.horz = 2
pat = my_style_1.pattern
pat.pattern = 1
pat.pattern_fore_colour = 0x11
bd = my_style_1.borders
bd.left = 1
bd.right = 1
bd.top = 1
bd.bottom = 1

my_style_2 = xlwt.XFStyle()
bd = my_style_2.borders
bd.left = 1
bd.right = 1
bd.top = 1
bd.bottom = 1

source_path = os.path.abspath(r'./emmclog')
if os.path.exists(source_path):
    for root, dirs, files in os.walk("emmclog", topdown=False):
        for file in files:
            src_file_dir = os.path.join(root, file)
            # print(src_file_dir)
            chapterObtain(src_file_dir)
        print('All chaprowter count: ' + str(len(chapterList)))
        for chapter in chapterList:
            dataFilter(chapter)

        cloumnName = ['File Name', 'Process Name', 'Thread Name', 'Write Bytes', 'write MegaBytes', 'Write Count', 'Sync Count', 'Write InteralTime Min', 'Write InteralTime Max', 'Write InteralTime Avg']
        refR = 3
        refC = 1
        for i in range(0, len(cloumnName)):
            dataSheet.write(refR - 1, refC + i, cloumnName[i], my_style_1)
            if cloumnName[i] == 'File Name':
                dataSheet.col(refC + i).width = 15555
            elif cloumnName[i] == 'Process Name':
                dataSheet.col(refC + i).width = 8888
            else :
                dataSheet.col(refC + i).width = 5151

        for key,value in dataMap.items():
            cc = refC
            # print(value)
            fileName = key[0]
            processName = key[1]
            threadName = key[2]
            writeBytes = int(value[0])
            writeMegaBytes =  float(value[1])
            writeCount =  int(value[2])
            fileSyncCount =  int(value[3])
            writeTimeGapMin =  float(value[4])
            writeTimeGapMax =  float(value[5])
            writeTimeGapAVG =  float(float(value[6][0]) / int(value[6][1]))
            # print(fileName + '    '+ processName + '   ' + threadName + '    ' +
            # str(writeBytes) + '    '+ str(writeMegaBytes) + '   ' + str(writeCount) + '   ' + str(fileSyncCount) + '   ' + str(writeTimeGapMin) + '   ' + str(writeTimeGapMax))
            
            for ik in range(0, len(key)) :
                dataSheet.write(refR, cc, key[ik], my_style_2)
                cc += 1
            for ic in range(0, len(value)) :
                if ic == 6 :
                    dataSheet.write(refR, cc, float(float(value[6][0]) / float(value[6][1])), my_style_2)
                else :
                    dataSheet.write(refR, cc, value[ic], my_style_2)
                cc += 1
            refR += 1
            
    wb.save(xlname)
    print('done!')
