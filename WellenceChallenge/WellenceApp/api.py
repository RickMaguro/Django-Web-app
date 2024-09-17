from ninja import NinjaAPI, Schema
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Tasks
from .services import TaskService
from typing import List, Optional
from django.db.models import Count

# Create Ninja API instance
api = NinjaAPI()

# Define schema for task input data
class TaskIn(Schema):
    email: str
    task: str
    due_by: str
    priority: int
    is_urgent: Optional[bool] = False

# Define schema for task output data
class TaskOut(Schema):
    id: int
    email: str
    task: str
    due_by: str
    priority: int
    is_urgent: bool

# API endpoint: Create a new task
@api.post("/tasks")
def create_task(request, task: TaskIn):
    # Convert the TaskIn object to a dictionary
    task_data = task.dict()
    
    # Use the TaskService to create a new task
    created_task = TaskService.create_task(task_data)
    
    # Return a success response with the new task's ID
    return {"success": True, "id": created_task.id}

# API endpoint: Get list of all tasks
@api.get("/tasks", response=List[TaskOut])
def list_tasks(request):
    return TaskService.get_all_tasks()

# API endpoint: Get details of a specific task
@api.get("/tasks/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    return TaskService.get_task(task_id)

# API endpoint: Update a specific task
@api.put("/tasks/{task_id}")
def update_task(request, task_id: int, task: TaskIn):
    return TaskService.update_task(task_id, task.dict())

# API endpoint: Delete a specific task
@api.delete("/tasks/{task_id}")
def delete_task(request, task_id: int):
    TaskService.delete_task(task_id)
    return {"success": True}

# API endpoint: Tasks due report
@api.get("/tasks-due-report", response=List[TaskOut])
def tasks_due_report(request):
    today = timezone.now()
    next_30_days = today + timezone.timedelta(days=30)
    tasks = Tasks.objects.filter(due_by__range=(today, next_30_days))
    return [TaskOut.from_orm(task) for task in tasks]

# API endpoint: Tasks priority due
@api.get("/tasks-priority-due")
def tasks_priority_due(request):
    today = timezone.now()
    next_30_days = today + timezone.timedelta(days=30)
    tasks = Tasks.objects.filter(due_by__range=(today, next_30_days))
    priority_counts = tasks.values('priority').annotate(count=Count('id'))
    return [{"priority": item['priority'], "count": item['count']} for item in priority_counts]

# API endpoint: Urgent tasks report
@api.get("/urgent-tasks-report", response=List[TaskOut])
def urgent_tasks_report(request):
    today = timezone.now()
    next_30_days = today + timezone.timedelta(days=30)
    tasks = Tasks.objects.filter(due_by__range=(today, next_30_days), is_urgent=True)
    return [TaskOut.from_orm(task) for task in tasks]

# API endpoint: All tasks report
@api.get("/all-tasks-report", response=List[TaskOut])
def all_tasks_report(request):
    tasks = Tasks.objects.all()
    return [TaskOut.from_orm(task) for task in tasks]
