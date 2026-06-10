from fastapi import FastAPI
from database import engine, Base
import models

# We only import market_prices here—marketprice is completely removed
from Router import market_prices, profile, trade, planner, help_system

# Automatically create database tables if they aren't initialized yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agri-App Backend")

# Register all routes onto the main FastAPI instance app engine
app.include_router(profile.router)
app.include_router(trade.router, prefix="/api/trade", tags=["Trade"])
app.include_router(planner.router, prefix="/api/planner", tags=["Planner"])
app.include_router(help_system.router, prefix="/api/help", tags=["Help System"])

# Using the correct module name with .router appended
app.include_router(market_prices.router, prefix="/api/market", tags=["Market Prices"])

@app.get("/")
def root():
    return {"message": "Agri-App Network Desk Engine is Live and Running."}