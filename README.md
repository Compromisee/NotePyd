# QuickNote - Full Project Summary

## Overview

**QuickNote** is a single-file, self-contained Python desktop notepad application built with `tkinter`. It features Markdown editing, a password-protected lock screen, a global hotkey, tabbed editing, themes, folder organization, and many productivity features.

---

## File Structure

```
QuickNote (single file: quicknote.py / pythonnote.py / NotePyd.py)
│
├── Data stored at: ~/.quicknote_pro/
│   ├── data.json      ← All notes, folders, trash, favorites, recent
│   └── settings.json  ← Theme, font, tabs, password hash, preferences
│
└── Dependencies:
    ├── tkinter        (stdlib - built in)
    ├── pynput         (pip install pynput)    ← global hotkey
    └── markdown2      (pip install markdown2) ← HTML export
```

---

## Architecture

```
QuickNoteApp (main class)
│
├── DataManager          ← JSON persistence layer
├── MDHighlighter        ← Markdown syntax highlighting engine
├── HoverButton          ← Animated tk.Label button widget
├── ToolTip              ← Delayed popup tooltip widget
├── LineNumbers          ← Canvas-based line number gutter
└── THEMES dict          ← 8 complete color schemes
```

---

## Core Classes

### `DataManager`
Handles all data persistence and operations.

```python
# Location
~/.quicknote_pro/data.json
~/.quicknote_pro/settings.json

# Data structure
{
  "folders": {
    "<uuid>": {
      "name": str,
      "parent": uuid | None,
      "children": [uuid, ...],
      "notes": [uuid, ...],
      "color": hex_str,
      "expanded": bool
    }
  },
  "notes": {
    "<uuid>": {
      "title": str,
      "content": str,
      "folder": uuid,
      "created": iso_datetime,
      "modified": iso_datetime,
      "color": hex_str | None,
      "pinned": bool,
      "bookmarked": bool,
      "tags": [str, ...],
      "word_goal": int,
      "snapshots": [{"content": str, "ts": iso_datetime}, ...]
    }
  },
  "root_folder": uuid,
  "trash": [uuid, ...],
  "favorites": [uuid, ...],
  "recent": [uuid, ...]
}
```

**Methods:**
| Method | Description |
|--------|-------------|
| `create_note(title, folder, content, template)` | Create note, add to folder, add to recent |
| `update_note(nid, **kw)` | Update any note fields + set modified timestamp |
| `delete_note(nid)` | Move to trash, remove from folder/favorites/recent |
| `duplicate_note(nid)` | Copy note with "(copy)" suffix |
| `move_note(nid, new_fid)` | Move between folders |
| `restore_note(nid)` | Move from trash back to folder |
| `take_snapshot(nid)` | Save current content as version snapshot (max 50) |
| `search(q)` | Full-text search across title, content, tags |
| `get_stats(nid)` | Words, chars, lines, sentences, paragraphs, reading time |
| `create_folder(name, parent, color)` | Create nested folder |
| `delete_folder(fid)` | Recursively delete folder + contents to trash |
| `_add_recent(nid)` | Prepend to recent list, trim to limit |

---

### `MDHighlighter`
Live Markdown syntax highlighter using `tk.Text` tag system.

**Supported syntax:**
| Pattern | Tag | Effect |
|---------|-----|--------|
| `# H1` `## H2` `### H3` `#### H4` | `h1`-`h4` | Colored + larger bold font |
| `**bold**` `__bold__` | `bold` | Bold + accent color |
| `*italic*` `_italic_` | `ital` | Italic + italic color |
| `***bold italic***` | `bold_ital` | Bold italic combined |
| `` `code` `` | `code_i` | Monospace + code background |
| ` ``` ` fenced blocks | `code_b` / `fence` | Full line code background |
| `~~strike~~` | `strike` | Overstrike + muted color |
| `==highlight==` | `highlight` | Background highlight |
| `[link](url)` | `link` | Underlined + link color |
| `![img](url)` | `img` | Accent4 color |
| `https://...` | `url` | Link color |
| `> quote` | `quote` | Italic + code background + indent |
| `- item` `1. item` | `lst` | Accent colored marker |
| `- [ ]` / `- [x]` | `chk_undone` / `chk_done` | Error / success color |
| `---` `***` `___` | `hr` | Muted tiny font |
| `\|table\|` | `tbl` | Muted pipe characters |
| `cur_line` | active line | Subtle background highlight |

**Performance:** Highlights are debounced with `root.after(80, ...)` to avoid blocking on every keystroke.

---

