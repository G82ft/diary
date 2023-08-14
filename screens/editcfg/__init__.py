import json
from os.path import basename
from tkinter import (
    Toplevel, Frame, Button, Event
)

from .table import Table, Column
from utils.config import is_config, DEFAULT_CONFIG
from ..screen import Screen


class EditConfigScreen(Screen):
    path: str
    config: dict = None
    columns_table: Table
    canceled: bool = True

    def __init__(self, master: Toplevel, path: str = DEFAULT_CONFIG):
        self.id = "editcfg"
        self.path = path

        super().__init__(master)

        if not is_config(self.path):
            raise ValueError(f'Passed path is not config! ("{self.path}")')

        with open(self.path) as file:
            self.config = json.load(file)

    def preconfigure_root(self, root_config: dict) -> None:
        if self.path == DEFAULT_CONFIG:
            root_config["title"] = 'Add config'
        else:
            root_config["title"] = f'Edit config {basename(self.path)}'

    def preconfigure_elements(self):
        save_cancel_frame: dict = self.elements["save_cancel_frame"]["elements"]
        save_cancel_frame["save"]["args"]["command"] = self.save
        save_cancel_frame["cancel"]["args"]["command"] = self.cancel

    def configure_element(self, name: str, element_type: type, element):
        match name:
            case "tags":
                element["text"] = ' '.join(self.config["tags"])

    def on_load(self, e: Event):
        columns_frame: Frame = self.compiled_elements["columns_frame"]
        self.columns_table: Table = Table(columns_frame)

        columns_frame.rowconfigure(0, weight=1)
        columns_frame.columnconfigure(0, weight=1)

        for i, (name, info) in enumerate(self.config["columns"].items()):
            column: Column = Column(self.columns_table)
            for j, (text, color) in enumerate((
                    (name, 'gray'),
                    (info["default"], 'white')
            )):
                column.append(
                    Button(
                        column.frame,
                        text=text,
                        background=color,
                        command=lambda i=i, j=j: self.edit_column(i, j)
                    )
                )

            self.columns_table.append(column)

        self.columns_table.grid(
            row=0, column=0,
            sticky='nesw'
        )

    def edit_column(self, i, j, new: bool = False):
        print(
            self.columns_table[i][j]['text']
        )

    def save(self):
        self.config["tags"] = self.compiled_elements["tags"].get().split()

        self.canceled = False
        self.root.destroy()

    def cancel(self):
        self.root.destroy()
