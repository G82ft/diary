from tkinter import (
    Toplevel,
    Event,
    StringVar
)

from ..screen import Screen

specific_setting: dict[str: dict] = {
    "scale": {
        "grid_config": {
            "rows": [1, 1],
            "cols": [1, 1]
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
                    "format": "%3.2f"
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
                    "format": "%3.2f"
                },
                "grid": {
                    "row": 1,
                    "column": 1,
                    "sticky": "e"
                }
            }
        }
    }
}


class EditColumnScreen(Screen):
    canceled: bool = False
    column_config: dict

    name_var: StringVar = StringVar()
    type_var: StringVar = StringVar()
    default_var: StringVar = StringVar()

    def __init__(self, master: Toplevel, column_config: dict):
        self.id = 'editcol'
        self.column_config = {
            "name": 'New column',
            "type": 'text',
            "data": {
                "default": 'empty'
            }
        }
        self.column_config |= column_config

        super().__init__(master)

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

        frame = specific_setting.get(self.column_config["type"], {})

        self.compiled_elements["specific_settings"] = Screen.compile_frame(
            self.frame,
            frame.get("args", {}), frame["grid_config"],
            frame["elements"], self.compiled_elements,
            lambda *_: _
        )
        self.compiled_elements["specific_settings"].grid(
            self.elements["specific_settings"]["grid"]
        )