### `HoverButton`
Animated button using `tk.Label` (Python 3.14 compatible).

```python
# Key fix: inherits tk.Label, NOT tk.Canvas or tk.Frame
# This avoids the Python 3.14 TypeError:
#   "unsupported operand type(s) for +: 'int' and 'str'"
#   in Widget._setup() when master._w is an int

class HoverButton(tk.Label):
    def _lerp(self, c1, c2, t):
        # Linear interpolate between two hex colors
        ...
    def _animate(self, target_bg, target_fg, step=0):
        # 6-step color animation via self.after(16, ...)
        # ~60fps smooth transition
        ...
```

**Animation:** Color lerp over 6 steps at 16ms intervals (~60fps). Uses `after()` so it's non-blocking.

---

### `LineNumbers`
Canvas that mirrors line positions from the editor.

```python
class LineNumbers(tk.Canvas):
    def redraw(self):
        # Uses text_widget.dlineinfo(index) to get pixel Y
        # positions of each line, draws text at exact positions
        # Handles wrapped lines correctly
```

---

## UI Structure

```
root (tk.Tk)
│
├── menubar (tk.Menu)
│   ├── File, Edit, Insert, View, Settings
│
├── main_frame (tk.Frame)
│   └── hpane (tk.PanedWindow, horizontal)
│       │
│       ├── sidebar (tk.Frame) ──────────────────────────────
│       │   ├── search bar (Entry in bordered Frame)
│       │   ├── buttons: Note | Folder | Template | Sort
│       │   ├── divider
│       │   └── ttk.Treeview (folders + notes tree)
│       │
│       └── right_pane (tk.Frame) ──────────────────────────
│           ├── tab_bar (tk.Frame, height=34)
│           │   ├── tab_container (tabs packed left)
│           │   └── new tab button (right)
│           ├── toolbar (tk.Frame, height=36, optional)
│           │   └── HoverButtons for markdown actions
│           ├── title_entry (tk.Entry, large bold)
│           ├── meta (tags entry + created date label)
│           ├── divider
│           └── editor_container (tk.Frame)
│               ├── line_nums (LineNumbers Canvas, optional)
│               ├── editor (tk.Text, main editing area)
│               └── scrollbar
│
└── statusbar (tk.Frame, height=24, bottom)
    ├── st_left   ← "Modified: Jan 01, 2025 12:00 PM"
    ├── st_theme  ← "Pastel Dark"
    ├── st_read   ← "~3 min read" or "Goal: 200/500 (40%)"
    ├── st_pos    ← "Ln 12, Col 4"
    └── st_right  ← "Words: 342 | Lines: 28 | Chars: 1840"
```

---

## Lock Screen

```
root
└── lock_frame (full screen)
    └── center (placed at relx=0.5, rely=0.42)
        ├── lock_canvas (animated lock icon, 80x80)
        │   └── _anim_lock() ← loops via after(50ms)
        │       └── math.sin(phase * 0.05) for shackle bob
        ├── APP title (serif font, 32pt bold)
        ├── subtitle (serif font, 12pt italic)
        ├── password entry (bordered Frame > Entry, show=●)
        ├── error label (red)
        └── HoverButton "Unlock"
    └── hint label ("Win+Shift+Q to toggle")
```

**Password:** SHA-256 hashed, stored in `settings.json`. Default: `1571127`.

---

## Tab System

```python
self._open_tabs = OrderedDict()  # nid -> tab_info dict
# tab_info = {
#   "frame": tk.Frame,
#   "label": tk.Label,
#   "close": tk.Label,
#   "accent": tk.Frame (2px colored bottom border)
# }
```

**Behavior:**
- Tabs restore from `settings["open_tabs"]` and `settings["active_tab"]` on launch
- `Ctrl+W` closes active tab
- `Ctrl+N` opens new tab
- Clicking X on tab closes it, switches to previous
- Active tab shows accent-colored bottom border
- Hover effects on both tab body and close button
- Title truncates at 20 characters + "..."

---

## Themes

8 complete themes, each with 30+ color keys:

| Theme | Style |
|-------|-------|
| **Pastel Dark** | Default. Soft dark with pastel purple/green/gold accents |
| **Pastel Light** | Warm cream/beige with muted pastels |
| **Blackboard** | Deep near-black with chalk-blue accents |
| **Whiteboard** | Clean white, subtle blue accents |
| **Midnight** | GitHub-dark inspired, pure blacks + blue |
| **Monokai** | Classic Sublime Text color scheme |
| **Nord** | Arctic blue-grey palette |
| **Solarized** | Ethan Schoonover's classic reduced-brightness scheme |

