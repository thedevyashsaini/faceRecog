# author: Devyash Saini
import cv2
import face_recognition
import time
import json
import os
import numpy as np
import pickle

# with open("apiArchive.json", "r") as f:
#     api = json.load(f)

class User():
    def verify(auth):
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        print("Authenticating...")

        my_face_encoding = np.load("main.tds.npy")

        start_time = time.time()
        found_me = False

        video_capture = cv2.VideoCapture(0)

        wt = 5
        while time.time() - start_time < wt:
            ret, frame = video_capture.read()
            frame = cv2.flip(frame, 1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            face_locations = face_recognition.face_locations(frame)
            
            if len(face_locations) == 0:
                found_me = False
                continue
            
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            wt = 10
            for face_encoding, face_location in zip(face_encodings, face_locations):
                if found_me:
                    return True
                
                results = face_recognition.compare_faces([my_face_encoding], face_encoding)
                if results[0]:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    found_me = True
                else:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.imshow('Press q to exit authentication...', frame)
                
            if found_me:
                return True
            
        if not found_me:
            return False

        video_capture.release()
        cv2.destroyAllWindows()

    def train(name):
        if not name: 
            return False, "Error (ALPHA.py, User.train): Train method expects a name parameter"
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        print("Loading Video Buffer (press s to finalise a frame)")

        video_capture = cv2.VideoCapture(0)
        start_time = time.time()
        trained = False

        while time.time() - start_time < 30:
            entered = cv2.waitKey(1)

            if entered & 0xFF == ord('q'):
                break

            ret, frame = video_capture.read()
            frame = cv2.flip(frame, 1)

            face_locations = face_recognition.face_locations(frame)

            if len(face_locations) == 0:
                continue

            face_encodings = face_recognition.face_encodings(frame, face_locations)

            t = str(time.time())

            if entered & 0xFF == ord('s'):
                with open("models.pickle", "rb") as model:
                    res = pickle.load(model)
                    res = json.loads(res)
                    res["./models/" + name + "." + t] = face_encodings[0]
                    pickle.dump(res, model)
                trained = True
                break

            for face_encoding, face_location in zip(face_encodings, face_locations):
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                cv2.imshow('Press q to exit training...', frame)

        video_capture.release()
        cv2.destroyAllWindows()
        print("Training Complete! Your face model has been saved as " + name + "." + t + ".tds.npy in the models directory") if trained else print("Training Failed! Please try again.")