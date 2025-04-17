"""
This module provides a social networking application.

The application allows users to post messages to their own timeline.
"""
from datetime import datetime

class Post:
    """
    A post on a user's timeline.

    Attributes:
        content:
            The content of the post.
        timestamp:
            The timestamp of the post.
    """

    def __init__(self, content: str):
        """
        Initializes a post.

        Args:
            content:
                The content of the post.
        """
        self.content = content
        self.timestamp = datetime.now().replace(second=0, microsecond=0)

    def get_content(self) -> str:
        """Returns the content of the post."""
        return self.content

    def is_recent(self) -> bool:
        """Checks if the post is recent."""
        return (
            datetime.now().replace(second=0, microsecond=0) - self.timestamp
        ).total_seconds() <= 60
