import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime, timedelta
import sys
import random
import PySimpleGUI as sg


def feature(result):
    # Query to fetch class information for the student within the next hour
    select = (
        "SELECT co.*, c.name as course_name, t.name as teacher_name, cr.classroom_address, l.zoom_link, \
              ltm.message, m.material_link FROM CourseOffered co \
              JOIN Course c ON co.course_code = c.course_code \
              JOIN Teacher t ON co.teacher_id = t.teacher_id \
              JOIN Classroom cr ON co.classroom_id = cr.classroom_id \
              JOIN Lecture l ON co.course_id = l.course_id \
              JOIN LectureTeacherMessage ltm ON l.course_id = ltm.course_id AND l.lecture_id = ltm.lecture_id \
              JOIN Material m ON co.course_id = m.course_id \
              WHERE co.course_id IN (SELECT course_id FROM Enrolls WHERE student_id='%s') AND \
              co.start_time >= '09:30:00' AND co.end_time < '12:30:00'"
        #   co.start_time >= CURRENT_TIME() AND co.start_time < ADDTIME(CURRENT_TIME(), '01:00:00')"
        % result[0][0]
    )
    cursor.execute(select)
    class_info = cursor.fetchall()
    print("CLASS INFO:", class_info)
    print("RESULT: ", result)

    # Case: If the student has class within one hour
    if class_info:
        message = "You have a class within one hour.\n"
        message += "Course Code: " + class_info[0][1] + "\n"
        message += "Course Name: " + class_info[0][9] + "\n"
        message += "Classroom Address: " + class_info[0][11] + "\n"
        message += "Teacher's Message: " + class_info[0][13] + "\n"
        message += "Zoom Link: " + class_info[0][12] + "\n"
        message += "Lecture Materials: " + class_info[0][14] + "\n"

        layout = [
            [
                sg.Text(
                    "Class Imminent",
                    size=(18, 1),
                    font=("Any", 18),
                    text_color="#1c86ee",
                    justification="left",
                )
            ],
            [sg.Text(message, size=(60, 8), justification="left")],
            [sg.Button("Send to my email")],
            [sg.OK()],
        ]
    # Case: If the student does not have class within one hour
    else:
        select = (
            "SELECT co.*, c.name as course_name, t.name as teacher_name, cr.classroom_address FROM CourseOffered co \
                  JOIN Course c ON co.course_code = c.course_code \
                  JOIN Teacher t ON co.teacher_id = t.teacher_id \
                  JOIN Classroom cr ON co.classroom_id = cr.classroom_id \
                  WHERE co.course_id IN (SELECT course_id FROM Enrolls WHERE student_id='%s') ORDER BY co.start_time"
            % result[0][0]
        )
        cursor.execute(select)
        timetable = cursor.fetchall()
        print("TIMETABLE: ", timetable)

        toprow = [
            "CourseCode",
            "CourseName",
            "StartTime",
            "EndTime",
            "Day",
            "Teacher",
            "Classroom",
        ]
        rows = [
            [
                class_info[1],
                class_info[9],
                f"{timedelta(seconds=class_info[4].seconds).seconds // 3600:02d}:{timedelta(seconds=class_info[4].seconds).seconds // 60 % 60:02d}",  # StartTime
                f"{timedelta(seconds=class_info[5].seconds).seconds // 3600:02d}:{timedelta(seconds=class_info[5].seconds).seconds // 60 % 60:02d}",  # EndTime
                class_info[6],
                class_info[10],
                class_info[11],
            ]
            for class_info in timetable
        ]
        tbl1 = sg.Table(
            values=rows,
            headings=toprow,
            auto_size_columns=True,
            display_row_numbers=False,
            justification="center",
            key="-TABLE-",
            selected_row_colors="red on yellow",
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True,
        )

        layout = [
            [
                sg.Text(
                    "Class TimeTable",
                    size=(18, 1),
                    font=("Any", 18),
                    text_color="#1c86ee",
                    justification="left",
                )
            ],
            [tbl1],
            [sg.OK()],
        ]
    win = sg.Window(
        "Attendance System",
        default_element_size=(21, 1),
        text_justification="right",
        auto_size_text=False,
    ).Layout(layout)

    while True:
        event, _ = win.Read(timeout=20)
        print(f"Event: {event}")
        if event is None or event == "OK":
            win.close()
            break
        # This feature does not really send the email
        elif event == "Send to my email":
            win.close()
            select = (
                "SELECT email FROM Student WHERE student_id='%s'"
                % result[0][0]
            )
            cursor.execute(select)
            email = cursor.fetchall()
            layout = [
                [sg.Text(f"Email sent to {email[0][0]}, please check your inbox.")],
                [sg.Button("OK")],
            ]
            win = sg.Window("Confirmation").Layout(layout)
            if event is None or event == "OK":
                win.close()
                break