**Color keys per theme:**
```python
{
  "bg", "fg",
  "sidebar_bg", "sidebar_fg", "sidebar_hover", "sidebar_active",
  "editor_bg", "editor_fg",
  "accent", "accent2", "accent3", "accent4",
  "toolbar_bg", "toolbar_fg", "toolbar_hover",
  "select_bg", "select_fg", "border",
  "heading_color", "bold_color", "italic_color",
  "code_bg", "code_fg", "link_color",
  "button_bg", "button_fg", "button_active",
  "line_num_fg", "cursor_color",
  "statusbar_bg", "statusbar_fg",
  "popup_bg", "popup_fg",
  "error", "warning", "success",
  "muted", "divider",
  "input_bg", "input_fg", "input_border"
}
```

---

## Note Templates

| Template | Content |
|----------|---------|
| Blank | Empty |
| Meeting Notes | Date, attendees, agenda, discussion, action items |
| To-Do List | High/medium/low priority + done section |
| Journal | Thoughts, grateful for, tomorrow goals |
| Project Plan | Overview, milestones, deadline |
| Code Snippet | Language, code block, notes |
| Weekly Review | Accomplishments, challenges, next week |

All templates replace `{date}` with `datetime.now().strftime("%Y-%m-%d")`.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Win+Shift+Q` | Toggle app visibility (global, works outside app) |
| `Ctrl+N` | New note / new tab |
| `Ctrl+W` | Close current tab |
| `Ctrl+S` | Save current note |
| `Ctrl+L` | Lock app |
| `Ctrl+F` | Find & Replace |
| `Ctrl+B` | Bold `**text**` |
| `Ctrl+I` | Italic `*text*` |
| `Ctrl+P` | Markdown preview |
| `Ctrl+=` / `Ctrl++` | Increase font size |
| `Ctrl+-` | Decrease font size |
| `Ctrl+Shift+F` | New folder |
| `Ctrl+Shift+S` | Note statistics |
| `Escape` | Exit focus mode |
| `Tab` | Insert N spaces (configurable tab size) |
| `Return` | Smart auto-indent / continue lists |
| `Backspace` | Smart de-indent on aligned spaces |

---

## Smart Editor Features

### Auto-indent
```
- List item       →  Return  →  - 
1. Numbered       →  Return  →  2. 
  indented line   →  Return  →    (same indent)
