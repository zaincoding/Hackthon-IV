from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from ...models.user import UserCreateRequest, UserLoginRequest, UserResponse, Token, User
from ...models.database import get_db, DBUser
from ...services.user_service import UserService
from ...utils.auth import authenticate_user, create_access_token, get_current_user
from datetime import timedelta


router = APIRouter()
user_service = UserService()


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        # Check if user already exists by username
        existing_user = user_service.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if user already exists by email
        existing_email = user_service.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    except HTTPException:
        # Re-raise HTTP exceptions (like already registered)
        raise
    except Exception as e:
        # Log the error and raise a generic error for other exceptions
        import logging
        logging.error(f"Error checking existing user during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration check"
        )

    # Create new user
    try:
        db_user = user_service.create_user(db, user_data)

        # Convert DBUser to UserResponse
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_active=db_user.is_active,
            created_at=db_user.created_at.isoformat(),
            updated_at=db_user.updated_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login a user and return an access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time if needed
    access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: DBUser = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat(),
        updated_at=current_user.updated_at.isoformat()
    )


@router.post("/logout")
async def logout_user():
    """Logout a user."""
    # In a stateless JWT system, logout is typically handled on the client side
    # by removing the token. We can add server-side invalidation if needed.
    return {"message": "Successfully logged out"}