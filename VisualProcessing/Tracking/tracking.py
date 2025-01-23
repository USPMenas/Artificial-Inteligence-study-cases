import cv2
print(cv2.__version__)


# Initialize video capture (0 for default camera)
cap = cv2.VideoCapture(0)

while True:
    # Read two consecutive frames
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    # Convert to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between frames
    diff = cv2.absdiff(gray1, gray2)

    # Apply threshold to highlight regions of movement
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Optional: Use morphological operations to clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Detect contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected movement
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter small movements
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow("Movement Detection", frame1)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
