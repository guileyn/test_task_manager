from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QColorDialog, QSlider, QComboBox
from database import create_connection, select_all_tasks, insert_task, delete_task, mark_task_completed
from home_tab import home_tab
from performance_insights_tab import performance_insights_tab
from settings_tab import settings_tab
import datetime

class TaskManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = create_connection()  # Initialize the database connection
        self.tasks = select_all_tasks(self.conn)  # Initialize the task list from the database

        # Initialize font settings with default values
        self.current_font_size = 12         # Default font size
        self.current_font_family = "Arial"  # Default font family
        self.current_theme_color = "white"  # Default theme color
        self.current_text_color = "black"  # Default text color

        self.initUI()  # Initialize UI elements after initializing tasks
        self.tasks_model = QStringListModel()
        self.tasks_list_view.setModel(self.tasks_model)
        self.update_task_list()

    def initUI(self):
        self.setWindowTitle('Task Manager GUI')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Define the stylesheet with dynamic font settings
        self.setStyleSheet(f"""
            QWidget {{ background-color: {self.current_theme_color}; color: {self.current_text_color}; font-family: {self.current_font_family}; font-size: {self.current_font_size}px; }}
            QTabWidget {{ background-color: {self.current_theme_color}; color: {self.current_text_color}; }}
            QTabBar::tab {{ background-color: #f0f0f0; color: {self.current_text_color}; padding: 10px; }}
            QTabBar::tab:selected {{ background-color: #dcdcdc; }}
            QPushButton {{ background-color: #f0f0f0; color: {self.current_text_color}; border: 1px solid #ccc; }}
            QCheckBox {{ color: {self.current_text_color}; }}
            QLabel {{ color: {self.current_text_color}; }}
            QComboBox {{ background-color: {self.current_theme_color}; color: {self.current_text_color}; border: 1px solid #ccc; }}
            QLineEdit {{ background-color: {self.current_theme_color}; color: {self.current_text_color}; border: 1px solid #ccc; }}
        """)

        # Font size slider and font family dropdown should be connected to the change functions
        self.font_size_slider = QSlider()  # Add font size slider
        self.font_size_slider.setRange(8, 30)  # Font size range (8px to 30px)
        self.font_size_slider.setValue(self.current_font_size)  # Set default font size
        self.font_size_slider.valueChanged.connect(self.change_font_size)

        self.font_type_dropdown = QComboBox()  # Add font family dropdown
        self.font_type_dropdown.addItems(["Arial", "Courier New", "Times New Roman", "Verdana", "Tahoma"])  # Add font options
        self.font_type_dropdown.setCurrentText(self.current_font_family)  # Set default font family
        self.font_type_dropdown.currentTextChanged.connect(self.change_font_type)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.home_tab()
        self.tabs.addTab(self.home_widget, "Home")

        self.performance_insights_tab()
        self.tabs.addTab(self.insights_widget, "Performance Insights")

        self.settings_tab()
        self.tabs.addTab(self.settings_widget, "Settings")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """Reload the content of the selected tab when the tab is changed."""
        tab_name = self.tabs.tabText(index)
        if tab_name == "Performance Insights":
            print("changed")
            self.reload_performance_insights_tab()

    def reload_performance_insights_tab(self):
        """Reload the Performance Insights tab."""
        self.insights_widget.layout().deleteLater()  # Delete the existing layout
        self.performance_insights_tab()  # Recreate the Performance Insights tab layout

    def update_task_list(self):
        self.tasks = select_all_tasks(self.conn)  # Refresh the task list from the database
        task_titles = []
        for task in self.tasks:
            completed = "(Not Completed)"
            if task[6] and task[7] != "0":
                completed = f"(Completed on {task[7]})"

            task_titles.append(f"{task[1]} {task[2]} {task[3]} {task[4]} {task[5]} {completed}")
        self.tasks_model.setStringList(task_titles)

    def add_task(self):
        title = self.title_edit.text()
        description = self.description_edit.text()
        category = self.category_dropdown.currentText()
        priority = self.priority_dropdown.currentText()
        deadline = self.deadline_edit.text()

        if title and priority and deadline:
            unique_title = True
            for task in self.tasks:
                if task[1] == title:
                    unique_title = False
                    break
            if unique_title:
                task = (title, description, category, priority, deadline)
                try:
                    # Attempt to insert the task
                    insert_task(self.conn, task)
                    self.update_task_list()
                    self.status_label.setText("Task added successfully")
                    self.clear_input_fields()
                except Exception as e:
                    # Handle any exception that occurs during insertion (e.g., duplicate title)
                    self.status_label.setText(f"Error: {str(e)}")
            else:
                self.clear_input_fields()
                self.status_label.setText("Title must be unique")
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

    def complete_task(self):
        # Get the selected task from the list view
        selected_index = self.tasks_list_view.currentIndex()

        if not selected_index.isValid():
            self.status_label.setText("Please select a task to complete.")
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
            # Mark the task completed
            if task[6] == 1:
                self.status_label.setText("Task already completed.")
            else:
                completion_date = datetime.datetime.today()
                mark_task_completed(self.conn, completion_date, task_id)
                self.update_task_list()
                self.status_label.setText("Task completed successfully.")
        else:
            self.status_label.setText("Task not found in the database.")

    def clear_input_fields(self):
        self.title_edit.clear()
        self.description_edit.clear()
        self.category_dropdown.setCurrentIndex(0)

    def home_tab(self):
        self.home_widget = home_tab(self)

    def performance_insights_tab(self):
        self.insights_widget = performance_insights_tab(self)

    def settings_tab(self):
        self.settings_widget = settings_tab(self)

    def open_color_picker(self):
        color = QColorDialog.getColor()  # Open color picker dialog for the theme
        if color.isValid():
            self.current_theme_color = color.name()
            self.update_stylesheet()  # Update the theme without affecting font settings
            self.color_label.setText(f"Selected Theme Color: {color.name()}")

    def open_text_color_picker(self):
        color = QColorDialog.getColor()  # Open color picker dialog for the text
        if color.isValid():
            self.current_text_color = color.name()
            self.update_stylesheet()  # Update the text color without affecting the theme
            self.text_color_label.setText(f"Selected Text Color: {color.name()}")

    def apply_preset_theme(self, index):
        # Define preset themes as (background_color, text_color)
        themes = [
            ("white", "black"),  # Default
            ("#1e90ff", "white"),  # Ocean
            ("#ff4500", "#5a3100"),  # Sunset
            ("#228b22", "white"),  # Forest
            ("#e6e6fa", "#4b0082"),  # Lavender Bliss
            ("#ffff00", "#8b0000"),  # Solar Flare
            ("#e0ffff", "#000080"),  # Cool Breeze
            ("#8b0000", "#dcdcdc"),  # Crimson Night
        ]

        if index < len(themes):
            self.current_theme_color, self.current_text_color = themes[index]
            self.update_stylesheet()  # Update theme and text color without affecting font settings

    def update_stylesheet(self):
        """
        Updates the entire stylesheet, including theme, font size, and font family.
        """
        self.setStyleSheet(f"""
            QWidget {{ background-color: {self.current_theme_color}; color: {self.current_text_color}; font-family: {self.current_font_family}; font-size: {self.current_font_size}px; }}
            QLabel {{ color: {self.current_text_color}; }}
            QPushButton {{ color: {self.current_text_color}; background-color: {self.current_theme_color}; border: 1px solid {self.current_text_color}; }}
            QCheckBox {{ color: {self.current_text_color}; }}
            QComboBox {{ color: {self.current_text_color}; background-color: {self.current_theme_color}; border: 1px solid {self.current_text_color}; }}
            QLineEdit {{ color: {self.current_text_color}; background-color: {self.current_theme_color}; border: 1px solid {self.current_text_color}; }}
        """)

    def change_font_size(self, value):
        """
        Adjusts the font size based on the slider value.
        """
        self.current_font_size = value
        self.update_stylesheet()  # Update the font size without affecting the theme
        self.font_size_display.setText(f"Font Size: {value}px")

    def change_font_type(self, font_name):
        """
        Updates the font family dynamically by changing the selected font.
        """
        self.current_font_family = font_name
        self.update_stylesheet()  # Update the font type without affecting the theme

    def on_checkbox_toggled(self):
        if self.theme_checkbox.isChecked():
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
