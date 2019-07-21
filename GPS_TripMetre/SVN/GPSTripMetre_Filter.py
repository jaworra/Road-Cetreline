
import math

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
  22/01/2012
  
Description:
  Reads Geodetic Report of DRCL and filters straight sections to given radius,
  unless z changes more than given value between 2 consecutive points. Angle is
  used to determine tightness of a corner - the tighter the corner, the smaller
  the filter radius. Filter radius is maximum on a straight, and minimum when
  the angle is more than the specified angle from straight. Triangle side length
  is the length to look ahead and behind to check for turning. 1/4 of this value
  is also checked. To use default values, leave the field blank. Output file is
  in the format X,Y,Z, and should be read into 12d to generate combined scale
  factor for chainage calculations.

  NOTE: assumes points in geodetic report are in the format x y z with no other
        columns, and that the points are in order along the road. Out of order
        points will result in incorrect filtering.
''')
#open user specified file for reading
inFile = open(raw_input('Geodetic Report Path: '), 'r')


#get maximum point radius from user or default to 10m
maxRadius = raw_input('Maximum Distance Between Points (default 10m): ')
while maxRadius != '' and not maxRadius.replace('.', '').isdigit() or maxRadius.count('.') > 1:
    maxRadius = raw_input('Please enter a number: ')
if maxRadius == '':
    maxRadius = 10.0
else:
    maxRadius = float(maxRadius)

#get minimum radius from user or default to 2.5m
minRad = raw_input('Minimum Distance Between Points (defaults to distance between points if none given): ')
while minRad != '' and not minRad.replace('.', '').isdigit() or minRad.count('.') > 1:
    minRad = raw_input('Please enter a number: ')
if minRad == '':
    minRad = -1
else:
    minRad = float(minRad)

#get radius tolerance from user or default to 0.25m
radTol = raw_input('Filter Tolerance (default 0.25m): ')
while radTol != '' and not radTol.replace('.', '').isdigit() or radTol.count('.') > 1:
    radTol = raw_input('Please enter a number: ')
if radTol == '':
    radTol = 0.25
else:
    radTol = float(radTol)

#get maximum z change from user or default to 100mm
maxZChange = raw_input('Maximum Z Change between points to accept (default 0.1m): ')
while maxZChange != '' and not maxZChange.replace('.', '').isdigit() or maxZChange.count('.') > 1:
    maxZChange = raw_input('Please enter a number: ')
if maxZChange == '':
    maxZChange = 0.1
else:
    maxZChange = float(maxZChange)

#get angle difference to keep all points from user or default to 4 degrees
angKeepPoints = raw_input('Angle difference to start using minimum radius (default 4 degrees): ')
while angKeepPoints != '' and not angKeepPoints.replace('.', '').isdigit() or angKeepPoints.count('.') > 1:
    angKeepPoints = raw_input('Please enter a number: ')
if angKeepPoints == '':
    angKeepPoints = 4.0
else:
    angKeepPoints = float(angKeepPoints)

#get side length for measuring angle from user or default to 150m
sideLen = raw_input('Triangle side length (default 200m): ')
while sideLen != '' and not sideLen.replace('.', '').isdigit() or sideLen.count('.') > 1:
    sideLen = raw_input('Please enter a number: ')
if sideLen == '':
    sideLen = 200.0
else:
    sideLen = float(sideLen)

print('Filtering...')

points = []                     #list of points along DRCL
lineNo = 0                      #current line in file

#cycle through each line in the file
for line in inFile:
    lineNo += 1         #don't get heading lines from geodetic report
    if lineNo > 19 and line <> '':
        #current point being read from file, 4 elements for x, y, z, combined scale
        curPoint = line.split()
        if len(curPoint) == 3:
            points.append(curPoint)     #add current point to list of points

inFile.close()      #close the file

pointsOut = []      #points to output in the format x, y, z
offset = 0          #index offset for skipping filtered points
if minRad == -1:
    calcMinRad = True
else:
    calcMinRad = False

#cycle through points
for pt in range(0,len(points)-2):
    if pt+offset <= len(points)-2:   #make sure the current point index is in the list
        pointsOut.append(points[pt + offset])    #add the current point to the output array

        if pt > 0:
            ptStart = pt + offset - 1        #index of start point for angle checking
            
            #check for vertical change
            if abs(float(points[pt + offset][2]) - float(points[pt + offset-1][2])) < maxZChange \
               and (abs(float(points[pt + offset+1][2]) - float(points[pt + offset][2])) < maxZChange):
                
                #find start point, ~ sideLen m before current point
                while ptDist(points[ptStart][:2], points[pt + offset][:2]) < sideLen and ptStart > 0:
                    ptStart -= 1
                
                ptEnd = pt + offset + 1     #index of end point for angle checking
                #find end point, ~ sideLen m from current point
                while ptDist(points[pt + offset][:2], points[ptEnd][:2]) < sideLen and ptEnd < len(points)-1:
                    ptEnd += 1
                    
                #calculate angle at apex - check along given length and 1/4 of given length and find largest angle
                if pt + offset > 4 and pt + offset < len(points) - 6:
                    ang = max(abs(180.0 - apexAngle(points[ptStart][:2], points[pt + offset][:2], points[ptEnd][:2])), \
                              abs(180.0 - apexAngle(points[pt + offset -(pt + offset - ptStart)/4][:2], points[pt + offset][:2], \
                                                    points[pt + offset + (ptEnd - pt - offset)/4][:2])))
                else:   #only check along given length if there's not enough points for 1/4 length
                    ang = abs(180.0 - apexAngle(points[ptStart][:2], points[pt + offset][:2], points[ptEnd][:2]))
                
                if calcMinRad == True:
                    minRad = ptDist(points[pt + offset][:2], points[pt + offset + 1][:2])
                
                radDist = minRad + ((maxRadius-minRad)/angKeepPoints)*(angKeepPoints-ang)  #calculate radius based on angle
                
                if calcMinRad == False:
                    radDist = max(minRad, radDist)  #if the radius is smaller than the minimum radius, bring it up to the minimum
                    

                oldOffset = offset      #store the old offset to calculate the distance between current point and next point
                #increase offset until the point is outside the radius
                while pt + offset < len(points)-1 and ptDist(points[pt + oldOffset][:2], points[pt + offset][:2]) < radDist:
                    offset += 1
                    
                #make sure point isn't second last point to prevent error
                if pt + offset + 1 <= len(points)-1:
                    #while the next point to keep is more than the tolerance away from the radius, come back one point
                    while ptDist(points[pt + oldOffset][:2], points[pt + offset + 1][:2]) > radDist + radTol and offset > oldOffset:
                        offset -= 1
    else:
        #exit the for loop if all points have been processed
        break



pointsOut.append(points[-1])    #add the last point to the output array

#tell the user how many points were filtered out
print('%i points removed' % (len (points) - len(pointsOut)))

#write the points to the output file specified by the user
outFile = open(raw_input('Output File: '), 'w')
outFile.write('Easting,Northing,Height\n')
prevPt = ''
for p in pointsOut:
    if '%.1F,%.1F,%.2F\n' % ( float(p[0]), float(p[1]), float(p[2]) ) != prevPt:
        prevPt = '%.1F,%.1F,%.2F\n' % ( float(p[0]), float(p[1]), float(p[2]) )
        outFile.write(prevPt)

outFile.close()     #close the output file
