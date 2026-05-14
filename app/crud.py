# Import MongoDB database and collection types
from motor.motor_asyncio import AsyncIOMotorDatabase

# Import ObjectId for MongoDB _id field
from bson import ObjectId

# Import datetime for timestamps
from datetime import datetime

# Import typing utilities
from typing import Optional, List, Dict


# CRUD = Create, Read, Update, Delete operations


async def create_todo(db: AsyncIOMotorDatabase, collection_name: str, todo_data: dict) -> dict: # type: ignore
    """
    Create a new todo in database.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of collection (like table name)
        todo_data: Todo data to insert
        
    Returns:
        dict: Created todo with _id and timestamps
    """
    
    # Get the collection where we store todos
    collection = db[collection_name]
    
    # Add timestamps to the todo
    todo_data["created_at"] = datetime.utcnow()
    todo_data["updated_at"] = datetime.utcnow()
    
    # Insert todo into database
    result = await collection.insert_one(todo_data)
    
    # Add the generated _id to our data
    todo_data["_id"] = str(result.inserted_id)
    
    return todo_data


async def get_all_todos(db: AsyncIOMotorDatabase, collection_name: str) -> List[dict]: # type: ignore
    """
    Get all todos from database.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of collection
        
    Returns:
        List[dict]: List of all todos
    """
    
    # Get the collection
    collection = db[collection_name]
    
    # Empty list to store todos
    todos = []
    
    # Find all documents in collection
    # find() with no filter returns everything
    cursor = collection.find()
    
    # Loop through all todos
    async for todo in cursor:
        # Convert ObjectId to string for JSON
        todo["_id"] = str(todo["_id"])
        todos.append(todo)
    
    return todos


async def get_todo_by_id(db: AsyncIOMotorDatabase, collection_name: str, todo_id: str) -> Optional[dict]: # type: ignore
    """
    Get a specific todo by ID.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of collection
        todo_id: MongoDB ObjectId as string
        
    Returns:
        Optional[dict]: Todo if found, None if not found
    """
    
    # Get the collection
    collection = db[collection_name]
    
    # Convert string ID to ObjectId
    try:
        object_id = ObjectId(todo_id)
    except Exception:
        # Invalid ID format
        return None
    
    # Find one document with this _id
    todo = await collection.find_one({"_id": object_id})
    
    # If found, convert _id to string
    if todo:
        todo["_id"] = str(todo["_id"])
    
    return todo


async def update_todo(db: AsyncIOMotorDatabase, collection_name: str, todo_id: str, update_data: dict) -> Optional[dict]: # type: ignore
    """
    Update a todo in database.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of collection
        todo_id: MongoDB ObjectId as string
        update_data: Fields to update
        
    Returns:
        Optional[dict]: Updated todo if found, None if not found
    """
    
    # Get the collection
    collection = db[collection_name]
    
    # Convert string ID to ObjectId
    try:
        object_id = ObjectId(todo_id)
    except Exception:
        return None
    
    # Update the updated_at timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update document and return the updated version
    # $set updates only specified fields
    # return_document=True returns document AFTER update
    result = await collection.find_one_and_update(
        {"_id": object_id},        # Find todo with this ID
        {"$set": update_data},      # Update these fields
        return_document=True        # Return updated document
    )
    
    # If found, convert _id to string
    if result:
        result["_id"] = str(result["_id"])
    
    return result


async def delete_todo(db: AsyncIOMotorDatabase, collection_name: str, todo_id: str) -> bool: # type: ignore
    """
    Delete a todo from database.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of collection
        todo_id: MongoDB ObjectId as string
        
    Returns:
        bool: True if deleted, False if not found
    """
    
    # Get the collection
    collection = db[collection_name]
    
    # Convert string ID to ObjectId
    try:
        object_id = ObjectId(todo_id)
    except Exception:
        return False
    
    # Delete the document
    result = await collection.delete_one({"_id": object_id})
    
    # Return True if something was deleted
    # deleted_count is 1 if successful, 0 if not found
    return result.deleted_count > 0


async def count_todos(db: AsyncIOMotorDatabase, collection_name: str) -> int: # type: ignore
    """
    Count total todos in database.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of collection
        
    Returns:
        int: Total count of todos
    """
    
    # Get the collection
    collection = db[collection_name]
    
    # Count all documents
    # {} means no filter (count everything)
    return await collection.count_documents({})