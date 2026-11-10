from .models import Subscription, Model, Form
from .view import CommandInterface, ModelInterface, View
from rich.prompt import Prompt, FloatPrompt
from rich.live import Live
from pathlib import Path
import click

class Controller:
    def __init__(self, data_folder:Path):
        self.model = Model(data_folder)
        self.view = View()

        self.commands = {
            "Add Subscription": self.add_subscription,
            "Remove Subscription": None,
            "Edit Subscription": None,
            "Exit": self.exit
        }

    def add_subscription(self):
        form = Form()
        form.add_field("subscription_name", Prompt.ask, "Subscription Name")
        form.add_field("expense_duration", Prompt.ask, "Duration Of Expense", ["Daily", "Monthly", "Yearly"])
        form.add_field("expense", FloatPrompt.ask, "Expense Amount")

        self.view.fill_form(form)

        inputs = form.get_answers()

        name:str = inputs["subscription_name"]
        expense_duration:str = inputs["expense_duration"].lower()
        expense:float = inputs["expense"]

        if expense_duration == "daily":
            expense = (expense * 365) / 12
        elif expense_duration == "yearly":
            expense /= 12

        self.model.add_subscription(name, expense)

    def exit(self):
        raise SystemExit()

    def run(self):
        while True:
            current_view = self.view.main(self.model, list(self.commands.keys()))

            if self.commands[current_view]:
                self.commands[current_view]()
