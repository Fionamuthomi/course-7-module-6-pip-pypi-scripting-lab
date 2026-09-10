"""
task_manager.py
----------------
A lightweight command-line Task Manager built with OOP + argparse.

Commands:
    python task_manager.py add-task "Buy groceries"
    python task_manager.py complete-task 1
    python task_manager.py list-tasks

Design:
    Task        -> represents a single task (id, description, status, timestamps)
    TaskManager -> owns the collection of tasks, handles load/save (File I/O)
                   and the business logic for adding / completing tasks.
    CLI wiring  -> argparse subparsers map each subcommand to a TaskManager method.

External package used: `rich` -> gives nicely formatted terminal feedback
(colored text, a table for list-tasks) instead of plain print statements.
"""

import argparse
import json
import os
from datetime import datetime

from rich.console import Console
from rich.table import Table

console = Console()

DATA_FILE = "tasks.json"


class Task:
    """Represents a single task."""

    def __init__(self, task_id, description, completed=False, created_at=None, completed_at=None):
        self.id = task_id
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.completed_at = completed_at

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["id"],
            description=data["description"],
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
        )


class TaskManager:
    """Manages the collection of tasks: loading, saving, adding, completing."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.tasks = self._load_tasks()

    # ---------- File I/O ----------
    def _load_tasks(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, "r") as f:
                raw = json.load(f)
            return [Task.from_dict(t) for t in raw]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_tasks(self):
        with open(self.data_file, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    # ---------- Business logic ----------
    def add_task(self, description):
        new_id = (max((t.id for t in self.tasks), default=0)) + 1
        task = Task(new_id, description)
        self.tasks.append(task)
        self._save_tasks()
        console.print(f"[bold green]Added task #{task.id}:[/bold green] {task.description}")
        return task

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    console.print(f"[yellow]Task #{task_id} is already complete.[/yellow]")
                    return task
                task.completed = True
                task.completed_at = datetime.now().isoformat(timespec="seconds")
                self._save_tasks()
                console.print(f"[bold green]Completed task #{task.id}:[/bold green] {task.description}")
                return task
        console.print(f"[bold red]No task found with id {task_id}[/bold red]")
        return None

    def list_tasks(self):
        if not self.tasks:
            console.print("[italic]No tasks yet. Add one with 'add-task'.[/italic]")
            return

        table = Table(title="Tasks")
        table.add_column("ID", justify="right")
        table.add_column("Description")
        table.add_column("Status")
        table.add_column("Created At")

        for t in self.tasks:
            status = "[green]Done[/green]" if t.completed else "[yellow]Pending[/yellow]"
            table.add_row(str(t.id), t.description, status, t.created_at)

        console.print(table)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="task_manager.py",
        description="A simple CLI task manager (add, complete, list tasks).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Description of the task")

    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to mark complete")

    subparsers.add_parser("list-tasks", help="List all tasks")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    manager = TaskManager()

    if args.command == "add-task":
        manager.add_task(args.description)
    elif args.command == "complete-task":
        manager.complete_task(args.task_id)
    elif args.command == "list-tasks":
        manager.list_tasks()


if __name__ == "__main__":
    main()