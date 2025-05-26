"""This module provides tests for the CommandProcessor class."""

from datetime import datetime, timedelta

from freezegun import freeze_time
import pytest

from src.sr_sw_dev.models import CommandModel
from src.sr_sw_dev.social_networking import CommandProcessor, SocialNetwork


def test_command_processor_init():
    """Checks that a command processor is initialized correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)
    assert processor.get_social_network() == social_network


def test_command_processor_parse_post_command():
    """Checks that post commands are parsed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    command = "Alice -> I love the weather today!"
    parsed = processor.parse_command(command)

    assert isinstance(parsed, CommandModel)
    assert parsed.model_dump() == {
        "username": "Alice",
        "action": "post",
        "target": "I love the weather today!",
    }


def test_command_processor_parse_follow_command():
    """Checks that follow commands are parsed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    command = "Alice follows Bob"
    parsed = processor.parse_command(command)

    assert isinstance(parsed, CommandModel)
    assert parsed.model_dump() == {
        "username": "Alice",
        "action": "follow",
        "target": "Bob",
    }


def test_command_processor_parse_wall_command():
    """Checks that wall commands are parsed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    command = "Alice wall"
    parsed = processor.parse_command(command)

    assert isinstance(parsed, CommandModel)
    assert parsed.model_dump() == {
        "username": "Alice",
        "action": "wall",
        "target": None,
    }


def test_command_processor_parse_timeline_command():
    """Checks that timeline commands are parsed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    command = "Alice"
    parsed = processor.parse_command(command)

    assert isinstance(parsed, CommandModel)
    assert parsed.model_dump() == {
        "username": "Alice",
        "action": "timeline",
        "target": None,
    }


def test_command_processor_execute_post_command():
    """Checks that post commands are executed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    with freeze_time(datetime.now() - timedelta(minutes=2)):
        command = "Alice -> I love the weather today!"
        processor.execute_command(command)

    timeline = processor.get_social_network().get_user_timeline("Alice")
    assert timeline == ["I love the weather today! (2 minutes ago)"]


def test_command_processor_execute_follow_command():
    """Checks that follow commands are executed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    # Create users and posts
    processor.execute_command("Alice -> I love the weather today!")
    processor.execute_command("Bob -> Damn! We lost!")

    # Execute follow command
    processor.execute_command("Alice follows Bob")

    following = processor.get_social_network().get_following("Alice")
    assert following == ["Bob"]


def test_command_processor_execute_wall_command():
    """Checks that wall commands are executed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    # Create users and posts
    with freeze_time(datetime.now() - timedelta(minutes=5)):
        processor.execute_command("Alice -> I love the weather today!")

    with freeze_time(datetime.now() - timedelta(minutes=2)):
        processor.execute_command("Bob -> Damn! We lost!")

    processor.execute_command("Alice follows Bob")

    # Execute wall command
    wall = processor.execute_command("Alice wall")
    expected_wall = [
        "Bob - Damn! We lost! (2 minutes ago)",
        "Alice - I love the weather today! (5 minutes ago)",
    ]
    assert wall == expected_wall


def test_command_processor_execute_timeline_command():
    """Checks that timeline commands are executed correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    # Create post
    with freeze_time(datetime.now() - timedelta(minutes=8)):
        processor.execute_command("Alice -> I love the weather today!")

    # Execute timeline command
    timeline = processor.execute_command("Alice")
    assert timeline == ["I love the weather today! (8 minutes ago)"]


def test_command_processor_execute_nonexistent_user():
    """Checks that commands for nonexistent users are handled correctly."""
    social_network = SocialNetwork()
    processor = CommandProcessor(social_network)

    with pytest.raises(ValueError, match="Invalid user: user Alice does not exist"):
        processor.execute_command("Alice")
