"""
Unit tests for ObsidianNote class.
"""

import unittest
import tempfile
import os
import shutil
from obsidian_vault import ObsidianNote


class TestObsidianNote(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_note.md")
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_note_creation(self):
        """Test creating a new note."""
        note = ObsidianNote(self.test_file, "Test content")
        self.assertEqual(note.name, "test_note")
        self.assertEqual(note.body, "Test content")
    
    def test_note_with_frontmatter(self):
        """Test note with YAML frontmatter."""
        content = """---
title: Test Note
tags:
  - test
  - example
---
This is the body."""
        
        note = ObsidianNote(self.test_file, content)
        self.assertEqual(note.frontmatter.get('title'), "Test Note")
        self.assertIn('test', note.frontmatter.get('tags', []))
        self.assertEqual(note.body.strip(), "This is the body.")
    
    def test_save_and_load(self):
        """Test saving and loading a note."""
        note = ObsidianNote(self.test_file, "Original content")
        note.save()
        
        # Create a new note object and load from file
        loaded_note = ObsidianNote(self.test_file)
        loaded_note.load()
        
        self.assertEqual(loaded_note.body, "Original content")
    
    def test_wiki_links(self):
        """Test extracting wiki links."""
        content = """This note links to [[Other Note]] and [[Another Note|with display text]].
        
Also links to [[Third Note]]."""
        
        note = ObsidianNote(self.test_file, content)
        links = note.get_wiki_links()
        
        self.assertEqual(len(links), 3)
        self.assertIn("Other Note", links)
        self.assertIn("Another Note", links)
        self.assertIn("Third Note", links)
    
    def test_update_frontmatter(self):
        """Test updating frontmatter."""
        note = ObsidianNote(self.test_file, "Content")
        note.update_frontmatter("status", "completed")
        
        self.assertEqual(note.frontmatter.get("status"), "completed")
    
    def test_empty_note(self):
        """Test handling empty notes."""
        note = ObsidianNote(self.test_file, "")
        self.assertEqual(note.body, "")
        self.assertEqual(note.frontmatter, {})


if __name__ == '__main__':
    unittest.main()
