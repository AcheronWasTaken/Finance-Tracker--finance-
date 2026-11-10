import json
from pathlib import Path
import click
from .exceptions import *
from functools import partial

cwd = Path(__file__).parent

class Field:
    def __init__(self, name:str, func, prompt:str, choices:list=[]):
        self.name = name
        self.prompt_function = func
        self.prompt = prompt
        self.choices = choices
        self.answer = None

    def __bool__(self):
        return bool(self.answer)

    def get(self) -> partial:
        if self.choices:
            return partial(
                self.prompt_function,
                self.prompt,
                choices=self.choices,
                case_sensitive=False
            )
        return partial(
            self.prompt_function,
            self.prompt
        )

    def put(self, answer):
        self.answer = answer

    def get_answer(self) -> dict:
        return {self.name:self.answer}

class Form:
    def __init__(self):
        self.fields:dict[str, Field] = {}
        self.completed = False
        self.answered = 0

    def add_field(self, name:str, func, prompt:str, choices:list=[]):
        if name in self.fields:
            raise FieldExists(f"Field {name} already exists in form")

        self.fields.update({name: Field(name, func, prompt, choices)})

    def ask(self, name:str) -> partial:
        field = self.fields[name]

        return field.get()

    def answer(self, name:str, answer):
        field = self.fields[name]

        if field:
            raise AnswerExists(f"Answer already exists for field {name}")

        field.put(answer)

        self.answered += 1
        if self.answered == len(self.fields):
            self.completed = True

    def get_answers(self) -> dict:
        if not self.completed:
            raise NotCompleted("Form is not completed")

        result = {}
        for name in self.fields:
            result.update(self.fields[name].get_answer())

        return result

    def __iter__(self):
        return iter(self.fields.keys())
        
class Subscription:
    def __init__(self, name:str, monthly_expense:float):
        self.name = name.strip().title()
        self.monthly_expense = round(monthly_expense, 3)
        self.yearly_expense = round(self.monthly_expense * 12, 3)

    def get_raw(self):
        return {"name": self.name, "monthly_expense": self.monthly_expense}

class Model:
    def __init__(self, data_folder:Path):
        self.data_folder = data_folder
        self.raw = self.get_file_data()

        self.empty = not bool(self.raw)
        self.data = self.parse_data()

    def add_subscription(self, name:str, monthly_expense:float):
        entry_name = name.lower().strip().replace(" ", "_")

        if entry_name in self.data:
            raise SubscriptionExists(f"{name} subscription already exists. Please pick a different name")

        self.data.update({entry_name: Subscription(name, monthly_expense)})
        self.update_file_data()

        self.empty = False

    def remove_subscription(self, name:str):
        entry_name = name.lower().strip().replace(" ", "_")

        if entry_name in self.data:
            del self.data[entry_name]
            self.update_file_data()
            return

        raise SubscriptionNotFound(f"{name} subscription does not exist. Ensure the name is typed correctly.")

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
        return not self.empty        