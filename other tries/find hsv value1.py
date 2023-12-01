import cv2

def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_value = hsv_frame[y, x]
        print("HSV Value at ({}, {}): {}".format(x, y, hsv_value))

# Open the video file
video_path = 'metronomes_slowed.mp4'
cap = cv2.VideoCapture(video_path)

# Check if video file is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Create a window to display the video
cv2.namedWindow("Video")

# Set the mouse callback function
cv2.setMouseCallback("Video", get_hsv_value)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If the frame is not read properly, exit the loop
    if not ret:
        break

    # Display the frame
    cv2.imshow("Video", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
