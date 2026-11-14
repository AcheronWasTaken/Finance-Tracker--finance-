from .models import Model
from .forms import Form
from .view import View
from rich.prompt import Prompt, FloatPrompt, Confirm
from pathlib import Path
from .exceptions import *

class Controller:
    def __init__(self, data_folder:Path):
        self.model = Model(data_folder)
        self.view = View()

        self.commands = {
            "Add Subscription": self.add_subscription,
            "Remove Subscription": self.remove_subscription,
            "Edit Subscription": self.edit_subscription,
            "Exit": self.exit
        }

    def add_subscription(self):
        pass

    def remove_subscription(self):
        pass

    def edit_subscription(self):
        pass

    def exit(self):
        raise SystemExit()

    def run(self):
        while True:
            current_view = self.view.main(self.model, list(self.commands.keys()))

            if self.commands[current_view]:
                self.commands[current_view]()
