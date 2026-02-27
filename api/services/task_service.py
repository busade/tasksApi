from sqlalchemy.orm import Session
from api.model.tasks import Tasks
from api.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from fastapi import HTTPException, status


class TaskService:
    """Service class for handling Task CRUD operations"""

    @staticmethod
    def create_task(db: Session, task: TaskCreate, owner_id: int) -> TaskResponse:
        """Create a new task"""
        db_task = Tasks(
            title=task.title,
            description=task.description,
            owner_id=owner_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return TaskResponse.from_orm(db_task)

    @staticmethod
    def get_task(db: Session, task_id: int, owner_id: int) -> TaskResponse:
        """Get a single task by ID"""
        task = db.query(Tasks).filter(
            Tasks.id == task_id,
            Tasks.owner_id == owner_id
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return TaskResponse.from_orm(task)

    @staticmethod
    def get_all_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 10) -> list[TaskResponse]:
        """Get all tasks for a user with pagination"""
        tasks = db.query(Tasks).filter(
            Tasks.owner_id == owner_id
        ).offset(skip).limit(limit).all()
        
        return [TaskResponse.from_orm(task) for task in tasks]

    @staticmethod
    def get_completed_tasks(db: Session, owner_id: int) -> list[TaskResponse]:
        """Get all completed tasks for a user"""
        tasks = db.query(Tasks).filter(
            Tasks.owner_id == owner_id,
            Tasks.completed == True
        ).all()
        
        return [TaskResponse.from_orm(task) for task in tasks]

    @staticmethod
    def get_pending_tasks(db: Session, owner_id: int) -> list[TaskResponse]:
        """Get all pending (incomplete) tasks for a user"""
        tasks = db.query(Tasks).filter(
            Tasks.owner_id == owner_id,
            Tasks.completed == False
        ).all()
        
        return [TaskResponse.from_orm(task) for task in tasks]

    @staticmethod
    def update_task(db: Session, task_id: int, owner_id: int, task_update: TaskUpdate) -> TaskResponse:
        """Update an existing task"""
        db_task = db.query(Tasks).filter(
            Tasks.id == task_id,
            Tasks.owner_id == owner_id
        ).first()
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update only provided fields
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed
        
        db.commit()
        db.refresh(db_task)
        return TaskResponse.from_orm(db_task)

    @staticmethod
    def delete_task(db: Session, task_id: int, owner_id: int) -> dict:
        """Delete a task by ID"""
        db_task = db.query(Tasks).filter(
            Tasks.id == task_id,
            Tasks.owner_id == owner_id
        ).first()
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        db.delete(db_task)
        db.commit()
        return {"message": "Task deleted successfully"}

    @staticmethod
    def delete_all_tasks(db: Session, owner_id: int) -> dict:
        """Delete all tasks for a user"""
        db.query(Tasks).filter(Tasks.owner_id == owner_id).delete()
        db.commit()
        return {"message": "All tasks deleted successfully"}

    

    @staticmethod
    def task_count(db: Session, owner_id: int) -> dict:
        """Get task statistics for a user"""
        total = db.query(Tasks).filter(Tasks.owner_id == owner_id).count()
        completed = db.query(Tasks).filter(
            Tasks.owner_id == owner_id,
            Tasks.completed == True
        ).count()
        pending = total - completed
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }
