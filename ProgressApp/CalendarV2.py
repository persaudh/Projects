import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QCalendarWidget,
    QPushButton, QListWidget, QDialog, QLineEdit, QTextEdit, QDialogButtonBox,
    QTextBrowser, QHBoxLayout
)
from PySide6.QtCore import Qt, QThread, Signal, QObject, QDate
import requests
from PySide6.QtGui import QMovie
import os
import ast
import datetime


print("Exists?", os.path.exists("ProgressApp/Loading.gif"))


class APICaller(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        url = "http://127.0.0.1:8000/generate_plan"
        try:
            response = requests.post(url, json={"goal": self.user_input})
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                    result = data

                # Fallback: check if it's a stringified dict
            if isinstance(data, str) and data.strip().startswith("{"):
                parsed = ast.literal_eval(data)  # safe eval for dicts
                if isinstance(parsed, dict):
                    result = parsed
                
            self.finished.emit(result)
        except requests.exceptions.RequestException as e:
            self.error.emit(str(e))

    def call_api(user_input):
        url = "http://127.0.0.1:8000/generate_plan"
        try:
            response = requests.post(url, json={"goal": user_input})
            response.raise_for_status()

            # Try to parse actual JSON
            try:
                data = response.json()
                if isinstance(data, dict):
                    return data

                # Fallback: check if it's a stringified dict
                if isinstance(data, str) and data.strip().startswith("{"):
                    parsed = ast.literal_eval(data)  # safe eval for dicts
                    if isinstance(parsed, dict):
                        return parsed

                return {"error": "API returned unexpected format."}

            except Exception as e:
                return {"error": f"JSON parse error: {e}"}

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


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

def add_event_to_db(date_str, title, description):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO events (date, title, description) VALUES (?, ?, ?)",
              (date_str, title, description))
    conn.commit()
    conn.close()

def update_event(event_id, title, description):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE events SET title = ?, description = ? WHERE id = ?", (title, description, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def get_events_for_date(date_str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, description FROM events WHERE date = ?", (date_str,))
    events = c.fetchall()
    conn.close()
    return events

def save_draft_event_to_db(date_qt, plan_text):
    date_str = date_qt.toString("yyyy-MM-dd")
    title = "SMART Goal Draft"
    add_event_to_db(date_str, title, plan_text)

