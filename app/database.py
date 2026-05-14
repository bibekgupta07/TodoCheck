# Import Motor - async MongoDB driver
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Import settings to get database configuration
from app.config import settings

# Import Optional for type hints
from typing import Optional


# Global variable to store database connection
# Initially None, will be set when app starts
database: Optional[AsyncIOMotorDatabase] = None # type: ignore


async def connect_to_mongo():
    """
    Connect to MongoDB database.
    Called when application starts up.
    """
    global database
    
    # Create MongoDB client using connection URL from .env file
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Get the specific database we want to use
    database = client[settings.DATABASE_NAME]
    
    # Test connection by pinging the database
    try:
        await client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection.
    Called when application shuts down.
    """
    global database
    
    # Close the connection if it exists
    if database is not None:
        database.client.close()
        print("🔌 MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase: # type: ignore
    """
    Get database instance.
    Used by API endpoints to access the database.
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
    """
    if database is None:
        raise Exception("Database not connected")
    return database