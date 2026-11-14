from .exceptions import *
from functools import partial
from typing import Literal
from rich.prompt import Prompt, FloatPrompt, PromptBase

class Field:
    def __init__(self, name:str, prompt:str, field_type:Literal["str", "float"], choices:list=[]):
        self.prompt_types:dict[str, type[Prompt]|type[FloatPrompt]] = {"str": Prompt, "float": FloatPrompt}

        if not self.field_type in self.prompt_types.keys():
            raise TypeError

        self.name = name
        self.field_type = field_type
        self.prompt = prompt
        self.choices = choices
        self.answer = None
        
    def __bool__(self):
        return bool(self.answer)

    def ask(self):
        prompt = self.prompt_types[self.field_type]

        if self.choices:
            self.answer = prompt.ask(self.prompt, choices=self.choices)
            return
        self.answer = prompt.ask(self.prompt)

    def reset(self):
        self.answer = None

    def get_answer(self) -> dict:
        return {self.name:self.answer}

class Form:
    def __init__(self):
        self.fields:dict[str, Field] = {}
        self.completed = False
        self.answered = 0

    def add_field(self, name:str, prompt:str, field_type:Literal["str", "float"], choices:list=[]):
        if name in self.fields:
            raise FieldExists(f"Field {name} already exists in form")

        self.fields.update({name: Field(name, prompt, field_type, choices)})

    def ask(self, name:str):
        field = self.fields[name]

        if field:
            raise AnswerExists

        field.ask()

        self.answered += 1
        if self.answered == len(self.fields):
            self.completed = True
        
    def retrieve(self) -> dict:
        if not self.completed:
            raise NotCompleted

        result = {}
        for name in self.fields:
            result.update(self.fields[name].get_answer())

        return result

    def reset(self):
        for field in self.fields.values():
            field.reset()
            self.completed = False
            self.answered = 0

    def __iter__(self):
        return iter(self.fields.keys())