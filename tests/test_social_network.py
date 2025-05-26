"""This module provides tests for the SocialNetwork class."""

import pytest

from src.social_network.social_networking import SocialNetwork


def test_social_network_init():
    """Checks that a social network is initialized correctly."""
    social_network = SocialNetwork()
    assert not social_network.has_users(), "SocialNetwork should start with no users"


def test_social_network_add_user():
    """Checks that a social network can add a user."""
    social_network = SocialNetwork()
    social_network.add_user("Alice")
    assert social_network.has_user("Alice"), "User should be added correctly"


def test_social_network_add_duplicate_user():
    """Checks that adding a duplicate user doesn't create a new user."""
    social_network = SocialNetwork()
    social_network.add_user("Alice")
    social_network.add_user("Alice")

    n_users = social_network.count_users()
    assert n_users == 1, "Adding duplicate user should not create new user"


def test_social_network_add_post():
    """Checks that users can post messages."""
    social_network = SocialNetwork()
    social_network.add_user("Alice")
    try:
        social_network.add_post("Alice", "I love the weather today")
    except ValueError:
        raise AssertionError("Posting should be successful") from None

    posts = social_network.get_user_timeline("Alice")
    expected_posts = ["I love the weather today (just now)"]
    assert posts == expected_posts, "Post should be visible in user's timeline"


def test_social_network_add_post_nonexistent_user():
    """Checks that posting for a nonexistent user raises ValueError."""
    social_network = SocialNetwork()
    with pytest.raises(ValueError, match="User Alice does not exist"):
        social_network.add_post("Alice", "I love the weather today")


def test_social_network_get_user_timeline_nonexistent_user():
    """Checks that users can get their timeline."""
    social_network = SocialNetwork()
    social_network.add_user("Alice")
    social_network.add_post("Alice", "I love the weather today")

    with pytest.raises(ValueError, match="User Bob does not exist"):
        social_network.get_user_timeline("Bob")


def test_social_network_get_user_wall_nonexistent_user():
    """Checks that users can get their wall."""
    social_network = SocialNetwork()
    social_network.add_user("Alice")
    social_network.add_post("Alice", "I love the weather today")

    with pytest.raises(ValueError, match="User Bob does not exist"):
        social_network.get_user_wall("Bob")


def test_social_network_follows():
    """Checks that users can follow other users."""
    social_network = SocialNetwork()
    social_network.add_user("Alice")
    social_network.add_user("Bob")
    social_network.follows("Alice", "Bob")

    following = social_network.get_following("Alice")
    expected_following = ["Bob"]
    assert following == expected_following, "User should follow the other user"


def test_social_network_follows_nonexistent_user():
    """Checks that following a nonexistent user raises ValueError."""
    social_network = SocialNetwork()
    with pytest.raises(ValueError, match="User Alice does not exist"):
        social_network.follows("Alice", "Bob")

    with pytest.raises(ValueError, match="User Bob does not exist"):
        social_network.add_user("Alice")
        social_network.follows("Alice", "Bob")

    with pytest.raises(ValueError, match="User Bob does not exist"):
        social_network.get_following("Bob")
