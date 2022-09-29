import cv2
import os
from glob import glob
import numpy
from . import image_resizing
from ..constraits import constants as cnst


def train_recognizer(faces_path, databases_path, face_width=500, face_height=500):
    recognizer_LBPH = cv2.face.LBPHFaceRecognizer_create()
    recognizer_Fisher = cv2.face.FisherFaceRecognizer_create()
    print(' Training recognizer...')

    faces_LBPH = []
    faces_Fischer = []
    ids = []

    people_faces = os.listdir(faces_path)
    id_number = 1
    for person in people_faces:
        photos_paths = []
        for extension in ['jpg', 'jpeg', 'png']:
            photos_paths.extend(glob(os.path.join(faces_path, person, '**.' + extension)))
        photos_paths.sort()

        for photo_path in photos_paths:
            gray_face_LBPH = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)
            gray_face_Fischer = image_resizing.resize_image(gray_face_LBPH, face_width, face_height, False)

            faces_LBPH.append(gray_face_LBPH)
            faces_Fischer.append(gray_face_Fischer)
            ids.append(id_number)

        id_number += 1

    recognizer_LBPH.train(faces_LBPH, numpy.array(ids))
    recognizer_Fisher.train(faces_Fischer, numpy.array(ids))

    if not os.path.exists(databases_path):
        os.mkdir(databases_path)

    recognizer_Fisher.write(os.path.join(databases_path, cnst.fisher_database))
    recognizer_LBPH.write(os.path.join(databases_path, cnst.lbph_database))

    print(' Train was successful')
    return None
