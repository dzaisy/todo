# cli todo app

this is a cli todo app built using python and click.

## features
- **user management**: create, view, list, and delete users.
- **task management**: create, view, list, complete, and mark tasks as important.
- **task list management**: create, view, list, and delete task lists for users.

## commands

- add-list: add a new task list to a user 
eg. python todo.py add-list NAME USER_ID

- add-task: add a new task to a task list
eg. python todo.py add-task DESCRIPTION TASKLIST_NAME USER_ID

- add-user: add a new user
eg. python todo.py add-user USERNAME

- complete-task: mark a task as completed by id
eg. python todo.py complete-task TASK_ID

- important-task: mark a task as important by id
eg. python todo.py important-task TASK_ID

- list-lists: list all task lists for a user
eg. python todo.py list-lists USER_ID

- list-tasks: list all tasks in a task list for a user
eg. python todo.py list-tasks USER_ID TASKLIST_NAME

- list-users: list all users
eg. python todo.py list-users

- remove-list: remove a task list by name and user id
eg. python todo.py remove-list NAME USER_ID

- remove-task: remove a task by id
eg. python todo.py remove-task TASK_ID

- remove-user: remove a user by id
eg. python todo.py remove-user USER_ID

- view-task: view a task by id
eg. python todo.py view-task TASK_ID

- view-user: view a user by id
eg. python todo.py view-user USER_ID

## storage
the application uses a JSON file (db.json) to store user and task data. the file is automatically created and updated as you use the application.

