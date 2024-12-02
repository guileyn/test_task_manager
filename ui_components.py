# ui_components.py
from PySide6.QtCore import QDate  # Add this import
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
    update_button.clicked.connect(gui_instance.update_task_list)
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

def on_checkbox_toggled(self):
    if self.theme_checkbox.isChecked():
        self.setStyleSheet(dark_mode_styles())
        self.result_label.setText("Dark Mode is ON")
    else:
        self.setStyleSheet(light_mode_styles())
        self.result_label.setText("Dark Mode is OFF")

def light_mode_styles():
    return """
        QWidget { background-color: white; color: black; }
        QTabWidget { background-color: white; color: black; }
        QTabBar::tab { background-color: #f0f0f0; color: black; padding: 10px; }
        QTabBar::tab:selected { background-color: #dcdcdc; }
        QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #ccc; }
        QCheckBox { color: black; }
        QLabel { color: black; }
        QComboBox { background-color: white; color: black; border: 1px solid #ccc; }
        QLineEdit { background-color: white; color: black; border: 1px solid #ccc; }
    """

def dark_mode_styles():
    return """
        QWidget { background-color: #2b2b2b; color: white; }
        QTabWidget { background-color: #2b2b2b; color: white; }
        QTabBar::tab { background-color: #555555; color: white; padding: 10px; }
        QTabBar::tab:selected { background-color: #888888; }
        QPushButton { background-color: #555555; color: white; border: 1px solid #333; }
        QCheckBox { color: white; }
        QLabel { color: white; }
        QComboBox { background-color: #444444; color: white; border: 1px solid #333; }
        QLineEdit { background-color: #444444; color: white; border: 1px solid #333; }
    """

def settings_tab():
    settings_widget = QWidget()
    settings_layout = QVBoxLayout()
    settings_widget.setLayout(settings_layout)

    # Theme setting
    theme_checkbox = QCheckBox("Enable Dark Theme")
    theme_checkbox.setChecked(False)
    theme_checkbox.toggled.connect(on_checkbox_toggled)  # Connect to function
    settings_layout.addWidget(theme_checkbox)
    
    result_label = QLabel('Dark Mode is OFF')
    settings_layout.addWidget(result_label)


    # Default priority setting
    priority_label = QLabel("Default Priority")
    default_priority_dropdown = QComboBox()
    default_priority_dropdown.addItems(["High", "Medium", "Low"])
    settings_layout.addWidget(priority_label)
    settings_layout.addWidget(default_priority_dropdown)

    # Default category setting
    category_label = QLabel("Default Category")
    default_category_dropdown = QComboBox()
    default_category_dropdown.addItems(["Work", "Personal", "Other"])
    settings_layout.addWidget(category_label)
    settings_layout.addWidget(default_category_dropdown)
    return settings_widget
