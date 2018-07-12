import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import time

def convex_hull(pts):
    xsort = sorted(pts, key=lambda p: p[0])
    xind = 0
    pi = xsort[xind]
    
    hull = [pi]
    while xind < len(xsort)-1:
        thsort = sorted(xsort[xind+1:], key=
                        lambda pj: np.pi + np.arctan2(pj[1]-pi[1],  pj[0]-pi[0]))
        pi = thsort[0]
        xind = xsort.index(pi)
        hull.append(pi)
    
    while xind > 0:
        thsort = sorted(xsort[:xind], key=
                        lambda pj: np.pi + np.arctan2(pi[1]-pj[1],  pi[0]-pj[0]))
        pi = thsort[0]
        xind = xsort.index(pi)
        hull.append(pi)
    
    return hull

def triangulate(pts):
    root = pts[0]
    tris = []
    for i in range(1, len(pts)-1):
        tri = [root, pts[i], pts[i+1]]
        tris.append(tri)
    
    return tris

"""
cam = cv2.VideoCapture(0)
_, img = cam.read()
r,c,_ = img.shape
scl = 5
mask = cv2.circle(np.zeros((r//scl, c//scl), dtype=np.uint8), 
                    (r//scl//2, c//scl//2), r//scl//2, [255,255,255], -1)
_, mask = cv2.threshold(mask, 127, 255, 0)

while cv2.waitKey(1) != 27:
    
    mini = cv2.resize(img, (c//scl,r//scl), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("source", mini)
    
    canny = mini.copy()
    canny = cv2.GaussianBlur(canny, (7,7), 0)
    cv2.imshow("blur", canny)
    
    canny = cv2.Canny(canny, 0, 255)
    canny = cv2.bitwise_or(canny, canny, mask=mask)
    cv2.imshow("canny", canny)
    
    cntimg = mini.copy()
    _, cnt, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(cntimg, cnt, -1, [0, 255, 0], 1)
    cv2.imshow("contour", cntimg)
    
    pathimg = np.zeros_like(img)
    points = [(c[0][0],c[0][1]) for c in [j for i in cnt for j in i]]
    path = triangulate(points)
    for curve in path:
        for i in range(len(curve)-1):
            (x1, y1),(x2, y2) = curve[i], curve[i+1]
            
            cv2.line(pathimg, (x1*scl, y1*scl), (x2*scl, y2*scl), (255,255,255), 1)
    cv2.imshow("path", pathimg)
    
    _, img = cam.read()
"""

points = np.random.rand(100,2).tolist()
t = time.time()
hull = convex_hull(points)
print(time.time()-t)
triangles = triangulate(hull)

plt.scatter([x for x,y in points], [y for x,y in points], color="r")
plt.plot([x for x,y in hull], [y for x,y in hull], color="g")
for tri in triangles:
    plt.plot([x for x,y in tri], [y for x,y in tri], color="b")
plt.show()














