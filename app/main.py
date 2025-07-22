import os
import sys

project_root = os.path.abspath(os.path.join(__file__, "..", ".."))  # adjust depth
sys.path.append(os.path.join(project_root, "app"))
sys.path.append(os.path.join(project_root, "app", "third_party", "PyFlow"))

from gui.gui import GUI
from core.core import Core
from controller.controller import Contorller


def main():
    core = Core()
    gui = GUI(core)
    controller = Contorller(core, gui)
    gui.show()


if __name__ == '__main__':
    main()