import json
import pandas as pd
import random
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from urllib.request import urlopen
import matplotlib.pyplot as plt


# open api link to database
# with urlopen("https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple") as webpage:
#     # read JSON file & extract data
#     data = json.loads(webpage.read().decode())
#     df = pd.DataFrame(data["results"])
#     # print(data)
#     # print("Test")
#     # print(df)

# Getting questions from list
df = pd.read_json('questions.json')
val = {"Never": 0, "Almost_Never": 1, "Sometimes": 2, "Fairly_offen": 3, "Very_offen": 4}


def load_ques():
    def init():
        return 0

    i = init()
    while True:
        val = (yield i)
        if val == 'restart':
            i = init()
        else:
            i += 1


gen = load_ques()


# load 1 instance of questions & answers at a time from the database
def preload_data(idx):
    try:
        # idx parm: selected randomly time and again at function call
        question = df["question"][idx]
        answers = df["answers"][idx]
        positive = df['positive'][idx]

        # store local values globally
        parameters["question"].append(question)
        parameters["positive"].append(positive)

        # all_answers = wrong + [correct]
        all_answers = answers
        # random.shuffle(all_answers)

        print(answers)

        parameters["answer1"].append(all_answers[0])
        parameters["answer2"].append(all_answers[1])
        parameters["answer3"].append(all_answers[2])
        parameters["answer4"].append(all_answers[3])
        parameters["answer5"].append(all_answers[4])
    except Exception as e:
        print(e)


# dictionary to store local pre-load parameters on a global level
parameters = {
    "question": [],
    "positive": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "answer5": [],
    "score": [],
    "index": [],
}

# global dictionary of dynamically changing widgets
widgets = {
    "logo": [],
    "customer_name": [],
    "mob": [],
    "c_label": [],
    "m_label": [],
    "graph": [],
    "try_again": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "answer5": [],
    "message": [],
    "message2": []
}

# initialize grid layout
grid = QGridLayout()


def clear_widgets():
    """hide all existing widgets and erase
    them from the global dictionary"""
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def clear_parameters():
    # clear the global dictionary of parameters
    for parm in parameters:
        if parameters[parm] != []:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()
    # populate with initial index & score values
    parameters["index"].append(next(gen))
    parameters["score"].append(0)


def start_game():
    # printing values , can log!!
    if len(widgets['customer_name'][-1].text()) == 0 or widgets['customer_name'][-1].text() == 0 or len(
            widgets['mob'][-1].text()) == 0 or widgets['mob'][-1].text() == 0:
        QMessageBox.critical(widgets['c_label'][-1], "Alert!", "Please fill your Details!")
        return
    print("Customer Name: {0} | Mob.: {1}".format(widgets['customer_name'][-1].text(), widgets['mob'][-1].text()))

    # start the game, reset all widgets and parameters
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    # display the game frame
    frame2()


def create_buttons(answer, l_margin, r_margin):
    # create identical buttons with custom left & right margins
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        # setting variable margins
        "*{margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    button.clicked.connect(lambda x: is_clicked(button))
    return button


def is_clicked(btn):
    if btn.text():
        # Adding points
        add_up = ""
        for key in val.keys():
            if btn.text() == key:
                add_up = val[key]

        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        # Checking questions are positive or negative to reverse the points.
        if parameters["positive"][-1] == 0:
            print("Question: {0} \n Answer: {1} | points: {2}".format(parameters['question'][-1], btn.text(),
                                                                      int(add_up)))
            parameters["score"].append(temp_score + int(add_up))
        else:
            if int(add_up) == 0:
                add_up = 4
            elif int(add_up) == 1:
                add_up = 3
            elif int(add_up) == 2:
                add_up = 2
            elif int(add_up) == 3:
                add_up = 1
            elif int(add_up) == 4:
                add_up = 0
            print("Question: {0} \n Answer: {1} | points: {2} [ Positive Question so points reversed ]".format(
                parameters['question'][-1], btn.text(), int(add_up)))
            parameters["score"].append(temp_score + int(add_up))

        # reset index if question idx ends
        parameters["index"].pop()
        idx = next(gen)
        # checking index with num of the questions
        if idx == len(df):
            gen.send('restart')

        if idx <= len(df) - 1:
            parameters["index"].append(idx)

            # preload data for new index value
            preload_data(parameters["index"][-1])

            # update the text of all widgets with new data
            widgets["score"][-1].setText(str(parameters["score"][-1]))
            widgets["question"][0].setText(parameters["question"][-1])
            widgets["answer1"][0].setText(parameters["answer1"][-1])
            widgets["answer2"][0].setText(parameters["answer2"][-1])
            widgets["answer3"][0].setText(parameters["answer3"][-1])
            widgets["answer4"][0].setText(parameters["answer4"][-1])
            widgets["answer5"][0].setText(parameters["answer5"][-1])
        else:
            # if parameters["score"][-1] == 10:
            clear_widgets()
            frame3()
    else:
        clear_widgets()
        frame4()


# *********************************************
#                  Graph
# *********************************************

def graph():
    temp_d = {"Your Score:": parameters["score"][-1]}
    courses = list(temp_d.keys())
    values = list(temp_d.values())
    
    fig = plt.figure(figsize = (2, 5))
    
    # creating the bar plot
    plt.bar(courses, values, color ='maroon',
            width = 0.1)
    
    plt.ylim(0,40)
    plt.ylabel("Score")
    plt.show()


