
import math
import sys

#distance between points on horizontal plane
def ptDist(pt1, pt2):
    return math.sqrt(pow(float(pt2[0])-float(pt1[0]),2) + pow(float(pt2[1])-float(pt1[1]),2))


#interpolated point along horizontal plane
def newPoint(pt0,pt1,lineCh,DistPTApart):
        
    StartPTEast = float(pt0[0])
    StartPTNorth = float(pt0[1])
    EndPTEast = float(pt1[0])
    EndPTNorth = float(pt1[1])
    
    AngleTmp = float((EndPTEast - StartPTEast)/DistPTApart)

    #Determine Quadrant
    if AngleTmp < -1:
        AngleFinal = float(math.asin(-1))
    elif AngleTmp > 1:
        AngleFinal = float(math.asin(1))
    else:
        AngleFinal = float(math.asin(AngleTmp))
        
    #Create coordinate based on quandrant and bearing (TRIG)
    #!!!!Future works combien (nw,ne and sw,se)
    if (EndPTNorth-StartPTNorth) >=0 and (EndPTEast-StartPTEast) < 0: #NW
        ptLineEast = StartPTEast + ( math.sin(AngleFinal) * lineCh)
        ptLineNorth = (math.cos (AngleFinal) * lineCh) + StartPTNorth
        return '%.3f,%.3f' % (ptLineEast,ptLineNorth)
    elif (EndPTNorth-StartPTNorth) >=0 and (EndPTEast-StartPTEast) >= 0: #NE
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = (math.cos (AngleFinal) * lineCh) + StartPTNorth
        return '%.3f,%.3f' % (ptLineEast,ptLineNorth)
    elif (EndPTNorth-StartPTNorth) < 0 and (EndPTEast-StartPTEast) >= 0: #SE
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = StartPTNorth - (math.cos(AngleFinal)*lineCh)
        return '%.3f,%.3f' % (ptLineEast,ptLineNorth)
    elif (EndPTNorth-StartPTNorth) < 0 and (EndPTEast-StartPTEast) < 0: #SW
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = StartPTNorth - (math.cos(AngleFinal)*lineCh)
        return '%.3f,%.3f' % (ptLineEast,ptLineNorth)

#angle at apex of triangle formed by points 1, 2 and 3, apex is assumed to be point 2
def apexAngle(pt1, pt2, pt3):
    sA = ptDist(pt1, pt2)
    sB = ptDist(pt2, pt3)
    sC = ptDist(pt1, pt3)
    #print('%.3f, %.3f, %.3f' % (sA, sB, sC))
    #print(math.degrees(math.acos((pow(sA, 2) + pow(sB, 2) - pow(sC, 2))/(2*sA*sB))))
    if 2*sA*sB == 0:
        return 360
    else:
        det = (pow(sA, 2) + pow(sB, 2) - pow(sC, 2))/(2*sA*sB)
        if det > 1:
            det = 1
        if det < -1:
            det = -1
        return math.degrees(math.acos(det))

print('''Programmer:
  John Worrall

Version:
  1.0

Last Update:
   18/04/2013
  
Description:
  Batch spliting polylines enter interval
  
  NOTE:.
  
''')


mport arcpy
import sys, math

def printit(inMessage):
    print inMessage
    arcpy.AddMessage(inMessage)

if len(sys.argv) > 1:
    inFC = sys.argv[1]
    outFC = sys.argv[2]
    alongDistin = sys.argv[3]
    alongDist = float(alongDistin)
else:
    inFC = "StateWide_MetrageRoads"
    OutDir = "\\Shocnc03_shrsedat2pool_server\SHRSEDAT2\GROUPS\Geospatial\GIS\JohnW\QRN\CaseStudy1\QLD_Development_Code_Noise_Contours\JW_Workings\StraightsOrCurves\OutDir\Dir.mdb"
    outFCName = "OutInterval"
    outFC = OutDir+"/"+outFCName
    alongDist = 1000

if (arcpy.Exists(inFC)):
    print(inFC+" does exist")
else:
    print("Cancelling, "+inFC+" does not exist")
    sys.exit(0)

def distPoint(p1, p2):
    calc1 = p1.X - p2.X
    calc2 = p1.Y - p2.Y

    return math.sqrt((calc1**2)+(calc2**2))