def system_start():
    layout = [
        [
            sg.Text(
                "Setting",
                size=(18, 1),
                font=("Any", 18),
                text_color="#1c86ee",
                justification="left",
            )
        ],
        [
            sg.Text("Confidence"),
            sg.Slider(
                range=(0, 100),
                orientation="h",
                resolution=1,
                default_value=60,
                size=(15, 15),
                key="confidence",
            ),
        ],
        [sg.OK(), sg.Cancel()],
    ]
    win = sg.Window(
        "Attendance System",
        default_element_size=(21, 1),
        text_justification="right",
        auto_size_text=False,
    ).Layout(layout)
    event, values = win.Read()
    if event is None or event == "Cancel":
        exit()
    args = values
    return (args["confidence"], False)


def authenticate(cap, face_cascade, recognizer, engine, rate, gui_confidence):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for x, y, w, h in faces:
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # If the face is recognized
        if conf >= gui_confidence:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the student information in the database.
            select = (
                "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'"
                % (name)
            )
            name = cursor.execute(select)
            result = cursor.fetchall()
            data = "error"

            for x in result:
                data = x

            # If the student's information is not found in the database
            if data == "error":
                # the student's data is not in the database
                print("The student", current_name, "is NOT FOUND in the database.")

            # If the student's information is found in the database
            else:
                update = "UPDATE Student SET login_date=%s WHERE name=%s"
                val = (date, current_name)
                cursor.execute(update, val)
                update = "UPDATE Student SET login_time=%s WHERE name=%s"
                val = (current_time, current_name)
                cursor.execute(update, val)
                myconn.commit()

                hello = ("Hello ", current_name, " authorized")
                print(hello)
                engine.say(hello)

                return (result, frame)

        # If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = "Your face is not recognized"
            print(hello)
            engine.say(hello)
    return (None, frame)


# 1 Create database connection
myconn = mysql.connector.connect(
    host="localhost", user="root", passwd="admin123", database="facerecognition"
)
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()


# 2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)


# 3 Define pysimplegui setting
gui_confidence, win_started = system_start()
authenticated = False

# 4 Open the camera and start face recognition
while True:
    student_data, frame = authenticate(
        cap=cap,
        face_cascade=face_cascade,
        recognizer=recognizer,
        engine=engine,
        rate=rate,
        gui_confidence=gui_confidence,
    )

    if not authenticated and student_data:
        authenticated = True
        feature(student_data)
    else:
        # GUI
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        if not win_started:
            win_started = True
            layout = [
                [sg.Text("Attendance System Interface", size=(30, 1))],
                [sg.Image(data=imgbytes, key="_IMAGE_")],
                [
                    sg.Text("Confidence"),
                    sg.Slider(
                        range=(0, 100),
                        orientation="h",
                        resolution=1,
                        default_value=60,
                        size=(15, 15),
                        key="confidence",
                    ),
                ],
                [sg.Exit()],
            ]
            win = (
                sg.Window(
                    "Attendance System",
                    default_element_size=(14, 1),
                    text_justification="right",
                    auto_size_text=False,
                )
                .Layout(layout)
                .Finalize()
            )
            image_elem = win.FindElement("_IMAGE_")
        else:
            image_elem.Update(data=imgbytes)

        event, values = win.Read(timeout=20)
        if event is None or event == "Exit":
            win.close()
            break
        gui_confidence = values["confidence"]


win.close()
cap.release()
