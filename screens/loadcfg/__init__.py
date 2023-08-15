import json
import os
from tkinter import (
    Toplevel,
    Event,
    messagebox as msgbox
)
from tkinter.font import Font, nametofont

from utils.config import CONFIGS_PATH, get_configs, is_config
from ..editcfg import EditConfigScreen
from ..screen import Screen


class LoadConfigScreen(Screen):
    default_label: str = "Please, select diary configuration:"
    edit_config_screen: EditConfigScreen | None = None

    def __init__(self, master: Toplevel = None):
        self.id = 'loadcfg'
        super().__init__(master)
        default_font: Font = nametofont('TkDefaultFont')
        default_font.config(
            family='Consolas',
            size=default_font["size"]
        )

    def preconfigure_root(self, root_config: dict) -> None:
        pass

    def preconfigure_elements(self):
        frame_elements: dict = self.elements["config_buttons"]["elements"]
        frame_elements["add_button"]["args"]["command"] = self.add_config
        frame_elements["delete_button"]["args"]["command"] = self.delete_config
        self.elements["open_button"]["args"]["command"] = self.open_config

    def configure_element(self, name: str, element_type: type, element):
        pass

    def on_load(self, e: Event):
        for i, total, name in get_configs():
            if name:
                self.compiled_elements["config_listbox"].insert('end', name)

            bars: int = round(i / total * 11)
            self.compiled_elements["info_label"]["text"] = (
                f"Searching for configs [{'*' * bars}{' ' * (11 - bars)}]"
            )
            self.root.update()
            self.root.update_idletasks()

        self.compiled_elements["info_label"]["text"] = self.default_label

    def add_config(self):
        if self.edit_config_screen is not None:
            msgbox.showwarning(
                'Config editing',
                'You\'ve already opened another config for editing.',
                parent=self.edit_config_screen.root
            )
            self.edit_config_screen.show()
            return

        self.edit_config_screen = EditConfigScreen(self.root)
        self.edit_config_screen.root.bind('<Destroy>', self.end_editing)

        self.root.update()
        self.root.update_idletasks()

        self.edit_config_screen.show()

    def end_editing(self, e: Event):
        if self.edit_config_screen is None:
            return

        if e.widget.winfo_toplevel() != e.widget:
            return

        if self.edit_config_screen.canceled:
            self.edit_config_screen = None
            return

        # TODO: Save config
        print(json.dumps(self.edit_config_screen.config, indent=2))

        self.edit_config_screen = None

    def delete_config(self) -> None:
        title = 'Config Deletion'
        to_delete = self.compiled_elements["config_listbox"].get('active')
        path: str = CONFIGS_PATH + to_delete

        if not msgbox.askokcancel(
                title,
                f'Are you sure you want to delete config "{to_delete}"?\n'
                'It will be lost forever (very long time).',
                default='cancel', icon='warning'
        ):
            return None

        if not is_config(path):
            if not msgbox.askokcancel(
                    title,
                    f'Somehow, the file you are trying to delete ("{to_delete}") is not a config file.\n'
                    'Proceed with deletion?',
                    default='cancel', icon='warning'
            ):
                return None

        if not os.access(path, os.W_OK):
            msgbox.showerror(
                title,
                f'Permission to delete {path} denied.'
            )
            return None

        self.compiled_elements["info_label"]["text"] = f'Removing {to_delete}...'
        self.root.update()
        self.root.update_idletasks()

        os.remove(path)

        self.compiled_elements["config_listbox"].delete('active')
        self.compiled_elements["info_label"]["text"] = self.default_label

        msgbox.showinfo(
            title,
            'Config successfully deleted.'
        )

    def open_config(self):
        pass
