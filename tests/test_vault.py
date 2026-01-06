"""
Unit tests for ObsidianVault class.
"""

import unittest
import tempfile
import os
import shutil
from obsidian_vault import ObsidianVault, ObsidianNote


class TestObsidianVault(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_vault_creation(self):
        """Test creating a vault."""
        vault = ObsidianVault(self.test_dir)
        self.assertEqual(vault.vault_path, os.path.abspath(self.test_dir))
    
    def test_vault_invalid_path(self):
        """Test vault with invalid path."""
        with self.assertRaises(ValueError):
            ObsidianVault("/nonexistent/path")
    
    def test_create_note(self):
        """Test creating a note in the vault."""
        vault = ObsidianVault(self.test_dir)
        note = vault.create_note("Test Note", "Test content")
        
        self.assertIsInstance(note, ObsidianNote)
        self.assertEqual(note.name, "Test Note")
        self.assertTrue(os.path.exists(note.path))
    
    def test_get_note(self):
        """Test retrieving a note by name."""
        vault = ObsidianVault(self.test_dir)
        vault.create_note("My Note", "Content here")
        
        note = vault.get_note("My Note")
        self.assertIsNotNone(note)
        self.assertEqual(note.name, "My Note")
    
    def test_get_all_notes(self):
        """Test getting all notes in vault."""
        vault = ObsidianVault(self.test_dir)
        vault.create_note("Note 1", "Content 1")
        vault.create_note("Note 2", "Content 2")
        vault.create_note("Note 3", "Content 3")
        
        notes = vault.get_all_notes()
        self.assertEqual(len(notes), 3)
    
    def test_delete_note(self):
        """Test deleting a note."""
        vault = ObsidianVault(self.test_dir)
        note = vault.create_note("To Delete", "Content")
        note_path = note.path
        
        result = vault.delete_note("To Delete")
        self.assertTrue(result)
        self.assertFalse(os.path.exists(note_path))
    
    def test_search_notes(self):
        """Test searching notes by content."""
        vault = ObsidianVault(self.test_dir)
        vault.create_note("Note 1", "This contains the keyword important")
        vault.create_note("Note 2", "This is just regular content")
        vault.create_note("Note 3", "Another important note")
        
        results = vault.search_notes("important")
        self.assertEqual(len(results), 2)
    
    def test_get_notes_by_tag(self):
        """Test filtering notes by tag."""
        vault = ObsidianVault(self.test_dir)
        vault.create_note("Note 1", "Content", {"tags": ["work", "project"]})
        vault.create_note("Note 2", "Content", {"tags": ["personal"]})
        vault.create_note("Note 3", "Content", {"tags": ["work"]})
        
        work_notes = vault.get_notes_by_tag("work")
        self.assertEqual(len(work_notes), 2)
    
    def test_create_note_with_frontmatter(self):
        """Test creating a note with frontmatter."""
        vault = ObsidianVault(self.test_dir)
        frontmatter = {
            "title": "My Title",
            "tags": ["test", "example"],
            "date": "2026-01-06"
        }
        note = vault.create_note("Frontmatter Note", "Body content", frontmatter)
        
        # Reload the note to verify it was saved correctly
        loaded_note = vault.get_note("Frontmatter Note")
        self.assertEqual(loaded_note.frontmatter.get("title"), "My Title")
        self.assertIn("test", loaded_note.frontmatter.get("tags", []))


if __name__ == '__main__':
    unittest.main()
