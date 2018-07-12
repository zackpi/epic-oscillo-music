import cv2
import numpy as np
import sys

MAX_LEN = 50
WINDOW = 100
def rand_short_path(pts):
    dedupe = list(set(pts))
    ysort = sorted(pts, key=lambda p: p[1])
    imap = {i: pt for i, pt in enumerate(ysort)}
    
    segs = {}
    from_pts = set(range(len(ysort)))
    to_pts = set(range(len(ysort)))       # implement as boolean array
    while from_pts:
        i = from_pts.pop()
        xi, yi = imap[i]
        
        min_d, min_j, min_pt = sys.maxsize, 0, None
        for j in range(max(0, i-WINDOW), min(len(ysort), i+WINDOW+1)):           
            if j not in to_pts or j == i:
                continue
            
            xj, yj = imap[j]
            dx = xi-xj
            dy = yi-yj
            distance = dx*dx+dy*dy
            if distance < min_d and distance < MAX_LEN:
                min_d = distance
                min_pt = (xj, yj)
                min_j = j
        if min_pt:
            segs[(xi, yi)] = min_pt
            to_pts.remove(min_j)
    
    curves = []
    from_pts = set(ysort)
    to_pts = set(ysort)
    while from_pts:
        pt = from_pts.pop()
        while pt not in segs:
            if from_pts:
                pt = from_pts.pop()
            else:
                break
        if not from_pts:
            break
        
        curve = []
        while pt in segs:
            if segs[pt] not in to_pts:
                break
            
            pt = segs[pt]
            curve.append(pt)
            to_pts.remove(pt)
            
            if pt not in from_pts:
                break
            from_pts.remove(pt)
        
        if len(curve):    
            curves.append(curve)
    
    while len(curves) > 1:
        c = curves.pop()
        (cx1, cy1), (cx2, cy2) = c[0], c[-1]
        
        min_d1, min_d2, min_p1, min_p2 = sys.maxsize, sys.maxsize, None, None
        for p in curves:
            if not len(p):
                continue
            (px1, py1), (px2, py2) = p[0], p[-1]
            d1, d2 = (cx2-px1)**2+(cy2-py1)**2, (px2-cx1)**2+(py2-cy1)**2
            if d1 < min_d1:
                min_p1 = p
                min_d1 = d1
            if d2 < min_d2:
                min_p2 = p
                min_d2 = d2
        
        if d1 < d2:
            curves.remove(min_p1)
            c.extend(min_p1)
            curves.append(c)
        else:
            curves.remove(min_p2)
            min_p2.extend(c)
            curves.append(min_p2)
            
    return curves.pop()


cam = cv2.VideoCapture(0)
_, img = cam.read()
r,c,_ = img.shape
scl = 5
mask = cv2.circle(np.zeros((r//scl, c//scl), dtype=np.uint8), 
                    (r//scl//2, c//scl//2), r//scl//2, [255,255,255], -1)
_, mask = cv2.threshold(mask, 127, 255, 0)

while cv2.waitKey(1) != 27:
    
    mini = cv2.resize(img, (c//scl,r//scl), interpolation=cv2.INTER_LINEAR)
    #cv2.imshow("source", mini)
    
    canny = mini.copy()
    canny = cv2.GaussianBlur(canny, (7,7), 0)
    #cv2.imshow("blur", canny)
    
    canny = cv2.Canny(canny, 127, 255)
    canny = cv2.bitwise_or(canny, canny, mask=mask)
    #cv2.imshow("canny", canny)
    
    cntimg = mini.copy()
    _, cnt, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(cntimg, cnt, -1, [0, 255, 0], 1)
    #cv2.imshow("contour", cntimg)
    
    pathimg = np.zeros_like(img)
    points = [(c[0][0],c[0][1]) for c in [j for i in cnt for j in i]]
    
    path = rand_short_path(points)
    for i in range(len(path)-1):
        (x1, y1),(x2, y2) = path[i], path[i+1]
        
        cv2.line(pathimg, (x1*scl, y1*scl), (x2*scl, y2*scl), (0,i*255//len(path),0), 2)
    cv2.imshow("path", pathimg)
    
    _, img = cam.read()


















