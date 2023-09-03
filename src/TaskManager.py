class Task:
    def __init__(self, title, due_date, status):
        self.title = title
        self.due_date = due_date
        self.status = status


class TaskManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, title, due_date, status):
        return Task(title, due_date, status)

    def add_task(self, task):
        self.tasks.append(task)

    def view_tasks(self):
        return self.tasks

    def update_task_status(self, task, status):
        task.status = status

    def remove_task(self, task):
        self.tasks.remove(task)
}