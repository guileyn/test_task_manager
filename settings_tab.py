# settings_tab.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QComboBox

# settings_tab.py
def settings_tab(gui_instance):
    settings_widget = QWidget()
    settings_layout = QVBoxLayout()
    settings_widget.setLayout(settings_layout)

    # Theme setting
    gui_instance.theme_checkbox = QCheckBox("Enable Dark Theme")
    gui_instance.theme_checkbox.setChecked(False)
    gui_instance.theme_checkbox.toggled.connect(gui_instance.on_checkbox_toggled)  # Now this correctly refers to the method
    settings_layout.addWidget(gui_instance.theme_checkbox)
    
    gui_instance.result_label = QLabel('Dark Mode is OFF', gui_instance)  # Ensure result_label is part of the GUI
    settings_layout.addWidget(gui_instance.result_label)

    # Default priority setting
    priority_label = QLabel("Default Priority")
    gui_instance.default_priority_dropdown = QComboBox()
    gui_instance.default_priority_dropdown.addItems(["High", "Medium", "Low"])
    settings_layout.addWidget(priority_label)
    settings_layout.addWidget(gui_instance.default_priority_dropdown)

    # Default category setting
    category_label = QLabel("Default Category")
    gui_instance.default_category_dropdown = QComboBox()
    gui_instance.default_category_dropdown.addItems(["Work", "Personal", "Other"])
    settings_layout.addWidget(category_label)
    settings_layout.addWidget(gui_instance.default_category_dropdown)

    return settings_widget
