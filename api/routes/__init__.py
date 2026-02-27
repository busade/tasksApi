from fastapi import APIRouter
from api.routes.auth_route import router as auth_router
from api.routes.task_routes import router as task_router


router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(task_router)