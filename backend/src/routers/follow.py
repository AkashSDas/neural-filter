from fastapi import APIRouter, HTTPException, Query, status
from src.dependencies import db_dependency, current_user
from src.models.follow import Follow
from src.models.user import User
from sqlalchemy.orm import joinedload
from src.schemas.auth import UserInDB


router = APIRouter(prefix="/follow", tags=["follow"])


@router.get("", tags=["follow"], status_code=status.HTTP_200_OK)
async def follow(
    db: db_dependency,
    user: current_user,
    followed_id: int = Query(..., alias="followedId"),
) -> dict:
    """Follow and unfollow a user."""

    follower = db.query(User).filter(User.email == user["email"]).first()
    if not follower:
        raise HTTPException(status_code=400, detail="Follower does not exist")

    is_following = (
        db.query(Follow)
        .filter(Follow.follower_id == follower.id, Follow.followed_id == followed_id)
        .first()
    )

    if is_following:
        db.query(Follow).filter(
            Follow.follower_id == follower.id, Follow.followed_id == followed_id
        ).delete()
    else:
        db.add(Follow(follower_id=follower.id, followed_id=followed_id))

    db.commit()
    return {"message": "Success", "is_following": not is_following}


@router.get("/followers", tags=["follow"], status_code=status.HTTP_200_OK)
async def get_followers(db: db_dependency, user: current_user) -> dict:
    """Get a list of followers for a user."""

    user = db.query(User).filter(User.email == user["email"]).first()
    if not user:
        raise HTTPException(status_code=400, detail="Follower does not exist")

    followers = (
        db.query(User)
        .join(Follow, User.id == Follow.follower_id)
        .filter(Follow.followed_id == user.id)
        .all()
    )

    return {
        "followers": [
            UserInDB(id=follower.id, username=follower.username, email=follower.email)  # type: ignore
            for follower in followers
        ],
    }


@router.get("/following", tags=["follow"], status_code=status.HTTP_200_OK)
async def get_following(db: db_dependency, user: current_user) -> dict:
    """Get a list of users that a user is following."""

    user = db.query(User).filter(User.email == user["email"]).first()
    if not user:
        raise HTTPException(status_code=400, detail="Follower does not exist")

    following = (
        db.query(User)
        .join(Follow, User.id == Follow.followed_id)
        .filter(Follow.follower_id == user.id)
        .all()
    )

    return {
        "following": [
            UserInDB(id=following_user.id, username=following_user.username, email=following_user.email)  # type: ignore
            for following_user in following
        ],
    }
