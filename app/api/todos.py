# Import FastAPI components
from fastapi import APIRouter, HTTPException, status, Depends

# Import database function
from app.database import get_database

# Import settings for collection name
from app.config import settings

# Import CRUD functions
from app import crud

# Import Pydantic models
from app.models import TodoCreate, TodoUpdate, TodoInDB

# Import Motor database type
from motor.motor_asyncio import AsyncIOMotorDatabase

# Import List type for type hints
from typing import List


# Create router for todo endpoints
# All routes in this router will start with /todos
router = APIRouter(
    prefix="/todos",
    tags=["Todos"]  # Groups endpoints in API docs
)


# CREATE: Create a new todo
@router.post("/", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,                           # Request body
    db: AsyncIOMotorDatabase = Depends(get_database)  # Database dependency # type: ignore
):
    """
    Create a new todo.
    
    - **title**: Todo title (required)
    - **description**: Todo description (optional)
    - **completed**: Completion status (default: False)
    """
    
    # Convert pydantic model to dictionary
    todo_dict = todo.model_dump()
    
    # Create todo in database
    created_todo = await crud.create_todo(db, settings.COLLECTION_NAME, todo_dict)
    
    # Return created todo
    return TodoInDB(**created_todo)


# READ: Get all todos
@router.get("/", response_model=List[TodoInDB])
async def get_todos(
    db: AsyncIOMotorDatabase = Depends(get_database) # type: ignore
):
    """
    Get all todos.
    
    Returns a list of all todo items.
    """
    
    # Get all todos from database
    todos = await crud.get_all_todos(db, settings.COLLECTION_NAME)
    
    # Convert each todo dict to TodoInDB model
    return [TodoInDB(**todo) for todo in todos]


# READ: Get single todo by ID
@router.get("/{todo_id}", response_model=TodoInDB)
async def get_todo(
    todo_id: str,                               # Path parameter
    db: AsyncIOMotorDatabase = Depends(get_database) # type: ignore
):
    """
    Get a specific todo by ID.
    
    - **todo_id**: MongoDB ObjectId as string
    """
    
    # Get todo from database
    todo = await crud.get_todo_by_id(db, settings.COLLECTION_NAME, todo_id)
    
    # If not found, raise 404 error
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Return todo
    return TodoInDB(**todo)


# UPDATE: Update a todo
@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo(
    todo_id: str,                               # Path parameter
    todo_update: TodoUpdate,                    # Request body
    db: AsyncIOMotorDatabase = Depends(get_database) # type: ignore
):
    """
    Update an existing todo.
    
    - **todo_id**: MongoDB ObjectId as string
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **completed**: New completion status (optional)
    
    Only send fields you want to update.
    """
    
    # Convert to dict, excluding fields that weren't set
    # exclude_unset=True means only include fields user sent
    update_dict = todo_update.model_dump(exclude_unset=True)
    
    # Check if any fields were provided
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update"
        )
    
    # Update todo in database
    updated_todo = await crud.update_todo(db, settings.COLLECTION_NAME, todo_id, update_dict)
    
    # If not found, raise 404 error
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Return updated todo
    return TodoInDB(**updated_todo)


# DELETE: Delete a todo
@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,                               # Path parameter
    db: AsyncIOMotorDatabase = Depends(get_database) # type: ignore
):
    """
    Delete a todo.
    
    - **todo_id**: MongoDB ObjectId as string
    """
    
    # Delete from database
    deleted = await crud.delete_todo(db, settings.COLLECTION_NAME, todo_id)
    
    # If not found, raise 404 error
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Return success message
    return {
        "message": "Todo deleted successfully",
        "id": todo_id
    }