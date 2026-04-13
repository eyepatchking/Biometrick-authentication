import cv2
import os


def start_capture(name):
    path = "./data/" + name
    num_of_images = 0
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")

    try:
        os.makedirs(path)
    except FileExistsError:
        print('Directory already exists')

    vid = cv2.VideoCapture(0)
    # BUG FIX D: kamera ochilganini tekshirish
    if not vid.isOpened():
        print("Error: Could not open camera.")
        return 0

    while True:
        ret, img = vid.read()
        # BUG FIX E: frame o'qilganini tekshirish
        if not ret or img is None:
            break

        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, f"{num_of_images} images captured", (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y + h, x:x + w]

        cv2.imshow("Face Detection", img)
        key = cv2.waitKey(1) & 0xFF

        if new_img is not None:
            try:
                cv2.imwrite(f"{path}/{num_of_images}{name}.jpg", new_img)
                num_of_images += 1
            except Exception as e:
                print(f"Image save error: {e}")

        if key == ord("q") or key == 27 or num_of_images >= 300:
            break

    vid.release()
    cv2.destroyAllWindows()
    return num_of_images


def take_video(name, video):
    path = "./data/" + name
    num_of_images = 0
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")

    try:
        os.makedirs(path)
    except FileExistsError:
        print('Directory already exists')

    vid = cv2.VideoCapture(video)
    if not vid.isOpened():
        print("Error: Could not open video file.")
        return 0

    while True:
        ret, img = vid.read()
        # BUG FIX F: ret tekshirish loop boshida (oldin oxirida edi - ba'zi framlar o'tkazib yuborilardi)
        if not ret or img is None:
            break

        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, f"{num_of_images} images captured", (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y + h, x:x + w]

        cv2.imshow("Face Detection", img)
        key = cv2.waitKey(1) & 0xFF

        if new_img is not None:
            try:
                cv2.imwrite(f"{path}/{num_of_images}{name}.jpg", new_img)
                num_of_images += 1
            except Exception as e:
                print(f"Image save error: {e}")

        if key == ord("q") or key == 27 or num_of_images >= 300:
            break

    vid.release()
    cv2.destroyAllWindows()
    return num_of_images
