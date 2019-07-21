import math

#distance between points on horizontal plane
def ptDist(pt1, pt2):
    return math.sqrt(pow(float(pt2[0])-float(pt1[0]),2) + pow(float(pt2[1])-float(pt1[1]),2))

#angle at apex of triangle formed by points 1, 2 and 3, apex is assumed to be point 2
def apexAngle(pt1, pt2, pt3):
    sA = ptDist(pt1, pt2)
    sB = ptDist(pt2, pt3)
    sC = ptDist(pt1, pt3)
    disc = 2*sA*sB
    if disc==0:
        return 90
    else:
        det = (pow(sA, 2) + pow(sB, 2) - pow(sC, 2))/disc
        if det > 1:
            det = 1
        if det < -1:
            det = -1
        return math.degrees(math.acos(det))

#calculate distance from pt1 to perpendicular point from pt2 along pt1 to pt3
def getCHDiff(pt1, pt2, pt3):
    return ptDist(pt1, pt2) * math.cos(math.radians(apexAngle(pt1, pt2, pt3)))

inFeatFile = raw_input('Feature File: ')
inChFile = raw_input('Chainage File: ')
startCH = float(raw_input('Start Chainage: '))
endCH = float(raw_input('End Chainage: '))
revCH = raw_input('Reverse lane chainage? (Y/N - Default N) ')
if revCH == 'y' or revCH == 'Y':
    revCH = -1
else:
    revCH = 1

#open files
featFile = open(inFeatFile)
chFile = open(inChFile)

#read features
lNo = 0
feats = []
firstLine = ''
for line in featFile:
    lNo += 1
    if lNo > 1:
        feats.append(line.split(','))
    else:
        firstLine = line

#read chainages
lNo = 0
CHs = []
for line in chFile:
    lNo += 1
    if lNo > 1:
        CHs.append(line.split(','))

#close the files
featFile.close()
chFile.close()


#re-align features
featsOut = []
chPos = 0
for feat in feats:
    #check if it's within the specified chainages
    if float(feat[0]) >= startCH and float(feat[0]) <= endCH:
        #find closest point on DRCL
        prevDist = ptDist(feat[1:3], CHs[chPos][1:3])
        chPos += 1
        while chPos <= len(CHs)-1 and ptDist(feat[1:3], CHs[chPos][1:3]) < prevDist:
            prevDist = ptDist(feat[1:3], CHs[chPos][1:3])
            chPos += 1
        chPos -= 1

        #calculate distance from closest point to perpendicular point
        distChange = 0
        #if the point isn't the last point in the chainage file
        if chPos < len(CHs) - 2:
            #calculate forward angle
            fAngle = apexAngle(feat[1:3], CHs[chPos][1:3], CHs[chPos + 1][1:3])
            #calculate reverse angle if it isn't the first point
            rAngle = 360
            if chPos > 0:
                rAngle = apexAngle(feat[1:3], CHs[chPos][1:3], CHs[chPos - 1][1:3])

            #calculate distance from closest point
            if rAngle < 90:
                distChange = -getCHDiff(feat[1:3], CHs[chPos][1:3], CHs[chPos - 1][1:3])
            elif fAngle < 90:
                distChange = getCHDiff(feat[1:3], CHs[chPos][1:3], CHs[chPos + 1][1:3])

        #if the point is the last point in the chainage file, only use reverse angle
        else:
            angle = apexAngle(feat[1:3], CHs[chPos][1:3], CHs[chPos - 1][1:3])
            if angle < 90:
                distChange = -getCHDiff(feat[1:3], CHs[chPos][1:3], CHs[chPos - 1][1:3])

        #adjust position of feature
        p = 0
        if distChange != 0: #if it moves
            #calculate whether it's before or after the closest point
            if distChange > 0:
                p = 1
            elif distChange < 0:
                p = -1
            #re-calculate chainage
            feat[0] = '%.3F' % (float(CHs[chPos][0]) + distChange/1000 * revCH)
            hDist = ptDist(CHs[chPos + p][1:3], CHs[chPos][1:3])    #horizontal distance movement
            distChange = abs(distChange)
            #re-calculate x, y and z coords
            feat[1] = '%.1F' % (float(CHs[chPos][1]) + (float(CHs[chPos+p][1]) - float(CHs[chPos][1])) / hDist * distChange)
            feat[2] = '%.1F' % (float(CHs[chPos][2]) + (float(CHs[chPos+p][2]) - float(CHs[chPos][2])) / hDist * distChange)
            feat[3] = '%.2F' % (float(CHs[chPos][3]) + (float(CHs[chPos+p][3]) - float(CHs[chPos][3])) / ptDist(CHs[chPos][1:3], CHs[chPos+p][1:3]) * distChange)
        else:
            #re-calculate z and ch even if point didn't move since it could be off
            feat[0] = '%.3F' % float(CHs[chPos][0])
            feat[3] = '%.2F' % float(CHs[chPos][3])


    #output the feature
    featsOut.append(feat)

#write the new feature file
outFile = raw_input('Feature Output File: ')
oFile = open(outFile, 'w')
oFile.write(firstLine)
for f in featsOut:
    tmpStr = ''
    for d in f:
        tmpStr += d + ','
    oFile.write(tmpStr.rstrip(','))
oFile.close()
