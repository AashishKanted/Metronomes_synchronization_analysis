
import cv2
import numpy as np

# Global variables
drawing = False
ix, iy = -1, -1
bbox = None
initial_color = None
threshold = 50
paused = False

# Mouse callback function
def draw_bbox(event, x, y, flags, param):
    global drawing, ix, iy, bbox, initial_color

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bbox = (ix, iy, x, y)
        initial_color = np.mean(frame[iy:y, ix:x], axis=(0, 1))

# Read the input video
cap = cv2.VideoCapture('metronomes_slowed.mp4')

# Create a window
cv2.namedWindow('Video')

# Set the mouse callback function
cv2.setMouseCallback('Video', draw_bbox)

while cap.isOpened():
    if not paused:
        ret, frame = cap.read()

        if not ret:
            break

        # Draw the bounding box
        if bbox is not None:
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

            # Calculate the average color inside the bounding box
            current_color = np.mean(frame[bbox[1]:bbox[3], bbox[0]:bbox[2]], axis=(0, 1))

            # Compare the color difference with the initial color
            color_diff = np.linalg.norm(current_color - initial_color)

            # If the color difference exceeds the threshold, record the time
            if color_diff > threshold:
                current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                print(f"Color change detected at time: {current_time} seconds")

        # Display the video frame
        cv2.imshow('Video', frame)

    # Handle key presses
    key = cv2.waitKey(25)
    if key == ord('q'):
        break
    elif key == ord(' '):
        paused = not paused
    elif key == ord('a'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)
        paused = True
    elif key == ord('d'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + 1)
        paused = True

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
