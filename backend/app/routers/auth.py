"""
Authentication routes: signup, login, and user management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_role
)
from ..models.user import User, UserRole
from ..schemas.auth import (
    UserSignup,
    UserLogin,
    Token,
    UserResponse,
    MessageResponse
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: Valid email address (must be unique)
    - **name**: User's full name
    - **password**: Password (minimum 8 characters)
    - **role**: User role (ADMIN or STAFF, defaults to STAFF)
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        new_user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=hash_password(user_data.password),
            role=UserRole(user_data.role)
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        import traceback
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)} | Trace: {traceback.format_exc()[-200:]}"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access token.
    
    - **email**: User's email address
    - **password**: User's password
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Requires valid JWT token in Authorization header.
    """
    return current_user


@router.get("/admin-only", response_model=MessageResponse)
async def admin_only_route(current_user: User = Depends(require_role("ADMIN"))):
    """
    Demo endpoint that requires ADMIN role.
    
    This demonstrates role-based authorization.
    """
    return {"message": f"Welcome, Admin {current_user.name}! You have access to this protected route."}
