from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from database import create_connection, select_all_tasks, insert_task, delete_task
from home_tab import home_tab
from performance_insights_tab import performance_insights_tab
from settings_tab import settings_tab

# Inside TaskManagerGUI class

class TaskManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = create_connection()  # Initialize the database connection
        self.tasks = select_all_tasks(self.conn)  # Initialize the task list from the database

        self.initUI()  # Initialize UI elements after initializing tasks
        self.tasks_model = QStringListModel()
        self.tasks_list_view.setModel(self.tasks_model)
        self.update_task_list()

    def initUI(self):
        self.setWindowTitle('Task Manager GUI')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget { background-color: white; color: black; }
            QTabWidget { background-color: white; color: black; }
            QTabBar::tab { background-color: #f0f0f0; color: black; padding: 10px; }
            QTabBar::tab:selected { background-color: #dcdcdc; }
            QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #ccc; }
            QCheckBox { color: black; }
            QLabel { color: black; }
            QComboBox { background-color: white; color: black; border: 1px solid #ccc; }
            QLineEdit { background-color: white; color: black; border: 1px solid #ccc; }
        """)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.home_tab()
        self.tabs.addTab(self.home_widget, "Home")

        self.performance_insights_tab()
        self.tabs.addTab(self.insights_widget, "Performance Insights")

        # Settings tab
        self.settings_tab()
        self.tabs.addTab(self.settings_widget, "Settings")

    def update_task_list(self):
        self.tasks = select_all_tasks(self.conn)  # Refresh the task list from the database
        task_titles = [f"{task[1]} {task[2]} {task[3]} {task[4]} {task[5]}" for task in self.tasks]  # task[1]: title, task[4]: priority
        self.tasks_model.setStringList(task_titles)

    def add_task(self):
        title = self.title_edit.text()
        description = self.description_edit.text()
        category = self.category_edit.text()
        priority = self.priority_dropdown.currentText()
        deadline = self.deadline_edit.text()
        if title and priority and deadline:
            task = (title, description, category, priority, deadline)
            insert_task(self.conn, task)
            self.update_task_list()
            self.status_label.setText("Task added successfully")
            self.clear_input_fields()
        else:
            self.status_label.setText("Please fill in title, priority, and deadline")

    def update_task_gui(self):
        self.status_label.setText("Update task logic not fully implemented")

    def delete_task(self):
        # Get the selected task from the list view
        selected_index = self.tasks_list_view.currentIndex()

        if not selected_index.isValid():
            self.status_label.setText("Please select a task to delete.")
            return

        # Retrieve the selected task's title (e.g., "Task Title - High")
        selected_task_title = self.tasks_model.data(selected_index, 0).split(" ")[0]

        # Find the task ID corresponding to the selected title
        task_id = None
        for task in self.tasks:
            if task[1] == selected_task_title:
                task_id = task[0]
                break

        if task_id:
            # Delete the task from the database
            delete_task(self.conn, task_id)
            self.update_task_list()
            self.status_label.setText("Task deleted successfully.")
        else:
            self.status_label.setText("Task not found in the database.")

    def clear_input_fields(self):
        self.title_edit.clear()
        self.description_edit.clear()
        self.category_edit.clear()

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.home_tab()
        self.tabs.addTab(self.home_widget, "Home")

        self.performance_insights_tab()
        self.tabs.addTab(self.insights_widget, "Performance Insights")

        # Settings tab
        self.settings_tab()
        self.tabs.addTab(self.settings_widget, "Settings")

    def home_tab(self):
        self.home_widget = home_tab(self)

    def performance_insights_tab(self):
        self.insights_widget = performance_insights_tab(self)

    def settings_tab(self):
        self.settings_widget = settings_tab(self)

    # Define the checkbox toggle handler
    def on_checkbox_toggled(self):
        if self.theme_checkbox.isChecked():
            # Apply dark mode theme to entire application, including tabs
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: white; }
                QTabWidget { background-color: #2b2b2b; color: white; }
                QTabBar::tab { background-color: #555555; color: white; padding: 10px; }
                QTabBar::tab:selected { background-color: #888888; }
                QPushButton { background-color: #555555; color: white; border: 1px solid #333; }
                QCheckBox { color: white; }
                QLabel { color: white; }
                QComboBox { background-color: #444444; color: white; border: 1px solid #333; }
                QLineEdit { background-color: #444444; color: white; border: 1px solid #333; }
            """)
            self.result_label.setText("Dark Mode is ON")
        else:
            # Revert to light mode theme
            self.setStyleSheet("""
                QWidget { background-color: white; color: black; }
                QTabWidget { background-color: white; color: black; }
                QTabBar::tab { background-color: #f0f0f0; color: black; padding: 10px; }
                QTabBar::tab:selected { background-color: #dcdcdc; }
                QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #ccc; }
                QCheckBox { color: black; }
                QLabel { color: black; }
                QComboBox { background-color: white; color: black; border: 1px solid #ccc; }
                QLineEdit { background-color: white; color: black; border: 1px solid #ccc; }
            """)
            self.result_label.setText("Dark Mode is OFF")
