"""This module provides tests for the Application class."""

from src.sr_sw_dev.social_networking import Application


def test_application_init():
    """Checks that an application is initialized correctly."""
    application = Application()
    assert application.has_social_network(), "Application should have a social network"
    assert application.has_commands(), "Application should have commands to execute"

def test_application_parse_command():
    """Checks that an application can parse a command."""
    application = Application()
    application.parse_command("Alice -> I love the weather today!")
    
    assert application.get_social_network().get_user_posts("Alice") == ["I love the weather today! (just now)"], "Post should be visible in user's timeline"
