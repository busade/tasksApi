from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.config.config import get_db
from api.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from api.services.task_service import TaskService
from api.utils import success_response
from api.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# CREATE - Create a new task
@router.post("", response_model=TaskResponse, summary="Create a new task", status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new task for the authenticated user"""
    try:
        result = TaskService.create_task(db, task, current_user["id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# READ - Get all tasks for current user
@router.get("", response_model=list[TaskResponse], summary="Get all tasks")
def get_all_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Retrieve all tasks for the authenticated user with pagination"""
    try:
        tasks = TaskService.get_all_tasks(db, current_user["id"], skip, limit)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/stats/count", summary="Get task statistics")
def get_task_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get task statistics (total, completed, pending) for the authenticated user"""
    try:
        stats = TaskService.task_count(db, current_user["id"])
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Task statistics retrieved successfully",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status/completed", response_model=list[TaskResponse], summary="Get completed tasks")
def get_completed_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all completed tasks for the authenticated user"""
    try:
        tasks = TaskService.get_completed_tasks(db, current_user["id"])
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# READ - Get pending tasks
@router.get("/status/pending", response_model=list[TaskResponse], summary="Get pending tasks")
def get_pending_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all pending (incomplete) tasks for the authenticated user"""
    try:
        tasks = TaskService.get_pending_tasks(db, current_user["id"])
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# READ - Get a single task by ID
@router.get("/{task_id}", response_model=TaskResponse, summary="Get task by ID")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific task by ID (user can only access their own tasks)"""
    try:
        task = TaskService.get_task(db, task_id, current_user["id"])
        return task
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# UPDATE - Update a task
@router.put("/{task_id}", response_model=TaskResponse, summary="Update a task")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an existing task (user can only update their own tasks)"""
    try:
        result = TaskService.update_task(db, task_id, current_user["id"], task_update)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




# DELETE - Delete a single task
@router.delete("/{task_id}", summary="Delete a task", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a specific task (user can only delete their own tasks)"""
    try:
        result = TaskService.delete_task(db, task_id, current_user["id"])
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Task deleted successfully"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# DELETE - Delete all tasks
@router.delete("", summary="Delete all tasks", status_code=status.HTTP_200_OK)
def delete_all_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete all tasks for the authenticated user"""
    try:
        result = TaskService.delete_all_tasks(db, current_user["id"])
        return success_response(
            status_code=status.HTTP_200_OK,
            message="All tasks deleted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
