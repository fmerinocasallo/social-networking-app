"""Pydantic models for data validation."""

from datetime import datetime

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PostModel(BaseModel):
    """A post on a user's timeline.

    Attributes:
        content: The content of the post.
        timestamp: The timestamp of the post.
        author: The author of the post.
    """

    content: str = Field(
        ...,
        min_length=1,
        max_length=280,
        json_schema_extra={"strip_whitespace": True},
        description="The content of the post",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0),
        description="The timestamp of the post",
    )
    author: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="The author of the post",
    )


class UserModel(BaseModel):
    """A user of the social network.

    Attributes:
        name: The name of the user.
        posts: The posts of the user.
        following: The users that the user is following.
    """

    name: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="The name of the user",
    )
    posts: list[PostModel] = Field(
        default_factory=list,
        description="The posts of the user",
    )
    following: list[str] = Field(
        default_factory=list,
        description="The users that the user is following",
    )

    @field_validator("following")
    @classmethod
    def validate_following(cls, v: list[str], info: ValidationInfo) -> list[str]:
        """Validate the following list.

        Args:
            v: The following list to validate.
            info: The validation info.

        Returns:
            The validated following list.

        Raises:
            ValueError: If the following list is invalid.
        """
        if "name" in info.data and info.data["name"] in v:
            raise ValueError("User cannot follow themselves")
        else:
            return v


class CommandModel(BaseModel):
    """A command to the social network.

    Attributes:
        username: The username of the command.
        action: The action of the command.
        target: The target of the command.
    """

    username: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="The username of the command",
    )
    action: str = Field(
        ...,
        pattern=r"^(post|follow|wall|timeline)$",
        description="The action of the command",
    )
    target: str | None = Field(
        None,
        description="The target of the command",
    )

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str | None, info: ValidationInfo) -> str | None:
        """Validate the target of the command.

        Args:
            v: The target to validate.
            info: The validation info.

        Returns:
            The validated target.

        Raises:
            ValueError: If the target is invalid.
        """
        if "action" in info.data:
            if info.data["action"] in ["post", "follow"] and not v:
                raise ValueError(f"Target is required for action {info.data['action']}")
            elif info.data["action"] in ["wall", "timeline"] and v:
                raise ValueError("Target should be None for wall/timeline action")
            else:
                return v
        else:
            return v
