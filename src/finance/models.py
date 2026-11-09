import json
from pathlib import Path
from typing import cast
import click

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
        Path(data_file_path).mkdir(exist_ok=True, parents=True)
        with open(data_file_path, "r") as file:
            self.raw:list[dict[str, float|str]] = json.load(file)

        self.empty = bool(self.raw)
        self.data:dict[str, Subscription] = {}

        for entry in self.raw:
            name = entry.get("name")
            monthly_expense = entry.get("monthly_expense")

            if not name or not monthly_expense:
                raise click.ClickException(f"Missing key data fields: Data is malformed. Manual intervention required at {cwd}")

            if not isinstance(name, str) or not isinstance(monthly_expense, float):
                raise click.ClickException(f"Wrong data types found in data: Data is malformed. Manual intervention required at {cwd}")
            
            self.data.update({name: Subscription(name, monthly_expense)})

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __bool__(self):
        return self.empty


        

        