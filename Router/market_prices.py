from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()


@router.get("/averages")
def get_market_averages(db: Session = Depends(get_db)):
    # Pull all crop sell listings currently active in the database
    listings = db.query(models.MarketListing).filter(models.MarketListing.listing_type == "sell").all()

    # Base dictionary to store total prices and counter pools for calculations
    crop_pools = {}

    # Calculate real-time dynamic valuation pools
    for item in listings:
        if item.crop_name not in crop_pools:
            crop_pools[item.crop_name] = {"total_price": 0, "count": 0}
        crop_pools[item.crop_name]["total_price"] += item.price_per_maund
        crop_pools[item.crop_name]["count"] += 1

    # Format the calculated averages to drop cleanly into your Flutter frontend lists
    calculated_averages = {}
    for crop, data in crop_pools.items():
        avg = round(data["total_price"] / data["count"])
        calculated_averages[crop] = f"{avg}"

    # Fallback to local reference values if no active crop items are listed for sale yet
    if not calculated_averages:
        calculated_averages = {
            "Fine Rice (Paddy)": "1,250",
            "Organic Jute": "3,000",
            "Seed Potato": "780"
        }

    return {"averages": calculated_averages}