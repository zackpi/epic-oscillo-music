import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import time


def dig(tridict, edge):
    hullseg = []
    edgetri = tridict[edge]

"""
def convex_hull(pts):
    ""
    computes and returns the convex hull of a set of data points.
    
    returns: a list of points on the hull counter-clockwise from the left-most point
    ""
    
    # sort the elements by their x-value to increase speed of next step and also
    # get the left-most point, which is the starting point
    xsort = sorted(pts, key=lambda p: p[0])
    xind = 0
    pi = xsort[xind]
    
    # compute the half-hull going to the right (increasing x-value)
    # this is where sorting gives a speed-up because we only need to 
    # evaluate the angle "in front" of the last point pi.
    hull = [pi]
    while xind < len(xsort)-1:
        thsort = sorted(xsort[xind+1:], key=
                        lambda pj: np.pi + np.arctan2(pj[1]-pi[1],  pj[0]-pi[0]))
        pi = thsort[0]
        xind = xsort.index(pi)
        hull.append(pi)
    
    # once we reach the right-most point, we repeat the process for decreasing x
    while xind > 0:
        thsort = sorted(xsort[:xind], key=
                        lambda pj: np.pi + np.arctan2(pi[1]-pj[1],  pi[0]-pj[0]))
        pi = thsort[0]
        xind = xsort.index(pi)
        hull.append(pi)
    
    return hull     # note:     hull[0] == hull[-1] 
"""


def triarea(x1, y1, x2, y2, x3, y3):
    """
    computes the area of a triangle defined by the passed points
    """
    return abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))/2


def trilen(x1, y1, x2, y2, x3, y3):
    """
    computes the maximum square distance between any two of a triangle's points
    """
    return max((x2-x1)**2 + (y2-y1)**2,
            (x3-x2)**2 + (y3-y2)**2,
            (x1-x3)**2 + (y1-y3)**2)

cam = cv2.VideoCapture(0)
_, img = cam.read()
r,c,_ = img.shape
scl = 2

while cv2.waitKey(1) != 27:
    
    mini = cv2.resize(img, (c//scl,r//scl), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("source", mini)
    
    """
    gray = cv2.cvtColor(mini, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    canny = cv2.Canny(blur, 64, 192)
    cv2.imshow("canny", canny)
    """
    
    hsv = cv2.cvtColor(mini, cv2.COLOR_BGR2HSV)
    facemask1 = cv2.inRange(hsv, (5, 50, 150), (25, 255, 255))
    facemask2 = cv2.inRange(hsv, (0, 60, 120), (75, 250, 160))
    hairmask = cv2.inRange(hsv, (0, 120, 60), (40, 140, 100))
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(shirtmask,kernel,iterations=1)
    cv2.imshow("erosion", erosion)
    cv2.imshow("hsv", hsv)
    
    """
    cntimg = mini.copy()
    _, cnt, hier = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(cntimg, cnt, -1, [0, 255, 0], 1)
    cv2.imshow("contour", cntimg)
    
    hullimg = mini.copy()
    points = [(c[0][0],c[0][1]) for c in [j for i in cnt for j in i]]
    dedupe = list(set(points))
    hull = cv2.convexHull(np.array(dedupe))
    for i in range(len(hull)-1):
        x1, y1, x2, y2 = *hull[i][0], *hull[i+1][0]
        cv2.line(hullimg, (x1, y1), (x2, y2), (0,0,255), 2)
    cv2.imshow("hull", hullimg)
    
    triimg = mini.copy()
    rect = (0,0,c//scl,r//scl)
    subdiv = cv2.Subdiv2D(rect)
    for pt in dedupe:
        subdiv.insert(pt)
    tris = subdiv.getTriangleList()
    """    
    
    
    """
    delaunay = {}
    for tri in tris:
        x1,y1,x2,y2,x3,y3 = tri
        if (x1, y1, x2, y2) in delaunay:
            delaunay[(x1, y1, x2, y2)].append(tri)
        else:
            delaunay[(x1, y1, x2, y2)] = [tri]
        
        if (x2, y2, x3, y3) in delaunay:
            delaunay[(x2, y2, x3, y3)].append(tri)
        else:
            delaunay[(x2, y2, x3, y3)] = [tri]
        
        if (x3, y3, x1, y1) in delaunay:
            delaunay[(x3, y3, x1, y1)].append(tri)
        else:
            delaunay[(x3, y3, x1, y1)] = [tri]
    
    for i1 in range(len(hull)):
        i2 = i1+1 if i1+1 < len(hull) else 0
        x1, y1, x2, y2 = *hull[i1][0], *hull[i2][0]
        
        tri = delaunay[(x1, y1, x2, y2)]
        tA = triarea(tri)
        tL = trilen(tri)
        
        if tA > AREA_THRESH or tL > LEN_THRESH:
           dig()      
    """
    """
    ## draw all
    #tris = np.array([[t[:2], t[2:4], t[4:6]] for t in subdiv.getTriangleList()], dtype=np.int32)
    #cv2.fillPoly(triimg, tris, (0,200,0))
    
    
    ## filter by area and length of longest edge
    #tris = list(filter(lambda t: triarea(*t)**2+trilen(*t) < 4000, tris))
    
    for tri in tris:
        x1, y1, x2, y2, x3, y3 = tri
        ## color by area
        #tA = triarea(*tri)
        #tricolor = [max(0, min(255, 255*tA/300)), 0, 0]
        
        ## color by length of longest edge
        #tL = trilen(*tri)
        #tricolor = [0, max(0, min(255, 255*tL/4000)), 0]
        
        ## color by area and length of longest edge
        tA = triarea(*tri)
        tL = trilen(*tri)
        tricolor = [max(0, min(255, 255*tA/300)), max(0, min(255, 255*tL/4000)), 0]
        
        cv2.fillConvexPoly(triimg, np.array([(x1,y1),(x2,y2),(x3,y3)], dtype=np.int32), tricolor)
        
    cv2.imshow("tris", triimg)
    
    
    
    """
    _, img = cam.read()




