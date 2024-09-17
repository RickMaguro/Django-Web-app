from .models import Tasks
from django.shortcuts import get_object_or_404

class TaskService:
    @staticmethod
    def create_task(task_data):
        # Handle the is_urgent field
        is_urgent = task_data.get('is_urgent')
        task_data['is_urgent'] = is_urgent in [True, 'on', 'true', 'True', 1] # Convert to boolean

        # Get the latest id and increment it
        latest_id = Tasks.objects.latest('id').id if Tasks.objects.exists() else 0
        new_id = latest_id + 1
        task_data['id'] = new_id

        # Create a new Tasks object
        task = Tasks.objects.create(**task_data)
        return task

    @staticmethod
    def get_all_tasks():
        # Retrieve all tasks
        return Tasks.objects.all()

    @staticmethod
    def get_task(task_id):
        # Retrieve a specific task
        return get_object_or_404(Tasks, id=task_id)

    @staticmethod
    def update_task(task_id, task_data):
        # Update a specific task
        task = get_object_or_404(Tasks, id=task_id)
        for key, value in task_data.items():
            setattr(task, key, value)
        task.save()
        return task

    @staticmethod
    def delete_task(task_id):
        # Delete a specific task
        task = get_object_or_404(Tasks, id=task_id)
        task.delete()
