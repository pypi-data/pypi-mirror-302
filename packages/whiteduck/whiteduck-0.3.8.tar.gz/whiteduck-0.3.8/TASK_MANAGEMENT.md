# Task Management Feature

The whiteduck project now includes a feature for managing VS Code tasks. This document provides instructions on how to use this new functionality.

## Accessing Task Management

When you run the whiteduck application without any parameters, you will be prompted to choose between "task" and "template" modes. To access the task management features, select "task" when prompted.

Alternatively, you can directly access task management features using the following command structure:

```
python -m whiteduck tasks [command]
```

## Commands

The task management feature is accessible through the following commands:

### Create a Task

To create a new VS Code task:

```
python -m whiteduck tasks create <label> <command> [--type <type>]
```

- `<label>`: A descriptive name for the task.
- `<command>`: The command to be executed by the task.
- `--type`: (Optional) The type of task. Defaults to "shell".

Example:

```
python -m whiteduck tasks create "Run Tests" "python -m pytest"
```

### List Tasks

To list all available VS Code tasks:

```
python -m whiteduck tasks list
```

This command will display all tasks currently defined in your `.vscode/tasks.json` file.

### Delete a Task

To delete a VS Code task:

```
python -m whiteduck tasks delete <label>
```

- `<label>`: The label of the task you want to delete.

Example:

```
python -m whiteduck tasks delete "Run Tests"
```

## Notes

- These commands will modify the `.vscode/tasks.json` file in your project directory.
- Make sure you have the necessary permissions to read and write to this file.
- After creating or deleting tasks, you may need to reload your VS Code window to see the changes reflected in the Tasks Explorer.

## Troubleshooting

If you encounter any issues while using these commands, please check the following:

1. Ensure you're running the commands from your project's root directory.
2. Verify that you have write permissions for the `.vscode` directory and its contents.
3. If tasks are not appearing in VS Code after creation, try reloading the VS Code window.

For any further issues or feature requests related to task management, please open an issue in the project repository.
