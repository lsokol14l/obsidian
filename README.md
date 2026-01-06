# Obsidian Vault Python Library

A Python library for working with Obsidian vaults, providing easy-to-use interfaces for reading, writing, and manipulating Obsidian markdown notes.

## Features

- 📝 Read and write Obsidian markdown files
- 🏷️ Parse and manage YAML frontmatter
- 🔗 Handle wiki-style links (`[[Note Name]]`)
- 🔍 Search notes by content or tags
- 📊 Find backlinks between notes
- 🗂️ Navigate vault structure

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from obsidian_vault import ObsidianVault

# Open an existing vault
vault = ObsidianVault("/path/to/your/vault")

# Get all notes
notes = vault.get_all_notes()
for note in notes:
    print(f"Note: {note.name}")

# Get a specific note
note = vault.get_note("My Note")
if note:
    print(f"Content: {note.body}")
    print(f"Frontmatter: {note.frontmatter}")

# Create a new note
new_note = vault.create_note(
    "New Note",
    content="This is my new note!",
    frontmatter={"tags": ["example", "tutorial"], "date": "2026-01-06"}
)

# Get wiki links from a note
links = note.get_wiki_links()
print(f"This note links to: {links}")

# Search for notes
results = vault.search_notes("important")
print(f"Found {len(results)} notes containing 'important'")

# Get notes by tag
tagged_notes = vault.get_notes_by_tag("example")
print(f"Found {len(tagged_notes)} notes with tag 'example'")
```

## Usage Examples

### Working with Notes

```python
from obsidian_vault import ObsidianVault, ObsidianNote

# Open a vault
vault = ObsidianVault("./my-vault")

# Get a note
note = vault.get_note("Daily Notes/2026-01-06")

# Access note properties
print(note.name)          # File name without extension
print(note.body)          # Content without frontmatter
print(note.frontmatter)   # Frontmatter as dictionary
print(note.content)       # Full content including frontmatter

# Modify frontmatter
note.update_frontmatter("status", "completed")
note.save()
```

### Managing Links

```python
# Get all links from a note
links = note.get_wiki_links()

# Get backlinks (notes that link to this note)
backlinks = note.get_backlinks(vault)
for backlink in backlinks:
    print(f"{backlink.name} links to {note.name}")
```

### Searching and Filtering

```python
# Search by content
results = vault.search_notes("project alpha")

# Filter by tags
notes = vault.get_notes_by_tag("work")

# Get all notes
all_notes = vault.get_all_notes()
```

## API Reference

### ObsidianVault

- `__init__(vault_path)`: Initialize a vault at the given path
- `get_note(note_name)`: Get a specific note by name
- `get_all_notes()`: Get all notes in the vault
- `create_note(note_name, content, frontmatter)`: Create a new note
- `delete_note(note_name)`: Delete a note
- `search_notes(query)`: Search notes by content
- `get_notes_by_tag(tag)`: Get notes with a specific tag

### ObsidianNote

- `name`: Note name (without extension)
- `content`: Full note content
- `frontmatter`: Frontmatter dictionary
- `body`: Content without frontmatter
- `load()`: Load note from file
- `save()`: Save note to file
- `get_wiki_links()`: Get all wiki-style links
- `get_backlinks(vault)`: Get notes linking to this note
- `update_frontmatter(key, value)`: Update frontmatter field

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
