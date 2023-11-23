from time import sleep
import PySimpleGUI as sg
from chatbot import chatbot_setup, get_completion
from feature import feature
from authenticate import login_setup, authenticate
import cv2
import urllib.request

"""
  DESIGN PATTERN 2 - Multi-read window. Reads and updates fields in a window
"""

sg.theme("Kayak")  # Add some color for fun
image_URL = f"https://www.cetl.hku.hk/tdgfest22/wp-content/uploads/2022/03/hkulogo3.png"
# 1- the layout
start_layout = [
    # [sg.Text("Your typed chars appear here:"), sg.Text(size=(15, 1), key="-OUTPUT-")],
    # [sg.Input(key="-IN-")],
    [sg.Text("", size=(30, 1), font="Helvetica 40")],
    [sg.Text("", size=(30, 1), font="Helvetica 40")],
    [
        sg.Column(
            [
                [
                    sg.Text(
                        "Intelligent Course Management System",
                        size=(30, 1),
                        font="Helvetica 40",
                        justification="center",
                    )
                ]
            ],
            justification="center",
        )
    ],
    [
        sg.Column(
            [[sg.Image(urllib.request.urlopen(image_URL).read())]],
            justification="center",
        )
    ],
    [
        sg.Column(
            [
                [
                    sg.Button("LOGIN", font="Helvetica 20"),
                    sg.Button("EXIT", font="Helvetica 20"),
                ]
            ],
            justification="center",
        )
    ],
]

# 2 - the window
window = sg.Window("Pattern 2", start_layout).Finalize()
window.Maximize()
window_login = None
window_chatbot = None
window_feature = None
state = "Start"
passer = ()
win_started = False
event_login = None
event_chatbot = None
event_feature = None
timetable = None
# 3 - the event loop
while True:
    if state == "Login":
        student_data, frame = authenticate(*passer)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        if student_data:
            window.write_event_value("AUTHENTICATED", "")
        elif not win_started:
            win_started = True
            layout = [
                [sg.Text("Intelligent Course Management System", size=(30, 1))],
                [sg.Image(data=imgbytes, key="_IMAGE_")],
                [sg.Exit()],
            ]
            window_login = (
                sg.Window(
                    "Intelligent Course Management System",
                    default_element_size=(14, 1),
                    text_justification="right",
                    auto_size_text=False,
                ).Layout(layout)
                # .Finalize()
                # .Maximize()
            )

            image_elem = window_login.FindElement("_IMAGE_")
        else:
            image_elem.Update(data=imgbytes)

    # read event
    event, value = window.read(timeout=20)

    if window_login:
        event_login, _ = window_login.read(timeout=20)
    if window_chatbot:
        event_chatbot, _ = window_chatbot.read(timeout=20)
    if window_feature:
        event_feature, _ = window_feature.read(timeout=20)

    # handle event
    if event_chatbot == "EXIT CHATBOT":
        window_chatbot.close()
        window_chatbot = None

    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "LOGIN":
        passer = login_setup()
        state = "Login"
    elif event == "AUTHENTICATED":
        if window_login:
            window_login.close()
        window_login = None
        state = "Authenticated"
        window.write_event_value("FEATURE", "")
    elif event == "FEATURE":
        state = "Feature"
        res, timetable = feature(student_data, passer[-1])
        if res == "CHATBOT":
            window.write_event_value("CHATBOT", "")
    elif event == "CHATBOT":
        state = "Chatbot"
        chatbot_setup(timetable)
