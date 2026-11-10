from .models import Subscription, Model
from .view import CommandInterface, ModelInterface, View
from rich.live import Live
from pathlib import Path
import click

class Controller:
    def __init__(self, data_file_path:str|Path):
        self.model = Model(data_file_path)
        self.view = View()

        

        self.commands = {
            "Add Subscription": None,
            "Remove Subscription": None,
            "Edit Subscription": None,
            "Exit": self.exit
        }

    def exit(self):
        raise SystemExit()

    def run(self):
        while True:
            current_view = self.view.main(self.model, list(self.commands.keys()))

            if self.commands[current_view]:
                self.commands[current_view]()

            


