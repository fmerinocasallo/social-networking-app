"""This module provides tests for the Post class."""

from datetime import datetime

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from src.social_network.models import PostModel
from src.social_network.social_networking import Post


def test_post_init():
    """Checks that a post is initialized correctly."""
    content = "I love the weather today!"
    validated_post = PostModel(content=content, author="Alice")
    post = Post(validated_post)
    assert post.get_content() == content, "Post should store the given content"
    assert post.is_recent(), "New post should be considered recent"


def test_post_is_recent():
    """Checks that a post is recent if the timestamp is within the last minute."""
    validated_post = PostModel(content="I love the weather today!", author="Alice")
    post = Post(validated_post)
    assert post.is_recent(), "New post should be considered recent"
    with freeze_time(datetime.now() + relativedelta(minutes=5)):
        assert not post.is_recent(), (
            "Post should not be considered recent after more than 1 minute"
        )


def test_post_eq():
    """Checks that two posts are equal if they have the same content and timestamp."""
    validated_post1 = PostModel(content="I love the weather today!", author="Alice")
    validated_post2 = PostModel(content="I love the weather today!", author="Alice")
    post1 = Post(validated_post1)
    post2 = Post(validated_post2)
    assert post1 == post2


def test_post_lt():
    """Checks that a post is less than another post if it has an earlier timestamp."""
    with freeze_time(datetime.now() + relativedelta(seconds=5)):
        validated_post1 = PostModel(content="I love the weather today!", author="Alice")
        post1 = Post(validated_post1)

    with freeze_time(datetime.now() + relativedelta(seconds=10)):
        validated_post2 = PostModel(content="I love the weather today!", author="Alice")
        post2 = Post(validated_post2)
        assert post1 < post2


def test_post_str():
    """Checks that a post is converted to a string correctly."""
    post_model = PostModel(content="I love the weather today!", author="Alice")
    post = Post(post_model)
    assert str(post) == "I love the weather today! (just now)"

    with freeze_time(datetime.now() + relativedelta(seconds=5)):
        assert str(post) == "I love the weather today! (5 seconds ago)"

    with freeze_time(datetime.now() + relativedelta(minutes=5, seconds=15)):
        assert str(post) == "I love the weather today! (5 minutes ago)"

    with freeze_time(datetime.now() + relativedelta(hours=1, minutes=15)):
        assert str(post) == "I love the weather today! (1 hour ago)"

    with freeze_time(datetime.now() + relativedelta(days=15, hours=5, minutes=30)):
        assert str(post) == "I love the weather today! (15 days ago)"

    with freeze_time(datetime.now() + relativedelta(months=6, hours=12, minutes=45)):
        assert str(post) == "I love the weather today! (6 months ago)"

    with freeze_time(
        datetime.now() + relativedelta(years=5, months=9, days=15, minutes=15)
    ):
        assert str(post) == "I love the weather today! (5 years ago)"
