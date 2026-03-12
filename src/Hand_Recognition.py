import mediapipe as mp
import cv2

vc = cv2.VideoCapture(0)
if vc.isOpened():
    read_val, frame = vc.read()
else:
    read_val = False

while read_val:
    cv2.imshow('Video', frame)
    read_val, frame = vc.read()
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyWindow('Video')
vc.release()