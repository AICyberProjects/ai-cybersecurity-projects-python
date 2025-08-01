import cv2
import os
from datetime import datetime

# ----------------------------
# Create output folder
# ----------------------------
OUTPUT_FOLDER = "captured_frames"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ----------------------------
# Open webcam (0 = default camera)
# ----------------------------
cap = cv2.VideoCapture(0)

# ----------------------------
# Read the first frame
# ----------------------------
ret, prev_frame = cap.read()
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)

img_count = 1
print("Surveillance system started. Press 'q' to quit.")

# ----------------------------
# Main Loop
# ----------------------------
while True:
    # Read next frame
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compare with previous frame
    frame_diff = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save frame if motion is detected
    if motion_detected:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"motion_{timestamp}.jpg"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        cv2.imwrite(filepath, frame)
        print(f"[+] Motion detected! Saved: {filename}")
        img_count += 1

    cv2.imshow("Live Surveillance", frame)

    # Press 'q' to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    # Update the previous frame
    prev_frame = gray

# ----------------------------
# Cleanup
# ----------------------------
cap.release()
cv2.destroyAllWindows()
print("Surveillance ended.")






