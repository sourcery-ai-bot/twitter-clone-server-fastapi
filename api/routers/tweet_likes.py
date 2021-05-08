# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List, Optional

# Custom Modules
from .. import schemas, crud
from ..dependencies import get_db, get_current_user
from ..core import security
from ..core.config import settings

# FastAPI router object
router = APIRouter(prefix="/tweet-likes", tags=['tweet-likes'])


@router.get("", response_model=List[schemas.TweetLikeResponseBody])
def get_all_tweet_likes(tweetId: Optional[int] = None, db: Session = Depends(get_db)):
    """
    The GET method for this endpoint will send back either all, or specific likes based on tweet. This endpoint will always return an array of objects.

    If you want all likes, simply make the GET request and send no data. If you want likes from a specific tweet, send the tweet Id

    In the example, we send the numeric id 1. The API returns all likes on tweets 1. If you want all likes on all tweets, send no data.

    An error will be returned if any tweetId does not exist.
    """
    tweet_likes = []
    if tweetId:
        tweet_likes = crud.get_all_tweet_likes_for_tweet(db, tweetId)

    else:
        tweet_likes = crud.get_all_tweet_likes(db)

    return [
        schemas.TweetLikeResponseBody(
            tweetId=like.tweet_id,
            userId=like.user.id,
            username=like.user.username
        ) for like in tweet_likes
    ]


@router.post("", response_model=schemas.EmptyResponse)
def like_a_tweet(
    tweet_body: schemas.TweetLikeCreateRequestBody,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    # validate & create the like record
    tweet_like = crud.create_tweet_like_for_tweet(
        db=db, tweet_id=tweet_body.tweetId, user_id=current_user.id)

    # TODO return 201 created
    return schemas.EmptyResponse()


@router.delete("", response_model=schemas.EmptyResponse)
def delete_tweet_like(
        request_body: schemas.TweetLikeDeleteRequestBody,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)):

    delete_successful = crud.delete_tweet_like(
        db, current_user.id, request_body.tweetId)

    # TODO return status for delete?
    return schemas.EmptyResponse()
