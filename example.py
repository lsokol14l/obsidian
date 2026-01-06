"""
Example script demonstrating how to use the Obsidian Vault library.
"""

from obsidian_vault import ObsidianVault
import os
import tempfile
import shutil


def main():
    # Create a temporary vault for demonstration
    temp_dir = tempfile.mkdtemp()
    vault_path = os.path.join(temp_dir, "demo-vault")
    os.makedirs(vault_path)
    
    print(f"Created temporary vault at: {vault_path}\n")
    
    try:
        # Initialize the vault
        vault = ObsidianVault(vault_path)
        print(f"✓ Initialized vault: {vault}\n")
        
        # Create some example notes
        print("Creating example notes...")
        
        # Note 1: A project note
        project_note = vault.create_note(
            "Project Alpha",
            content="""# Project Alpha

This is the main project documentation.

## Tasks
- [ ] Review requirements
- [ ] Design architecture
- [ ] Implementation

## Related Notes
- [[Team Meeting]]
- [[Technical Specs]]
""",
            frontmatter={
                "tags": ["project", "work"],
                "status": "in-progress",
                "created": "2026-01-06"
            }
        )
        print(f"  ✓ Created: {project_note.name}")
        
        # Note 2: A meeting note
        meeting_note = vault.create_note(
            "Team Meeting",
            content="""# Team Meeting

## Attendees
- Alice
- Bob
- Charlie

## Discussion
We discussed [[Project Alpha]] and decided to move forward.

## Action Items
- Review [[Technical Specs]]
""",
            frontmatter={
                "tags": ["meeting", "work"],
                "date": "2026-01-06"
            }
        )
        print(f"  ✓ Created: {meeting_note.name}")
        
        # Note 3: Technical specs
        specs_note = vault.create_note(
            "Technical Specs",
            content="""# Technical Specifications

Technical details for [[Project Alpha]].

## Architecture
- Frontend: React
- Backend: Python
- Database: PostgreSQL
""",
            frontmatter={
                "tags": ["technical", "work"],
                "version": "1.0"
            }
        )
        print(f"  ✓ Created: {specs_note.name}\n")
        
        # Demonstrate features
        print("=" * 50)
        print("DEMONSTRATION OF FEATURES")
        print("=" * 50 + "\n")
        
        # 1. List all notes
        print("1. All notes in vault:")
        all_notes = vault.get_all_notes()
        for note in all_notes:
            print(f"   - {note.name}")
        print()
        
        # 2. Get a specific note
        print("2. Getting 'Project Alpha' note:")
        note = vault.get_note("Project Alpha")
        print(f"   Name: {note.name}")
        print(f"   Tags: {note.frontmatter.get('tags', [])}")
        print(f"   Status: {note.frontmatter.get('status', 'N/A')}")
        print()
        
        # 3. Extract wiki links
        print("3. Wiki links in 'Project Alpha':")
        links = note.get_wiki_links()
        for link in links:
            print(f"   - [[{link}]]")
        print()
        
        # 4. Find backlinks
        print("4. Notes that link to 'Project Alpha':")
        backlinks = note.get_backlinks(vault)
        for backlink in backlinks:
            print(f"   - {backlink.name}")
        print()
        
        # 5. Search notes
        print("5. Search for notes containing 'review':")
        results = vault.search_notes("review")
        for result in results:
            print(f"   - {result.name}")
        print()
        
        # 6. Filter by tag
        print("6. Notes with 'work' tag:")
        work_notes = vault.get_notes_by_tag("work")
        for work_note in work_notes:
            print(f"   - {work_note.name}")
        print()
        
        # 7. Update a note
        print("7. Updating 'Project Alpha' status:")
        note.update_frontmatter("status", "completed")
        note.save()
        note.load()  # Reload to verify
        print(f"   New status: {note.frontmatter.get('status')}")
        print()
        
        print("=" * 50)
        print("Demo completed successfully!")
        print("=" * 50)
        
    finally:
        # Clean up temporary vault
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"\nCleaned up temporary vault: {temp_dir}")


if __name__ == "__main__":
    main()
