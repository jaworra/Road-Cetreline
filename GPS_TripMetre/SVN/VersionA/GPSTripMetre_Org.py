import math
import numpy
#import gdal  Fix with GDAL python binding


#distance between points on horizontal plane
def ptDist(pt1, pt2):
    return math.sqrt(pow(float(pt2[0])-float(pt1[0]),2) + pow(float(pt2[1])-float(pt1[1]),2))

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
  8/01/2013
  
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



#G:\Geospatial\GIS\JohnW\spine_file_build_LGA\SRRC_GPS_Road_CL\test.dat
#open user specified file for reading
inFile = open(raw_input('CenterLine CSV Import Path: '), 'r')
outFile = open(raw_input('output file: '), 'w')

print('Filtering.....')

# Calculate chainage
points = []    #list of points along a file
lineNo = 0     #current line in file
DistBet = 0    #start
PointCh = 0

#cycle through each line in file
for line in inFile:
    lineNo += 1  #Dont get header
    #splits line into 4 elements, x, y, Max Dist, Road Name
    if lineNo > 1:
        prvPoint = prvLine.split(',')
        curPoint = line.split(',')
        DistBet = ptDist(prvPoint[:2],curPoint[:2])
        PointCh += DistBet
        
         
        if curPoint[3] == prvPoint[3]:       #Different Road
            print curPoint[3].rstrip('\n')+" "+str(round((PointCh/1000),3))+" "+curPoint[0]+" "+curPoint[1]
            outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+curPoint[0]+","+curPoint[1]+"\n")
        else:
            PointCh = 0
            print curPoint[3].rstrip('\n')+" "+str(round((PointCh/1000),3))+" "+curPoint[0]+" "+curPoint[1]
            outFile.write(curPoint[3].rstrip('\n')+","+str(round((PointCh/1000),3))+","+curPoint[0]+","+curPoint[1]+"\n")
        prvLine = line
        
    else:
        prvLine = line
        curPoint = line.split(',')
        PointCh = 0

        print curPoint[3].rstrip('\n')+" "+str(PointCh)+" "+curPoint[0]+" "+curPoint[1]
        outFile.write(curPoint[3].rstrip('\n')+","+str(PointCh)+","+curPoint[0]+","+curPoint[1]+"\n")
    prvLine = line 


#3m difference in 2km figure.... mapinfo vs python chainage calc
inFile.close()
outFile.close()
print points

