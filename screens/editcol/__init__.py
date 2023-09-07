from tkinter import (
    Toplevel,
    Event,
    StringVar
)

from ..screen import Screen

scale: dict[str: dict] = {
    "args": {},
    "grid_config": {
        "rows": [],
        "cols": []
    },
    "elements": {
        "min_label": {
            "type": "Label",
            "args": {
                "text": "Minimum",
                "anchor": "w"
            },
            "grid": {
                "row": 0,
                "column": 0,
                "sticky": "w"
            }
        },
        "min_spinbox": {
            "type": "Spinbox",
            "args": {
                "format": "%3.2"
            },
            "grid": {
                "row": 0,
                "column": 1,
                "sticky": "e"
            }
        },
        "max_label": {
            "type": "Label",
            "args": {
                "text": "Maximum",
                "anchor": "w"
            },
            "grid": {
                "row": 1,
                "column": 0,
                "sticky": "w"
            }
        },
        "max_spinbox": {
            "type": "Spinbox",
            "args": {
                "format": "%3.2"
            },
            "grid": {
                "row": 1,
                "column": 1,
                "sticky": "e"
            }
        }
    }
}


class EditColumnScreen(Screen):
    column_config: dict = {
        "name": 'New column',
        "type": 'text',
        "data": {
            "default": 'empty'
        }
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

        print(self.compiled_elements["default_value"])
