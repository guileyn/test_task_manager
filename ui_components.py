# ui_components.py
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QCheckBox, QDateEdit, QLabel, QWidget

def home_tab(gui_instance):
    home_widget = QWidget()
    home_layout = QVBoxLayout()
    home_widget.setLayout(home_layout)

    # Input fields
    input_layout = QHBoxLayout()
    home_layout.addLayout(input_layout)
    
    gui_instance.title_edit = QLineEdit()
    gui_instance.description_edit = QLineEdit()
    gui_instance.category_edit = QLineEdit()
    gui_instance.priority_dropdown = QComboBox()
    gui_instance.priority_dropdown.addItems(["High", "Medium", "Low"])
    gui_instance.deadline_edit = QDateEdit()
    gui_instance.deadline_edit.setDate(QDate.currentDate())
    input_layout.addWidget(QLabel("Title:"))
    input_layout.addWidget(gui_instance.title_edit)
    input_layout.addWidget(QLabel("Description:"))
    input_layout.addWidget(gui_instance.description_edit)
    input_layout.addWidget(QLabel("Category:"))
    input_layout.addWidget(gui_instance.category_edit)
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
    buttons_layout.addWidget(add_button)
    buttons_layout.addWidget(update_button)
    buttons_layout.addWidget(delete_button)

    return home_widget

def performance_insights_tab(tasks):
    insights_widget = QWidget()
    insights_layout = QVBoxLayout()
    insights_widget.setLayout(insights_layout)

    # Calculate insights and create views for charts
    # (this logic will be in the next section)

    return insights_widget

def settings_tab():
    settings_widget = QWidget()
    settings_layout = QVBoxLayout()
    settings_widget.setLayout(settings_layout)

    # Settings UI (checkbox, dropdowns for priority, category)
    return settings_widget
