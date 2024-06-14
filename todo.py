import click
from classes import *

@click.group()
def cli():
    pass

# users
@cli.command()
@click.argument('username')
def add_user(username):
    """add a new user"""
    user = create_user(username)
    click.echo(f'user "{user.username}" created with id {user.id}')

@cli.command()
@click.argument('user_id', type=int)
def remove_user(user_id):
    """remove a user by id"""
    if delete_user(user_id):
        click.echo(f'user with id {user_id} deleted')
    else:
        click.echo(f'user with id {user_id} not found')

@cli.command()
def list_users():
    """list all users"""
    users = get_all_users()
    if users:
        for user in users:
            click.echo(f'id: {user.id}, username: {user.username}')
    else:
        click.echo('no users found')

@cli.command()
@click.argument('user_id', type=int)
def view_user(user_id):
    """view a user by id"""
    user = find_user_by_id(user_id)
    if user:
        click.echo(f'id: {user.id}, username: {user.username}')
    else:
        click.echo(f'user with id {user_id} not found')
        

# tasks
@cli.command()
@click.argument('description')
@click.argument('tasklist_name')
@click.argument('user_id', type=int)
def add_task(description, user_id, tasklist_name):
    """add a new task to a task list"""
    task = create_task(description, user_id, tasklist_name)
    if task:
        click.echo(f'task "{task.description}" created with id {task.id} in task list "{tasklist_name}" for user {user_id}')
    else:
        click.echo(f'failed to create task in task list "{tasklist_name}" for user {user_id}')

@cli.command()
@click.argument('task_id', type=int)
def remove_task(task_id):
    """remove a task by id"""
    if delete_task(task_id):
        click.echo(f'task with id {task_id} deleted')
    else:
        click.echo(f'task with id {task_id} not found')

@cli.command()
@click.argument('task_id', type=int)
def view_task(task_id):
    """view a task by id"""
    task = find_task_by_id(task_id)
    if task:
        click.echo(f'id: {task.id}, description: {task.description}, completed: {task.completed}, important: {task.important}')
    else:
        click.echo(f'task with id {task_id} not found')

@cli.command()
@click.argument('task_id', type=int)
def complete_task(task_id):
    """mark a task as completed by id"""
    task = mark_task_as_completed(task_id)
    if task:
        click.echo(f'task with id {task.id} marked as completed')
    else:
        click.echo(f'task with id {task_id} not found')

@cli.command()
@click.argument('task_id', type=int)
def important_task(task_id):
    """mark a task as important by id"""
    task = mark_task_as_important(task_id)
    if task:
        click.echo(f'task with id {task.id} marked as important')
    else:
        click.echo(f'task with id {task_id} not found')

# tasklist
@cli.command()
@click.argument('name')
@click.argument('user_id', type=int)
def add_list(name, user_id):
    """add a new task list to a user"""
    tasklist = create_tasklist(name, user_id)
    if tasklist:
        click.echo(f'task list "{tasklist.name}" created for user {user_id}')
    else:
        click.echo(f'failed to create task list "{name}" for user {user_id}')

@cli.command()
@click.argument('name')
@click.argument('user_id', type=int)
def remove_list(name, user_id):
    """remove a task list by name and user id"""
    user = find_user_by_id(user_id)
    if user and name in user.tasklists:
        user.tasklists.remove(name)
        db.tasks = [task for task in db.tasks if task['tasklist_name'] != name or task['user_id'] != user_id]
        db.save()
        click.echo(f'task list "{name}" removed for user {user_id}')
    else:
        click.echo(f'task list "{name}" not found for user {user_id}')

@cli.command()
@click.argument('user_id', type=int)
def list_lists(user_id):
    """list all task lists for a user"""
    tasklists = get_all_tasklists(user_id)
    if tasklists:
        for tasklist in tasklists:
            click.echo(f'task list: {tasklist}')
    else:
        click.echo(f'no task lists found for user id {user_id}')

@cli.command()
@click.argument('user_id', type=int)
@click.argument('tasklist_name')
def list_tasks(user_id, tasklist_name):
    """list all tasks in a task list for a user"""
    tasks = get_tasks_by_tasklist(user_id, tasklist_name)
    if tasks:
        for task in tasks:
            click.echo(f'id: {task.id}, description: {task.description}, completed: {task.completed}, important: {task.important}')
    else:
        click.echo(f'no tasks found for task list "{tasklist_name}" and user id {user_id}')

if __name__ == '__main__':
    cli()
