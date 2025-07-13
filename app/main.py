from gui.gui import GUI
from core.core import Core
from controller.controller import Contorller
import os

def main():
    core = Core()
    gui = GUI(core)
    controller = Contorller(core, gui)
    gui.show()


if __name__ == '__main__':
    main()