import os
import cv2
import pickle
import face_recognition

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")
# print(image_dir)

all_face_encodings = []
all_face_know = []
for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename((os.path.basename((path)).lower()))
                image_ = face_recognition.load_image_file(os.path.join(root,file))
                all_face_encodings.append((face_recognition.face_encodings(image_)[0]))
                all_face_know.append((label)[0])
                print(all_face_know)

with open('dataset_faces.xml', 'wb') as f:
    pickle.dump(all_face_encodings, f)
with open('dataset_label.xml', 'wb') as f:
    pickle.dump(all_face_know, f)
