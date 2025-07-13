from gui.gui import GUI
from core.core import Core
from controller.controller import Contorller
import os

def main():
    core = Core()
    controller = Contorller(core)
    gui = GUI(core, controller)


if __name__ == '__main__':
    main()