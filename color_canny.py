import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import time

def convex_hull(pts):
    """
    computes and returns the convex hull of a set of data points.
    
    returns: a list of points on the hull counter-clockwise from the left-most point
    """
    
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

def triangulate(pts):
    root = pts[0]
    tris = []
    for i in range(1, len(hull)-1):
        tri = (root, hull[i], hull[i+1])
        tris.append(tri)
    
    
    
    return tris


cam = cv2.VideoCapture(0)
_, img = cam.read()
r,c,_ = img.shape
scl = 2
mask = cv2.circle(np.zeros((r//scl, c//scl), dtype=np.uint8), 
                    (r//scl//2, c//scl//2), r//scl//2, [255,255,255], -1)
_, mask = cv2.threshold(mask, 127, 255, 0)

while cv2.waitKey(1) != 27:
    
    mini = cv2.resize(img, (c//scl,r//scl), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("source", mini)
    
    blue = mini[:,:,0]
    green = mini[:,:,1]
    red = mini[:,:,2]
    blue = cv2.GaussianBlur(blue, (7,7), 0)
    green = cv2.GaussianBlur(green, (7,7), 0)
    red = cv2.GaussianBlur(red, (7,7), 0)
    #cv2.imshow("blue", blue)
    #cv2.imshow("green", green)
    #cv2.imshow("red", red)
    
    blue = cv2.Canny(blue, 64, 192)
    green = cv2.Canny(green, 64, 192)
    red = cv2.Canny(red, 64, 192)
    #cv2.imshow("blue_canny", blue)
    #cv2.imshow("green_canny", green)
    #cv2.imshow("red_canny", red)
    
    canny = cv2.merge([blue, green, red])
    cv2.imshow("canny", canny)
    """
    cntimg = mini.copy()
    _, cnt, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(cntimg, cnt, -1, [0, 255, 0], 1)
    cv2.imshow("contour", cntimg)
    
    pathimg = img # np.zeros_like(img)
    points = [(c[0][0],c[0][1]) for c in [j for i in cnt for j in i]]
    dedupe = list(set(points))
    curve = convex_hull(dedupe)
    
    for i in range(len(curve)-1):
        (x1, y1),(x2, y2) = curve[i], curve[i+1]
        cv2.line(pathimg, (x1*scl, y1*scl), (x2*scl, y2*scl), (0,255,0), 1)
    cv2.imshow("path", pathimg)
    """
    _, img = cam.read()
"""

points = np.random.rand(4000,2).tolist()
t = time.time()
hull = convex_hull(points)
print(points)
print(time.time()-t)
#triangles = triangulate(hull)

plt.scatter([x for x,y in points], [y for x,y in points], color="r")
plt.plot([x for x,y in hull], [y for x,y in hull], color="g")
#for tri in triangles:
#    plt.plot([x for x,y in tri], [y for x,y in tri], color="b")
plt.show()
"""












