"""
This module provides functionality for managing VS Code tasks within the whiteduck project.
"""

import json
import os
from typing import List, TypedDict


class Task(TypedDict):
    label: str
    type: str
    command: str


class TasksFile(TypedDict):
    version: str
    tasks: List[Task]


class TaskManager:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.tasks_file = os.path.join(project_root, ".vscode", "tasks.json")

    def create_task(self, label: str, command: str, type: str = "shell") -> None:
        """
        Create a new VS Code task.

        Args:
            label (str): The label for the task.
            command (str): The command to be executed.
            type (str, optional): The type of task. Defaults to "shell".
        """
        task: Task = {
            "label": label,
            "type": type,
            "command": command,
        }

        tasks = self.get_tasks()
        tasks["tasks"].append(task)
        self._save_tasks(tasks)

    def get_tasks(self) -> TasksFile:
        """
        Retrieve all tasks from the tasks.json file.

        Returns:
            TasksFile: A dictionary containing the version and list of tasks.
        """
        if not os.path.exists(self.tasks_file):
            return {"version": "2.0.0", "tasks": []}

        with open(self.tasks_file, "r") as f:
            return json.load(f)

    def list_tasks(self) -> List[str]:
        """
        List all task labels.

        Returns:
            List[str]: A list of all task labels.
        """
        tasks = self.get_tasks()
        return [task["label"] for task in tasks["tasks"]]

    def delete_task(self, label: str) -> bool:
        """
        Delete a task by its label.

        Args:
            label (str): The label of the task to delete.

        Returns:
            bool: True if the task was deleted, False otherwise.
        """
        tasks = self.get_tasks()
        initial_count = len(tasks["tasks"])
        tasks["tasks"] = [task for task in tasks["tasks"] if task["label"] != label]

        if len(tasks["tasks"]) < initial_count:
            self._save_tasks(tasks)
            return True
        return False

    def _save_tasks(self, tasks: TasksFile) -> None:
        """
        Save tasks to the tasks.json file.

        Args:
            tasks (TasksFile): The tasks to save.
        """
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
        with open(self.tasks_file, "w") as f:
            json.dump(tasks, f, indent=2)


# Example usage
if __name__ == "__main__":
    task_manager = TaskManager(".")
    task_manager.create_task("Run Tests", "python -m pytest")
    print(task_manager.list_tasks())
