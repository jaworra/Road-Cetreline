import math
fileName = raw_input('input file: ')
inFile = open(fileName)
outFileName = raw_input('output file: ')
outFile = open(outFileName, 'w')
filterDist = float(raw_input('filter distance: '))
prevLine = ''
prvLine = ''
lineNo = 0
for line in inFile:
    justSkipped = False
    lineNo += 1
    if lineNo > 2:
        prevPoint = prevLine.split(',')
        curPoint = line.split(',')
        if math.sqrt(pow(float(prevPoint[1])-float(curPoint[1]),2) + \
                     pow(float(prevPoint[2])-float(curPoint[2]),2) + \
                     pow(float(prevPoint[3])-float(curPoint[3]),2)) >= filterDist:
            prevLine = line
            outFile.write(line)
        else:
            justSkipped = True
    else:
        prevLine = line
        outFile.write(line)
    prvLine = line
    
if justSkipped == True:
    outFile.write(prvLine)
inFile.close()
outFile.close()
