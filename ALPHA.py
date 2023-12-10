# author:Devyash Saini
import cv2
import face_recognition
import time
import json
import os
import pickle

# with open("apiArchive.json", "r") as f:
#     api = json.load(f)

class User():
    def verify(auth):
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        print("Authenticating...")

        if os.path.exists("models.pickle"):
            print("--> Pickle Located")
            with open("models.pickle", "rb") as model:
                res = pickle.load(model)
                my_face_encoding = res["Devyash.tds"]
        else:
            import numpy as np
            my_face_encoding = np.load("main.tds.npy")

        start_time = time.time()
        found_me = False

        video_capture = cv2.VideoCapture(0)

        wt = 5 if auth else 300
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

            wt = 10 if auth else 300
            for face_encoding, face_location in zip(face_encodings, face_locations):
                if auth:
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
                else:
                    results = face_recognition.compare_faces(list(res.values()), face_encoding)
                    c = 0
                    for i in results:
                        if i:
                            name = list(res.keys())[c]
                            top, right, bottom, left = face_location
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                            face_locations.remove(face_location)
                            break
                        c += 1
            
            for i in face_locations:
                top, right, bottom, left = i
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "anjaana", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            cv2.imshow('Press q to exit authentication...', frame)
                
            if found_me and auth:
                return True
            
        if not found_me and auth:
            return False
        
        if not auth:
            return True

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

                if os.path.exists("models.pickle"):
                    with open("models.pickle", "rb") as model:
                        res = pickle.load(model)
                        # print(res)
                else:
                    res = {}

                res[name + '.tds'] = face_encodings[0]
                
                with open("models.pickle", "wb") as model:
                    pickle.dump(res, model)

                trained = True
                break

            for face_encoding, face_location in zip(face_encodings, face_locations):
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                cv2.imshow('Press q to exit training...', frame)

        video_capture.release()
        cv2.destroyAllWindows()
        print(f"Training Complete! Your face model ({name + '.tds'}) has been saved without errors...") if trained else print("Training Failed! Please try again.")