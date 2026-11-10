from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from .models import Model, Form
from keyboard import read_event
from rich.prompt import Prompt

class ModelInterface:
    def __init__(self, data_model:Model):
        self.model = data_model
        self.layout = self.build_layout()

    def build_table(self) -> Table:
        table = Table()

        table.add_column("Subscription Name")
        table.add_column("Subscription Expense")

        return table

    def build_layout(self) -> Layout:
        print(self.model.data)

        if not self.model:
            return Layout(Panel("Wow...such empty!"))

        model_table = self.build_table()

        for subscription_name in self.model:
            subscription = self.model[subscription_name]

            model_table.add_row(
                subscription.name,
                str(subscription.monthly_expense)
            )

        return Layout(model_table, name="model", size=10)

    def view(self, update:bool=False):
        if update:
            self.layout = self.build_layout()
        return self.layout
        
class CommandInterface:
    def __init__(self, commands:list[str]):
        self.commands = commands

    def build_table(self) -> Table:
        table = Table.grid()

        table.add_column()
        table.add_column()

        return table

    def build_layout(self, cursor:int) -> Layout:
        command_table = self.build_table()
        space = " "*2

        for index, name in enumerate(self.commands):
            name = Text(name)

            if cursor == index:
                name.stylize("yellow")
                
            command_table.add_row(f"{index + 1}.{space}", name)
        
        return Layout(command_table, name="command")

    def view(self, cursor:int) -> Layout:
        self.layout = self.build_layout(cursor)
        return self.layout

class View:
    def __init__(self):
        pass

    @staticmethod
    def shift_cursor_down(cursor:int, upper_bound:int):
        if cursor == upper_bound:
            return 0

        return cursor + 1

    @staticmethod
    def shift_cursor_up(cursor:int, upper_bound:int):
        if cursor == 0:
            return upper_bound

        return cursor - 1

    def main(self, model:Model, commands:list[str]) -> str:
        model_interface = ModelInterface(model)
        command_interface = CommandInterface(commands)

        cursor = 0
        layout = Layout()
        layout.split_column(
            model_interface.view(),
            command_interface.view(cursor)
        )

        with Live(layout, auto_refresh=False) as live:
            while True:
                event = read_event(suppress=True)
                if event.event_type != "down":
                    continue
                key = event.name
                
                if key == "w":
                    cursor = self.shift_cursor_up(cursor, len(commands) - 1)
                elif key == "s":
                    cursor = self.shift_cursor_down(cursor, len(commands) - 1)
                elif key == "enter" or key == "space":
                    live.update("", refresh=True)
                    return commands[cursor]

                layout["command"].update(command_interface.view(cursor))
                live.update(layout, refresh=True)

    def fill_form(self, form:Form):
        with Live(auto_refresh=False) as live:
            for name in form:
                form.answer(name, form.ask(name)())
                live.refresh()