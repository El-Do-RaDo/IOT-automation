from lcd import lcd_prt
import cv2
from gpiozero import LED
vc = cv2.VideoCapture(0)
led17 = LED(17)
led18 = LED(18)

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    ret, frame = vc.read()
    frame = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    led17_cond = 0
    led18_cond = 0
    count = 0
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5
    )
    
    if len(faces) == 0:
        led17.on()
        led18.on()
        #lcd_prt("LIGHT_OFF")
    
    for (x, y, w, h) in faces:
        print(" x: ", x, " y: ", y, " w: ", w, " h: ", h)
        count = str(len(faces))
        lcd_prt(count)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        if (x > 160):
            led17.off()
            led17_cond = 1
            #lcd_prt("LEFT_LIGHT_ON")
        elif(led17_cond == 0):
            led17.on()
            #lcd_prt("LEFT_LIGHT_OFF")
        if (x+h < 160):
            led18.off()
            led18_cond = 1
            #lcd_prt("RIGHT_LIGHT_ON")
        elif(led18_cond == 0):
            led18.on()
            #lcd_prt("RIGHT_LIGHT_OFF")
    
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vc.release()
cv2.destroyAllWindows()