from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse
from employees.models import Employee
import face_recognition
import cv2
import numpy as np
import pickle
from django.utils import timezone
import datetime
import time
import os


# Create your views here.


def detect(request):
    employees = Employee.objects.all()
        # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    with open('dataset_faces.xml', 'rb') as f:
        data_encoding = pickle.load(f)
    with open('dataset_label.xml', 'rb') as f:
        data_known=pickle.load(f)

   
    # print(data)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(data_encoding, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = data_known[first_match_index]
                    context={
                            'x':'Sucessfull ✅'
                            }
                    for employee in employees:
                        store_corporate = Employee.objects.get(id=name)
                        if store_corporate.in_out == False:
                            store_corporate.in_out = True
                            store_corporate.in_time = datetime.datetime.now()
                            store_corporate.how_many_times += 1
                            diff1 = float(store_corporate.in_time.strftime('%S.%f'))-float(store_corporate.out_time.strftime('%S.%f'))
                            store_corporate.time_outside_office += datetime.timedelta( seconds=diff1)
                            store_corporate.save()
                            cv2.destroyAllWindows()
                            return render(request,'employees/index.html',context)    
                        elif store_corporate.in_out == True:
                            store_corporate.in_out = False
                            store_corporate.out_time = datetime.datetime.now()
                            store_corporate.save()
                            cv2.destroyAllWindows()
                            return render(request,'employees/index.html',context)
                else:
                    context={
                            'x':'Not Sucessfull ❎'
                            }
                    return render(request,'employees/index.html',context)
    return render(request,'employees/index.html',context)

def index(request):
    employees = Employee.objects.all()
    for employee in employees:
        store_corporate = Employee.objects.get(id=1)
        store_corporate.name = 'Not sure about this name'
        store_corporate.save()
    return render(request,'employees/index.html')

def train(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_dir = os.path.join(BASE_DIR, "images")
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
    return render(request,'employees/train.html')

def photo(request):
    employee = Employee.objects.latest('id')
    img_counter = employee.id+1
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_dir = os.path.join(BASE_DIR, "images")
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.imshow("take_photo", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            cam.release()
            cv2.destroyAllWindows()
        elif k%256 == 32:
            # SPACE pressed
            img_name = "{}.png".format(img_counter)
            cv2.imwrite(os.path.join(image_dir, img_name), frame)
            cam.release()
            cv2.destroyAllWindows()
            return render(request,'employees/photo.html')
        

def search(request):
	employeeName=request.POST['shr']
	employees=Employee.objects.filter(name__contains=employeeName)
	context={
		'keyword':employeeName,
		'employees':employees
	}
	return render(request, 'employees/employeeSearch.html',context)
