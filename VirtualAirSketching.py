import numpy as np
import cv2
from flask import Flask, render_template, request
from threading import Thread
from collections import deque
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# Flask app setup
app = Flask(__name__)

# Default trackbar callback function
def setValues(x):
    pass

@app.route('/')
def home():
    return render_template('frontend.html')

@app.route('/draw', methods=['POST'])
def draw():
    return "Draw endpoint placeholder"

# Show save confirmation dialog
def show_save_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    messagebox.showinfo("Save Confirmation", "Drawing saved as 'drawing.png' and 'drawing.pdf'!")
    root.destroy()

# OpenCV Drawing Loop
def opencv_loop():
    # Initialize OpenCV windows
    cv2.namedWindow("Color detectors", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)

    # Resize the "Tracking" window
    cv2.resizeWindow("Tracking", 1400, 800)

    cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
    cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
    cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
    cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
    cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
    cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)

    # Color settings
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 255)]  # Includes eraser
    colorIndex = 0
    bpoints, gpoints, rpoints, ypoints = [deque(maxlen=512) for _ in range(4)]
    blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Webcam not found or cannot be accessed!")
        return

    # Canvas for drawing
    canvas = None
    prev_center = None  # Previous pointer position for movement reset

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame from webcam!")
                break

            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape

            if canvas is None:
                canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Get HSV values from trackbars
            u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
            u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
            u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
            l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
            l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
            l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")

            Upper_hsv = np.array([u_hue, u_saturation, u_value])
            Lower_hsv = np.array([l_hue, l_saturation, l_value])

            # Mask creation
            mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
            mask = cv2.erode(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=1)

            # Detect contours for pointer
            cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            center = None

            if len(cnts) > 0:
                cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    # Reset the pointer deque if movement is large
                    if prev_center and np.linalg.norm(np.array(center) - np.array(prev_center)) > 50:
                        bpoints, gpoints, rpoints, ypoints = [deque(maxlen=512) for _ in range(4)]
                        blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0

                    prev_center = center

                    # Draw the pointer circle for visual feedback
                    cv2.circle(frame, center, 20, (0, 255, 0), 5)  # Larger pointer circle

                    # Check if the pointer is in the top region (to interact with buttons)
                    if center[1] <= 50:
                        if 20 <= center[0] <= 100:  # Clear All
                            bpoints, gpoints, rpoints, ypoints = [deque(maxlen=512) for _ in range(4)]
                            blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0
                            canvas[:, :, :] = 0  # Clear the canvas
                        elif 120 <= center[0] <= 180:
                            colorIndex = 0  # Blue
                        elif 200 <= center[0] <= 260:
                            colorIndex = 1  # Green
                        elif 280 <= center[0] <= 340:
                            colorIndex = 2  # Red
                        elif 360 <= center[0] <= 420:
                            colorIndex = 3  # Yellow
                        elif 440 <= center[0] <= 520:  # Save Button
                            save_image(canvas)
                            save_as_pdf(canvas)
                            show_save_dialog()
                    else:
                        # Add points to the appropriate deque
                        if colorIndex == 0:
                            while len(bpoints) <= blue_index:
                                bpoints.append(deque(maxlen=512))
                            bpoints[blue_index].appendleft(center)
                        elif colorIndex == 1:
                            while len(gpoints) <= green_index:
                                gpoints.append(deque(maxlen=512))
                            gpoints[green_index].appendleft(center)
                        elif colorIndex == 2:
                            while len(rpoints) <= red_index:
                                rpoints.append(deque(maxlen=512))
                            rpoints[red_index].appendleft(center)
                        elif colorIndex == 3:
                            while len(ypoints) <= yellow_index:
                                ypoints.append(deque(maxlen=512))
                            ypoints[yellow_index].appendleft(center)

            # Draw points directly on the canvas
            points = [bpoints, gpoints, rpoints, ypoints]
            for i, color_points in enumerate(points):
                for j in range(len(color_points)):
                    for k in range(1, len(color_points[j])):
                        if color_points[j][k - 1] is None or color_points[j][k] is None:
                            continue
                        cv2.line(canvas, color_points[j][k - 1], color_points[j][k], colors[i], 5)  # Thicker lines

            # Merge canvas with the frame
            frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

            # Add buttons to the frame
            frame = cv2.rectangle(frame, (20, 1), (100, 50), (122, 122, 122), -1)  # Clear
            frame = cv2.rectangle(frame, (120, 1), (180, 50), colors[0], -1)  # Blue
            frame = cv2.rectangle(frame, (200, 1), (260, 50), colors[1], -1)  # Green
            frame = cv2.rectangle(frame, (280, 1), (340, 50), colors[2], -1)  # Red
            frame = cv2.rectangle(frame, (360, 1), (420, 50), colors[3], -1)  # Yellow
            frame = cv2.rectangle(frame, (440, 1), (520, 50), (0, 255, 0), -1)  # Save

            cv2.putText(frame, "CLEAR", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "SAVE", (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the tracking window
            cv2.imshow("Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Save the canvas as an image
def save_image(canvas):
    cv2.imwrite("drawing.png", canvas)
    print("Image saved as 'drawing.png'")

# Save the canvas as a PDF
def save_as_pdf(canvas):
    image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    image.save("drawing.pdf", "PDF")
    print("PDF saved as 'drawing.pdf'")

# Run OpenCV in a separate thread
opencv_thread = Thread(target=opencv_loop)
opencv_thread.daemon = True
opencv_thread.start()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
