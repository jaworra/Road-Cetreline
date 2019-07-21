
import math

#distance between points on horizontal plane
def ptDist(pt1, pt2):
    return math.sqrt(pow(float(pt2[0])-float(pt1[0]),2) + pow(float(pt2[1])-float(pt1[1]),2))


#interpolated point along horizontal plane
def newPoint(pt0,pt1,lineCh):
    
    print pt0[0]
    print pt0[1]
    
    StartPTEast = float(pt0[0])
    StartPTNorth = float(pt0[1])
    EndPTEast = float(pt1[0])
    EndPTNorth = float(pt1[1])
    
    #DistPTApart = lineCh.
    DistPTApart = math.sqrt(pow(float(EndPTEast)-float(StartPTEast),2) + pow(float(EndPTNorth)-float(StartPTNorth ),2)) #USED DIFFERENT AREA HERE!!
    print '3 - Distance apart'
    print DistPTApart
    AngleTmp = float((EndPTEast - StartPTEast)/DistPTApart)

    #Assigned DistPTApart to distance from start node  DELETE ME
    lineCh = DistPTApart - lineCh
    print 'Line Ch'
    print DistPTApart

    
    #HERE ---->>>>
    #Determine Quadrant
    if AngleTmp < -1:
        AngleFinal = float(math.asin(-1))
    elif AngleTmp > 1:
        AngleFinal = float(math.asin(1))
    else:
        AngleFinal = float(math.asin(AngleTmp))
        
    #Create coordinate based on bearing
    #Future works combien (nw,ne and sw,se)
    if (EndPTNorth-StartPTNorth) >=0 and (EndPTEast-StartPTEast) < 0: #NW
        ptLineEast = StartPTEast + ( math.sin(AngleFinal) * lineCh)
        ptLineNorth = (math.cos (AngleFinal) * lineCh) + StartPTNorth
        print 'nw'
        return ptLineEast,ptLineNorth
    elif (EndPTNorth-StartPTNorth) >=0 and (EndPTEast-StartPTEast) >= 0: #NE
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = (math.cos (AngleFinal) * lineCh) + StartPTNorth
        print 'ne'
        return ptLineEast,ptLineNorth
    elif (EndPTNorth-StartPTNorth) < 0 and (EndPTEast-StartPTEast) >= 0: #SE
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = StartPTNorth - (math.cos(AngleFinal)*lineCh)
        print 'se'
        return ptLineEast,ptLineNorth
    elif (EndPTNorth-StartPTNorth) < 0 and (EndPTEast-StartPTEast) < 0: #SW
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = StartPTNorth - (math.cos(AngleFinal)*lineCh)
        print 'sw'
        return ptLineEast,ptLineNorth

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
   10/01/2013
  
Description:
  Reads a dat file report on cooridnates of nodes along a line,
  calculates a plane distance between consecutive nodes (same road)
  and assigns chainages.
  User must input the correct dat format for the program to work
  i.e Easting, Northing, Max Distance, Name.
  #448078.392,6911980.887,2399.000,Moorang La
  
  Output dat file is in the formatt Name, CH, Easting, Northing.
  Hall St,0,473471.486,6926651.99
  
  NOTE: assumes point in input file have no header.
  
''')

#G:\Geospatial\GIS\JohnW\py\GPS_TripMetre\test.dat
#open user specified file for reading
inFile = open(raw_input('CenterLine CSV Import Path: '), 'r')
outFile = open(raw_input('output file: '), 'w')


#get point intervals from user or default to 10m
userInterval = raw_input('Enter interval between points (default 10m): ')
while userInterval != '' and not userInterval.replace('.', '').isdigit() or userInterval.count('.') > 1:
    userInterval = raw_input('Please enter a number: ')
if userInterval == '':
    userInterval = 10.0
else:
    userInterval = float(userInterval)

print('Filtering.....')

# Calculate chainage
points = []    #list of points along a file
lineNo = 0     #current line in file
DistBet = 0    #start
PointCh = 0    #actual chainage
InterCh = 0    #Interval chainage
NewPointBol = 0 #New point created
NewPointCh = 0 #Newly created point


#cycle through each line in file
for line in inFile:
    lineNo += 1  #Dont get header
    #splits line into 4 elements, x, y, Max Dist, Road Name
    if lineNo > 1:
        prvPoint = prvLine.split(',')
        curPoint = line.split(',')
        DistBet = ptDist(prvPoint[:2],curPoint[:2])
        PointCh += DistBet
        InterCh += DistBet
    
         
        if curPoint[3] == prvPoint[3]:       #Same Road

            if InterCh/userInterval >= 1:
                #Calculate interpolated point here!
                #print curPoint[3].rstrip('\n')+" "+str(round((PointCh/1000),3))+" "+curPoint[0]+" "+curPoint[1]
                #outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+curPoint[0]+","+curPoint[1]+"\n")

                NewPointCh = InterCh - userInterval
                print InterCh - userInterval
                print '1'
                #print newPoint(prvPoint[:2],curPoint[:2],(InterCh - userInterval))
                print '2'

                NewPointCord = str(newPoint(prvPoint[:2],curPoint[:2],(InterCh - userInterval))).rstrip(')').lstrip('(')+"\n"
                outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+ NewPointCord)
                              
                #outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+str(newPoint(prvPoint[:2],curPoint[:2],(InterCh - userInterval))).rstrip(')').lstrip('(')+"\n")


                
                #InterCh = 0
                InterCh = InterCh/userInterval  
                #Set new point coordinates to previous points value..
                #prvLine = curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+str(newPoint(prvPoint[:2],curPoint[:2],(InterCh - userInterval))).rstrip(')').lstrip('(')+"\n"

                #prvLine = str(newPoint(prvPoint[:2],curPoint[:2],(InterCh - userInterval))).rstrip(')').lstrip('(')+","+str(userInterval)+","+curPoint[3]
                prvLine = NewPointCord.rstrip('\n')+","+str(userInterval)+","+curPoint[3]
                              
                NewPointBol = 1


        else:                            #Different Road
            PointCh = 0
            InterCh = 0
            print curPoint[3].rstrip('\n')+" "+str(round((PointCh/1000),3))+" "+curPoint[0]+" "+curPoint[1]
            outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+curPoint[0]+","+curPoint[1]+"\n")
        prvLine = line
        
    else:
        prvLine = line
        curPoint = line.split(',')
        PointCh = 0
        InterCh = 0
        
        print curPoint[3].rstrip('\n')+" "+str(PointCh)+" "+curPoint[0]+" "+curPoint[1]
        outFile.write(curPoint[3].rstrip('\n')+","+str(PointCh)+","+curPoint[0]+","+curPoint[1]+"\n")
    prvLine = line 


#3m difference in 2km figure.... mapinfo vs python chainage calc
inFile.close()
outFile.close()



