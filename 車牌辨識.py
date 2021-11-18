# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 19:51:01 2021

@author: USER
"""

import cv2
import pytesseract

img = cv2.imread('img/car4.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #轉灰階

blur = cv2.GaussianBlur(gray, (5,5), 0) #高斯模糊, (5,5)為size需奇數, 0為自動
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2) #二值化
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(img, contours, -1, (0,0,255), 1)

for cnt in contours:
    if cv2.contourArea(cnt) > 2300 and cv2.contourArea(cnt) < 140000:
        area = cv2.contourArea(cnt)
        # print(f'面積:{area}')
        
        [x,y,w,h] = cv2.boundingRect(cnt)
        if w > 450:
            # print(f'寬:{w}, 高:{h}')
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
            #cv2.imshow('img', img)
            
            number = img[y:y+h, x:x+w]
            #cv2.imshow('car', number)

            gray = cv2.cvtColor(number, cv2.COLOR_BGR2GRAY) #轉灰階
            blur = cv2.GaussianBlur(gray, (3,3), 0) #高斯模糊, (5,5)為size需奇數, 0為自動

            # 車牌辨識
            ocr_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.pytesseract.tesseract_cmd = ocr_path
            txt = pytesseract.image_to_string(
                    blur, 
                    lang = 'eng',
                    config = "-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 10"
                )
            print(f'車牌: {txt.strip()}')
            #cv2.waitKey(0)

# cv2.imshow('img', img)
# cv2.waitKey()
#cv2.destroyAllWindows()
