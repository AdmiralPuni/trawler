import cv2

# Opens the Video file
cap= cv2.VideoCapture('input/video/6.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i%5 == 0:
        cv2.imwrite('output/video/6-' + str(i) + '.jpg',frame)
    i+=1

cap.release()
cv2.destroyAllWindows()