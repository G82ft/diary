from tkinter import (
    Toplevel, Text,
    Event,
    StringVar
)

from ..screen import Screen


class EditColumnScreen(Screen):
    column_config: dict = {
        "name": 'New column',
        "type": 'text',
        "default": 'empty'
    }

    name_var: StringVar = StringVar()
    type_var: StringVar = StringVar()
    default_var: StringVar = StringVar()

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
        self.elements["name_entry"]["args"]["textvariable"] = self.name_var

        self.elements["type_selection"]["args"].insert(0, self.type_var)

    def configure_element(self, name: str, element_type: type, element):
        pass

    def on_load(self, e: Event):
        self.name_var.set(self.column_config["name"])

        self.type_var.set(self.column_config["type"])

        default_text: Text = self.compiled_elements["default_text"]
        default_text.insert(0, self.column_config["default"])
