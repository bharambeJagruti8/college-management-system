import cv2
import face_recognition
import numpy as np
from .models import Student, Attendance

def run_face_scanner():
    # 1. Database se students ki photos aur unke encodings load karo
    known_face_encodings = []
    known_face_names = []
    
    students = Student.objects.exclude(profile_pic='') # Jinki photo hai unhe lo
    
    for student in students:
        image = face_recognition.load_image_file(student.profile_pic.path)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(student.roll_no)

    # 2. Webcam start karo
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1] # BGR to RGB conversion

        # Face locations aur encodings dhoondo live frame mein
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                roll_no = known_face_names[first_match_index]
                
                # Database mein attendance mark karo (Logic)
                student_obj = Student.objects.get(roll_no=roll_no)
                Attendance.objects.get_or_create(student=student_obj, date=datetime.date.today())
                name = student_obj.name

            # Frame pe rectangle aur naam draw karo
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Educore AI Attendance Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): # 'q' dabane par band ho jayega
            break

    video_capture.release()
    cv2.destroyAllWindows()