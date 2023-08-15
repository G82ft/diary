import json
from abc import ABC, abstractmethod
from tkinter import (
    Tk,
    Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame, Listbox, Menu, Menubutton, Message, OptionMenu,
    PanedWindow, Radiobutton, Scale, Scrollbar, Spinbox, Text, Toplevel,
    Variable,
    Event
)
from tkinter.font import nametofont

TYPES: dict[str: type] = {
    "Tk": Tk,
    "Button": Button,
    "Canvas": Canvas,
    "Checkbutton": Checkbutton,
    "Entry": Entry,
    "Frame": Frame,
    "Label": Label,
    "LabelFrame": LabelFrame,
    "Listbox": Listbox,
    "Menu": Menu,
    "Menubutton": Menubutton,
    "Message": Message,
    "OptionMenu": OptionMenu,
    "PanedWindow": PanedWindow,
    "Radiobutton": Radiobutton,
    "Scale": Scale,
    "Scrollbar": Scrollbar,
    "Spinbox": Spinbox,
    "Text": Text,
    "Toplevel": Toplevel
}

ROOT = Tk()
ROOT.withdraw()


def load(path: str) -> dict:
    with open(path) as file:
        data: dict = json.load(file)

    for name, e in data["elements"].items():
        data["elements"][name]["type"] = TYPES[data["elements"][name]["type"]]

    return data


class Screen(ABC):
    id: str = ''
    root: Toplevel = None
    master = None
    frame: Frame = None

    args: dict[str: tuple[any] | dict[str: any]] = {}
    elements: dict[
        dict[str: type | list[any] | dict[str: any]]
    ] = {}
    compiled_elements: dict = {}
    variables: dict[str: Variable] = {}
    grid_config: dict[str: list[int]] = {
        "rows": (),
        "cols": ()
    }

    def __init__(self, master: Toplevel = None):
        self.master = master
        self.root = Toplevel(master=master)

        with open(f"screens/{self.id}/data.json") as file:
            data: dict = json.load(file)

        root_config: dict[str: str | list[int, int]] = {
            "title": "tk",
            "min_size": [1, 1],
            "max_size": [1024, 720]
        }
        root_config |= data["root_config"]

        self.preconfigure_root(root_config)
        self.configure_root(root_config)

        self.args |= data["args"]
        self.elements = data["elements"]
        self.grid_config |= data["grid_config"]

    def configure_root(self, root_config: dict):
        self.root.title(root_config["title"])
        self.root.maxsize(*root_config["max_size"])
        self.root.minsize(*root_config["min_size"])
        if "start_size" in root_config:
            self.root.geometry("{}x{}".format(*root_config["start_size"]))

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.withdraw()
        self.root.bind('<Destroy>', self.destroy)

    def compile(self) -> Frame:
        """Compiles frame from class.

        ***Note: It changes master's sizes!***

        :returns: Compiled Frame."""
        self.preconfigure_elements()

        self.frame = self._compile_frame(self.root,
                                         self.args, self.grid_config,
                                         self.elements, self.compiled_elements, self.configure_element)

        self.frame.bind('<Map>', self.on_load)

        self.frame.grid(row=0, column=0, sticky='nesw')

        return self.frame

    def show(self):
        if self.frame is None:
            self.compile()

        self.root.deiconify()
        self.root.lift()

    def minimize(self):
        self.root.iconify()

    def hide(self):
        self.root.withdraw()

    def destroy(self, e: Event):
        if e.widget != e.widget.winfo_toplevel():
            return

        self.root.destroy()

        if self.master is None:
            ROOT.destroy()

    def mainloop(self):
        if self.master is None:
            self.root.mainloop()

    @abstractmethod
    def preconfigure_root(self, root_config: dict) -> None:
        """Prepares config for use in configure_root().

        Changes initial root_config dict."""
        pass

    @abstractmethod
    def preconfigure_elements(self):
        pass

    @abstractmethod
    def configure_element(self, name: str, element_type: type, element):
        pass

    @abstractmethod
    def on_load(self, e: Event):
        pass

    @staticmethod
    def _compile_frame(root,
                       args, grid: dict[str: list[int, int]],
                       elements: dict, compiled_elements: dict, configure_element):
        frame: Frame = Frame(
            root,
            **args
        )

        for row, w in enumerate(grid.get("rows", ())):
            frame.rowconfigure(row, weight=w)
        for col, w in enumerate(grid.get("cols", ())):
            frame.columnconfigure(col, weight=w)

        for name, e in elements.items():
            e: dict
            e.setdefault("args", {})
            args: dict = e["args"]

            match e["type"]:
                case 'Frame':
                    element = Screen._compile_frame(
                        frame,
                        e["args"], e.get("grid_config", {}),
                        e.get("elements", {}), compiled_elements, configure_element
                    )
                case 'OptionMenu':
                    element = TYPES[e["type"]](frame, *args.pop("values"), **args)
                case 'Entry':
                    args["font"] = nametofont('TkDefaultFont')
                    element = TYPES[e["type"]](frame, **args)
                case _:
                    element = TYPES[e["type"]](frame, **args)

            element.grid(**e["grid"])
            configure_element(name, e["type"], element)
            compiled_elements[name] = element

        return frame
