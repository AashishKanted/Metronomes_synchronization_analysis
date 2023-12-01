import cv2

def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_value = hsv[y, x]
        print("HSV value at ({}, {}): {}".format(x, y, hsv_value))

# Create a video capture object
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Unable to open the webcam")
    exit()

# Create a window and set the callback function
cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", get_hsv_value)

while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is successfully read
    if not ret:
        print("Unable to read frame from the webcam")
        break

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
