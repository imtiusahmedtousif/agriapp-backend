from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models

router = APIRouter(prefix="/api/profile", tags=["Profile"])

class ProfileUpdateSchema(BaseModel):
    name: str
    land_size: float
    soil_type: str
    types_of_crops: str
    crops_planned: str
    expected_crops: str
    actual_crops: str
    crops_for_sell: str
    crops_sold: str

@router.get("/")
def get_profile(user_id: str = Header(...), db: Session = Depends(get_db)):
    """
    Fetches the profile metadata matching the User-Id passed in the request header.
    If no entry exists, it returns a 404 prompting the app to show the onboarding form.
    """
    profile = db.query(models.FarmerProfile).filter(models.FarmerProfile.user_id == user_id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Onboarding required.")

    return {
        "farmer_name": profile.name,
        "land_size": profile.land_size,
        "soil_type": profile.soil_type,
        "types_of_crops": profile.types_of_crops,
        "crops_planned": profile.crops_planned,
        "expected_crops": profile.expected_crops,
        "actual_crops": profile.actual_crops,
        "crops_for_sell": profile.crops_for_sell,
        "crops_sold": profile.crops_sold,
    }

@router.post("/update")
def update_profile(data: ProfileUpdateSchema, user_id: str = Header(...), db: Session = Depends(get_db)):
    """
    Creates or updates the profile metrics linked to the authenticated user ID.
    """
    profile = db.query(models.FarmerProfile).filter(models.FarmerProfile.user_id == user_id).first()
    
    if not profile:
        # Create a new profile row for a first-time user
        profile = models.FarmerProfile(user_id=user_id)
        db.add(profile)

    # Sync incoming form fields to the user's database entry
    profile.name = data.name
    profile.land_size = data.land_size
    profile.soil_type = data.soil_type
    profile.types_of_crops = data.types_of_crops
    profile.crops_planned = data.crops_planned
    profile.expected_crops = data.expected_crops
    profile.actual_crops = data.actual_crops
    profile.crops_for_sell = data.crops_for_sell
    profile.crops_sold = data.crops_sold

    db.commit()
    return {"status": "Success", "message": "Profile metrics synchronized successfully."}