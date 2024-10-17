import flet as ft

from .gui.gui import kintree_gui


def main(view='flet_app'):
    if view == 'browser':
        ft.app(target=kintree_gui, view=ft.AppView.WEB_BROWSER)
        return
    ft.app(target=kintree_gui, view=ft.AppView.FLET_APP)
