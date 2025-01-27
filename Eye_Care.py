import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
from plyer import notification
import pygame
import time
import threading

# Initialize video capture and face mesh detector
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

# Initialize the live plot for visualizing eye aspect ratio
plotY = LivePlot(640, 360, [20, 50])

# Key facial landmarks for detecting eye region
idList = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]

# Initialize variables for eye ratio tracking and states
ratioList = []
counter = 0
color = (0, 0, 255)

# Thresholds and timers for notifications and alarms
open_start_time = None
close_start_time = None
open_threshold_duration = 5  # Time (seconds) before blinking reminder
close_threshold_duration = 5  # Time (seconds) before alarm for closed eyes

# Flags to manage threading
alarm_thread_running = False
notification_thread_running = False
stop_alarm = False


def show_notification():
    """Send a desktop notification to remind the user to blink."""
    global notification_thread_running
    notification_thread_running = True
    notification.notify(
        title="Eye Care Reminder",
        message="Remember to Blink!",
        timeout=5
    )
    notification_thread_running = False


def play_alarm():
    """Play an alarm sound if the eyes are closed for too long."""
    global alarm_thread_running, stop_alarm
    alarm_thread_running = True
    pygame.mixer.init()
    pygame.mixer.music.load('Alarm.wav')  # Ensure 'Alarm.wav' is in the same directory
    pygame.mixer.music.play(-1)
    while not stop_alarm:
        time.sleep(0.1)
    pygame.mixer.music.stop()
    alarm_thread_running = False


while True:
    # Capture a frame from the webcam
    success, img = cap.read()

    # Detect face and its landmarks
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        # Process the first detected face
        face = faces[0]

        # Draw circles around key eye landmarks
        for id in idList:
            cv2.circle(img, face[id], 2, color, cv2.FILLED)

        # Calculate vertical and horizontal distances of the left eye
        leftUp, leftDown = face[159], face[145]
        leftLeft, leftRight = face[33], face[133]
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        # Compute eye aspect ratio
        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 5:  # Maintain a moving average
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        # Blink detection and visualization
        if ratioAvg < 25.5 and counter == 0:  # Detect a blink
            color = (0, 200, 0)  # Green for blink
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 15:  # Reset after counting enough frames
                counter = 0
                color = (0, 0, 255)

        # Check for prolonged open eyes to trigger blinking reminder
        if ratioAvg > 26.5:  # Adjust threshold as needed
            if open_start_time is None:
                open_start_time = time.time()
            elif time.time() - open_start_time > open_threshold_duration:
                if not notification_thread_running:  # Avoid duplicate notifications
                    threading.Thread(target=show_notification).start()
                open_start_time = None
        else:
            open_start_time = None

        # Check for prolonged closed eyes to trigger alarm
        if ratioAvg < 23:  # Adjust threshold as needed
            if close_start_time is None:
                close_start_time = time.time()
            elif time.time() - close_start_time > close_threshold_duration:
                if not alarm_thread_running:  # Avoid duplicate alarms
                    stop_alarm = False
                    threading.Thread(target=play_alarm).start()
        else:
            close_start_time = None
            if alarm_thread_running:
                stop_alarm = True  # Stop alarm when eyes open

        # Update and display the live plot
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 1, 1)

    else:
        # Display the frame even if no face is detected
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 1, 1)

    # Show the combined output of video feed and plot
    cv2.imshow("Eye Care System", imgStack)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources on exit
stop_alarm = True  # Ensure alarm thread stops
cap.release()
cv2.destroyAllWindows()
