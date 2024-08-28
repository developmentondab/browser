import sys
import socket
import json
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.history = []
        self.ip_address = self.get_ip_address()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))        
        self.setWindowIcon(QIcon("bb.png"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Initialize variables
        self.start_time = None
        self.current_url = None

        # Load existing data or initialize an empty dictionary
        try:
            with open('web_usage.json', 'r') as file:
                self.website_data = json.load(file)
        except FileNotFoundError:
            self.website_data = {}

         # Timer to update the time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Display IP address and History
        self.statusBar().showMessage(f"IP Address: {self.ip_address}")

        history_menu = self.menuBar().addMenu("&History")
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.ip_address = self.get_ip_address()
        self.url_bar.setText(q.toString())

    def get_ip_address(self):
        try:
            # Get the hostname and IP address
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            print(ip_address)
            return ip_address
        except:
            return "Error: Unable to fetch IP address"

    def clear_history(self):
        print(self.history)
        self.history.clear()
        QMessageBox.information(self, "History Cleared", "History has been cleared.")

    def update_time(self):
        if self.browser.url() != self.current_url:
            # If the URL has changed, start tracking time for the new URL
            self.current_url = self.browser.url()
            self.start_time = datetime.datetime.now()
        else:
            # If the URL remains the same, update the time spent
            if self.start_time:
                elapsed_time = datetime.datetime.now() - self.start_time
                url_string = self.current_url.toString()
                if url_string not in self.website_data:
                    self.website_data[url_string] = 0
                self.website_data[url_string] += elapsed_time.total_seconds()

                # Save the updated data to the JSON file
                with open('web_usage.json', 'w') as file:
                    json.dump(self.website_data, file, indent=4)

                print(f"Time spent on {url_string}: {elapsed_time}")

    def closeEvent(self, event):
        # Save data when the application is closed
        with open('web_usage.json', 'w') as file:
            json.dump(self.website_data, file, indent=4)
        event.accept()


app = QApplication(sys.argv)
QApplication.setApplicationName('Basic Browser')
window = MainWindow()
app.exec_()