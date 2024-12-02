# main.py
from PySide6.QtWidgets import QApplication
from task_manager_gui import TaskManagerGUI
import sys

def main():
    app = QApplication(sys.argv)
    ex = TaskManagerGUI()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
