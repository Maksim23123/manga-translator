import os
import sys

from PySide6.QtWidgets import QApplication

project_root = os.path.abspath(os.path.join(__file__, "..", ".."))  # adjust depth
sys.path.append(os.path.join(project_root, "app"))
sys.path.append(os.path.join(project_root, "app", "third_party", "PyFlow"))

from gui.gui import GUI
from core.core import Core
from controller.controller import Contorller


def main():
    app = QApplication(sys.argv)
    core = Core()
    gui = GUI(core)
    controller = Contorller(core, gui)
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()