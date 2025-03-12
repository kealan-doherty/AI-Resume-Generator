import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QLineEdit, QListWidget, QMainWindow
import sql_functions
import ai_generator

job_listing = {}
input_text = ''
input_text2 = ''
pulled_jobs = []

"""
this code runs the GUI for the project providing a UI for the user to interact in order to find a job, input their perso
nal info and save it to a profile with a user name, which is sent ti the LLM model to generate the resume and cover lett
er. 
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup()

    def on_button_clicked(self):
        input_text = self.input.text()
        sql_functions.pull_data_rapid2(input_text, pulled_jobs)

    def setup(self):
        self.intro_message = QLabel("Welcome to the Resume Generator using AI, please enter the job title you are"
                                    " looking for below", self)
        self.intro_message.setGeometry(250, 250, 250, 250)
        self.intro_message.resize(600, 100)
        self.resize(1000, 1000)
        self.setWindowTitle('AI resume generator')
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter job title here please")
        self.input.setGeometry(400, 400, 150, 50)
        self.button = QPushButton("find jobs", self)
        self.button.setGeometry(425, 500, 100, 50)
        self.button.clicked.connect(self.on_button_clicked)
        self.button.clicked.connect(self.open_second_window)

        self.show()

    def open_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.close()


class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup2()

    def on_button_clicked(self):
        input_text2 = self.input.text()
        sql_functions.pull_single_listing(input_text2, job_listing)

    def setup2(self):
        self.setWindowTitle('AI resume generator')
        self.resize(1000, 1000)
        self.list_widget = QListWidget()

        for job in pulled_jobs:
            self.list_widget.addItem(str(job))

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Please enter the job id to access the full listing")
        self.button = QPushButton("Submit", self)
        self.button.setGeometry(550, 700, 100, 50)
        self.input.setGeometry(500, 650, 275, 50)
        self.button.clicked.connect(self.on_button_clicked)
        self.button.clicked.connect(self.open_third_window)

        self.show()

    def open_third_window(self):
        self.third_window = ThirdWindow()
        self.third_window.show()
        self.close()


class ThirdWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup3()

    def on_button_clicked(self):
        user_data = {}
        username = self.input_username.text()
        contact_info = self.input_contact_info.text()
        project_info = self.input_projects.text()
        classes_info = self.input_classes.text()
        other_info = self.input_others.text()
        sql_functions.load_user_db(username, contact_info, project_info, classes_info, other_info)
        sql_functions.pull_user(username, user_data)
        ai_generator.create_reumse(user_data)

    def on_button2_clicked(self):
        user_data = {}
        username = self.profile_search.text()
        sql_functions.pull_user(username, user_data)
        ai_generator.create_reumse(user_data)

    def setup3(self):
        self.setWindowTitle("AI resume generator")
        self.resize(1000, 1000)
        self.list_widget = QListWidget()

        self.list_widget.addItem(job_listing["JOB_SITE"])
        self.list_widget.addItem(job_listing["JOB_URL"])
        self.list_widget.addItem(job_listing["JOB_TITLE"])
        self.list_widget.addItem(job_listing["JOB_LOCATION"])
        self.list_widget.addItem(job_listing["JOB_TYPE"])

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.input_contact_info = QLineEdit(self)
        self.input_projects = QLineEdit(self)
        self.input_classes = QLineEdit(self)
        self.input_others = QLineEdit(self)
        self.input_username = QLineEdit(self)
        self.profile_search = QLineEdit(self)
        self.intro_message = QLabel("here you can either input your info for the resume generator or access a profile"
                                    , self)
        self.profile_search.setPlaceholderText("already have an account, please enter username here")
        self.input_username.setPlaceholderText("PLease enter a username for accessing profile")
        self.input_contact_info.setPlaceholderText("Please enter your contact info here")
        self.input_projects.setPlaceholderText("Please enter your projects here")
        self.input_classes.setPlaceholderText("Please enter your classes here")
        self.input_others.setPlaceholderText("Please enter any other important info here")
        self.intro_message.setGeometry(350, 250, 500, 250)
        self.profile_search.setGeometry(100, 575, 275, 50)
        self.input_username.setGeometry(500, 575, 275, 50)
        self.input_contact_info.setGeometry(500, 650, 275, 50)
        self.input_projects.setGeometry(500, 725, 275, 50)
        self.input_classes.setGeometry(500, 800, 275, 50)
        self.input_others.setGeometry(500, 875, 275, 50)
        self.button = QPushButton("Submit", self)
        self.button.setGeometry(800, 700, 100, 50)
        self.button2 = QPushButton("Search for profile", self)
        self.button2.setGeometry(150, 650, 150, 50)
        self.button.clicked.connect(self.on_button_clicked)
        self.button.clicked.connect(self.open_final_window)
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button2.clicked.connect(self.open_final_window)

        self.show()

    def open_final_window(self):
        self.final_window = finalWindow()
        self.final_window.show()
        self.close()


class finalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("AI resume generator")
        self.resize(1000, 1000)
        self.final_message = QLabel("resume has been generated into a PDF file and saved to your machine ", self)
        self.final_message.setGeometry(250, 100, 400, 50)
        self.show()


def run():
    app = QApplication(sys.argv)
    ex = MainWindow()  # noqa
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
