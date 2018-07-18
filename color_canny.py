import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import time

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
    
    blue = cv2.Canny(blue, 64, 192)
    green = cv2.Canny(green, 64, 192)
    red = cv2.Canny(red, 64, 192)
    
    canny = cv2.merge([blue, green, red])
    cv2.imshow("canny", canny)
    
    _, img = cam.read()



