from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QLabel, QComboBox, QSlider, QPushButton, QColorDialog, QHBoxLayout
)
from PySide6.QtCore import Qt

def settings_tab(gui_instance):
    settings_widget = QWidget()
    settings_layout = QVBoxLayout()
    settings_widget.setLayout(settings_layout)

    # Text color picker
    text_color_layout = QHBoxLayout()
    text_color_button = QPushButton("Choose Text Color")
    text_color_button.clicked.connect(gui_instance.open_text_color_picker)
    gui_instance.text_color_label = QLabel("Selected Text Color: None")
    text_color_layout.addWidget(text_color_button)
    text_color_layout.addWidget(gui_instance.text_color_label)
    settings_layout.addLayout(text_color_layout)

    # Preset themes dropdown
    preset_theme_label = QLabel("Preset Themes")
    gui_instance.preset_theme_dropdown = QComboBox()
    gui_instance.preset_theme_dropdown.addItems([
        "Default (White Background, Black Text)",
        "Ocean (Blue Background, White Text)",
        "Sunset (Orange Background, Dark Brown Text)",
        "Forest (Green Background, White Text)",
        "Lavender Bliss (Light Purple Background, Dark Purple Text)",
        "Solar Flare (Bright Yellow Background, Dark Red Text)",
        "Cool Breeze (Light Cyan Background, Navy Blue Text)",
        "Crimson Night (Dark Red Background, Light Gray Text)",
    ])
    gui_instance.preset_theme_dropdown.currentIndexChanged.connect(gui_instance.apply_preset_theme)
    settings_layout.addWidget(preset_theme_label)
    settings_layout.addWidget(gui_instance.preset_theme_dropdown)

    # Font type setting
    font_label = QLabel("Select Font Type")
    gui_instance.font_dropdown = QComboBox()
    gui_instance.font_dropdown.addItems(["Arial", "Verdana", "Tahoma", "Courier New", "Times New Roman", "Helvetica"])
    gui_instance.font_dropdown.currentTextChanged.connect(gui_instance.change_font_type)
    settings_layout.addWidget(font_label)
    settings_layout.addWidget(gui_instance.font_dropdown)

    # Font size setting
    font_size_label = QLabel("Adjust Font Size")
    gui_instance.font_size_slider = QSlider(Qt.Horizontal)
    gui_instance.font_size_slider.setMinimum(8)
    gui_instance.font_size_slider.setMaximum(36)
    gui_instance.font_size_slider.setValue(12)
    gui_instance.font_size_slider.valueChanged.connect(gui_instance.change_font_size)
    gui_instance.font_size_display = QLabel("Font Size: 12px")
    settings_layout.addWidget(font_size_label)
    settings_layout.addWidget(gui_instance.font_size_slider)
    settings_layout.addWidget(gui_instance.font_size_display)

    # Dark mode checkbox
    gui_instance.theme_checkbox = QCheckBox("Enable Dark Theme")
    gui_instance.theme_checkbox.setChecked(False)
    gui_instance.theme_checkbox.toggled.connect(gui_instance.on_checkbox_toggled)
    settings_layout.addWidget(gui_instance.theme_checkbox)

    # Result label for current theme mode
    gui_instance.result_label = QLabel("Dark Mode is OFF", gui_instance)
    settings_layout.addWidget(gui_instance.result_label)

    return settings_widget
