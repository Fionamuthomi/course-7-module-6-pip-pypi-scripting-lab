# Automation Tool Lab

Simple Python scripts for the pip/PyPI/scripting lab.

## What's included

task_manager.py - a command line task manager. You can add tasks, mark them
complete, and list them. Tasks are saved to tasks.json. Built with the rich
package for colored terminal output.

generate_log.py - writes a small activity log to a text file.

fetch_data.py - uses the requests package to fetch data from a public API
and saves the results to a CSV file.

## Setup

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## How to run

python task_manager.py add-task "Buy groceries"
python task_manager.py list-tasks
python task_manager.py complete-task 1

python generate_log.py

python fetch_data.py