import json
from pathlib import Path
import click
from .exceptions import *

cwd = Path(__file__).parent

class Subscription:
    def __init__(self, name:str, monthly_expense:float):
        self.name = name.strip().title()
        self.monthly_expense = round(monthly_expense, 3)
        self.yearly_expense = round(self.monthly_expense * 12, 3)

    def get_raw(self):
        return {"name": self.name, "monthly_expense": self.monthly_expense}

class Model:
    def __init__(self, data_file_path:str|Path):
        self.raw_file_path = data_file_path
        self.raw = self.get_file_data()

        self.empty = bool(self.raw)
        self.data = self.parse_data()

    def add_subscription(self, name:str, monthly_expense:float):
        entry_name = name.lower().strip().replace(" ", "_")

        if name in self.data:
            raise SubscriptionExists

        self.data.update({entry_name: Subscription(name, monthly_expense)})
        self.update_file_data()
        
    def get_file_data(self) -> list[dict]:
        if Path(self.raw_file_path).exists():
            with open(self.raw_file_path, "r") as file:
                return json.load(file)
        return []

    def update_file_data(self):
        buffer = []

        for name in self.data:
            buffer.append(self.data[name].get_raw())

        Path(self.raw_file_path).mkdir(exist_ok=True, parents=True)
        with open(self.raw_file_path, "w") as file:
            json.dump(buffer, file)

    def parse_data(self) -> dict[str, Subscription]:
        data = {}

        for entry in self.raw:
            name = entry.get("name")
            monthly_expense = entry.get("monthly_expense")

            if not name or not monthly_expense:
                raise click.ClickException(f"Missing key data fields: Data is malformed. Manual intervention required at {cwd}")

            if not isinstance(name, str) or not isinstance(monthly_expense, float):
                raise click.ClickException(f"Wrong data types found in data: Data is malformed. Manual intervention required at {cwd}")
            
            data.update({name: Subscription(name, monthly_expense)})

        return data
        

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __bool__(self):
        return self.empty


        

        