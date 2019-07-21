
import math

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
   10/01/2013
  
Description:
  Reads a dat file report on cooridnates of nodes along a line,
  calculates a users intervale nodes (same road)
  and assigns chainages. 
  User must input the correct dat format for the program to work
  i.e Easting, Northing, Max Distance, Name.
  448078.392,6911980.887,2399.000,Moorang La
  
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
TotalCh = 0


testPoint = userInterval

#cycle through each line in file
for line in inFile:
    lineNo += 1  #Dont get header
    #splits line into 4 elements, x, y, Max Dist, Road Name
    if lineNo > 1:
        #Try Reseting List/Arrays
        curPoint[:]= []
        prvPoint[:]= []
        points[:]= []
        
        prvPoint = prvLine.split(',')
        curPoint = line.split(',')
        DistBet = ptDist(prvPoint[:2],curPoint[:2])
        InterCh += DistBet #Distance between points
        PointCh += InterCh #Overall Chainage

        if curPoint[3] == prvPoint[3]:          #Same Road
            if InterCh/userInterval >= 1:       #Check if interpolation is required 
                if morethan2points == 1:        #More than one point created between originals

                    #Calls intperpolated function, converst to string, removes () & " "
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],DistBet -(InterCh - userInterval),DistBet)).rstrip(')').lstrip('(').replace(" ","")
                else:
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],userInterval-addCh,DistBet)).rstrip(')').lstrip('(').replace(" ","")


                newpoint = NewPointStr.split(',')                 #assigning interpolated point to list     
                newpointDist = ptDist(newpoint[:2],prvPoint[:2])  #Distances between last original point to interpolated point
                
                TotalCh += userInterval #Total Chaiange
                outFile.write(curPoint[3].rstrip('\n')+","+str(round(TotalCh,3))+","+NewPointStr+"\n")
                NewPointCh = InterCh - userInterval
                        
                addCh = 0
                InterCh = 0
                addCh = DistBet - newpointDist
                
                while DistBet - newpointDist > userInterval: # If there requires more than one interpolated points in a section (between two original points)
                      
                    if morethan2points == 1:  #More than one point created between originals
                        test = DistBet -(InterCh - userInterval) + userInterval
                    else:
                        test =(DistBet -(DistBet - newpointDist))+ userInterval    
                    
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],test,DistBet)).rstrip(')').lstrip('(').replace(" ","")
                    
                    TotalCh += userInterval #Total Chaiange
                    outFile.write(curPoint[3].rstrip('\n')+","+str(round(TotalCh,3))+","+NewPointStr+"\n")
                    
                    newpoint = NewPointStr.split(',')
                    newpointDist = ptDist(newpoint[:2],prvPoint[:2])
                    addCh = 0
                    InterCh = 0
                    addCh = DistBet - newpointDist    

                morethan2points = 0
                InterCh = NewPointCh
                NewPointBol = 1
                InterLine = NewPointStr+","+str(round((PointCh/1000),3))+","+curPoint[3]
                intePoint = InterLine.split(',')
                ItestPoint = userInterval - (InterCh - userInterval)
                #Add new chaiange from interpolated point
            else:
                morethan2points = 1
            
        else:           #Different Road - write out last point of old road and first point of new road
            #Try Reseting List/Arrays
            #curPoint[:]= []
            #prvPoint[:]= []
            
            PointCh = 0
            InterCh = 0
            addCh = 0
            NewPointBol = 0
            TotalCh += userInterval #Total Chaiange
            outFile.write(prvPoint[3].rstrip('\n')+","+str(round(TotalCh,3))+","+prvPoint[0]+","+prvPoint[1]+"\n") #Last Point
            TotalCh = 0
            outFile.write(curPoint[3].rstrip('\n')+","+str(round(TotalCh,3))+","+curPoint[0]+","+curPoint[1]+"\n") #First Point
        prvLine = line

    else:               #First record
        prvLine = line
        curPoint = line.split(',')
        PointCh = 0
        InterCh = 0
        addCh = 0
        NewPointBol = 0
        TotalCh = 0 #Total Chaiange
        outFile.write(curPoint[3].rstrip('\n')+","+str(TotalCh)+","+curPoint[0]+","+curPoint[1]+"\n")
    prvLine = line 
  
#Last record
outFile.write(curPoint[3].rstrip('\n')+","+str(TotalCh+userInterval)+","+curPoint[0]+","+curPoint[1]+"\n")

#3m difference in 2km figure.... mapinfo vs python chainage calc
inFile.close()
outFile.close()