def midpoint(prevpoint,nextpoint,targetDist,totalDist):
    newX = prevpoint.X + ((nextpoint.X - prevpoint.X) * (targetDist/totalDist))
    newY = prevpoint.Y + ((nextpoint.Y - prevpoint.Y) * (targetDist/totalDist))
    return arcpy.Point(newX, newY)

def splitShape(feat,splitDist):
    # Count the number of points in the current multipart feature
    #
    partcount = feat.partCount
    partnum = 0
    # Enter while loop for each part in the feature (if a singlepart feature
    # this will occur only once)
    #
    lineArray = arcpy.Array()

    while partnum < partcount:
        # Print the part number
        #
        #print "Part " + str(partnum) + ":"
        part = feat.getPart(partnum)
        #print part.count

        totalDist = 0

        pnt = part.next()
        pntcount = 0

        prevpoint = None
        shapelist = []

        # Enter while loop for each vertex
        #
        while pnt:

            if not (prevpoint is None):
                thisDist = distPoint(prevpoint,pnt)
                maxAdditionalDist = splitDist - totalDist

                print thisDist, totalDist, maxAdditionalDist

                if (totalDist+thisDist)> splitDist:
                    while(totalDist+thisDist) > splitDist:
                        maxAdditionalDist = splitDist - totalDist
                        #print thisDist, totalDist, maxAdditionalDist
                        newpoint = midpoint(prevpoint,pnt,maxAdditionalDist,thisDist)
                        lineArray.add(newpoint)
                        shapelist.append(lineArray)

                        lineArray = arcpy.Array()
                        lineArray.add(newpoint)
                        prevpoint = newpoint
                        thisDist = distPoint(prevpoint,pnt)
                        totalDist = 0

                    lineArray.add(pnt)
                    totalDist+=thisDist
                else:
                    totalDist+=thisDist
                    lineArray.add(pnt)
                    #shapelist.append(lineArray)
            else:
                lineArray.add(pnt)
                totalDist = 0

            prevpoint = pnt                
            pntcount += 1

            pnt = part.next()

            # If pnt is null, either the part is finished or there is an
            #   interior ring
            #
            if not pnt:
                pnt = part.next()
                if pnt:
                    print "Interior Ring:"
        partnum += 1

    if (lineArray.count > 1):
        shapelist.append(lineArray)

    return shapelist

if arcpy.Exists(outFC):
    arcpy.Delete_management(outFC)

arcpy.Copy_management(inFC,outFC)

#origDesc = arcpy.Describe(inFC)
#sR = origDesc.spatialReference

#revDesc = arcpy.Describe(outFC)
#revDesc.ShapeFieldName

deleterows = arcpy.UpdateCursor(outFC)
for iDRow in deleterows:       
     deleterows.deleteRow(iDRow)

del iDRow
del deleterows

inputRows = arcpy.SearchCursor(inFC)
outputRows = arcpy.InsertCursor(outFC)
fields = arcpy.ListFields(inFC)

numRecords = int(arcpy.GetCount_management(inFC).getOutput(0))
OnePercentThreshold = numRecords // 100

printit(numRecords)

iCounter = 0
iCounter2 = 0

for iInRow in inputRows:
    inGeom = iInRow.shape
    iCounter+=1
    iCounter2+=1    
    if (iCounter2 > (OnePercentThreshold+0)):
        printit("Processing Record "+str(iCounter) + " of "+ str(numRecords))
        iCounter2=0

    if (inGeom.length > alongDist):
        shapeList = splitShape(iInRow.shape,alongDist)

        for itmp in shapeList:
            newRow = outputRows.newRow()
            for ifield in fields:
                if (ifield.editable):
                    newRow.setValue(ifield.name,iInRow.getValue(ifield.name))
            newRow.shape = itmp
            outputRows.insertRow(newRow)
    else:
        outputRows.insertRow(iInRow)

del inputRows
del outputRows

printit("Done!")

#--------------------GPS TRIPMETRE--------------------------------

