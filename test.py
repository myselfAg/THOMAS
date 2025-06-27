import streamlit as st
import cv2
import tempfile
from ultralytics import YOLO
from PIL import Image
import numpy as np
import time

st.set_page_config(layout="wide")
st.title("🚆 Train Seat and Human Detection")

# Load YOLOv8 model (replace with your custom model if available)
model = YOLO("yolov8n.pt")  # Use YOLO("best.pt") for a custom model

# Detect objects and return image + lists of seats/persons
def detect_objects(image):
    results = model(image)[0]
    boxes = results.boxes
    classes = results.names

    seats = []
    persons = []

    for i, box in enumerate(boxes.xyxy.cpu().numpy()):
        class_id = int(boxes.cls[i].cpu().numpy())
        class_name = classes[class_id]
        x1, y1, x2, y2 = box.astype(int)
        bbox = (x1, y1, x2, y2)

        if class_name == "seat":
            seats.append(bbox)
        elif class_name == "person":
            persons.append(bbox)

    result_img = results.plot()
    return result_img, seats, persons

# Calculate occupancy and density
def calculate_occupancy(seats, persons, iou_threshold=0.3):
    def iou(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        iou_val = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
        return iou_val

    occupied = 0
    for seat in seats:
        for person in persons:
            if iou(seat, person) > iou_threshold:
                occupied += 1
                break

    total = len(seats)
    available = total - occupied
    occupancy_rate = (occupied / total) * 100 if total > 0 else 0

    if occupancy_rate >= 80:
        density = "High"
    elif occupancy_rate >= 50:
        density = "Medium"
    else:
        density = "Low"

    return total, occupied, available, occupancy_rate, density

# Sidebar input option
option = st.sidebar.selectbox("Select Input Source", ("Image Upload", "Video Upload", "Webcam Image", "Webcam Live"))

# --- IMAGE UPLOAD ---
if option == "Image Upload":
    file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if file:
        image = Image.open(file)
        image_np = np.array(image)
        st.image(image_np, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Detecting..."):
            result_img, seats, persons = detect_objects(image_np)
            total, occupied, available, percent, density = calculate_occupancy(seats, persons)

        col1, col2 = st.columns(2)
        col1.image(result_img, caption="Detection Result", use_column_width=True)
        with col2:
            st.metric("🧍 Total Persons", len(persons))

# --- VIDEO UPLOAD ---
elif option == "Video Upload":
    file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
    if file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        cap = cv2.VideoCapture(tfile.name)
        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result_img, seats, persons = detect_objects(frame)
            total, occupied, available, percent, density = calculate_occupancy(seats, persons)
            overlay = f"Seats: {total}, Occupied: {occupied}, Available: {available}, Persons: {len(persons)}, {percent:.1f}% - {density}"
            cv2.putText(result_img, overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            stframe.image(result_img, channels="RGB", use_column_width=True)
        cap.release()

# --- WEBCAM IMAGE ---
elif option == "Webcam Image":
    img_file = st.camera_input("Take a picture")
    if img_file:
        image = Image.open(img_file)
        image_np = np.array(image)
        st.image(image_np, caption="Captured Image", use_column_width=True)

        with st.spinner("Detecting..."):
            result_img, seats, persons = detect_objects(image_np)
            total, occupied, available, percent, density = calculate_occupancy(seats, persons)

        col1, col2 = st.columns(2)
        col1.image(result_img, caption="Detection Result", use_column_width=True)
        with col2:
            st.metric("", len(persons))

# --- WEBCAM LIVE STREAM ---
elif option == "Webcam Live":
    if st.button("Start Webcam"):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("Unable to access webcam.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result_img, seats, persons = detect_objects(frame)
            total, occupied, available, percent, density = calculate_occupancy(seats, persons)
            overlay = f"Total Persons: {len(persons)}"
            cv2.putText(result_img, overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            stframe.image(result_img, channels="RGB", use_column_width=True)
            time.sleep(0.1)
        cap.release()