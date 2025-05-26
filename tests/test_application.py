"""This module provides tests for the Application class."""

from datetime import datetime, timedelta
import io
import sys

from freezegun import freeze_time
from pydantic import ValidationError
import pytest
from pytest_mock import MockerFixture

from src.social_network.social_networking import Application


def test_application_init():
    """Checks that an application is initialized correctly."""
    application = Application()
    assert application.has_social_network(), "Application should have a social network"


def test_application_parse_command_posting():
    """Checks that an application can parse postings."""
    application = Application()
    application.execute_command("Alice -> I love the weather today!")

    posts = application.get_social_network().get_user_timeline("Alice")
    expected_posts = ["I love the weather today! (just now)"]
    assert posts == expected_posts, "Post should be visible in user's timeline"


def test_application_parse_command_reading():
    """Checks that an application can parse readings."""
    application = Application()

    with freeze_time(datetime.now() - timedelta(minutes=5)):
        application.execute_command("Alice -> I love the weather today!")

    with freeze_time(datetime.now() - timedelta(minutes=2)):
        application.execute_command("Bob -> Damn! We lost!")

    with freeze_time(datetime.now() - timedelta(minutes=1)):
        application.execute_command("Bob -> Good game though.")

    timeline = application.execute_command("Alice")
    expected_timeline = ["I love the weather today! (5 minutes ago)"]
    assert timeline == expected_timeline, "Timeline should contain Alice's post"

    timeline = application.execute_command("Bob")
    expected_timeline = [
        "Good game though. (1 minute ago)",
        "Damn! We lost! (2 minutes ago)",
    ]
    assert timeline == expected_timeline, "Timeline should contain Bob's posts"


def test_application_parse_command_reading_nonexistent_user():
    """Checks that an application can parse readings with a nonexistent user."""
    application = Application()

    with pytest.raises(ValueError, match="Invalid user: user Charlie does not exist"):
        application.execute_command("Charlie")


def test_application_parse_command_following():
    """Checks that an application can parse following commands."""
    application = Application()
    application.execute_command("Alice -> I love the weather today!")
    application.execute_command(
        "Charlie -> I'm in New York today! Anyone want to have a coffee?"
    )
    application.execute_command("Charlie follows Alice")

    following = application.get_social_network().get_following("Charlie")
    expected_following = ["Alice"]
    assert following == expected_following, "Charlie should follow Alice"


def test_application_parse_command_wall():
    """Checks that an application can parse wall commands."""
    application = Application()

    with freeze_time(datetime.now() - timedelta(minutes=5)):
        application.execute_command("Alice -> I love the weather today!")

    with freeze_time(datetime.now() - timedelta(minutes=2)):
        application.execute_command("Bob -> Damn! We lost!")

    with freeze_time(datetime.now() - timedelta(minutes=1)):
        application.execute_command("Bob -> Good game though.")

    with freeze_time(datetime.now() - timedelta(seconds=2)):
        application.execute_command(
            "Charlie -> I'm in New York today! Anyone want to have a coffee?"
        )
        application.execute_command("Charlie follows Alice")

    wall = application.execute_command("Charlie wall")
    expected_wall = [
        "Charlie - I'm in New York today! Anyone want to have a coffee? (2 seconds ago)",
        "Alice - I love the weather today! (5 minutes ago)",
    ]

    assert wall == expected_wall, (
        "Charlie's wall should contain Alice's and his own posts"
    )

    with freeze_time(datetime.now() + timedelta(seconds=13)):
        application.execute_command("Charlie follows Bob")
        wall = application.execute_command("Charlie wall")

        expected_wall = [
            "Charlie - I'm in New York today! Anyone want to have a coffee? (15 seconds ago)",
            "Bob - Good game though. (1 minute ago)",
            "Bob - Damn! We lost! (2 minutes ago)",
            "Alice - I love the weather today! (5 minutes ago)",
        ]
        assert wall == expected_wall, (
            "Charlie's wall should contain Alice's, Bob's and his own posts"
        )


def test_application_execute_invalid_command():
    """Checks that executing an invalid command raises a validation error."""
    application = Application()

    with pytest.raises(ValidationError, match="String should match pattern"):
        application.execute_command("invalid command")


def test_application_execute_empty_command():
    """Checks that executing an empty command raises a validation error."""
    application = Application()

    with pytest.raises(ValidationError, match="String should match pattern"):
        application.execute_command("")


def test_application_run_exit_command(mocker: MockerFixture) -> None:
    """Checks that the run method exits on 'exit' command."""
    app = Application()

    # Simulate user input
    mocker.patch("builtins.input", return_value="exit")

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Run the application
    app.run()

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that no output was produced
    assert captured_output.getvalue() == ""


def test_application_run_keyboard_interrupt(mocker: MockerFixture) -> None:
    """Checks that the run method exits on keyboard interrupt."""
    app = Application()

    # Simulate user input and keyboard interrupt
    mocker.patch("builtins.input", side_effect=KeyboardInterrupt)

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Run the application
    app.run()

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that "Exit" was printed
    assert captured_output.getvalue() == "Exit\n"


def test_application_run_eof_error(mocker: MockerFixture) -> None:
    """Checks that the run method exits on EOF error."""
    app = Application()

    # Simulate user input and EOF error
    mocker.patch("builtins.input", side_effect=EOFError)

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Run the application
    app.run()

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that "Exit" was printed
    assert captured_output.getvalue() == "Exit\n"


def test_application_run_command_execution(mocker: MockerFixture) -> None:
    """Checks that the run method executes commands correctly."""
    app = Application()

    # Simulate user input
    mocker.patch("builtins.input", side_effect=["Alice -> Hello!", "Alice", "exit"])

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Run the application
    app.run()

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that the command output was printed
    assert captured_output.getvalue() == "Hello! (just now)\n"


def test_application_run_invalid_command(mocker: MockerFixture) -> None:
    """Checks that the run method handles invalid commands correctly."""
    app = Application()

    # Simulate user input
    mocker.patch("builtins.input", side_effect=["invalid command", "exit"])

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Run the application
    app.run()

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that the error was printed
    assert "String should match pattern" in captured_output.getvalue()
