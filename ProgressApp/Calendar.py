import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QCalendarWidget,
    QPushButton, QListWidget, QDialog, QLineEdit, QTextEdit, QDialogButtonBox
)
from PySide6.QtCore import QDate

DB_FILE = "calendar_events.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_events_for_date(date_str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT title, description FROM events WHERE date = ?", (date_str,))
    events = c.fetchall()
    conn.close()
    return events

def add_event_to_db(date_str, title, description):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO events (date, title, description) VALUES (?, ?, ?)",
              (date_str, title, description))
    conn.commit()
    conn.close()

class EventDialog(QDialog):
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Event - {date.toString()}")
        self.date = date

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Event title")

        self.desc_input = QTextEdit(self)
        self.desc_input.setPlaceholderText("Event description")

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_data(self):
        return self.title_input.text(), self.desc_input.toPlainText()

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📅 Smart Calendar with SQLite")
        self.resize(500, 500)

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.refresh_events)

        self.event_list = QListWidget()
        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.add_event)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(QLabel("Events:"))
        layout.addWidget(self.event_list)
        layout.addWidget(self.add_event_button)
        self.setLayout(layout)

        self.refresh_events()

    def refresh_events(self):
        self.event_list.clear()
        date_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
        for title, desc in get_events_for_date(date_str):
            self.event_list.addItem(f"{title} - {desc}")

    def add_event(self):
        date = self.calendar.selectedDate()
        dialog = EventDialog(date, self)
        if dialog.exec():
            title, desc = dialog.get_data()
            if title.strip():
                date_str = date.toString("yyyy-MM-dd")
                add_event_to_db(date_str, title, desc)
                self.refresh_events()

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