###G:\Geospatial\GIS\JohnW\py\GPS_TripMetre\test.dat
###open user specified file for reading
###inFile = open(raw_input('CenterLine CSV Import Path: '), 'r')
###outFile = open(raw_input('output file: '), 'w')
##
##
###inFile = open('C:\\Users\\John\\Desktop\\Python\\CentreLine\\test.dat', 'r')
###outFile = open('C:\\Users\\John\\Desktop\\Python\\CentreLine\\2.dat', 'w')
##inFile = open('G:\\Geospatial\\GIS\\JohnW\\py\\GPS_TripMetre\\Prep\\SRRC_GPS_Road_CL_NEW.DAT', 'r')
##outFile = open('G:\\Geospatial\\GIS\\JohnW\\py\\GPS_TripMetre\\Prep\\1.dat', 'w')
##
##
###get point intervals from user or default to 10m
##userInterval = raw_input('Enter interval between points (default 10m): ')
##while userInterval != '' and not userInterval.replace('.', '').isdigit() or userInterval.count('.') > 1:
##    userInterval = raw_input('Please enter a number: ')
##if userInterval == '':
##    userInterval = 10.0
##else:
##    userInterval = float(userInterval)
##
##print('Filtering.....')
##
### Calculate chainage
##points = []             #list of points along a file
##lineNo = 0              #current line in file
##distBet = 0             #Distance between two  points read from file
##distFromLastPoint = 0   #Distance from last interopolated point
##distOnGrad = 0          #Distance along a gradiant
##remainder =0            #Distance to add from last coordinate
##distTemp = 0            #Temporary hold
##counter = 0             #Couter
##lstPointCh =0           #Last Point Ch
##
##for line in inFile:
##    lineNo += 1  #Dont get header
##    if lineNo > 1:
##        #splits line into 4 elements, x, y, Max Dist, Road Name
##        prvPoint = prvLine.split(',')
##        curPoint = line.split(',')
##        distBet = ptDist(prvPoint[:2],curPoint[:2])
##
##        if curPoint[3] == prvPoint[3]:      
##            distFromLastPoint = distBet + remainder 
##    
##            #if distance is  > than userinterval and distance <= userInterval *2, create a point half way
##            if (distBet > userInterval) and (distBet <= (2*userInterval)):
##                NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2], distBet/2,distBet)).rstrip(')').lstrip('(').replace(" ","")
##                outFile.write(curPoint[3].rstrip('\n')+","+str(round(chainage,3))+","+NewPointStr+", single point\n")
##
##            else:
##                
##                #than interpolate point as close to interval useing while statement
##                distFromLastPoint = distBet
##                while (distFromLastPoint / userInterval) > 1:
##                    counter += 1
##                    distAdd = distBet /(int(distBet/userInterval)+1)
##                    
##                    #find the closes divisble number > userinterval 
##                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],distAdd*counter,distBet)).rstrip(')').lstrip('(').replace(" ","")
##                    outFile.write(curPoint[3].rstrip('\n')+","+str(round(chainage,3))+","+NewPointStr+", more than two points\n")
##
##                    distFromLastPoint = distFromLastPoint - distAdd
##
##                counter= 0
##
##            #Output the original point
##            outFile.write(curPoint[3].rstrip('\n')+","+str(999)+","+curPoint[0]+","+curPoint[1]+", original point\n")
##            
##        else: #Different Road
##            interpolPoint = NewPointStr.split(',')                    #assign the last interpolated point
##            lastpointDis = ptDist(interpolPoint[:2],prvPoint[:2])     #Distance between last interpolated point and last original point
##            outFile.write(prvPoint[3].rstrip('\n')+","+str(round(chainage+lastpointDis,3))+","+prvPoint[0]+","+prvPoint[1]+", Last Point\n") #Last Point
##            #sys.exit('This program exit due to chanage in road!')
##            remainder = 0
##            chainage = 0
##            outFile.write(curPoint[3].rstrip('\n')+","+str(round(0,3))+","+curPoint[0]+","+curPoint[1]+", vFirst Point differnt point\n") #First Point
##    else:
##        prvLine = line
##        curPoint = line.split(',')
##        remainder = 0
##        chainage = 0
##        outFile.write(curPoint[3].rstrip('\n')+","+str(round(0,3))+","+curPoint[0]+","+curPoint[1]+",ssLastPoint points\n")
##    prvLine = line
##
##inFile.close()
##outFile.close()



