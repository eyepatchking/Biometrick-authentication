import cv2
from time import time
from tkinter import messagebox
import os


def main_app(name, timeout=5):
    # BUG FIX A: classifier fayli mavjudligini tekshirish
    classifier_path = f"./data/classifiers/{name}_classifier.xml"
    if not os.path.exists(classifier_path):
        messagebox.showerror("ERROR", f"Classifier not found for '{name}'. Please train the model first.")
        return

    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(classifier_path)

    cap = cv2.VideoCapture(0)
    # BUG FIX B: kamera ochilganini tekshirish
    if not cap.isOpened():
        messagebox.showerror("ERROR", "Could not open camera!")
        return

    pred = False
    start_time = time()

    while True:
        ret, frame = cap.read()
        # BUG FIX C: frame o'qilganini tekshirish
        if not ret or frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id, confidence = recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)

            if confidence > 50:
                pred = True
                text = 'Recognized: ' + name.upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else:
                pred = False
                text = "Unknown Face"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow("image", frame)

        elapsed_time = time() - start_time
        if elapsed_time >= timeout:
            if pred:
                messagebox.showinfo('Congrat', 'You have been successfully recognized!')
            else:
                messagebox.showerror('Alert', 'Face not recognized. Please try again.')
            break

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
