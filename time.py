import sys
import json
import datetime
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Website Time Tracker")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        # Initialize variables
        self.start_time = None
        self.current_url = None

        # Load initial webpage
        self.load_webpage(QUrl("https://www.example.com"))

        # Load existing data or initialize an empty dictionary
        try:
            with open('website_usage.json', 'r') as file:
                self.website_data = json.load(file)
        except FileNotFoundError:
            self.website_data = {}

        # Timer to update the time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def load_webpage(self, url):
        self.web_view.load(url)

    def update_time(self):
        if self.web_view.url() != self.current_url:
            # If the URL has changed, start tracking time for the new URL
            self.current_url = self.web_view.url()
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
                with open('website_usage.json', 'w') as file:
                    json.dump(self.website_data, file, indent=4)

                print(f"Time spent on {url_string}: {elapsed_time}")

    def closeEvent(self, event):
        # Save data when the application is closed
        with open('website_usage.json', 'w') as file:
            json.dump(self.website_data, file, indent=4)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
