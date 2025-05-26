"""This module provides tests for the User class."""

from datetime import datetime, timedelta

from freezegun import freeze_time

from src.sr_sw_dev.models import PostModel, UserModel
from src.sr_sw_dev.social_networking import Post, User


def test_user_init():
    """Checks that the user is initialized correctly."""
    validated_user = UserModel(name="Alice")
    user = User(validated_user)
    assert user.get_name() == "Alice", "User name should be set correctly"
    assert not user.has_posts(), "User should start with no posts"


def test_user_eq():
    """Checks that the user is equal to another user with the same name."""
    validated_user1 = UserModel(name="Alice")
    validated_user2 = UserModel(name="Alice")
    user1 = User(validated_user1)
    user2 = User(validated_user2)
    assert user1 == user2, "Users with same name should be equal"

    post_model = PostModel(content="I love the weather today", author="Alice")
    post = Post(post_model)
    user1.add_post(post)
    user2.add_post(post)
    assert user1 == user2, "Users with same name and posts should be equal"


def test_user_ne():
    """Checks that the user is not equal to another user with a different name."""
    validated_user1 = UserModel(name="Alice")
    validated_user2 = UserModel(name="Bob")
    user1 = User(validated_user1)
    user2 = User(validated_user2)
    assert user1 != user2, "Users with different names should not be equal"

    validated_user3 = UserModel(name="Alice")
    user3 = User(validated_user3)
    validated_post = PostModel(content="I love the weather today", author="Alice")
    post = Post(validated_post)
    user3.add_post(post)
    assert user1 != user3, "Users with different posts should not be equal"


def test_user_add_post():
    """Checks that the user can add a post."""
    validated_user = UserModel(name="Alice")
    user = User(validated_user)
    validated_post = PostModel(content="I love the weather today", author="Alice")
    post = Post(validated_post)
    user.add_post(post)
    assert user.has_posts(), "User should have posts after adding one"
    assert user.count_posts() == 1, "User should have one post"

    posts = user.get_timeline()
    expected_posts = ["I love the weather today (just now)"]
    assert posts == expected_posts, "Latest post should match added content"


def test_user_following():
    """Checks that the user can follow another user."""
    validated_user1 = UserModel(name="Alice")
    validated_user2 = UserModel(name="Bob")
    user1 = User(validated_user1)
    user2 = User(validated_user2)
    user1.follows(user2)
    assert user1.get_following() == [user2], "User should follow the other user"


def test_user_wall():
    """Checks that the user can get their wall."""
    validated_user1 = UserModel(name="Alice")
    user1 = User(validated_user1)

    with freeze_time(datetime.now() - timedelta(minutes=5)):
        validated_post1 = PostModel(content="I love the weather today", author="Alice")
        post1 = Post(validated_post1)
        user1.add_post(post1)

    validated_user2 = UserModel(name="Charlie")
    user2 = User(validated_user2)
    with freeze_time(datetime.now() - timedelta(minutes=2)):
        validated_post2 = PostModel(
            content="I'm in New York today! Anyone wants to have a coffee?",
            author="Charlie",
        )
        post2 = Post(validated_post2)
        user2.add_post(post2)

    user1.follows(user2)

    wall = user1.get_wall()
    expected_wall = [
        "Alice - I love the weather today (5 minutes ago)",
        "Charlie - I'm in New York today! Anyone wants to have a coffee? (2 minutes ago)",
    ]
    assert wall == expected_wall, "User should have two posts on their wall"
