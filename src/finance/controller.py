from .models import Model, Form
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
        form = Form()
        form.add_field("subscription_name", Prompt.ask, "Subscription Name")
        form.add_field("expense_duration", Prompt.ask, "Duration Of Expense", ["Daily", "Monthly", "Yearly"])
        form.add_field("expense", FloatPrompt.ask, "Expense Amount")

        self.view.fill_form(form)

        inputs = form.get_answers()

        name:str = inputs["subscription_name"].strip()
        expense_duration:str = inputs["expense_duration"].lower()
        expense:float = inputs["expense"]

        if expense_duration == "daily":
            expense = (expense * 365) / 12
        elif expense_duration == "yearly":
            expense /= 12

        self.model.add_subscription(name, expense)

    def remove_subscription(self):
        form = Form()
        form.add_field("subscription_name", Prompt.ask, "Subscription name")
        form.add_field("confirm", Confirm.ask, "Are you sure?")

        while True:
            self.view.fill_form(form)

            inputs = form.get_answers()
            name = inputs["subscription_name"]

            if not inputs["confirm"]:
                return

            try:
                self.model.remove_subscription(inputs["subscription_name"])
                return
            except SubscriptionNotFound:
                form.invalidate()
                continue

    def edit_subscription(self):
        form = Form()
        form.add_field("old_subscription_name", Prompt.ask, "Name of Subscription To Change")
        form.add_field("new_subscription_name", Prompt.ask, "New Subscription Name ('.' to keep the same)")
        form.add_field("expense_duration", Prompt.ask, "New Duration Of Expense ('.' to keep the same)", ["Daily", "Monthly", "Yearly", '.'])
        form.add_field("expense", FloatPrompt.ask, "New Expense Amount ('-1' to keep the same)")

        while True:
            self.view.fill_form(form)

            inputs = form.get_answers()
            old_name = inputs["old_subscription_name"]
            new_name = inputs["new_subscription_name"]
            duration = inputs["expense_duration"].lower()
            expense = inputs["expense"]

            if duration == "daily":
                expense = (expense * 365) / 12
            elif duration == "yearly":
                expense /= 12

            for key, input in [("name", new_name), ("monthly_expense", expense)]:
                if input == "." or int(input) == -1:
                    continue

                try:
                    self.model.update_subscription(old_name, key, input)
                    return
                except SubscriptionNotFound:
                    print("Name of the subscription to change does not exist!")
                    form.invalidate()
                    continue
                except SubscriptionExists:
                    print("A subscription with the new name already exists!")
                    form.invalidate()
                    continue

    def exit(self):
        raise SystemExit()

    def run(self):
        while True:
            current_view = self.view.main(self.model, list(self.commands.keys()))

            if self.commands[current_view]:
                self.commands[current_view]()
