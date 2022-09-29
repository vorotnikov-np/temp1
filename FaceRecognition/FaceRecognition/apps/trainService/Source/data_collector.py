import cv2
import os
from glob import glob
from ..constraits import paths


def collect_data(people_path, faces_path):
    detector = cv2.CascadeClassifier(paths.haarcascade_path)
    print(' Building a database of faces...')

    people = os.listdir(people_path)

    for person in people:
        img = os.path.join(faces_path, person)
        if not os.path.exists(img):
            os.makedirs(img)

        photos_paths = []
        for extension in ['jpg', 'jpeg', 'png']:
            photos_paths.extend(glob(os.path.join(people_path, person, '**.' + extension)))
        photos_paths.sort()

        count = 0
        for photo_path in photos_paths:
            image = cv2.imread(photo_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 15, minSize=(100, 100))

            for (x, y, w, h) in faces:
                count += 1
                gray_face = gray[y: y + h, x: x + w]
                cv2.imwrite(os.path.join(faces_path, person, str(count) + '.jpg'), gray_face)

    print(' Build was successful')
    return None
