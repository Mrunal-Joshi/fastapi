"""
utility function
"""

from fastapi import HTTPException, status


def find_post(posts, path_id):
    print("\n\n", posts, path_id)
    for post in posts:
        if post["id"] == int(path_id):
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post not found for the path_id {path_id}",
    )
