"""This module provides tests for the Pydantic models."""

from pydantic import ValidationError
import pytest

from src.social_network.models import CommandModel, PostModel, UserModel
from src.social_network.social_networking import Application


# PostModel validation tests
def test_post_model_validation_content_too_long():
    """Checks that post content exceeding max length is rejected."""
    with pytest.raises(
        ValidationError, match="String should have at most 280 characters"
    ):
        PostModel(content="a" * 281, author="Alice")


def test_post_model_validation_author_invalid():
    """Checks that invalid author names are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        PostModel(content="Hello", author="Alice!")


def test_post_model_validation_author_empty():
    """Checks that empty author names are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        PostModel(content="Hello", author="")


# UserModel validation tests
def test_user_model_validation_name_invalid():
    """Checks that invalid user names are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        UserModel(name="Alice!")


def test_user_model_validation_name_empty():
    """Checks that empty user names are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        UserModel(name="")


def test_user_model_validation_following_self():
    """Checks that users cannot follow themselves."""
    with pytest.raises(ValidationError, match="User cannot follow themselves"):
        UserModel(name="Alice", following=["Alice"])


def test_user_model_validation_following_others():
    """Checks that users can follow other users."""
    # Test following a different user
    user = UserModel(name="Alice", following=["Bob"])
    assert user.following == ["Bob"]

    # Test following multiple users
    user = UserModel(name="Alice", following=["Bob", "Charlie"])
    assert user.following == ["Bob", "Charlie"]

    # Test following no users
    user = UserModel(name="Alice", following=[])
    assert user.following == []


# CommandModel validation tests
def test_command_model_validation_username_invalid():
    """Checks that invalid usernames are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        CommandModel(username="Alice!", action="post", target="Hello")


def test_command_model_validation_username_empty():
    """Checks that empty usernames are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        CommandModel(username="", action="post", target="Hello")


def test_command_model_validation_action_invalid():
    """Checks that invalid actions are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        CommandModel(username="Alice", action="reacts", target="Bob")


def test_command_model_validation_posting_missing_target():
    """Checks that posting commands without a target are rejected."""
    with pytest.raises(ValidationError, match="Target is required for action"):
        CommandModel(username="Alice", action="post", target=None)


def test_command_model_validation_following_missing_target():
    """Checks that following commands without a target are rejected."""
    with pytest.raises(ValidationError, match="Target is required for action"):
        CommandModel(username="Alice", action="follow", target=None)


def test_command_model_validation_wall_extra_target():
    """Checks that wall commands with an extra target are rejected."""
    with pytest.raises(
        ValidationError, match="Target should be None for wall/timeline action"
    ):
        CommandModel(username="Alice", action="wall", target="Bob")


def test_command_model_validation_posting_empty_user():
    """Checks that posting commands with an empty username are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        CommandModel(username="", action="post", target="Hello")


def test_command_model_validation_posting_empty_message():
    """Checks that posting commands with an empty message are rejected."""
    with pytest.raises(ValidationError, match="Target is required for action"):
        CommandModel(username="Alice", action="post", target=None)


def test_command_model_validation_following_empty_user():
    """Checks that following commands with an empty username are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        CommandModel(username="", action="follow", target="Bob")


def test_command_model_validation_following_empty_target():
    """Checks that following commands with an empty target are rejected."""
    with pytest.raises(ValidationError, match="Target is required for action"):
        CommandModel(username="Alice", action="follow", target=None)


def test_command_model_validation_wall_empty_user():
    """Checks that wall commands with an empty username are rejected."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        CommandModel(username="", action="wall", target=None)


def test_command_model_structure():
    """Checks that command models have the correct structure."""
    application = Application()

    # Test post command
    cmd = application.parse_command("Alice -> I love the weather today!")
    assert isinstance(cmd, CommandModel)
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "post",
        "target": "I love the weather today!",
    }

    # Test follow command
    cmd = application.parse_command("Alice follows Bob")
    assert isinstance(cmd, CommandModel)
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "follow",
        "target": "Bob",
    }

    # Test wall command
    cmd = application.parse_command("Alice wall")
    assert isinstance(cmd, CommandModel)
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "wall",
        "target": None,
    }

    # Test timeline command
    cmd = application.parse_command("Alice")
    assert isinstance(cmd, CommandModel)
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "timeline",
        "target": None,
    }


def test_command_model_whitespace():
    """Checks that command models handle whitespace correctly."""
    application = Application()

    # Test post command with extra whitespace
    cmd = application.parse_command("  Alice  ->  I love the weather today!  ")
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "post",
        "target": "I love the weather today!",
    }

    # Test follow command with extra whitespace
    cmd = application.parse_command("  Alice  follows  Bob  ")
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "follow",
        "target": "Bob",
    }

    # Test wall command with extra whitespace
    cmd = application.parse_command("  Alice  wall  ")
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "wall",
        "target": None,
    }

    # Test timeline command with extra whitespace
    cmd = application.parse_command("  Alice  ")
    assert cmd.model_dump() == {
        "username": "Alice",
        "action": "timeline",
        "target": None,
    }
