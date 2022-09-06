print("Warming up machine learning models, this may take a few minutes...")
print("-"*50)
import threading
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QIcon, QImage, QFontDatabase
import chatting
import reviewing
import sys
import os
from worker import Worker
from time import sleep

PALETTE = []
MAIN_BG = "#FEF5ED"
BUTTON_COLOR = "#D3E4CD"
FIELD_COLOR = "#99A799"
BUTTON_TEXT_COLOR = "#3A3A3A"
FIELD_TEXT_COLOR = "#001333"
FONT = ("Roboto", 12) 
class Window(QObject):
    def __init__(self, window_title="", window_type="", app=""):
        super().__init__()
        
        self.app = app
        self.window_title = window_title
        self.window_type = window_type

        self.init_ui()

        

    def init_ui(self):
        self.window_size = (400, 500)

        font_list = []

        for file in os.listdir("Fonts"):
            id = QFontDatabase.addApplicationFont(f"Fonts/{file}")
            if id < 0:
                pass
            else:
                families = QFontDatabase.applicationFontFamilies(id)
                font_list.append(families)
                        

        self.image = QImage()
        self.image.load("Icons/500x500icon.png")
        self.window = QWidget()
        self.font = QFont("Roboto Medium", 14)
        self.window.setFixedSize(400, 500)
        
        self.font.setWeight(1)
        self.window.setWindowIcon(QIcon('Icons/500x500icon.png'))
        
        self.line_edit = QLineEdit(font=self.font)
        self.text_field = QTextBrowser(font=self.font)        
        
        self.window.setStyleSheet("""QWidget 
                                {background-image: url("Icons/500x500icon.png");
                                alignment: center;
                                background-repeat: no-repeat;
                                background-position: center;
                                position: center;
                                background-attachment: scroll;
                                selection-color: #eebaca;
                                selection-background-color: #520a21;
}
                                  """)      
        self.line_edit.setStyleSheet("""QLineEdit 
                                     {
                                     color: %s;
                                     background-image: url("Icons/textgradient.png");
                                     background-attachment: fixed;
                                     border-width: 1px;
                                     border-radius: 10px;
                                     border-color: %s;}
                                     """ % (FIELD_TEXT_COLOR, FIELD_COLOR))
        self.text_field.setStyleSheet("""QTextBrowser 
                                      {
                                      color: %s;
                                      background-image: url("Icons/redtoyellowgradient.png");
                                      border-width: 1px;
                                      border-radius: 10px;
                                      background-attachment: fixed;}
                                      """ % (FIELD_TEXT_COLOR))

               
        self.window.setWindowTitle(self.window_title)
        self.layout = QVBoxLayout()
        self.widgets= []
        if self.window_type == "chat":
            self.chat_window()
        elif self.window_type == "main":
            self.main_window()
            
    def onIntReady(self, i):
        self.label.setText("{}".format(i))
         
    def delay_response(self, text, time):
        
        QTimer.singleShot(time, lambda: self.text_field.append(text))
    
    def send_to_generation(self, text="", clicked_btn=None):
        
        prompt = text
        

        output = chatting.generating_reply(prompt)
        print(output)
        return output  
    
    def send_to_review(self, text="", clicked_btn=None):
        
        prompt = text
        output, movie, score, review =reviewing.generating_review(prompt)
        print(output)
        return output, movie, score, review     
        
    def button(self, btns, text):
        
        for i in range(len(btns)):
            btns[i] = QPushButton(text[i], font=self.font)
            btns[i].setStyleSheet("""QPushButton 
                                  {
                                  color: %s; 
                                  font-family: "Raleway Black";
                                  border-style: inset; 
                                  border-width: 3px;
                                  border-radius: 10px;
                                  border-color: %s;
                                  max-width: 200px;
                                  position: center;
                                  margin-left: 110px;
                                  margin-right: 110px;
                                  background-image: url("Icons/greentobluegradient.png");
}
                                  """ % ( BUTTON_TEXT_COLOR, FIELD_COLOR))
        return btns
    
    def creating_list_of_clicked_buttons(self, btns):
        
        click_list = []
        for i in range(len(btns)):
            btn_name = btns[i].text()
            connect_fun = self.on_btn_clicked(btn_name)
            clicked = btns[i].clicked.connect(connect_fun)
            click_list.append(clicked)
        return click_list
    
    
    def send_button(self, clicked_btn=None):
        clicked_btn = self.send_b
        user_input = "User: " + self.line_edit.text()
        self.text_field.append(user_input)
        robot_response = "CHATBOT: " + self.send_to_generation(user_input, clicked_btn=clicked_btn)
        self.delay_response(robot_response, 1000)
        self.line_edit.clear()
        
    def chat_button(self, clicked_btn=None):
        
        self.change_window()
        self.chat_window()
        
    def review_button(self, clicked_btn=None):
        
        self.change_window()
        self.review_window()
    
    def create_button(self, clicked_btn=""):
        clicked_btn = self.create_b
        user_input = self.line_edit.text()
        if user_input == "":
            self.text_field.append("Generating a review for any movie it would like...\n")
        else:
            self.text_field.append(f"Generating review for {user_input}...\n")
            user_input += " Score:"
        self.text_field.repaint()
        output, movie, score, review = self.send_to_review(user_input, clicked_btn=clicked_btn)
        self.line_edit.clear()
        
        self.delay_response("Movie:", 100)
        self.delay_response(movie+"\n", 500)
        self.delay_response("Score:", 1000)
        self.delay_response(score+"\n", 1500)
        self.delay_response("Review:", 2000)
        self.delay_response(review+"\n", 3000)
    
    def exit_button(self):
        self.app.quit()
        
    
    def on_btn_clicked(self, btn_name):
        
        if btn_name == "Chat":
            return self.chat_button
        elif btn_name == "Review":
            return self.review_button
        elif btn_name == "Exit":
            return self.exit_button
        elif btn_name == "Send":
            return self.send_button
        elif btn_name == "Main Menu":
            return self.main_window
        elif btn_name == "Create Review":
            return self.create_button

    def add_widgets(self, widgets, main=False):
        self.widgets = widgets
        if main == True:
            pad_widget = QTextBrowser()
            pad_widget.setStyleSheet("""QTextBrowser 
                                      {
                                      background: transparent;
                                      border: none;
                                      }
                                      """)
            widgets.insert(0, pad_widget)
            
            
            for widget in self.widgets:
                self.layout.addWidget(widget)
        else:
            for widget in widgets:
                self.layout.addWidget(widget)
    
    def show_window(self):
        
        self.window.resize(self.window_size[0], self.window_size[1])
        self.window.setLayout(self.layout)
        self.window.show()
                  
    def main_window(self):
        
        self.change_window()
        self.window_title = "Main Menu"
        self.window.setWindowTitle(self.window_title)
        self.chat_b, self.review_b, self.exit_b= self.button(["a", "b", "c"], ["Chat", "Review", "Exit"])
        self.add_widgets([self.chat_b, self.review_b, self.exit_b], main=True)
        self.chat_c, self.review_c, self.exit_c = self.creating_list_of_clicked_buttons([self.chat_b, self.review_b, self.exit_b])
        self.show_window()
        
    def chat_window(self):
        
        self.window_title = "Chat"
        self.window.setWindowTitle(self.window_title)
        self.send_b, self.main_b, self.exit_b = self.button(["a", "b", "c"], ["Send", "Main Menu", "Exit"])
        self.add_widgets([self.text_field, self.line_edit, self.send_b, self.main_b, self.exit_b])
        self.send_c, self.main_c, self.exit_c = self.creating_list_of_clicked_buttons([self.send_b, self.main_b, self.exit_b])
        self.show_window()
    
    def review_window(self):
        
        self.window_title = "Create a Review"
        self.window.setWindowTitle(self.window_title)
        self.create_b, self.main_b, self.exit_b = self.button(["a", "b", "c"], ["Create Review", "Main Menu", "Exit"])
        movie_label = QLabel("Movie:", self.window, font=self.font)
        movie_label.setStyleSheet("""QLabel 
                                      {
                                      background-image: url("Icons/textgradient.png");
                                      font-family: "Roboto Slab SemiBold";
                                      alignment: center;
                                      max-width: 500px;
                                      font-size: 25px;
                                      background: transparent;
                                      text-align: center;

                                      }
                                      """)
        self.add_widgets([movie_label, self.line_edit, self.create_b, self.text_field, self.main_b, self.exit_b])
        self.send_c, self.main_c, self.exit_c = self.creating_list_of_clicked_buttons([self.create_b, self.main_b, self.exit_b])
        self.show_window()
    
    def change_window(self):
        
        self.chat_history = []
        self.line_edit.clear()
        self.text_field.clear()
        self.window.close()
        self.widgets = []
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
    
    def app_exec(self):
        self.app.exec()


def main():
    
    app = QApplication(sys.argv)
    window_title = "Main Menu"
    window_type = "main"
    window = Window(window_title=window_title, window_type=window_type, app=app)
    window.app_exec()


if __name__ == "__main__":
    main()   