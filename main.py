# coding:utf-8

from controller.controller import Controller
from view.views import Views


def main():
    view = Views()
    program = Controller(view)
    program.run()


main()
