from fastapi import FastAPI, Request, HTTPException, status
from fastapi.openapi.utils import get_openapi
from api.utils import success_response
from api.routes import router as api_router


app = FastAPI(
    title="Task Manager API",
    description="API for managing tasks with JWT authentication",
    version="1.0.0",
)

app.include_router(api_router)


def custom_openapi():
    """Configure OpenAPI schema with JWT security"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Task Manager API",
        version="1.0.0",
        description="API for managing tasks with JWT authentication",
        routes=app.routes,
    )
    
    # Add security scheme for JWT
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT access token"
        }
    }
    
    # Apply security to relevant endpoints only
    # Skip authentication routes so users can register/login without a token
    for route_path, path_item in openapi_schema["paths"].items():
        # do not secure any /api/v1/auth/* paths
        if route_path.startswith("/api/v1/auth"):
            continue
        for method in path_item.values():
            if isinstance(method, dict):
                method["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def read_root(request: Request) -> success_response:
    return success_response(
        status_code=status.HTTP_200_OK,
        message="welcome to the Task Manager API",
        data={
            "docs": f"{request.base_url}docs"
        }
    )
