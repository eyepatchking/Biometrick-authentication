import numpy as np
from PIL import Image
import os
import cv2


def train_classifer(name):
    path = os.path.join(os.getcwd(), "data", name)

    # BUG FIX G: papka mavjudligini tekshirish
    if not os.path.exists(path):
        print(f"Error: Data directory '{path}' not found.")
        return

    faces = []
    ids = []

    for root, dirs, files in os.walk(path):
        pictures = files

    for pic in pictures:
        # BUG FIX H: faqat .jpg fayllarni o'qish (boshqa fayllar xato berishi mumkin)
        if not pic.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        imgpath = os.path.join(path, pic)
        try:
            img = Image.open(imgpath).convert('L')
            imageNp = np.array(img, 'uint8')
            # BUG FIX I: fayl nomidan id ajratishda xato bo'lsa o'tkazib yuborish
            id_str = pic.split(name)[0]
            if not id_str.isdigit():
                continue
            id = int(id_str)
            faces.append(imageNp)
            ids.append(id)
        except Exception as e:
            print(f"Skipping {pic}: {e}")
            continue

    if len(faces) == 0:
        print("Error: No valid face images found for training.")
        return

    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)

    os.makedirs("./data/classifiers", exist_ok=True)
    clf.write(f"./data/classifiers/{name}_classifier.xml")
    print(f"Classifier saved: ./data/classifiers/{name}_classifier.xml")
