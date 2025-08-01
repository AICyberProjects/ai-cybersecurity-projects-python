import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# ----------------------------
# Configuration
# ----------------------------
VIDEO_PATH = "video_input/sample.mp4"
FRAME_FOLDER = "frames"
MODEL_PATH = "saved_model.h5"
FRAME_INTERVAL = 5
IMAGE_SIZE = (128, 128)

# ----------------------------
# Extract frames from video
# ----------------------------
def extract_frames(video_path, output_folder, interval):
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created frame output folder: {output_folder}")
    else:
        for file in os.listdir(output_folder):
            if file.endswith(".jpg"):
                os.remove(os.path.join(output_folder, file))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return 0

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {saved_count} frames every {interval} frame(s).")
    return saved_count

# ----------------------------
# Classify a single frame
# ----------------------------
def classify_frame(image_path, model):
    img = load_img(image_path, target_size=IMAGE_SIZE)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)[0][0]
    return prediction

# ----------------------------
# Analyze all extracted frames
# ----------------------------
def analyze_frames(model, frame_folder):
    results = []

    print("Classifying extracted frames...\n")
    for filename in sorted(os.listdir(frame_folder)):
        if filename.lower().endswith(".jpg"):
            frame_path = os.path.join(frame_folder, filename)
            score = classify_frame(frame_path, model)
            label = "FAKE" if score > 0.5 else "REAL"
            print(f"{filename}: {label} ({score:.2f})")
            results.append(score)

    if not results:
        print("No frames found or analyzed.")
        return

    avg_score = sum(results) / len(results)
    print("Final verdict based on frame analysis:")
    if avg_score > 0.5:
        print(f"Deepfake Likely! Average fake confidence: {avg_score:.2f}")
    else:
        print(f"Video appears real. Average fake confidence: {avg_score:.2f}")

# ----------------------------
# Main logic
# ----------------------------
if __name__ == "__main__":
    print(f"Analyzing video: {VIDEO_PATH}")
    print(f"Using model: {MODEL_PATH}")
    print(f"Extracting every {FRAME_INTERVAL}th frame...\n")

    frame_count = extract_frames(VIDEO_PATH, FRAME_FOLDER, FRAME_INTERVAL)

    if frame_count > 0:
        model = load_model(MODEL_PATH)
        analyze_frames(model, FRAME_FOLDER)


