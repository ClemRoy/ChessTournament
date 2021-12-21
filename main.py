# coding:utf-8

from view.views import Views
from controller.controller import Controller


def main():
    view = Views()
    program = Controller(view)
    program.run()


main()
