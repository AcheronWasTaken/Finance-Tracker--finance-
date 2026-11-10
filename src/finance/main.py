import click
from .controller import Controller
from pathlib import Path

cwd = Path(__file__).parent

@click.command()
def cli():
    controller = Controller(cwd / "data/subscriptions.json")

    controller.run()

if __name__ == "__main__":
    cli()