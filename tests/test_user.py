"""This module provides tests for the User class."""

from datetime import datetime, timedelta

from freezegun import freeze_time

from src.sr_sw_dev.social_networking import User


def test_user_init():
    """Checks that the user is initialized correctly."""
    user = User("Alice")
    assert user.get_name() == "Alice", "User name should be set correctly"
    assert not user.has_posts(), "User should start with no posts"

def test_user_eq():
    """Checks that the user is equal to another user with the same name."""
    user1 = User("Alice")
    user2 = User("Alice")
    assert user1 == user2, "Users with same name should be equal"

    user1.add_post("I love the weather today")
    user2.add_post("I love the weather today")
    assert user1 == user2, "Users with same name and posts should be equal"

def test_user_ne():
    """Checks that the user is not equal to another user with a different name."""
    user1 = User("Alice")
    user2 = User("Bob")
    assert user1 != user2, "Users with different names should not be equal"

    user3 = User("Alice")
    user3.add_post("I love the weather today")
    assert user1 != user2, "Users with different posts should not be equal"

def test_user_add_post():
    """Checks that the user can add a post."""
    user = User("Alice")
    user.add_post("I love the weather today")
    assert user.has_posts(), "User should have posts after adding one"
    assert user.count_posts() == 1, "User should have one post"

    posts = user.get_timeline()
    expected_posts = ["I love the weather today (just now)"]
    assert posts == expected_posts, "Latest post should match added content"

def test_user_following():
    """Checks that the user can follow another user."""
    user1 = User("Alice")
    user2 = User("Bob")
    user1.follows(user2)
    assert user1.get_following() == [user2], "User should follow the other user"

def test_user_wall():
    """Checks that the user can get their wall."""
    user1 = User("Alice")

    with freeze_time(datetime.now() - timedelta(minutes=5)):
        user1.add_post("I love the weather today")

    user2 = User("Charlie")
    with freeze_time(datetime.now() - timedelta(minutes=2)):
        user2.add_post("I'm in New York today! Anyone wants to have a coffee?")

    user1.follows(user2)

    wall = user1.get_wall()
    expected_wall = ["Alice - I love the weather today (5 minutes ago)", "Charlie - I'm in New York today! Anyone wants to have a coffee? (2 minutes ago)"]
    assert wall == expected_wall, "User should have two posts on their wall"
