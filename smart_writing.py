from tkinter import *
root = Tk()
root.geometry("600x400")
root.title("Smart_Writing")
#frame 1
f1=Frame(root,width=600,height=100,bg='gray',relief=SUNKEN)
f1.pack(side=TOP)
l1=Label(f1,font=('arial',40,'bold'),text='Smart writing',fg='Steel Blue',bd=30,anchor='w')
l1.grid(row=0,column=0)
#frame 2
f2=Frame(root,width=600,height=150,relief=SUNKEN)
f2.pack()
#button
def smartwriting():
    import math
    import cv2
    import numpy as np
    import random
    from collections import deque

    cap = cv2.VideoCapture(0)
    center_points = deque()
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        blur_frame = cv2.GaussianBlur(frame, (7, 7), 0)

        # Convert from BGR to HSV color format
        hsv = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper range of hsv color to detect. Blue here
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Make elliptical kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

        # Opening morph(erosion followed by dilation)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Find all contours
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        if len(contours) > 0:
            # Find the biggest contour
            biggest_contour = max(contours, key=cv2.contourArea)

            # Find center of contour and draw filled circle
            moments = cv2.moments(biggest_contour)
            centre_of_contour = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))
            cv2.circle(frame, centre_of_contour, 5, (0, 0, 255), -1)

            # Bound the contour with circle
            ellipse = cv2.fitEllipse(biggest_contour)
            cv2.ellipse(frame, ellipse, (0, 255, 255), 2)

            # Save the center of contour so we draw line tracking it
            center_points.appendleft(centre_of_contour)

        # Draw line from center points of contour
        for i in range(1, len(center_points)):
            b = random.randint(230, 255)
            g = random.randint(100, 255)
            r = random.randint(100, 255)
            if math.sqrt(((center_points[i - 1][0] - center_points[i][0]) ** 2) + (
                        (center_points[i - 1][1] - center_points[i][1]) ** 2)) <= 50:
                cv2.line(frame, center_points[i - 1], center_points[i], (b, g, r), 4)
        cv2.imshow('original', frame)
        cv2.imshow('mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
b1 = Button(f2, text = "Write", command= smartwriting,font =('arial',25,'bold'), foreground = "Steel Blue",bd=10,bg='powder blue').place(relx=0.48, rely=0.5, anchor=CENTER)
#frame 3
f3=Frame(root,width=600,height=150,relief=SUNKEN)
f3.pack(side=BOTTOM)
l2=Label(f3,font=('arial',12,'italic'),text='Note- \n 1. Please use blue color pen for smart writing \n 2. Write in proper light \n 3. Do not use any other blue thing in your frame \n 4. Press q to quit',fg='Steel Blue',anchor='w')
l2.grid(row=0,column=0)

mainloop()