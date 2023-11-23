import PySimpleGUI as sg
from openai import OpenAI
from dotenv import load_dotenv


def get_completion(
    prompt: str, student_data: str
):  # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    model = "gpt-3.5-turbo"
    messages = [
        {
            "role": "system",
            "content": f"""
            You are an assistant to help student answer queries on his/her courseworks.
            The relevant data is in triple backticks
            ```{student_data} ```
    """,
        },
    ]

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,  # this is the degree of randomness of the model's output
        )
        print(completion.choices[0].message.content, flush=True)
        messages.append(
            {
                "role": "assistant",
                "content": prompt,
            }
        )
    except Exception as e:
        print(e)


def chatbot_setup(timetable):
    load_dotenv()
    sg.theme("GreenTan")  # give our window a spiffy set of colors

    layout = [
        [sg.Text("Coursework Chatbot", size=(40, 1))],
        [sg.Output(size=(110, 20), font=("Helvetica 10"))],
        [
            sg.Multiline(
                size=(70, 5), enter_submits=True, key="-QUERY-", do_not_clear=False
            ),
            sg.Button(
                "SEND", button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True
            ),
            sg.Button("EXIT CHAT BOT", button_color=(sg.YELLOWS[0], sg.GREENS[0])),
        ],
    ]

    window = sg.Window(
        "Chat window",
        layout,
        font=("Helvetica", " 13"),
        default_button_element_size=(8, 2),
        use_default_focus=False,
    )

    while True:  # The Event Loop
        event, value = window.read()
        if event in (None, "EXIT CHAT BOT"):  # quit if exit button or X
            break
        if event == "SEND":
            query = value["-QUERY-"].rstrip()
            get_completion(query, timetable)


if __name__ == "__main__":
    window = chatbot_setup()
    student_data = """Course Title: Introduction to Culinary Arts

Course Code: CUL101
Description: This course provides an overview of basic culinary techniques, including knife skills, cooking methods, and food safety. Students will gain hands-on experience in the kitchen and develop a foundation for further studies in the culinary arts.
Course Title: Pastry Fundamentals

Course Code: BAK201
Description: Explore the art of pastry making, including dough preparation, baking techniques, and the creation of various pastries and desserts. Emphasis will be placed on mastering the principles of pastry creation and presentation.
Course Title: Advanced Baking and Cake Decoration

Course Code: BAK301
Description: This advanced course focuses on complex baking concepts and advanced cake decoration techniques. Students will delve into the artistry of cake design, working with fondant, gum paste, and other decorative elements.
Course Title: Food Photography and Styling

Course Code: ART305
Description: Combine culinary skills with visual artistry in this course focused on food photography and styling. Students will learn the principles of composition, lighting, and styling to create visually appealing food images for various media platforms.
Course Title: Culinary Entrepreneurship

Course Code: ENT401
Description: This course explores the business side of the culinary industry, covering topics such as restaurant management, menu planning, and entrepreneurship. Students will develop a business plan for a culinary venture."
"""

    while True:  # The Event Loop
        event, value = window.read()
        if event in (None, "EXIT"):  # quit if exit button or X
            break
        if event == "SEND":
            query = value["-QUERY-"].rstrip()
            get_completion(query, student_data)
