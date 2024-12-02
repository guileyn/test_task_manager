# task_manager_gui.py
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from ui_components import home_tab, performance_insights_tab, settings_tab
from task_operations import update_task_list, add_task, delete_task
from insights import calculate_average_task_completion_time, calculate_priority_based_time_distribution, calculate_weekly_monthly_trends
from database import select_all_tasks

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















import sys
from PySide6.QtCore import Qt, QDate, QStringListModel
from PySide6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListView, QComboBox, QCheckBox, QDateEdit
)
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet
from PySide6.QtGui import QPainter
from insights import calculate_average_task_completion_time, calculate_priority_based_time_distribution, calculate_weekly_monthly_trends
from database import create_connection, select_all_tasks, insert_task, delete_task

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

    def home_tab(self):
        self.home_widget = QWidget()
        home_layout = QVBoxLayout()
        self.home_widget.setLayout(home_layout)

        # Input fields
        input_layout = QHBoxLayout()
        home_layout.addLayout(input_layout)
        self.title_edit = QLineEdit()
        self.description_edit = QLineEdit()
        self.category_edit = QLineEdit()
        self.priority_dropdown = QComboBox()
        self.priority_dropdown.addItems(["High", "Medium", "Low"])
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setDate(QDate.currentDate())
        input_layout.addWidget(QLabel("Title:"))
        input_layout.addWidget(self.title_edit)
        input_layout.addWidget(QLabel("Description:"))
        input_layout.addWidget(self.description_edit)
        input_layout.addWidget(QLabel("Category:"))
        input_layout.addWidget(self.category_edit)
        input_layout.addWidget(QLabel("Priority:"))
        input_layout.addWidget(self.priority_dropdown)
        input_layout.addWidget(QLabel("Deadline:"))
        input_layout.addWidget(self.deadline_edit)

        # Buttons
        buttons_layout = QHBoxLayout()
        home_layout.addLayout(buttons_layout)
        add_button = QPushButton('Add Task')
        add_button.clicked.connect(self.add_task)
        update_button = QPushButton('Update Task')
        update_button.clicked.connect(self.update_task_gui)
        delete_button = QPushButton('Delete Task')
        delete_button.clicked.connect(self.delete_task)
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(update_button)
        buttons_layout.addWidget(delete_button)

        # Task list
        self.tasks_list_view = QListView()
        home_layout.addWidget(self.tasks_list_view)

        # Status label
        self.status_label = QLabel()
        home_layout.addWidget(self.status_label)

    def performance_insights_tab(self):
        self.insights_widget = QWidget()
        insights_layout = QVBoxLayout()
        self.insights_widget.setLayout(insights_layout)

        # Average Task Completion Time
        average_time = calculate_average_task_completion_time(self.tasks)
        average_time_label = QLabel(f"Average Task Completion Time: {average_time} days")
        insights_layout.addWidget(average_time_label)

        # Priority-Based Time Distribution
        priority_time = calculate_priority_based_time_distribution(self.tasks)
        priority_pie_series = QPieSeries()
        priority_pie_series.append("High", priority_time["high"])
        priority_pie_series.append("Medium", priority_time["medium"])
        priority_pie_series.append("Low", priority_time["low"])
        priority_chart = QChart()
        priority_chart.legend().hide()
        priority_chart.addSeries(priority_pie_series)
        priority_chart.createDefaultAxes()
        priority_chart.setTitle("Priority-Based Time Distribution")
        priority_chart_view = QChartView(priority_chart)
        insights_layout.addWidget(priority_chart_view)

        # Weekly/Monthly Trends
        tasks_per_week, tasks_per_month = calculate_weekly_monthly_trends(self.tasks)
        week_bar_set = QBarSet("Tasks per Week")
        for week, count in tasks_per_week.items():
            week_bar_set.append(count)
        month_bar_set = QBarSet("Tasks per Month")
        for month, count in tasks_per_month.items():
            month_bar_set.append(count)
        trends_bar_series = QBarSeries()
        trends_bar_series.append(week_bar_set)
        trends_bar_series.append(month_bar_set)
        trends_chart = QChart()
        trends_chart.addSeries(trends_bar_series)
        trends_chart.setTitle("Weekly and Monthly Trends")
        trends_chart_view = QChartView(trends_chart)
        insights_layout.addWidget(trends_chart_view)

        if not self.tasks:
            no_data_label = QLabel("No sufficient data to provide time management insights.")
            insights_layout.addWidget(no_data_label)

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
    
    def settings_tab(self):
        
        self.settings_widget = QWidget()
        settings_layout = QVBoxLayout()
        self.settings_widget.setLayout(settings_layout)

        # Theme setting
        self.theme_checkbox = QCheckBox("Enable Dark Theme")
        self.theme_checkbox.setChecked(False)
        self.theme_checkbox.toggled.connect(self.on_checkbox_toggled)  # Connect to function
        settings_layout.addWidget(self.theme_checkbox)
        
        self.result_label = QLabel('Dark Mode is OFF', self)
        settings_layout.addWidget(self.result_label)


        # Default priority setting
        priority_label = QLabel("Default Priority")
        self.default_priority_dropdown = QComboBox()
        self.default_priority_dropdown.addItems(["High", "Medium", "Low"])
        settings_layout.addWidget(priority_label)
        settings_layout.addWidget(self.default_priority_dropdown)

        # Default category setting
        category_label = QLabel("Default Category")
        self.default_category_dropdown = QComboBox()
        self.default_category_dropdown.addItems(["Work", "Personal", "Other"])
        settings_layout.addWidget(category_label)
        settings_layout.addWidget(self.default_category_dropdown)

def main():
    app = QApplication(sys.argv)
    ex = TaskManagerGUI()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
