# Import BaseModel from pydantic for data validation
from pydantic import BaseModel, Field

# Import datetime for timestamp fields
from datetime import datetime

# Import Optional for fields that can be None
from typing import Optional


# Schema for creating a new todo (what user sends)
class TodoCreate(BaseModel):
    """
    Schema for creating a new todo.
    Used when user sends POST request to create todo.
    """
    
    # Title is required, must be 1-200 characters
    title: str = Field(..., min_length=1, max_length=200)
    
    # Description is optional, max 1000 characters
    description: Optional[str] = Field(None, max_length=1000)
    
    # Completed status, defaults to False for new todos
    completed: bool = False
    
    # Example for API documentation
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }


# Schema for updating a todo (all fields optional)
class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo.
    All fields are optional - only send what you want to change.
    """
    
    # All fields are optional (can be None)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    
    # Example for API documentation
    class Config:
        json_schema_extra = {
            "example": {
                "completed": True
            }
        }


# Schema for todo response (what API sends back)
class TodoInDB(BaseModel):
    """
    Schema for todo in database and responses.
    Includes ID and timestamps.
    """
    
    # MongoDB's _id field converted to string
    # alias="_id" maps MongoDB's _id to our id field
    id: str = Field(alias="_id")
    
    # Todo fields
    title: str
    description: Optional[str] = None
    completed: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Configuration
    class Config:
        # Allow using both "id" and "_id" 
        populate_by_name = True
        
        # Example for API documentation
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2024-01-20T10:30:00",
                "updated_at": "2024-01-20T10:30:00"
            }
        }