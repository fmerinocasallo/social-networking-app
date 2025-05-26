"""Paths for logs and config used by the social_networking package."""

from pathlib import Path

root = Path(__file__).parent.parent.parent

log_dir = root / "logs"
config_dir = root / "config"
