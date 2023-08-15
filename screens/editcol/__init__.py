from tkinter import (
    Toplevel,
    Event
)

from ..screen import Screen


class EditColumnScreen(Screen):
    column_config: dict = {
        "name": 'New column',
        "type": 'text',
        "default": 'empty'
    }

    def __init__(self, master: Toplevel, column_config: dict):
        self.id = 'editcol'
        super().__init__(master)

        self.column_config |= column_config

    def preconfigure_root(self, root_config: dict) -> None:
        if self.column_config["name"] == 'New column':
            root_config["title"] = 'Add column'
        else:
            root_config["title"] = f'Edit column "{self.column_config["name"]}"'

    def preconfigure_elements(self):
        pass

    def configure_element(self, name: str, element_type: type, element):
        pass

    def on_load(self, e: Event):
        pass
