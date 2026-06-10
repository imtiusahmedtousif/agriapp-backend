from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models

router = APIRouter()


# Data Validation Blueprint for accepting incoming mobile trade entries
class CreateListingSchema(BaseModel):
    crop_name: str
    price_per_maund: int
    listing_type: str  # Must accept either "buy" or "sell"


@router.get("/listings")
def get_marketplace_listings(db: Session = Depends(get_db)):
    # Pulls all commercial active transactions inside the app database
    listings = db.query(models.MarketListing).all()

    # If a brand new user loads an empty database, seed standard reference lines
    if not listings:
        default_listings = [
            models.MarketListing(crop_name="Fine Rice (Paddy)", price_per_maund=1250, listing_type="sell"),
            models.MarketListing(crop_name="Organic Jute", price_per_maund=3000, listing_type="sell"),
            models.MarketListing(crop_name="Premium Zinc Fertilizer", price_per_maund=850, listing_type="buy")
        ]
        db.add_all(default_listings)
        db.commit()
        listings = db.query(models.MarketListing).all()

    return {"listings": listings}


@router.post("/listings/new")
def post_market_listing(item: CreateListingSchema, db: Session = Depends(get_db)):
    # Basic data validation step
    if item.listing_type not in ["buy", "sell"]:
        raise HTTPException(status_code=400, detail="Invalid trade listing channel. Must specify 'buy' or 'sell'.")

    new_item = models.MarketListing(
        crop_name=item.crop_name,
        price_per_maund=item.price_per_maund,
        listing_type=item.listing_type
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"status": "Success", "message": f"Asset {item.crop_name} broadcast live to network desk."}