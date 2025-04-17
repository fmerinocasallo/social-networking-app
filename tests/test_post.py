"""This module provides tests for the Post class."""

from src.sr_sw_dev.social_networking import Post


def test_post_init():
    """Checks that a post is initialized correctly."""
    content = "I love the weather today!"
    post = Post(content)
    assert post.get_content() == content, "Post should store the given content"
    assert post.is_recent(), "New post should be considered recent"

def test_post_eq():
    """Checks that two posts are equal if they have the same content and timestamp."""
    post1 = Post("I love the weather today!")
    post2 = Post("I love the weather today!")
    assert post1 == post2
