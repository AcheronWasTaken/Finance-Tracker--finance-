from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from .models import Subscription, Model

class Interface[T:(Model, Subscription, None)]:
    def __init__(self, data_model:T):
        self.model = data_model

    def build_layout(self) -> Layout:
        layout = Layout(Panel("Wow...such empty!"))
        self.layout = layout
        return layout

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
            return super().build_layout()

        model_table = self.build_table()

        for subscription_name in self.model:
            subscription = self.model[subscription_name]

            model_table.add_row(
                subscription_name,
                str(subscription.monthly_expense)
            )

        layout = Layout(model_table, size=10)
        self.layout = layout
        return layout

class InputInterface(Interface):
    def __init__(self, commands:list[tuple[str, function]]):
        super().__init__(None)

        self.commands = commands

    def build_table(self) -> Table:
        table = Table()

        table.add_column("Index")
        table.add_column("Command Name")

        return table

    def build_layout(self, cursor:int|None = None) -> Layout:
        command_table = self.build_table()

        for index, command_tuple in enumerate(self.commands):
            name, *_ = command_tuple

            name = Text(name)

            if cursor == index:
                name.stylize("gold")
                
            command_table.add_row(f"{index + 1}.")
            command_table.add_row(name)

        layout = Layout(command_table)
        self.layout = layout
        return layout



    

        
