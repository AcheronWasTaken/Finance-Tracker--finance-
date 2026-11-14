import json
from pathlib import Path
from typing import Any
import click
from .exceptions import *
from functools import partial

cwd = Path(__file__).parent
        
class Subscription:
    def __init__(self, name:str, monthly_expense:float):
        self.name = name
        self.monthly_expense = round(monthly_expense, 3)
        self.yearly_expense = round(self.monthly_expense * 12, 3)

    def get_raw(self):
        return {"name": self.name, "monthly_expense": self.monthly_expense}

    def set(self, key:str, value:str|float):
        self.__dict__[key] = value

    def __bool__(self):
        return True

class Model:
    def __init__(self, data_folder:Path):
        self.data_folder = data_folder
        self.raw = self.get_file_data()

        self.empty = not bool(self.raw)
        self.data = self.parse_data()

    def add_subscription(self, name:str, monthly_expense:float):
        if name in self.data:
            raise SubscriptionExists

        self.data.update({name: Subscription(name, monthly_expense)})
        self.update_file_data()

        self.empty = False

    def remove_subscription(self, name:str):
        if not name in self.data:
            raise SubscriptionNotFound

        del self.data[name]
        self.update_file_data()

        if not self.data:
            self.empty = True
        return

    def update_subscription(self, name:str, key:str, value:str|float):
        if not name in self.data:
            raise SubscriptionNotFound

        if key == "name" and value in self.data:
            raise SubscriptionExists

        subscription = self.data[name]

        subscription.set(key, value)
        if key == "name" and isinstance(value, str):
            self.data[name] = self.data.pop(value)

    def get_file_data(self) -> list[dict]:
        if Path(self.data_folder / "subscriptions.json").exists():
            with open(self.data_folder / "subscriptions.json", "r") as file:
                return json.load(file)
        return []

    def update_file_data(self):
        buffer = []

        for name in self.data:
            buffer.append(self.data[name].get_raw())

        Path(self.data_folder).mkdir(exist_ok=True)
        with open(self.data_folder / "subscriptions.json", "w") as file:
            json.dump(buffer, file, indent=4)

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
        return not self.empty        