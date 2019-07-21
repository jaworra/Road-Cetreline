
import math

#distance between points on horizontal plane
def ptDist(pt1, pt2):
    return math.sqrt(pow(float(pt2[0])-float(pt1[0]),2) + pow(float(pt2[1])-float(pt1[1]),2))


#interpolated point along horizontal plane
def newPoint(pt0,pt1,lineCh,DistPTApart):
    
    ##print pt0[0]
    ##print pt0[1]
    
    StartPTEast = float(pt0[0])
    StartPTNorth = float(pt0[1])
    EndPTEast = float(pt1[0])
    EndPTNorth = float(pt1[1])
    
    #DistPTApart = lineCh.
    #DistPTApart = math.sqrt(pow(float(EndPTEast)-float(StartPTEast),2) + pow(float(EndPTNorth)-float(StartPTNorth ),2)) #USED DIFFERENT AREA HERE!!
    ##print DistPTApart
    AngleTmp = float((EndPTEast - StartPTEast)/DistPTApart)


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
        ##print 'nw'
        return ptLineEast,ptLineNorth
    elif (EndPTNorth-StartPTNorth) >=0 and (EndPTEast-StartPTEast) >= 0: #NE
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = (math.cos (AngleFinal) * lineCh) + StartPTNorth
        ##print 'ne'
        return ptLineEast,ptLineNorth
    elif (EndPTNorth-StartPTNorth) < 0 and (EndPTEast-StartPTEast) >= 0: #SE
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = StartPTNorth - (math.cos(AngleFinal)*lineCh)
        ##print 'se'
        return ptLineEast,ptLineNorth
    elif (EndPTNorth-StartPTNorth) < 0 and (EndPTEast-StartPTEast) < 0: #SW
        ptLineEast = StartPTEast + (math.sin(AngleFinal)*lineCh)
        ptLineNorth = StartPTNorth - (math.cos(AngleFinal)*lineCh)
        ##print 'sw'
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
PointCh = 0    #overall chainage
InterCh = 0    #Interval chainage
NewPointBol = 0 #New point created
NewPointCh = 0 #Newly created point
linetest =0
addCh = 0 #distance from previous interpolated point to previous point
morethan2points = 0


testPoint = userInterval

#cycle through each line in file
for line in inFile:
    lineNo += 1  #Dont get header
    #splits line into 4 elements, x, y, Max Dist, Road Name
    if lineNo > 1:
        prvPoint = prvLine.split(',')
        curPoint = line.split(',')

        DistBet = ptDist(prvPoint[:2],curPoint[:2])
        InterCh += DistBet #Distance between points
        PointCh += InterCh #Overall Chainage
        print 'Inter Chainage:'
        print DistBet
        print InterCh

        if curPoint[3] == prvPoint[3]:       #Same Road and last point 

            if InterCh/userInterval >= 1:       #Distance between original points greater than users interval 
                if morethan2points == 1:
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],DistBet -(InterCh - userInterval),DistBet)).rstrip(')').lstrip('(').replace(" ","")
                else:
                    #Calls intperpolated function, converst to string, removes () & " "
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],userInterval-addCh,DistBet)).rstrip(')').lstrip('(').replace(" ","")


                print 'x'
                print NewPointStr
                
                newpoint = NewPointStr.split(',')                 #assigning interpolated point to list     
                newpointDist = ptDist(newpoint[:2],prvPoint[:2])  #Distances between last original point to interpolated point
                print 'y'
                
                outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+NewPointStr+"\n")
                NewPointCh = InterCh - userInterval
                
                print DistBet - newpointDist #difference between (Distance between original points and users interval and previous orinal point and interpolate point. 
                print 'z'
                
                addCh = 0
                InterCh = 0
                addCh = DistBet - newpointDist
                
                while DistBet - newpointDist > userInterval: # If there requires more than one interpolated points in a section (between two original points)
                    (DistBet -(DistBet - newpointDist))+ userInterval
                    print 'zzzz'
                    print (DistBet -(DistBet - newpointDist))+ userInterval

                    if morethan2points == 1:
                        test = DistBet -(InterCh - userInterval) + userInterval
                    else:
                        test =(DistBet -(DistBet - newpointDist))+ userInterval    
                    
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],test,DistBet)).rstrip(')').lstrip('(').replace(" ","")
                    outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+NewPointStr+"\n")
                    
                    newpoint = NewPointStr.split(',')
                    newpointDist = ptDist(newpoint[:2],prvPoint[:2])

                    addCh = 0
                    InterCh = 0
                    addCh = DistBet - newpointDist    
                    print '@@@@@@@@@@@'


                morethan2points = 0
                
                InterCh = NewPointCh
                NewPointBol = 1
                InterLine = NewPointStr+","+str(round((PointCh/1000),3))+","+curPoint[3]
                intePoint = InterLine.split(',')
                ItestPoint = userInterval - (InterCh - userInterval)
                #Add new chaiange from interpolated point
            else:
                morethan2points = 1

            
            #InterCh = DistBet
            #print InterCh
            
        else:                               #Different Road
            PointCh = 0
            InterCh = 0
            addCh = 0
            NewPointBol = 0
            print curPoint[3].rstrip('\n')+" "+str(round((PointCh/1000),3))+" "+curPoint[0]+" "+curPoint[1]
            #output last point of old road and first point of new road
            outFile.write("LastPoint"+","+str(round((PointCh/1000),3))+","+prvPoint[0]+","+prvPoint[1]+"\n")
            outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+curPoint[0]+","+curPoint[1]+",CCCCc  \n")
            print 'test2'
        prvLine = line

        
    else:
        prvLine = line
        curPoint = line.split(',')
        PointCh = 0
        InterCh = 0
        addCh = 0
        NewPointBol = 0
        
        print curPoint[3].rstrip('\n')+" "+str(PointCh)+" "+curPoint[0]+" "+curPoint[1]
        outFile.write(curPoint[3].rstrip('\n')+","+str(PointCh)+","+curPoint[0]+","+curPoint[1]+"\n")
        print 'First Point'
    prvLine = line 
  
#last point output
outFile.write(curPoint[3].rstrip('\n')+","+str(PointCh)+","+curPoint[0]+","+curPoint[1]+"\n")

#3m difference in 2km figure.... mapinfo vs python chainage calc
inFile.close()
outFile.close()



