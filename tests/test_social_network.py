"""This module provides tests for the social networking application."""

from src.sr_sw_dev.social_networking import SocialNetwork


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
    assert social_network.count_users() == 1, "Adding duplicate user should not create new user"