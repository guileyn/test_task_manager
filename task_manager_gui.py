# task_manager_gui.py
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from ui_components import home_tab, performance_insights_tab, settings_tab
from task_operations import update_task_list, add_task, delete_task
from insights import calculate_average_task_completion_time, calculate_priority_based_time_distribution, calculate_weekly_monthly_trends
from database import create_connection, select_all_tasks

class TaskManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = create_connection()  # Initialize the database connection
        self.tasks = select_all_tasks(self.conn)  # Initialize the task list from the database

        self.initUI()  # Initialize UI elements after initializing tasks

    def initUI(self):
        self.setWindowTitle('Task Manager GUI')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.home_tab()
        self.tabs.addTab(self.home_widget, "Home")

        self.performance_insights_tab()
        self.tabs.addTab(self.insights_widget, "Performance Insights")

        self.settings_tab()
        self.tabs.addTab(self.settings_widget, "Settings")

    def update_task_list(self):
        self.tasks = select_all_tasks(self.conn)  # Refresh the task list from the database
        update_task_list(self.tasks)  # Function for updating task list display

    def add_task(self):
        add_task(self)  # Moves add task logic to a separate function

    def delete_task(self):
        delete_task(self)  # Moves delete task logic to a separate function

    def home_tab(self):
        self.home_widget = home_tab(self)

    def performance_insights_tab(self):
        self.insights_widget = performance_insights_tab(self.tasks)

    def settings_tab(self):
        self.settings_widget = settings_tab()