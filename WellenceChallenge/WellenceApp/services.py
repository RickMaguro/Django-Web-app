from datetime import date, timedelta
from typing import List
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Tasks
from .schemas import TaskIn, TaskOut
import logging

logger = logging.getLogger(__name__)

class TaskService:
    @staticmethod
    def create_task(task_data: TaskIn) -> TaskOut:
        try:
            task_data_dict = task_data.dict()
            latest_id = Tasks.objects.latest('id').id if Tasks.objects.exists() else 0
            new_id = latest_id + 1
            task_data_dict['id'] = new_id
            task = Tasks.objects.create(**task_data_dict)
            return TaskOut.from_orm(task)
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            raise

    @staticmethod
    def get_all_tasks() -> List[TaskOut]:
        # Retrieve all tasks
        tasks = Tasks.objects.all()
        return [TaskOut.from_orm(task) for task in tasks]

    @staticmethod
    def get_task(task_id: int) -> TaskOut:
        # Retrieve a specific task
        try:
            task = Tasks.objects.get(id=task_id)
            return TaskOut.from_orm(task)
        except ObjectDoesNotExist:
            raise ValueError(f"Task with id {task_id} does not exist")

    @staticmethod
    def update_task(task_id: int, task_data: TaskIn) -> TaskOut:
        # Update a specific task
        try:
            task = Tasks.objects.get(id=task_id)
            task_data_dict = task_data.dict(exclude_unset=True)
            for key, value in task_data_dict.items():
                setattr(task, key, value)
            task.save()
            return TaskOut.from_orm(task)
        except ObjectDoesNotExist:
            raise ValueError(f"Task with id {task_id} does not exist")

    @staticmethod
    def delete_task(task_id: int) -> None:
        # Delete a specific task
        try:
            task = Tasks.objects.get(id=task_id)
            task.delete()
        except ObjectDoesNotExist:
            raise ValueError(f"Task with id {task_id} does not exist")

    @staticmethod
    def get_filtered_tasks(start_date: date, end_date: date) -> List[TaskOut]:
        # Retrieve tasks within a date range
        tasks = Tasks.objects.filter(due_by__range=(start_date, end_date))
        return [TaskOut.from_orm(task) for task in tasks]

    @staticmethod
    def get_priority_due_tasks() -> List[TaskOut]:
        # Retrieve priority tasks due in the next 30 days
        today = timezone.now()
        next_30_days = today + timedelta(days=30)
        tasks = Tasks.objects.filter(due_by__range=(today, next_30_days)).order_by('priority')
        return [TaskOut.from_orm(task) for task in tasks]

    @staticmethod
    def get_urgent_tasks() -> List[TaskOut]:
        # Retrieve urgent tasks due in the next 30 days
        today = timezone.now()
        next_30_days = today + timedelta(days=30)
        tasks = Tasks.objects.filter(due_by__range=(today, next_30_days), is_urgent=True)
        return [TaskOut.from_orm(task) for task in tasks]


