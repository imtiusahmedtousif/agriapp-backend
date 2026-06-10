from sqlalchemy import Column, Integer, String, Float
from database import Base


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, default="Anisur Rahman")
    land_size = Column(Float, default=2.5)  # Measured in Acres
    soil_type = Column(String, default="Clay Soil")

    # Core Crop Lifecycle Matrix Metrics
    types_of_crops = Column(String, default="Paddy, Jute")
    crops_planned = Column(String, default="Aman Rice")
    expected_crops = Column(String, default="45 Maunds")
    actual_crops = Column(String, default="42 Maunds")
    crops_for_sell = Column(String, default="15 Maunds Listed")
    crops_sold = Column(String, default="27 Maunds Complete")