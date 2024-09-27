from http.client import HTTPException
from ninja import NinjaAPI
from django.utils import timezone
from typing import List
from datetime import timedelta
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .models import Tasks
from .schemas import TaskIn, TaskOut
from .services import TaskService

import logging

# Create Ninja API instance
api = NinjaAPI()
logger = logging.getLogger(__name__)

# funciton that allows authentication in an async setting
async def async_auth(request):
    session_key = request.COOKIES.get("sessionid")
    if session_key:
        session = await sync_to_async(Session.objects.get)(session_key=session_key)
        user_id = session.get_decoded().get("_auth_user_id")
        if user_id:
            user = await sync_to_async(User.objects.get)(id=user_id)
            return user
    return None

# API endpoint: Create a new task
@api.post("/tasks/", response={201: TaskOut, 400: dict, 422: dict}, auth=async_auth)
async def create_task(request, task: TaskIn):
    try:
        created_task = await sync_to_async(TaskService.create_task)(task)
        return 201, created_task
    except Exception as e:
        return 422, {"detail": str(e)}

# API endpoint: Get list of all tasks
@api.get("/tasks/", response=List[TaskOut], auth=async_auth)
async def get_tasks(request):
    now = timezone.now()
    tasks_queryset = Tasks.objects.filter(due_by__gte=now, due_by__lte=now + timedelta(days=30))
    tasks = await sync_to_async(list)(tasks_queryset)
    return [TaskOut.from_orm(task) for task in tasks]

# API endpoint: Get details of a specific task
@api.get("/tasks/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    try:
        return TaskService.get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# API endpoint: Update a specific task
@api.put("/tasks/{task_id}/", response={200: TaskOut, 404: dict}, auth=async_auth)
async def update_task(request, task_id: int, task: TaskIn):
    try:
        updated_task = await sync_to_async(TaskService.update_task)(task_id, task)
        return 200, updated_task
    except Tasks.DoesNotExist:
        return 404, {"detail": "Task not found"}

# API endpoint: Delete a specific task
@api.delete("/tasks/{task_id}/", response={204: None, 404: dict}, auth=async_auth)
async def delete_task(request, task_id: int):
    try:
        await sync_to_async(TaskService.delete_task)(task_id)
        return 204, None
    except Tasks.DoesNotExist:
        return 404, {"detail": "Task not found"}

# API endpoint: Tasks due report (no authentication required)
@api.get("/tasks-due-report", response=List[TaskOut])
async def tasks_due_report(request):
    @sync_to_async
    def get_tasks():
        today = timezone.now()
        next_30_days = today + timedelta(days=30)
        return list(Tasks.objects.filter(due_by__range=(today, next_30_days)))

    tasks = await get_tasks()
    return [TaskOut.from_orm(task) for task in tasks]

# API endpoint: Tasks priority due (no authentication required)
@api.get("/tasks-priority-due", response=List[TaskOut])
async def tasks_priority_due(request):
    tasks = await sync_to_async(TaskService.get_priority_due_tasks)()
    return tasks

# API endpoint: Urgent tasks report (no authentication required)
@api.get("/urgent-tasks-report", response=List[TaskOut])
async def urgent_tasks_report(request):
    tasks = await sync_to_async(TaskService.get_urgent_tasks)()
    return tasks

# API endpoint: All tasks report with pagination (no authentication required)
@api.get("/all-tasks-report", response=dict)
async def all_tasks_report(request, page: int = 1, page_size: int = 10):
    @sync_to_async
    def get_paginated_tasks():
        tasks = Tasks.objects.all().order_by('-due_by')
        paginator = Paginator(tasks, page_size)
        page_obj = paginator.get_page(page)
        return {
            "tasks": [TaskOut.from_orm(task) for task in page_obj],
            "total_pages": paginator.num_pages,
            "current_page": page
        }

    return await get_paginated_tasks()