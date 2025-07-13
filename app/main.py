from gui.gui import GUI
from core.core import Core
from controller.controller import Contorller

def main():
    core = Core()
    controller = Contorller(core)
    gui = GUI(controller)


if __name__ == '__main__':
    main()