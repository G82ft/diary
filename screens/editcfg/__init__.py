import json
from os.path import basename
from tkinter import (
    Widget,
    Toplevel, Frame, Entry,
    Event,
    StringVar, messagebox as msgbox
)

from utils.config import validate_config, DEFAULT_CONFIG
from .table import Table, Column
from ..editcol import EditColumnScreen
from ..screen import Screen


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
            for j in range(2):
                cell = self.create_cell(
                    column.frame,
                    info,
                    i, j
                )
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

    def update_config(self):
        pass

    def edit_column(self, x: int):
        # TODO (low): Add button pressing
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
        self.edit_column_screen.root.bind('<Destroy>', self.end_editing)

        self.root.update()
        self.root.update_idletasks()

        self.edit_column_screen.show()

    def end_editing(self, e: Event):
        if self.edit_column_screen is None:
            return

        if e.widget.winfo_toplevel() != e.widget:
            return

        if self.edit_column_screen.canceled:
            self.edit_column_screen = None
            return

        # TODO: Save config
        print(json.dumps(self.edit_column_screen.column_config, indent=2))

        self.edit_column_screen = None

    def save(self):
        self.config["tags"] = self.compiled_elements["tags"].get().split()

        self.canceled = False
        self.root.destroy()

    def cancel(self):
        self.root.destroy()

    def create_cell(self, root, data: dict, i: int, j: int):
        # TODO: Add color evaluation
        element: dict = {
            "type": 'Button',
            "args": {
                "text": str(data["data"]["default"]) if j == 1 else data["name"],
                "background": 'gray' if j == 0 else 'white',  # ! ! !
                "command": lambda x=i, y=j: self.edit_text(x, y)
            }
        }

        if j != 0:
            # TODO: Refactor this nonsense
            match data["type"]:
                case "scale":
                    # TODO: Fix wierd display of scale
                    element["type"] = 'Scale'
                    element["args"] = {
                        "background": 'gray' if j == 0 else 'white',  # ! ! !
                        "orient": 'horizontal',
                        "command": lambda _, x=i: self.update_config()
                    }
                case "bool":
                    element["type"] = 'Checkbutton'
                    element["args"] = {
                        "background": 'gray' if j == 0 else 'white',  # ! ! !
                        "command": lambda x=i: self.update_config()
                    }
                case _:
                    element["type"] = 'Button'

        cell: Widget = Screen.compile_element(
            root,
            element
        )
        cell.bind('<ButtonRelease-3>', lambda _, x=i, y=j: self.edit_column(x))

        return cell
