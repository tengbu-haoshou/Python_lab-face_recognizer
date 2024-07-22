#!/usr/bin/env python3

#
# test_recognize_face.py
#
# Date    : 2024-05-26
# Author  : Hirotoshi FUJIBE
# History :
#
# Copyright (c) 2024 Hirotoshi FUJIBE
#

# Import Libraries
import cv2
import matplotlib.pyplot as plt


# Main
def main() -> None:

    cascade_file = '.\\xml\\haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(cascade_file)
    image_org = cv2.imread('.\\input\\face.jpg')
    image_gray = cv2.cvtColor(image_org, cv2.COLOR_BGR2GRAY)
    face_list = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    for (x, y, w, h) in face_list:
        red = (0, 0, 255)
        cv2.rectangle(image_org, (x, y), (x + w, y + h), red, thickness=5)
    cv2.imwrite('.\\output\\face.jpg', image_org)
    plt.imshow(cv2.cvtColor(image_org, cv2.COLOR_BGR2RGB))
    plt.show()


# Goto Main
if __name__ == '__main__':
    main()
