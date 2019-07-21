
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
#inFile = open(raw_input('CenterLine CSV Import Path: '), 'r')
#outFile = open(raw_input('output file: '), 'w')


#inFile = open('C:\\Users\\John\\Desktop\\Python\\CentreLine\\test.dat', 'r')
#outFile = open('C:\\Users\\John\\Desktop\\Python\\CentreLine\\2.dat', 'w')
inFile = open('G:\\Geospatial\\GIS\\JohnW\\py\\GPS_TripMetre\\Prep\\test.dat', 'r')
outFile = open('G:\\Geospatial\\GIS\\JohnW\\py\\GPS_TripMetre\\Prep\\22.dat', 'w')


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
points = []             #list of points along a file
lineNo = 0              #current line in file
distBet = 0             #Distance between two  points read from file
distFromLastPoint = 0   #Distance from last interopolated point
distOnGrad = 0          #Distance along a gradiant
remainder =0            #Distance to add from last coordinate
distTemp = 0            #Temporary hold
counter = 0             #Couter
lstPointCh =0           #Last Point Ch

for line in inFile:
    lineNo += 1  #Dont get header
    if lineNo > 1:
        #splits line into 4 elements, x, y, Max Dist, Road Name
        prvPoint = prvLine.split(',')
        curPoint = line.split(',')
        distBet = ptDist(prvPoint[:2],curPoint[:2])

        if curPoint[3] == prvPoint[3]:      

            distFromLastPoint = distBet + remainder 
            print str(distFromLastPoint)+' distance from last point'
            print str(distBet)+' distance between points'


            #if distance is  > than userinterval and distance <= userInterval *2, create a point half way
            if (distBet > userInterval) and (distBet <= (userInterval*2)):
                NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2], distBet/2,distBet)).rstrip(')').lstrip('(').replace(" ","")
                outFile.write(curPoint[3].rstrip('\n')+","+str(round(chainage,3))+","+NewPointStr+"\n")

            #elif distance is > than userinterval and distance > userInterval *2
            if (distBet > userInterval) and (distBet > (userInterval*2)):
                
                #than interpolate point as close to interval useing while statement
                distFromLastPoint = distBet
                while (distFromLastPoint / userInterval) > 1:
                    counter += 1

                    #find the closes divisble number > userinterval 
                    #NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],(distBet/(userInterval+1))*counter,distBet)).rstrip(')').lstrip('(').replace(" ","")
                    NewPointStr = str(newPoint(prvPoint[:2],curPoint[:2],(distBet/int(distBet/(userInterval-1)))*counter,distBet)).rstrip(')').lstrip('(').replace(" ","")
                    outFile.write(curPoint[3].rstrip('\n')+","+str(round(chainage,3))+","+NewPointStr+"\n")

                    #distFromLastPoint = distFromLastPoint -(distBet/(userInterval+1))                    
                    distFromLastPoint = distFromLastPoint -(distBet/int(distBet/(userInterval-1)))

                    
                counter= 0

            #Output the original point
            outFile.write(curPoint[3].rstrip('\n')+","+str(999)+","+curPoint[0]+","+curPoint[1]+"\n")

        else: #Different Road
            interpolPoint = NewPointStr.split(',')                    #assign the last interpolated point
            lastpointDis = ptDist(interpolPoint[:2],prvPoint[:2])     #Distance between last interpolated point and last original point
            outFile.write(prvPoint[3].rstrip('\n')+","+str(round(chainage+lastpointDis,3))+","+prvPoint[0]+","+prvPoint[1]+"\n") #Last Point
            #sys.exit('This program exit due to chanage in road!')
            remainder = 0
            chainage = 0
            outFile.write(curPoint[3].rstrip('\n')+","+str(round(0,3))+","+curPoint[0]+","+curPoint[1]+"\n") #First Point
    else:
        prvLine = line
        curPoint = line.split(',')
        remainder = 0
        chainage = 0
        outFile.write(curPoint[3].rstrip('\n')+","+str(round(0,3))+","+curPoint[0]+","+curPoint[1]+"\n")
    prvLine = line

inFile.close()
outFile.close()



