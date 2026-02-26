from fastapi import FastAPI, Request, HTTPException,status
from api.utils import success_response



app= FastAPI(
    title= "Task Manager API",
    description= "API for managing tasks",
    version= "1.0.0"

)



@app.get("/")
def read_root(request:Request)-> success_response:
    return  success_response(
        status_code=status.HTTP_200_OK,
        message="welcome to the Task Manager API",
        data={
            "docs":f"{request.base_url}docs"
        }
    )
