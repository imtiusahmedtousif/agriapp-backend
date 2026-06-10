from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models
import httpx  

router = APIRouter()

class TaskCreateSchema(BaseModel):
    task_title: str
    due_date: str

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return {"tasks": db.query(models.FarmTask).all()}

@router.post("/tasks")
def create_task(task: TaskCreateSchema, db: Session = Depends(get_db)):
    db_task = models.FarmTask(task_title=task.task_title, due_date=task.due_date)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"status": "Success", "message": "Task logged successfully."}

@router.get("/weather")
async def get_weather(lat: float = 22.54, lon: float = 89.99): 
    API_KEY = "YOUR_OPENWEATHER_API_KEY" 
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Weather service unavailable")
            
            data = response.json()
            return {
                "location": data.get("name", "Bhandaria Region"),
                "temperature": f"{round(data['main']['temp'])}°C",
                "humidity": f"{data['main']['humidity']}%",
                "condition": data["weather"][0]["description"].title()
            }
        except Exception:
            return {"location": "Bhandaria", "temperature": "--°C", "humidity": "--%", "condition": "Offline"}