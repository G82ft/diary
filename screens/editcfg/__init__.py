import json
from os.path import basename
from tkinter import (
    Widget,
    Toplevel, Frame, Entry,
    Event,
    StringVar, Button,
    messagebox as msgbox
)

from utils.config import validate_config, DEFAULT_CONFIG
from .table import Table, Column
from ..screen import Screen
from ..editcol import EditColumnScreen


class EditConfigScreen(Screen):
    path: str
    config: dict = None

    canceled: bool = True

    columns_table: Table

    selected_cell: tuple[int, int] = 0, 0
    entry: Entry | None = None
    entry_var: StringVar = StringVar()

    edit_column_screen: EditColumnScreen | None = None

    def __init__(self, master: Toplevel, path: str = DEFAULT_CONFIG):
        self.id = "editcfg"
        self.path = path

        super().__init__(master)

        # TODO: Add handling
        validate_config(self.path)

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

        for i, info in enumerate(self.config["columns"]):
            column: Column = Column(self.columns_table)
            for j, (text, color) in enumerate((
                    (info["name"], 'gray'),
                    (info["default"], 'white')
            )):
                cell: Button = Screen.compile_element(
                    column.frame,
                    {
                        "type": 'Button',
                        "args": {
                            "text": text,
                            "background": color,
                            "command": lambda x=i, y=j: self.edit_text(x, y)
                        }
                    }
                )
                cell.bind('<ButtonRelease-3>', lambda _, x=i, y=j: self.edit_column(x))
                column.append(
                    cell
                )

            self.columns_table.append(column)

        self.columns_table.grid(
            row=0, column=0,
            sticky='nesw'
        )

    def edit_text(self, x: int, y: int):
        if self.entry is not None:
            self.end_text_edit()

        self.selected_cell = x, y

        if self.config["columns"][x]["type"] != "text" and y != 0:
            return

        widget: Widget = self.columns_table[x][y]
        self.entry_var.set(widget["text"])

        self.entry: Entry = Screen.compile_element(
            self.columns_table[x].frame,
            {
                "type": 'Entry',
                "args": {
                    "background": widget["background"],
                    "font": widget["font"],
                    "justify": 'left',
                    "relief": 'sunken',
                    "textvariable": self.entry_var
                }
            }
        )

        self.entry.place(
            x=widget.winfo_x(), y=widget.winfo_y(),
            width=widget.winfo_width(), height=widget.winfo_height()
        )

        self.entry.select_range(0, 'end')
        self.entry.focus_set()

        self.entry.bind('<FocusOut>', lambda e: self.end_text_edit())
        self.entry.bind('<Return>', lambda e: self.end_text_edit())

    def end_text_edit(self):
        if self.entry is None:
            return

        self.entry.destroy()
        self.entry = None

        x, y = self.selected_cell

        if y == 0:
            self.config["columns"][x]["name"] = \
                self.columns_table[x][y]["text"] = \
                self.entry_var.get()
        else:
            self.config["columns"][x]["default"] = \
                self.columns_table[x][y]["text"] = \
                self.entry_var.get()

    def edit_column(self, x: int):
        if self.edit_column_screen is not None:
            msgbox.showwarning(
                'Edit column',
                'You are already editing another column.'
            )
            return

        self.edit_column_screen = EditColumnScreen(
            self.root,
            self.config["columns"][x]
        )
        self.edit_column_screen.show()

    def save(self):
        self.config["tags"] = self.compiled_elements["tags"].get().split()

        self.canceled = False
        self.root.destroy()

    def cancel(self):
        self.root.destroy()
