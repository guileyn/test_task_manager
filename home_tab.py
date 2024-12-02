# home_tab.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QDateEdit, QLabel, QPushButton, QListView
from PySide6.QtCore import QDate

def home_tab(gui_instance):
    home_widget = QWidget()
    home_layout = QVBoxLayout()
    home_widget.setLayout(home_layout)

    # Input fields
    input_layout = QHBoxLayout()
    home_layout.addLayout(input_layout)
    gui_instance.title_edit = QLineEdit()
    gui_instance.description_edit = QLineEdit()
    gui_instance.category_dropdown = QComboBox()
    gui_instance.category_dropdown.addItems(["Academic", "Work", "Personal", "Extracurricular"])
    gui_instance.priority_dropdown = QComboBox()
    gui_instance.priority_dropdown.addItems(["High", "Medium", "Low"])
    gui_instance.deadline_edit = QDateEdit()
    gui_instance.deadline_edit.setDate(QDate.currentDate())
    gui_instance.deadline_edit.setMinimumWidth(120)
    input_layout.addWidget(QLabel("Title:"))
    input_layout.addWidget(gui_instance.title_edit)
    input_layout.addWidget(QLabel("Description:"))
    input_layout.addWidget(gui_instance.description_edit)
    input_layout.addWidget(QLabel("Category:"))
    input_layout.addWidget(gui_instance.category_dropdown)
    input_layout.addWidget(QLabel("Priority:"))
    input_layout.addWidget(gui_instance.priority_dropdown)
    input_layout.addWidget(QLabel("Deadline:"))
    input_layout.addWidget(gui_instance.deadline_edit)

    # Buttons
    buttons_layout = QHBoxLayout()
    home_layout.addLayout(buttons_layout)
    add_button = QPushButton('Add Task')
    add_button.clicked.connect(gui_instance.add_task)
    update_button = QPushButton('Update Task')
    update_button.clicked.connect(gui_instance.update_task_gui)
    delete_button = QPushButton('Delete Task')
    delete_button.clicked.connect(gui_instance.delete_task)
    complete_button = QPushButton('Complete Task')
    complete_button.clicked.connect(gui_instance.complete_task)
    buttons_layout.addWidget(add_button)
    buttons_layout.addWidget(update_button)
    buttons_layout.addWidget(delete_button)
    buttons_layout.addWidget(complete_button)

    # Task list
    gui_instance.tasks_list_view = QListView()
    home_layout.addWidget(gui_instance.tasks_list_view)

    # Status label
    gui_instance.status_label = QLabel()
    home_layout.addWidget(gui_instance.status_label)

    return home_widget
