import webbrowser
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
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

sg.theme("Kayak")

# Common styling
TITLE_FONT = ("Roboto Slab", 24, "bold")
SUBTITLE_FONT = ("Roboto", 18)
BUTTON_FONT = ("Roboto", 16)
TEXT_COLOR = "#2a9d8f"
BUTTON_COLOR = ("#264653", "#e9c46a")
ALTERNATE_ROW_COLOR = "#f4a261"

BACKGROUND_COLOR = "#264653"
HEADER_COLOR = "#2a9d8f"
SLIDER_COLOR = "#e76f51"
BUTTON_HOVER_COLOR = "#f4a261"


def feature(
    result,
    cursor,
):
    # Query to fetch class information for the student within the next hour
    curr_time = datetime.now().strftime("%H:%M:%S")
    # curr_time = "14:00:00"
    one_hour_later = (datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")
    select = f"SELECT co.*, c.name as course_name,t.name as teacher_name, cr.classroom_address, l.zoom_link, \
              ltm.message, m.material_link FROM CourseOffered co \
              JOIN Course c ON co.course_code = c.course_code \
              JOIN Teacher t ON co.teacher_id = t.teacher_id \
              JOIN Classroom cr ON co.classroom_id = cr.classroom_id \
              JOIN Lecture l ON co.course_id = l.course_id \
              JOIN LectureTeacherMessage ltm ON l.course_id = ltm.course_id AND l.lecture_id = ltm.lecture_id \
              JOIN Material m ON co.course_id = m.course_id \
              WHERE co.course_id IN (SELECT course_id FROM Enrolls WHERE student_id='{result[0][0]}') AND \
              co.start_time >= '{curr_time}' AND co.end_time < '{one_hour_later}'"

    cursor.execute(select)
    class_info = cursor.fetchall()
    print("CLASS INFO:", class_info)
    print("RESULT: ", result)

    # Case: If the student has class within one hour
    if class_info:
        table_data = []
        message = ""
        courses = set()
        for item in class_info:
            if item[1] not in courses:
                courses.add(item[1])
                table_data.append(
                    [
                        item[1],  # Course Code
                        item[9],  # Course Name
                        item[11],  # Classroom Address
                        item[4],
                        item[5],
                        item[13],  # Teacher's Message
                    ]
                )
                message += f"Zoom link \n\t {item[12]} \n Notes \n"
            message += f"\t {item[14]}\n"

        table_headings = [
            "Course Code",
            "Course Name",
            "Classroom Address",
            "Class Start Time",
            "Class End Time",
            "Teacher's Message",
        ]
        sg.theme("DarkTeal9")

        grid_layout = [
            [
                sg.Text(
                    f"Class at {class_info[0][4]}",
                    size=(18, 1),
                    font=TITLE_FONT,
                    text_color=TEXT_COLOR,
                    pad=(0, 10),
                    justification="left",
                )
            ],
            [
                sg.Table(
                    values=table_data,
                    headings=table_headings,
                    max_col_width=25,
                    auto_size_columns=True,
                    justification="center",
                    num_rows=min(5, len(table_data)),
                    header_background_color=HEADER_COLOR,
                    header_text_color="white",
                    alternating_row_color=ALTERNATE_ROW_COLOR,
                    pad=(0, 10),
                )
            ],
            [
                sg.Text(
                    "Lecture Materials",
                    size=(18, 1),
                    font=TITLE_FONT,
                    text_color=TEXT_COLOR,
                    pad=(0, 10),
                    justification="left",
                )
            ],
            [
                sg.Text(message, size=(60, 8), justification="left"),
            ],
            [
                sg.Button(
                    "EMAIL",
                    button_color=BUTTON_COLOR,
                    font=BUTTON_FONT,
                    border_width=2,
                    pad=(10, 10),
                    mouseover_colors=BUTTON_HOVER_COLOR,
                )
            ],
            [
                sg.Button(
                    "OK", button_color=BUTTON_COLOR, font=BUTTON_FONT, border_width=2
                ),
            ],
        ]

    # Case: If the student does not have class within one hour
    else:
        select = f"SELECT co.*, c.name as course_name, t.name as teacher_name, cr.classroom_address FROM CourseOffered co \
                  JOIN Course c ON co.course_code = c.course_code \
                  JOIN Teacher t ON co.teacher_id = t.teacher_id \
                  JOIN Classroom cr ON co.classroom_id = cr.classroom_id \
                  WHERE co.course_id IN (SELECT course_id FROM Enrolls WHERE student_id='{result[0][0]}') ORDER BY co.start_time"
        cursor.execute(select)
        timetable = cursor.fetchall()

        # Creating Timetable Grids
        grid_size = {
            "width": 10,
            "height": 5,
            "pad": (1, 1),
        }  # Creating grid-layout for time table
        week_columns = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}
        headers = [
            sg.Text(
                day,
                size=(grid_size["width"], 1),
                justification="center",
                pad=10,
                font=TITLE_FONT,
                text_color=TEXT_COLOR,
                background_color=BACKGROUND_COLOR,
            )
            for day in ["MON", "TUE", "WED", "THU", "FRI"]
        ]
        grid_layout = [headers]
        grid = [
            [
                sg.Text("", size=(30, grid_size["height"]), pad=grid_size["pad"])
                for _ in range(5)
            ]
            for _ in range(10)
        ]

        for class_info in timetable:
            course_code = class_info[1]
            course_name = class_info[9]
            start_time = timedelta(seconds=class_info[4].seconds)
            end_time = timedelta(seconds=class_info[5].seconds)
            day = class_info[6]
            classroom = class_info[11]
            teacher = class_info[10]

            start_hour = (
                start_time.seconds // 3600 - 9
            )  # assuming the first class starts at 9 AM
            duration = (end_time.seconds - start_time.seconds) // 3600

            button_height = duration * grid_size["height"]

            button_text = (
                f"{course_code}\n{course_name}\n{classroom}\n{start_time}-{end_time}"
            )
            class_button = sg.Button(
                button_text,
                button_color=(TEXT_COLOR),
                size=(30, button_height),
                pad=grid_size["pad"],
            )

            col = week_columns[day]
            grid[start_hour][col] = class_button

        for row in grid:
            grid_layout.append(row)

    grid_layout.insert(
        0,
        [
            [
                sg.Button("CHATBOT", font="Helvetica 20"),
            ],
            [
                sg.Text(
                    f"Hello",
                    size=(30, 1),
                    font="Helvetica 10",
                    justification="center",
                ),
                sg.Text(
                    f"{result[0][1]}",
                    size=(30, 1),
                    font="Helvetica 10",
                    justification="center",
                ),
                sg.Text(
                    f"Logged In",
                    size=(30, 1),
                    font="Helvetica 10",
                    justification="center",
                ),
                sg.Text(
                    f"{('-'.join(str(num) for num in result[0][2:5]))} ",
                    size=(30, 1),
                    font="Helvetica 10",
                    justification="center",
                ),
                sg.Text(
                    f"{result[0][-1]}",
                    size=(30, 1),
                    font="Helvetica 10",
                    justification="center",
                ),
            ],
        ],
    )

    win = sg.Window(
        "Attendance System",
        default_element_size=(21, 1),
        text_justification="right",
        auto_size_text=False,
        background_color=BACKGROUND_COLOR,
    ).Layout(grid_layout)

    while True:
        event, _ = win.read(timeout=20)
        if event is None or event == "OK":
            win.close()
            break
        # This feature does not really send the email
        elif event == "EMAIL":
            win.close()
            select = "SELECT email FROM Student WHERE student_id='%s'" % result[0][0]
            cursor.execute(select)
            email = cursor.fetchall()

            # msg = EmailMessage()
            # msg["Subject"] = f"{class_info}"
            # msg["From"] = "mjypark1212@gmail.com"
            # msg["To"] = email

            # # Send the message via our own SMTP server.
            # s = smtplib.SMTP("localhost")
            # s.send_message(msg)
            # s.quit()
            layout = [
                [sg.Text(f"Email sent to {email[0][0]}, please check your inbox.")],
                [sg.Button("OK")],
            ]
            win = sg.Window("Confirmation").Layout(layout)
            if event is None or event == "OK":
                return ("EMAIL", class_info)
        elif event == "CHATBOT":
            return ("CHATBOT", timetable)
