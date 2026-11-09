from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from .models import Subscription, Model

class Interface[T:(Model, Subscription, None)]:
    def __init__(self, data_model:T):
        self.model = data_model

class ModelInterface(Interface[Model]):
    def __init__(self, data_model:Model):
        super().__init__(data_model)

    def build_table(self) -> Table:
        table = Table()

        table.add_column("Name")
        table.add_column("Expense")

        return table

    def build_layout(self) -> Layout:
        if not self.model:
            return Layout(Panel("Wow...such empty!"))

        model_table = self.build_table()

        for subscription_name in self.model:
            subscription = self.model[subscription_name]

            model_table.add_row(
                subscription_name,
                str(subscription.monthly_expense)
            )

        return Layout(model_table, size=10)

    def view(self, update:bool=False):
        if update:
            self.layout = self.build_layout()
        
class InputInterface(Interface):
    def __init__(self, commands:list[tuple[str, function]]):
        super().__init__(None)

        self.commands = commands

    def build_table(self) -> Table:
        table = Table()

        table.add_column("Index")
        table.add_column("Command Name")

        return table

    def build_layout(self, cursor:int) -> Layout:
        command_table = self.build_table()

        for index, command_tuple in enumerate(self.commands):
            name, *_ = command_tuple

            name = Text(name)

            if cursor == index:
                name.stylize("gold")
                
            command_table.add_row(f"{index + 1}.")
            command_table.add_row(name)
        
        return Layout(command_table)

    def view(self, cursor:int) -> Layout:
        self.layout = self.build_layout(cursor)
        return self.layout

    




    

        
