"""This module provides tests for the Application class."""

from datetime import datetime, timedelta

from freezegun import freeze_time
import pytest

from src.sr_sw_dev.social_networking import Application


def test_application_init():
    """Checks that an application is initialized correctly."""
    application = Application()
    assert application.has_social_network(), "Application should have a social network"
    assert application.has_commands(), "Application should have commands to execute"

def test_application_parse_command_posting():
    """Checks that an application can parse postings."""
    application = Application()
    application.parse_command("Alice -> I love the weather today!")
    
    posts = application.get_social_network().get_user_timeline("Alice")
    expected_posts = ["I love the weather today! (just now)"]
    assert posts == expected_posts, "Post should be visible in user's timeline"

def test_application_parse_command_posting_empty_user():
    """Checks that an application can parse postings with an empty user."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid posting command: username is empty"):
        application.parse_command("-> I love the weather today!")

def test_application_parse_command_posting_empty_message():
    """Checks that an application can parse postings with an empty message."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid posting command: message is empty"):
        application.parse_command("Alice ->")

def test_application_parse_command_reading():
    """Checks that an application can parse readings."""
    application = Application()

    with freeze_time(datetime.now() - timedelta(minutes=5)):
        application.parse_command("Alice -> I love the weather today!")

    with freeze_time(datetime.now() - timedelta(minutes=2)):
        application.parse_command("Bob -> Damn! We lost!")

    with freeze_time(datetime.now() - timedelta(minutes=1)):
        application.parse_command("Bob -> Good game though.")

    timeline = application.parse_command("Alice")
    expected_timeline = ["I love the weather today! (5 minutes ago)"]
    assert timeline == expected_timeline, "Timeline should contain Alice's post"

    timeline = application.parse_command("Bob")
    expected_timeline = [
        "Good game though. (1 minute ago)",
        "Damn! We lost! (2 minutes ago)",
    ]
    assert timeline == expected_timeline, "Timeline should contain Bob's posts"

def test_application_parse_command_reading_nonexistent_user():
    """Checks that an application can parse readings with a nonexistent user."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid user: Charlie"):
        application.parse_command("Charlie")

def test_application_parse_command_following():
    """Checks that an application can parse following commands."""
    application = Application()
    application.parse_command("Alice -> I love the weather today!")
    application.parse_command("Charlie -> I'm in New York today! Anyone want to have a coffee?")
    application.parse_command("Charlie follows Alice")

    following = application.get_social_network().get_following("Charlie")
    expected_following = ["Alice"]
    assert following == expected_following, "Charlie should follow Alice"

def test_application_parse_command_following_nonexistent_user():
    """Checks that an application can parse following commands with a nonexistent user."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid following command: username is empty"):
        application.parse_command("follows Alice")

    with pytest.raises(ValueError, match="Invalid following command: user to follow is empty"):
        application.parse_command("Charlie follows ")

def test_application_parse_command_wall():
    """Checks that an application can parse wall commands."""
    application = Application()

    with freeze_time(datetime.now() - timedelta(minutes=5)):
        application.parse_command("Alice -> I love the weather today!")

    with freeze_time(datetime.now() - timedelta(minutes=2)):
        application.parse_command("Bob -> Damn! We lost!")

    with freeze_time(datetime.now() - timedelta(minutes=1)):
        application.parse_command("Bob -> Good game though.")

    with freeze_time(datetime.now() - timedelta(seconds=2)):
        application.parse_command("Charlie -> I'm in New York today! Anyone want to have a coffee?")
        application.parse_command("Charlie follows Alice")

    wall = application.parse_command("Charlie wall")
    expected_wall = [
        "Charlie - I'm in New York today! Anyone want to have a coffee? (2 seconds ago)",
        "Alice - I love the weather today! (5 minutes ago)",
    ]

    assert wall == expected_wall, "Charlie's wall should contain Alice's and his own posts"

    with freeze_time(datetime.now() + timedelta(seconds=13)):
        application.parse_command("Charlie follows Bob")
        wall = application.parse_command("Charlie wall")

        expected_wall = [
            "Charlie - I'm in New York today! Anyone want to have a coffee? (15 seconds ago)",
            "Bob - Good game though. (1 minute ago)",
            "Bob - Damn! We lost! (2 minutes ago)",
            "Alice - I love the weather today! (5 minutes ago)",
        ]
        assert wall == expected_wall, "Charlie's wall should contain Alice's, Bob's and his own posts"

def test_application_parse_command_wall_nonexistent_user():
    """Checks that an application can parse wall commands with a nonexistent user."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid wall command: username is empty"):
        application.parse_command("wall")

def test_application_parse_command_invalid_command():
    """Checks that an application can parse a command with an invalid command."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid command: Alice reacts"):
        application.parse_command("Alice reacts")
