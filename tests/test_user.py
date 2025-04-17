"""This module provides tests for the User class."""
from src.sr_sw_dev.social_networking import User


def test_user_init():
    """Checks that the user is initialized correctly."""
    user = User('Alice')
    assert user.get_name() == 'Alice', "User name should be set correctly"
    assert not user.has_posts(), "User should start with no posts"

def test_user_eq():
    """Checks that the user is equal to another user with the same name."""
    user1 = User('Alice')
    user2 = User('Alice')
    assert user1 == user2, "Users with same name should be equal"