"""This module provides tests for the social networking application."""

from src.sr_sw_dev.social_networking import SocialNetwork


def test_social_networking_init():
    """Checks that a social network is initialized correctly."""
    social_network = SocialNetwork()
    assert not social_network.has_users(), "SocialNetwork should start with no users"