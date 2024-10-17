import json
import os
from typing import List, Optional

import questionary
from rich.console import Console
from rich.traceback import install

# Install rich traceback handler for better error display
install()
console = Console()


def load_tasks() -> List[dict]:
    """Load tasks from tasks.json file."""
    tasks_file = os.path.join(os.path.dirname(__file__), "..", "tasks", "tasks.json")
    with open(tasks_file, "r") as f:
        tasks_data = json.load(f)
    return tasks_data.get("tasks", [])


def display_tasks(tasks: List[dict]) -> Optional[dict]:
    """Display tasks and let user select one."""
    choices = [f"{task['label']} ({task['command']} {' '.join(task['args'])})" for task in tasks]
    selected = questionary.select(
        "Select a task to execute",
        qmark="🔧 ",
        choices=choices,
    ).ask()

    if selected:
        return tasks[choices.index(selected)]
    return None


def execute_task(task: dict) -> None:
    """Execute the selected task."""
    command = f"{task['command']} {' '.join(task['args'])}"
    console.print(f"[bold green]Executing task: {task['label']}[/bold green]")
    console.print(f"[cyan]Command: {command}[/cyan]")

    # Here you would typically use subprocess to run the command
    # For demonstration, we'll just print the command
    console.print("[yellow]Task execution simulated. In a real scenario, this would run the command.[/yellow]")
