import cv2

# Opens the Video file
cap= cv2.VideoCapture('input/video/A2.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i%10 == 0:
        cv2.imwrite('output/video/A2-' + str(round(i/10)) + '.jpg',frame)
    i+=1

cap.release()
cv2.destroyAllWindows()