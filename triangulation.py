import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import time

def triarea(x1, y1, x2, y2, x3, y3):
    return abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))/2

def trilen(x1, y1, x2, y2, x3, y3):
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
    
    gray = cv2.cvtColor(mini, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    canny = cv2.Canny(blur, 64, 192)
    cv2.imshow("canny", canny)
    
    cntimg = mini.copy()
    _, cnt, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(cntimg, cnt, -1, [0, 255, 0], 1)
    cv2.imshow("contour", cntimg)
    
    triimg = mini.copy()
    rect = (0,0,c//scl,r//scl)
    subdiv = cv2.Subdiv2D(rect)
    points = [(c[0][0],c[0][1]) for c in [j for i in cnt for j in i]]
    for pt in list(set(points)):
        subdiv.insert(pt)
    
    ## draw all
    #tris = np.array([[t[:2], t[2:4], t[4:6]] for t in subdiv.getTriangleList()], dtype=np.int32)
    #cv2.fillPoly(triimg, tris, (0,200,0))
    
    
    ## fill indiv
    tris = subdiv.getTriangleList()
    
    ## filter by area and length of longest edge
    tris = list(filter(lambda t: triarea(*t)**2+trilen(*t) < 4000, tris))
    
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
    
    _, img = cam.read()




