import re
from collections import Counter
import string
from sqltools import sqltools as sq


def get_recommendations(email):
    favorites_result = sq.get_column_value_by_name("users", "favorites", ("email", email), "data.db")
    if not favorites_result:
        return []
    user_favorites = favorites_result[0][0] or ""
    favorite_tags = set(user_favorites.split())
    all_posts = sq.get_column_value_by_name("posts", "*", (1, 1), "data.db")
    if not all_posts:
        return []
    recommended_posts = []
    for post in all_posts:
        post_tags = set(post[9].split()) if post[9] else set()
        matching_tags = len(favorite_tags.intersection(post_tags))
        if matching_tags > 0:
            recommended_posts.append((matching_tags, post))
    recommended_posts.sort(reverse=True)
    return [post for score, post in recommended_posts]


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_raiting(veiws, posts_amount, comments_amount):
    raiting = 0
    if posts_amount == 0:
        return raiting
    raiting = int((veiws + comments_amount)/posts_amount)
    return raiting

