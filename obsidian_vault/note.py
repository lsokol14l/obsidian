"""
ObsidianNote class for representing individual notes in an Obsidian vault.
"""

import os
import re
from typing import Dict, List, Optional
import yaml


class ObsidianNote:
    """Represents a single note in an Obsidian vault."""
    
    def __init__(self, path: str, content: Optional[str] = None):
        """
        Initialize an ObsidianNote.
        
        Args:
            path: Path to the note file
            content: Optional content to initialize the note with
        """
        self.path = path
        self._content = content
        self._frontmatter: Optional[Dict] = None
        self._body: Optional[str] = None
        
        if content is not None:
            self._parse_content()
    
    @property
    def name(self) -> str:
        """Get the note name (filename without extension)."""
        return os.path.splitext(os.path.basename(self.path))[0]
    
    @property
    def content(self) -> str:
        """Get the full content of the note."""
        if self._content is None:
            self.load()
        return self._content or ""
    
    @content.setter
    def content(self, value: str):
        """Set the content and re-parse."""
        self._content = value
        self._parse_content()
    
    @property
    def frontmatter(self) -> Dict:
        """Get the YAML frontmatter as a dictionary."""
        if self._frontmatter is None and self._content is not None:
            self._parse_content()
        return self._frontmatter or {}
    
    @property
    def body(self) -> str:
        """Get the note body (content without frontmatter)."""
        if self._body is None and self._content is not None:
            self._parse_content()
        return self._body or ""
    
    def _parse_content(self):
        """Parse the content to extract frontmatter and body."""
        if not self._content:
            self._frontmatter = {}
            self._body = ""
            return
        
        # Check for YAML frontmatter
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(frontmatter_pattern, self._content, re.DOTALL)
        
        if match:
            try:
                self._frontmatter = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                self._frontmatter = {}
            self._body = match.group(2)
        else:
            self._frontmatter = {}
            self._body = self._content
    
    def load(self):
        """Load the note content from file."""
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                self._content = f.read()
            self._parse_content()
        else:
            self._content = ""
            self._frontmatter = {}
            self._body = ""
    
    def save(self):
        """Save the note to file."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(self._build_content())
    
    def _build_content(self) -> str:
        """Build the full content from frontmatter and body."""
        if self._frontmatter:
            frontmatter_str = yaml.dump(self._frontmatter, default_flow_style=False)
            return f"---\n{frontmatter_str}---\n{self._body or ''}"
        return self._body or ""
    
    def get_wiki_links(self) -> List[str]:
        """
        Extract all wiki-style links from the note.
        
        Returns:
            List of note names linked from this note
        """
        # Pattern matches [[Note Name]] and [[Note Name|Display Text]]
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        return re.findall(pattern, self.body)
    
    def get_backlinks(self, vault) -> List['ObsidianNote']:
        """
        Get all notes that link to this note.
        
        Args:
            vault: The ObsidianVault instance to search in
            
        Returns:
            List of ObsidianNote objects that link to this note
        """
        backlinks = []
        for note in vault.get_all_notes():
            if self.name in note.get_wiki_links():
                backlinks.append(note)
        return backlinks
    
    def update_frontmatter(self, key: str, value):
        """
        Update or add a frontmatter field.
        
        Args:
            key: The frontmatter key
            value: The value to set
        """
        if self._frontmatter is None:
            self._frontmatter = {}
        self._frontmatter[key] = value
    
    def __repr__(self) -> str:
        return f"ObsidianNote(name='{self.name}', path='{self.path}')"
