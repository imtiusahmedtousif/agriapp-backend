from sqlalchemy import Column, Integer, String, Float
from database import Base

class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True) # Connects this profile to a specific logged-in user
    name = Column(String, nullable=True)
    land_size = Column(Float, nullable=True)
    soil_type = Column(String, nullable=True)
    types_of_crops = Column(String, nullable=True)
    crops_planned = Column(String, nullable=True)
    expected_crops = Column(String, nullable=True)
    actual_crops = Column(String, nullable=True)
    crops_for_sell = Column(String, nullable=True)
    crops_sold = Column(String, nullable=True)

# Keep your other models (MarketListing, OfficialHelper, ForumPost, FarmTask) exactly the same below...

class MarketListing(Base):
    __tablename__ = "market_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, index=True)
    price_per_maund = Column(Integer)
    listing_type = Column(String)  # "buy" or "sell"

class OfficialHelper(Base):
    __tablename__ = "official_helpers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    region = Column(String)
    contact_number = Column(String)

class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String)
    content = Column(String)