# *********************************************
#                  FRAME 1
# *********************************************

def frame1():
    clear_widgets()
    # logo widget
    image = QPixmap("AI_logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    customer_name = QLineEdit()
    customer_name.setAlignment(Qt.AlignCenter)
    customer_name.setStyleSheet(
        # setting variable margins
        "*{margin-left: " + str(85) + "px;" +
        "margin-right: " + str(5) + "px;" +
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    widgets["customer_name"].append(customer_name)

    mob = QLineEdit()
    mob.setAlignment(Qt.AlignCenter)
    mob.setMaxLength(10)
    mob.setValidator(QIntValidator())
    mob.setStyleSheet(
        # setting variable margins
        "*{margin-left: " + str(5) + "px;" +
        "margin-right: " + str(85) + "px;" +
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    widgets["mob"].append(mob)

    c_label = QLabel("NAME.")
    c_label.setAlignment(Qt.AlignCenter)
    c_label.setStyleSheet(
        "color: white; font-size: 16px; margin-top: 30px; margin-left: 5px; margin-right: 85px;"
    )
    m_label = QLabel("MOB.")
    m_label.setAlignment(Qt.AlignCenter)
    m_label.setStyleSheet(
        "color: white; font-size: 16px; margin-top: 30px; margin-left: 5px; margin-right: 85px;"
    )
    widgets["c_label"].append(c_label)
    widgets["m_label"].append(m_label)

    # button widget
    button = QPushButton("START")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#BC006C';
            border-radius: 45px;
            font-size: 35px;
            color: 'white';
            padding: 25px 0;
            margin: 100px 200px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    # button callback
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    # place global widgets on the grid
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(c_label, 2, 0)
    grid.addWidget(widgets["customer_name"][-1], 3, 0)
    grid.addWidget(m_label, 2, 1)
    grid.addWidget(widgets["mob"][-1], 3, 1)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)


# *********************************************
#                  FRAME 2
# *********************************************

def frame2():
    # score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        '''
        font-size: 35px;
        color: 'white';
        padding: 15px 10px;
        margin: 20px 200px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 35px;
        '''
    )
    widgets["score"].append(score)

    # question widget
    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        '''
        font-family: 'shanti';
        font-size: 25px;
        color: 'white';
        padding: 75px;
        '''
    )
    widgets["question"].append(question)

    # answer button widgets
    button1 = create_buttons(parameters["answer1"][-1], 85, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 85)
    button3 = create_buttons(parameters["answer3"][-1], 85, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 85)
    button5 = create_buttons(parameters["answer5"][-1], 85, 5)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)
    widgets["answer5"].append(button5)

    # logo widget
    image = QPixmap("AI_bottomlogo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 75px; margin-bottom: 30px;")
    widgets["logo"].append(logo)

    # place widget on the grid
    # grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets["answer5"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 1, 2)


# *********************************************
#             FRAME 3 - QUESTIONNAIRES Complete
# *********************************************

def frame3():
    # congratulations  widget
    message = QLabel("Congratulations! You\nhave completed the session!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
    )
    widgets["message"].append(message)

    # score widget
    score = QLabel(str(parameters["score"][-1]) + '/' + str(len(parameters["question"]*4)))
    # score = QLabel("20")
    a = 100 - int((parameters["score"][-1]/len(parameters["question"]*4)) * 100)
    def hsv_to_rgb(h, s, v):
        if s == 0.0: v*=255; return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
    hue = a*1.2
    rgb = hsv_to_rgb(hue/360, 1, .5)
    rgb = list(map(int, rgb))
    hex = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
    score.setStyleSheet(f"font-size: 100px; color: {hex}; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # go back to work widget
    if parameters["score"][-1] >= len(parameters["question"]) * 2:
        msg = "OK. Need to consult a doctor!"
    else:
        msg = "You're doing great!"
    message2 = QLabel(msg)
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white';"
    )
    widgets["message2"].append(message2)

    # button widget
    try_btn = QPushButton('TRY AGAIN')
    try_btn.setStyleSheet(
        "*{background:'#BC006C';"
        " padding:25px 0px; border: "
        "1px solid '#BC006C'; color: "
        "'white'; font-family: 'Arial'; "
        "font-size: 15px; border-radius: "
        "40px; margin: 10px 300px;} "
        "*:hover{background:'#ff1b9e';}"
    )
    try_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    try_btn.clicked.connect(frame1)
    widgets["try_again"].append(try_btn)

    # GRAPH widget
    graph_btn = QPushButton('GRAPH')
    graph_btn.setStyleSheet(
        "*{background:'#BC006C'; "
        "padding:25px 0px; border: "
        "1px solid '#BC006C'; color: "
        "'white'; font-family: 'Arial'; "
        "font-size: 15px; border-radius: "
        "40px; margin: 10px 300px;} "
        "*:hover{background:'#ff1b9e';}"
    )
    graph_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    graph_btn.clicked.connect(graph)
    widgets["graph"].append(graph_btn)

    # logo widget
    pixmap = QPixmap('AI_bottomlogo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["graph"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["try_again"][-1], 5, 0, 2, 2)

    # *********************************************
    #                  FRAME 4 - FAIL
    # *********************************************


def frame4():
    # sorry widget
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
    )
    widgets["message"].append(message)

    # score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#BC006C';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#ff1b9e';
        }'''
    )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    # logo widget
    pixmap = QPixmap('AI_bottomlogo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)
