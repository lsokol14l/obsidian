"""
Obsidian Vault Python Library

A Python library for working with Obsidian vaults, including reading and writing
markdown files, parsing frontmatter, and handling wiki-links.
"""

from .vault import ObsidianVault
from .note import ObsidianNote

__version__ = "0.1.0"
__all__ = ["ObsidianVault", "ObsidianNote"]