- [x] Done list   →  Return  →  - [ ] (new checkbox)
empty list marker →  Return  →  (removes marker, newline)
```

### Auto-bracket
Typing `(`, `[`, `{`, `"`, `'` inserts the closing character and places cursor between them. If text is selected, wraps the selection.

### Smart Backspace
If cursor is at a multiple-of-tab-size column and the preceding characters are all spaces, deletes one full tab-width.

---

## Features Index

### Writing
- [x] Markdown live syntax highlighting
- [x] 18 monospace font choices
- [x] Serif fonts on lock screen (Georgia, Palatino, etc.)
- [x] Configurable font size (8-32pt)
- [x] Word wrap toggle
- [x] Line numbers (toggleable)
- [x] Current line highlight
- [x] Tab size configuration (2-8 spaces)
- [x] Undo/redo (unlimited, native tk.Text)
- [x] Auto-indent
- [x] Smart list continuation
- [x] Auto-bracket pairing
- [x] Smart backspace de-indent

### Organization
- [x] Nested folder hierarchy (unlimited depth)
- [x] Folder colors
- [x] Note pinning (shown first in sidebar)
- [x] Note bookmarking
- [x] Favorites list
- [x] Recent notes list (configurable limit, default 25)
- [x] Tag system (comma-separated, saved on Enter)
- [x] Sort notes by name / modified / created
- [x] Move notes between folders

### Tabs
- [x] Multi-tab editing
- [x] Tab session memory (restored on relaunch)
- [x] Active tab memory
- [x] Hover effects on tabs
- [x] Accent underline on active tab
- [x] Close button with red hover
- [x] Title truncation at 20 chars

### Productivity
- [x] 7 note templates
- [x] Version history (auto snapshots every N edits, max 50)
- [x] Snapshot restore
- [x] Word goal with progress bar in stats + status bar
- [x] Note statistics (words, chars, lines, sentences, paragraphs, reading time)
- [x] Configurable reading speed (WPM)
- [x] Find & Replace with regex mode + case sensitivity
- [x] Sort lines
- [x] Remove duplicate lines
- [x] Trim trailing whitespace
- [x] Duplicate note
- [x] Markdown preview window
- [x] Focus mode (hides all UI except editor)
- [x] Auto-save (configurable interval, default 3s)

### Import / Export
- [x] Export as `.md` (raw markdown)
- [x] Export as themed `.html` (full CSS matching current theme)
- [x] Import `.md` / `.txt` files

### Security
- [x] Password lock screen with animated icon
- [x] SHA-256 password hashing
- [x] Password change dialog (requires current password)
- [x] Auto-lock on `Ctrl+L`
- [x] Locked state persists across restarts

### UI/UX
- [x] 8 color themes
- [x] Animated fade-in on launch
- [x] Animated lock icon (sine wave bobbing shackle)
- [x] Smooth color-lerp hover animations on all buttons
- [x] Delayed tooltips on all toolbar buttons
- [x] Dark title bar on Windows (DWM API)
- [x] Context menus on right-click in sidebar
- [x] Folder expand/collapse on double-click
- [x] Full-text search with live results
- [x] Status bar (position, word count, reading time, theme)

---

## Settings Reference

All stored in `~/.quicknote_pro/settings.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `theme` | `"Pastel Dark"` | Active theme name |
| `font_family` | `"Consolas"` | Editor font |
| `font_size` | `13` | Editor font size in pt |
| `geometry` | `"1300x800"` | Window size/position |
| `auto_save` | `true` | Enable auto-save |
| `auto_save_ms` | `3000` | Auto-save interval in ms |
| `line_numbers` | `true` | Show line number gutter |
| `word_wrap` | `true` | Word wrap in editor |
| `password_hash` | SHA-256 of "1571127" | Hashed password |
| `locked` | `true` | Show lock screen on open |
| `last_note` | `null` | Last opened note UUID |
| `show_toolbar` | `true` | Show formatting toolbar |
| `show_statusbar` | `true` | Show status bar |
| `tab_size` | `4` | Spaces per tab press |
| `highlight_line` | `true` | Highlight current line |
| `auto_bracket` | `true` | Auto-close brackets |
| `auto_indent` | `true` | Smart indent on Return |
| `reading_wpm` | `200` | Words per minute for reading time |
| `sidebar_sort` | `"name"` | Sort: name/modified/created |
| `snap_interval` | `30` | Edits between auto-snapshots |
| `open_tabs` | `[]` | UUIDs of open tabs (session) |
| `active_tab` | `null` | UUID of active tab (session) |
| `sidebar_width` | `260` | Sidebar width in px |
| `recent_limit` | `25` | Max recent notes to track |

---

## Known Python 3.14 Compatibility Notes

Python 3.14 changed how tkinter widget internal paths (`_w`) are resolved. The symptom is:

```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Fixes applied:**
1. `HoverButton` uses `tk.Label` as base class instead of `tk.Canvas` or `tk.Frame`
2. `LineNumbers` calls `self.configure(width=50)` after `super().__init__()` instead of passing `width=` to constructor
3. All `tk.Frame` subclasses avoid positional arguments that could be misinterpreted as widget names
4. `tk.Canvas` in lock screen is created with `configure()` calls after init

---

## Installation & Running

```bash
# Install optional dependencies
pip install pynput markdown2

# Run
python quicknote.py

# Default password
1571127

# Global hotkey (toggle app from anywhere)
Win + Shift + Q
```

---

## Data Location

| OS | Path |
|----|------|
| Windows | `C:\Users\<user>\.quicknote_pro\` |
| macOS | `/Users/<user>/.quicknote_pro/` |
| Linux | `/home/<user>/.quicknote_pro/` |

---

## Dependency Summary

| Library | Purpose | Required? | Install |
|---------|---------|-----------|---------|
| `tkinter` | All UI | Yes (stdlib) | Built-in |
| `json` | Data persistence | Yes (stdlib) | Built-in |
| `hashlib` | Password hashing | Yes (stdlib) | Built-in |
| `re` | Markdown regex | Yes (stdlib) | Built-in |
| `uuid` | Note/folder IDs | Yes (stdlib) | Built-in |
| `math` | Lock animation | Yes (stdlib) | Built-in |
| `datetime` | Timestamps | Yes (stdlib) | Built-in |
| `pathlib` | Data dir path | Yes (stdlib) | Built-in |
| `collections` | `OrderedDict` for tabs | Yes (stdlib) | Built-in |
| `pynput` | Global hotkey | Optional | `pip install pynput` |
| `markdown2` | HTML export | Optional | `pip install markdown2` |
