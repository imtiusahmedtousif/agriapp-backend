
import os

import os

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel  # <-- MAKE SURE THIS LINE IS HERE!
from database import get_db
import models
import google.generativeai as genai

import httpx

router = APIRouter()

class ForumCreateSchema(BaseModel):
    author: str
    title: str
    content: str

class AIChatSchema(BaseModel):
    message: str

@router.post("/ai-chat")
async def process_ai_chat(payload: AIChatSchema):
    import os
    
    # Replace your raw API key assignment with this line:
    api_key = os.environ.get("AQ.Ab8RN6KETNoVn7P2TYHYBSNeaU50R2BVHzyyw4DwchvhH5UFMg")
    
    # Context framing to keep the AI working strictly as a digital agronomist
    system_instruction = "You are an expert digital agronomist helping rural farmers. Give concise, actionable advice regarding crops, soil, and fertilizers."
    
    payload_data = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nFarmer Question: {payload.message}"}]}]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload_data)
            res_json = response.json()
            ai_reply = res_json['candidates'][0]['content']['parts'][0]['text']
            return {"reply": ai_reply.strip()}
        except Exception as e:
            return {"reply": "I'm having trouble reaching the network desk right now. Please try again shortly."}

@router.get("/officials")
def get_officials(db: Session = Depends(get_db)):
    return db.query(models.OfficialHelper).all()

@router.get("/forum")
def get_forum_posts(db: Session = Depends(get_db)):
    return db.query(models.ForumPost).all()

@router.post("/forum/new")
def create_forum_post(post: ForumCreateSchema, db: Session = Depends(get_db)):
    db_post = models.ForumPost(author=post.author, title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"status": "Success", "message": "Forum entry broadcast live."}