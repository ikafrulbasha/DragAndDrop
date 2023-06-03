import cv2
from cvzone.HandTrackingModule import HandDetector

class DragRect():
    def __init__(self, posCenter, size=[150,150]):
        self.posCenter = posCenter
        self.size = size

    def update(self,cursor):
        cx,cy = self.posCenter
        w,h = self.size
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

if __name__ == '__main__':
    print('Starting Drag & Drop application...')
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    detector = HandDetector(detectionCon=0.8)
    color = (255,0,255)
    cx,cy,w,h = 100,100,200,200
    rectList = []
    for i in range(6):
        rectList.append(DragRect([i*200+100,100]))
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img)
        if lmList: #is there a hand
            l,_,_ = detector.findDistance(8,12,img)
            if l < 60:
                cursor = lmList[8] #index finger
                for rect in rectList:
                    rect.update(cursor)

        for rect in rectList:
            cx, cy = rect.posCenter
            w, h = rect.size
            cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), color, cv2.FILLED)

        cv2.imshow("Image",img)
        cv2.waitKey(1)



