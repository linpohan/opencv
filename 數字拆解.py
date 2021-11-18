# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 21:27:12 2021

@author: USER
"""

import cv2
binary_threshold = 100
spacing = 0.95

img = cv2.imread('img/car2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret , img_thr = cv2.threshold(gray,binary_threshold,255,cv2.THRESH_BINARY_INV)

cv2.imshow('img',img_thr)
cv2.waitKey()
cv2.destroyAllWindows()


white = []
black = []
height = img_thr.shape[0]
width = img_thr.shape[1]
print(width,height)
white_max=0
black_max =0
count = 0
for i in range(width):
    w_count = 0
    b_count = 0
    for x in range(height):
        if img_thr[x][i] == 255:
            w_count += 1
        else:
            b_count += 1
     
    white_max = max(white_max,w_count)
    black_max = max(black_max,b_count)

    white.append(w_count)
    black.append(b_count)  
    
arg = black_max > white_max

# 找白字終點
def find_end(start_):
    end_ = start_ + 1
    for m in range(start_ + 1, width - 1):
        if (black[m] if arg else white[m]) > (spacing * black_max if arg else spacing * white_max):
            end_ = m
            break
    return end_
    
n = 1
start = 1
end = 2
i = 0
while n < width - 1:
    n += 1
    # 找白字起點
    if (white[n] if arg else black[n]) > ((1 - spacing) * white_max if arg else (1 - spacing) * black_max):
        start = n
        end = find_end(start)
        n = end
        if end - start > 12:
            i += 1
            print(start, end)
            photo = img_thr[1:height, start - 10:end + 10]

            cv2.imwrite('img/' + str(i) + '.jpg', photo)
            cv2.imshow('img', photo)
            cv2.waitKey()
            cv2.destroyAllWindows()    


