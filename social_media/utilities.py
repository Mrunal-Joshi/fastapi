"""
utility function
"""


def find_post(posts, id):
    print("\n\n", posts, id)
    for post in posts:
        if post["id"] == int(id):
            return post
