import json
import os

DB_FILE = 'db.json'

class InMemoryDB: # storage
    def __init__(self):
        self.load() # loads data from json

    def load(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as file:
                data = json.load(file)
                self.users = data.get('users', [])
                self.tasks = data.get('tasks', [])
                self.user_id_counter = data.get('user_id_counter', 1)
                self.task_id_counter = data.get('task_id_counter', 1)
        else:
            self.users = []
            self.tasks = []
            self.user_id_counter = 1
            self.task_id_counter = 1

    def save(self):
        data = {
            'users': self.users,
            'tasks': self.tasks,
            'user_id_counter': self.user_id_counter,
            'task_id_counter': self.task_id_counter
        }
        with open(DB_FILE, 'w') as file:
            json.dump(data, file, indent=3 )

db = InMemoryDB()

class User:
    def __init__(self, username):
        self.id = db.user_id_counter
        db.user_id_counter += 1
        self.username = username
        self.tasklists = []

    def to_dict(self): # convert to dict from obj
        return {
            'id': self.id,
            'username': self.username,
            'tasklists': self.tasklists
        }

    @staticmethod
    def from_dict(data): # create obj from dict 
        user = User(data['username'])
        user.id = data['id']
        user.tasklists = data['tasklists']
        return user

class Task:
    def __init__(self, description, tasklist_name):
        self.id = db.task_id_counter
        db.task_id_counter += 1
        self.description = description
        self.tasklist_name = tasklist_name
        self.completed = False
        self.important = False

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'tasklist_name': self.tasklist_name,
            'completed': self.completed,
            'important': self.important
        }

    @staticmethod
    def from_dict(data):
        task = Task(data['description'], data['tasklist_name'])
        task.id = data['id']
        task.completed = data['completed']
        task.important = data['important']
        return task

class Tasklist:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def get_tasks(self):
        return [Task.from_dict(task) for task in db.tasks if task['tasklist_name'] == self.name and task['user_id'] == self.user_id]

# saving helpers
def save_users():
    db.users = [user.to_dict() for user in db.users]
    db.save()

def save_tasks():
    db.tasks = [task.to_dict() for task in db.tasks]
    db.save()

# users
def create_user(username):
    user = User(username)
    db.users.append(user.to_dict())
    db.save()
    return user

def delete_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        db.users = [u for u in db.users if u['id'] != user_id]
        db.tasks = [task for task in db.tasks if task['user_id'] != user_id]
        db.save()
        return True
    return False

def get_all_users():
    return [User.from_dict(user) for user in db.users]

def find_user_by_id(user_id):
    for user in db.users:
        if user['id'] == user_id:
            return User.from_dict(user)
    return None

# tasks
def create_task(description, user_id, tasklist_name):
    user = find_user_by_id(user_id)
    if user and tasklist_name in user.tasklists:
        task = Task(description, tasklist_name)
        db.tasks.append(task.to_dict())
        db.save()
        return task
    return None

def delete_task(task_id):
    task = find_task_by_id(task_id)
    if task:
        db.tasks = [t for t in db.tasks if t['id'] != task_id]
        db.save()
        return True
    return False

def get_all_tasks():
    return [Task.from_dict(task) for task in db.tasks]

def find_task_by_id(task_id):
    for task in db.tasks:
        if task['id'] == task_id:
            return Task.from_dict(task)
    return None

def get_tasks_by_tasklist(user_id, tasklist_name):
    return [Task.from_dict(task) for task in db.tasks if task['tasklist_name'] == tasklist_name and task['user_id'] == user_id]

def mark_task_as_completed(task_id):
    task = find_task_by_id(task_id)
    if task:
        task.completed = True
        db.save()
        return task
    return None

def mark_task_as_important(task_id):
    task = find_task_by_id(task_id)
    if task:
        task.important = True
        db.save()
        return task
    return None

# tasklists
def create_tasklist(name, user_id):
    user = find_user_by_id(user_id)
    if user:
        user.tasklists.append(name)
        db.save()
        return Tasklist(name, user_id)
    return None

def get_all_tasklists(user_id):
    user = find_user_by_id(user_id)
    if user:
        return user.tasklists
    return []

def find_tasklist_by_name(user_id, tasklist_name):
    user = find_user_by_id(user_id)
    if user and tasklist_name in user.tasklists:
        return Tasklist(tasklist_name, user_id)
    return None

