"""
ObsidianVault class for working with Obsidian vaults.
"""

import os
from pathlib import Path
from typing import List, Optional
from .note import ObsidianNote


class ObsidianVault:
    """Represents an Obsidian vault (a directory containing markdown notes)."""
    
    def __init__(self, vault_path: str):
        """
        Initialize an ObsidianVault.
        
        Args:
            vault_path: Path to the vault directory
        """
        self.vault_path = os.path.abspath(vault_path)
        if not os.path.exists(self.vault_path):
            raise ValueError(f"Vault path does not exist: {self.vault_path}")
        if not os.path.isdir(self.vault_path):
            raise ValueError(f"Vault path is not a directory: {self.vault_path}")
    
    def get_note(self, note_name: str) -> Optional[ObsidianNote]:
        """
        Get a note by name.
        
        Args:
            note_name: Name of the note (with or without .md extension)
            
        Returns:
            ObsidianNote object or None if not found
        """
        if not note_name.endswith('.md'):
            note_name += '.md'
        
        # Search for the note in the vault
        for root, _, files in os.walk(self.vault_path):
            if note_name in files:
                note_path = os.path.join(root, note_name)
                note = ObsidianNote(note_path)
                note.load()
                return note
        
        return None
    
    def get_all_notes(self) -> List[ObsidianNote]:
        """
        Get all notes in the vault.
        
        Returns:
            List of ObsidianNote objects
        """
        notes = []
        for root, _, files in os.walk(self.vault_path):
            for file in files:
                if file.endswith('.md'):
                    note_path = os.path.join(root, file)
                    note = ObsidianNote(note_path)
                    note.load()
                    notes.append(note)
        return notes
    
    def create_note(self, note_name: str, content: str = "", 
                    frontmatter: Optional[dict] = None) -> ObsidianNote:
        """
        Create a new note in the vault.
        
        Args:
            note_name: Name of the note (with or without .md extension)
            content: Initial content for the note
            frontmatter: Optional frontmatter dictionary
            
        Returns:
            The created ObsidianNote object
        """
        if not note_name.endswith('.md'):
            note_name += '.md'
        
        note_path = os.path.join(self.vault_path, note_name)
        
        # Build content with frontmatter if provided
        if frontmatter:
            import yaml
            frontmatter_str = yaml.dump(frontmatter, default_flow_style=False)
            full_content = f"---\n{frontmatter_str}---\n{content}"
        else:
            full_content = content
        
        note = ObsidianNote(note_path, full_content)
        note.save()
        return note
    
    def delete_note(self, note_name: str) -> bool:
        """
        Delete a note from the vault.
        
        Args:
            note_name: Name of the note to delete
            
        Returns:
            True if deleted, False if not found
        """
        note = self.get_note(note_name)
        if note and os.path.exists(note.path):
            os.remove(note.path)
            return True
        return False
    
    def search_notes(self, query: str) -> List[ObsidianNote]:
        """
        Search for notes containing the query string.
        
        Args:
            query: Text to search for
            
        Returns:
            List of ObsidianNote objects containing the query
        """
        results = []
        for note in self.get_all_notes():
            if query.lower() in note.content.lower():
                results.append(note)
        return results
    
    def get_notes_by_tag(self, tag: str) -> List[ObsidianNote]:
        """
        Get all notes with a specific tag in frontmatter.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of ObsidianNote objects with the tag
        """
        results = []
        for note in self.get_all_notes():
            tags = note.frontmatter.get('tags', [])
            if isinstance(tags, list) and tag in tags:
                results.append(note)
            elif isinstance(tags, str) and tag == tags:
                results.append(note)
        return results
    
    def __repr__(self) -> str:
        return f"ObsidianVault(path='{self.vault_path}')"
