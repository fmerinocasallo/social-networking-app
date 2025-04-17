"""This module provides tests for the User class."""
from src.sr_sw_dev.social_networking import User


def test_user_init():
    """Checks that the user is initialized correctly."""
    user = User('Alice')
    assert user.get_name() == 'Alice', "User name should be set correctly"
    assert not user.has_posts(), "User should start with no posts"