class EventDialog(QDialog):
    def __init__(self, date, title="", description="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Event - {date.toString()}")
        self.date = date

        self.title_input = QLineEdit(self)
        self.title_input.setText(title)

        self.desc_input = QTextEdit(self)
        self.desc_input.setText(description)

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
        self.setWindowTitle("📅 Calendar + API Panel")
        self.resize(800, 500)

        ### Calendar section
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.refresh_events)

        self.event_list = QListWidget()
        self.event_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.event_list.customContextMenuRequested.connect(self.show_context_menu)
        self.event_list.itemDoubleClicked.connect(self.edit_event)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.add_event)

        calendar_layout = QVBoxLayout()
        calendar_layout.addWidget(self.calendar)
        calendar_layout.addWidget(QLabel("Events:"))
        calendar_layout.addWidget(self.event_list)
        calendar_layout.addWidget(self.add_event_button)

        ### API interaction section
        self.api_input = QTextEdit()
        self.api_input.setPlaceholderText("Type a message for the API...")

        self.send_button = QPushButton("Send to API")
        self.send_button.clicked.connect(self.send_to_api)

        self.api_output = QTextBrowser()

        # Spinner
        self.spinner_label = QLabel()
        self.spinner = QMovie("ProgressApp/Loading.gif")
        self.spinner_label.setMovie(self.spinner)
        self.spinner_label.setVisible(False)

        api_layout = QVBoxLayout()
        api_layout.addWidget(QLabel("Input:"))
        api_layout.addWidget(self.api_input)
        api_layout.addWidget(self.send_button)
        api_layout.addWidget(self.spinner_label)
        api_layout.addWidget(QLabel("API Output:"))
        api_layout.addWidget(self.api_output)

        ### Combine both sections side by side
        main_layout = QHBoxLayout()
        main_layout.addLayout(api_layout, 1)
        main_layout.addLayout(calendar_layout, 2)

        self.setLayout(main_layout)
        
    def refresh_events(self):
        self.event_list.clear()
        date_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.current_events = get_events_for_date(date_str)
        for _, title, desc in self.current_events:
            self.event_list.addItem(f"{title} - {desc}")

    def add_event(self):
        date = self.calendar.selectedDate()
        dialog = EventDialog(date, parent=self)
        if dialog.exec():
            title, desc = dialog.get_data()
            if title.strip():
                date_str = date.toString("yyyy-MM-dd")
                add_event_to_db(date_str, title, desc)
                self.refresh_events()

    def edit_event(self, item):
        index = self.event_list.row(item)
        event_id, title, desc = self.current_events[index]
        date = self.calendar.selectedDate()
        dialog = EventDialog(date, title, desc, parent=self)
        if dialog.exec():
            new_title, new_desc = dialog.get_data()
            update_event(event_id, new_title, new_desc)
            self.refresh_events()

    def delete_event_ui(self, index):
        event_id, _, _ = self.current_events[index]
        delete_event(event_id)
        self.refresh_events()

    def save_smart_goal_plan(self, plan):
        # Save SMART goal summary
        summary = plan.get("goal_summary", {})
        summary_text = "\n".join([
            f"Specific: {summary.get('specific', '')}",
            f"Measurable: {summary.get('measurable', '')}",
            f"Achievable: {summary.get('achievable', '')}",
            f"Relevant: {summary.get('relevant', '')}",
            f"Time-Bound: {summary.get('time_bound', '')}"
        ])

        start_date_str = summary.get("start_date")
        try:
            dt = datetime.datetime.strptime(start_date_str, "%B %d, %Y")
            start_qdate = QDate(dt.year, dt.month, dt.day)
        except Exception as e:
            print(f"Date parse error for start_date: {e}")
            start_qdate = self.calendar.selectedDate()

        save_draft_event_to_db(start_qdate, summary_text)

        # --- TASK PLAN ---
        for task_item in plan.get("task_plan", []):
            task = task_item.get("task")
            desc = task_item.get("description", "")
            due_date_str = task_item.get("due_date")

            try:
                due_dt = datetime.datetime.strptime(due_date_str, "%B %d, %Y")
                due_qdate = QDate(due_dt.year, due_dt.month, due_dt.day)
            except Exception as e:
                print(f"Date parse error for task due_date: {e}")
                continue

            # Add task to calendar
            add_event_to_db(due_qdate.toString("yyyy-MM-dd"), task, desc)

            self.refresh_events()

    def show_context_menu(self, pos):
        from PySide6.QtWidgets import QMenu
        index = self.event_list.indexAt(pos).row()
        if index == -1:
            return

        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        action = menu.exec(self.event_list.mapToGlobal(pos))

        if action == edit_action:
            self.edit_event(self.event_list.item(index))
        elif action == delete_action:
            self.delete_event_ui(index)

    def send_to_api(self):
        user_input = self.api_input.toPlainText()
        if not user_input.strip():
            return

        self.api_output.append(f"> You: {user_input}")
        self.api_input.setDisabled(True)
        self.send_button.setDisabled(True)
        self.spinner_label.setVisible(True)
        self.spinner.start()

        self.thread = QThread()
        self.worker = APICaller(user_input)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handle_api_success)
        self.worker.error.connect(self.handle_api_error)

        # Clean up
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handle_api_success(self, response):
        print(f"Valid? {isinstance(response, dict)}")
        if isinstance(response, dict) and "goal_summary" in response:
            self.api_output.append("< API: SMART plan received.\n")
            self.save_smart_goal_plan(response)
        else:
            self.api_output.append(f"< API ERROR: Unexpected response format:\n{response}")
        self.cleanup_after_api()

    def handle_api_error(self, error_msg):
        self.api_output.append(f"< API ERROR: {error_msg}\n")
        self.cleanup_after_api()

    def cleanup_after_api(self):
        self.spinner.stop()
        self.spinner_label.setVisible(False)
        self.api_input.setDisabled(False)
        self.send_button.setDisabled(False)
        self.api_input.clear()

    
        


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
