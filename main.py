#!/usr/bin/env python3
"""
QuickNote - Premium single-file notepad with Markdown, global hotkey, password lock.
pip install pynput markdown2
Default Password: 1571127 | Global Hotkey: Win+Shift+Q
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, simpledialog
import json
import os
import hashlib
import re
import uuid
import math
from datetime import datetime
from pathlib import Path
from collections import OrderedDict

try:
    from pynput import keyboard as pynput_kb
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False

try:
    import markdown2
    HAS_MD = True
except ImportError:
    HAS_MD = False


# ═══════════════════════════════════════════
# ICONS
# ═══════════════════════════════════════════

class I:
    NOTE = "\u2637"
    FOLDER = "\u25B9"
    FOLDER_OPEN = "\u25BF"
    ADD = "+"
    DELETE = "\u2715"
    SAVE = "\u2713"
    SEARCH = "\u2315"
    LOCK = "\u2588\u2588"
    PIN = "\u2605"
    UNPIN = "\u2606"
    GEAR = "\u2699"
    TRASH = "\u2672"
    EXPORT = "\u21E5"
    IMPORT = "\u21E4"
    BOLD = "B"
    ITALIC = "I"
    CODE = "</>"
    LINK = "\u2197"
    HEADING = "H"
    BULLET = "\u2022"
    NUM = "#"
    QUOTE = "\u201C"
    HRULE = "\u2500"
    CHECK = "\u2610"
    CHECK_DONE = "\u2611"
    UNDO = "\u21B6"
    REDO = "\u21B7"
    CUT = "\u2702"
    FIND = "\u2315"
    PREVIEW = "\u25A3"
    THEME = "\u25D0"
    CLOCK = "\u25F7"
    TAG = "\u2302"
    STAR = "\u2605"
    CLOSE = "\u2715"
    FOCUS = "\u25CE"
    STATS = "\u2261"
    TEMPLATE = "\u2756"
    HISTORY = "\u21BA"
    BOOKMARK = "\u2691"
    COLOR = "\u25C9"
    DUP = "\u2750"
    SORT = "\u21C5"
    TAB_CLOSE = "\u00D7"
    DOT = "\u25CF"
    RING = "\u25CB"
    FILLED = "\u25CF"


# ═══════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════

APP = "QuickNote"
DATA_DIR = os.path.join(str(Path.home()), ".quicknote_pro")
DATA_FILE = os.path.join(DATA_DIR, "data.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
PWD_HASH = hashlib.sha256("1571127".encode()).hexdigest()

FONT_FAMILIES = [
    "Consolas", "Cascadia Code", "Fira Code", "JetBrains Mono",
    "Source Code Pro", "Ubuntu Mono", "Inconsolata", "Monaco",
    "Courier New", "Menlo", "SF Mono", "Roboto Mono",
    "IBM Plex Mono", "Hack", "Droid Sans Mono",
    "DejaVu Sans Mono", "Liberation Mono", "Anonymous Pro",
]

SERIF_FONTS = [
    "Georgia", "Palatino Linotype", "Book Antiqua", "Garamond",
    "Times New Roman", "Cambria", "Didot", "Baskerville",
]


# ═══════════════════════════════════════════
# THEMES
# ═══════════════════════════════════════════

THEMES = {
    "Blackboard": {
        "bg": "#1a1a1d", "fg": "#d4d4d8",
        "sidebar_bg": "#111114", "sidebar_fg": "#8888a0",
        "sidebar_hover": "#222230", "sidebar_active": "#2a2a40",
        "editor_bg": "#1a1a1d", "editor_fg": "#e0e0e8",
        "accent": "#7c9cde", "accent2": "#de7c7c",
        "accent3": "#7cde9c", "accent4": "#deb87c",
        "toolbar_bg": "#0e0e11", "toolbar_fg": "#6a6a80",
        "toolbar_hover": "#1e1e28",
        "select_bg": "#2a4a7c", "select_fg": "#e4e4e7",
        "border": "#222230",
        "heading_color": "#7c9cde", "bold_color": "#deb87c",
        "italic_color": "#7cdeb8",
        "code_bg": "#222230", "code_fg": "#7cde9c",
        "link_color": "#7cbade",
        "button_bg": "#222230", "button_fg": "#d4d4d8",
        "button_active": "#2a2a40",
        "line_num_fg": "#2a2a40", "cursor_color": "#7c9cde",
        "statusbar_bg": "#0e0e11", "statusbar_fg": "#555570",
        "popup_bg": "#1e1e28", "popup_fg": "#d4d4d8",
        "error": "#de7c7c", "warning": "#deb87c", "success": "#7cde9c",
        "muted": "#3a3a4e", "divider": "#222230",
        "input_bg": "#1e1e28", "input_fg": "#e0e0e8",
        "input_border": "#2a2a40",
    },
    "Whiteboard": {
        "bg": "#fafafa", "fg": "#2d2d30",
        "sidebar_bg": "#f0f0f2", "sidebar_fg": "#5a5a60",
        "sidebar_hover": "#e4e4e8", "sidebar_active": "#d8d8dd",
        "editor_bg": "#ffffff", "editor_fg": "#1a1a1d",
        "accent": "#4a6fa5", "accent2": "#c25550",
        "accent3": "#3a8a4a", "accent4": "#b8860b",
        "toolbar_bg": "#eaeaee", "toolbar_fg": "#6a6a70",
        "toolbar_hover": "#dddde2",
        "select_bg": "#b0c8e8", "select_fg": "#1a1a1d",
        "border": "#d8d8dd",
        "heading_color": "#4a6fa5", "bold_color": "#b8860b",
        "italic_color": "#3a8a4a",
        "code_bg": "#f0f0f2", "code_fg": "#3a8a4a",
        "link_color": "#4a8fa5",
        "button_bg": "#e0e0e4", "button_fg": "#3a3a40",
        "button_active": "#d0d0d5",
        "line_num_fg": "#cdcdd2", "cursor_color": "#4a6fa5",
        "statusbar_bg": "#eaeaee", "statusbar_fg": "#9a9aa0",
        "popup_bg": "#ffffff", "popup_fg": "#2d2d30",
        "error": "#c25550", "warning": "#b8860b", "success": "#3a8a4a",
        "muted": "#b0b0b5", "divider": "#e0e0e4",
        "input_bg": "#ffffff", "input_fg": "#1a1a1d",
        "input_border": "#d0d0d5",
    },
    "Pastel Dark": {
        "bg": "#1c1c28", "fg": "#d8d8e8",
        "sidebar_bg": "#161620", "sidebar_fg": "#a0a0b8",
        "sidebar_hover": "#252535", "sidebar_active": "#303048",
        "editor_bg": "#1c1c28", "editor_fg": "#dadae8",
        "accent": "#a4b9ef", "accent2": "#f0a0a0",
        "accent3": "#b5e8b0", "accent4": "#f2d5a0",
        "toolbar_bg": "#121218", "toolbar_fg": "#707088",
        "toolbar_hover": "#1e1e2c",
        "select_bg": "#3a4a6e", "select_fg": "#dadae8",
        "border": "#252535",
        "heading_color": "#a4b9ef", "bold_color": "#f2d5a0",
        "italic_color": "#b5e8b0",
        "code_bg": "#222233", "code_fg": "#b5e8b0",
        "link_color": "#a4d5ef",
        "button_bg": "#252535", "button_fg": "#dadae8",
        "button_active": "#303048",
        "line_num_fg": "#303048", "cursor_color": "#a4b9ef",
        "statusbar_bg": "#121218", "statusbar_fg": "#5a5a70",
        "popup_bg": "#222233", "popup_fg": "#dadae8",
        "error": "#f0a0a0", "warning": "#f2d5a0", "success": "#b5e8b0",
        "muted": "#3a3a50", "divider": "#252535",
        "input_bg": "#222233", "input_fg": "#dadae8",
        "input_border": "#303048",
    },
    "Pastel Light": {
        "bg": "#fdf6f0", "fg": "#3d3535",
        "sidebar_bg": "#f5eee8", "sidebar_fg": "#6b5e5e",
        "sidebar_hover": "#ede4dc", "sidebar_active": "#e0d5cc",
        "editor_bg": "#fdf8f4", "editor_fg": "#3d3535",
        "accent": "#8faabe", "accent2": "#c2877a",
        "accent3": "#7aaa7a", "accent4": "#bea06a",
        "toolbar_bg": "#f2ebe4", "toolbar_fg": "#8a7a7a",
        "toolbar_hover": "#e8dfd8",
        "select_bg": "#c8d8e8", "select_fg": "#3d3535",
        "border": "#e0d5cc",
        "heading_color": "#6a8aa0", "bold_color": "#bea06a",
        "italic_color": "#7aaa7a",
        "code_bg": "#f0e8e0", "code_fg": "#7aaa7a",
        "link_color": "#6a8aaa",
        "button_bg": "#e8dfd8", "button_fg": "#5a4e4e",
        "button_active": "#ddd2c8",
        "line_num_fg": "#d0c5ba", "cursor_color": "#8faabe",
        "statusbar_bg": "#f2ebe4", "statusbar_fg": "#a09090",
        "popup_bg": "#fdf8f4", "popup_fg": "#3d3535",
        "error": "#c2877a", "warning": "#bea06a", "success": "#7aaa7a",
        "muted": "#b0a0a0", "divider": "#e0d5cc",
        "input_bg": "#fdf8f4", "input_fg": "#3d3535",
        "input_border": "#d0c5ba",
    },
    "Midnight": {
        "bg": "#0d1117", "fg": "#c9d1d9",
        "sidebar_bg": "#080c12", "sidebar_fg": "#8b949e",
        "sidebar_hover": "#161b22", "sidebar_active": "#1f2937",
        "editor_bg": "#0d1117", "editor_fg": "#e6edf3",
        "accent": "#58a6ff", "accent2": "#f85149",
        "accent3": "#3fb950", "accent4": "#d29922",
        "toolbar_bg": "#060a10", "toolbar_fg": "#6e7681",
        "toolbar_hover": "#111820",
        "select_bg": "#1f3d6f", "select_fg": "#e6edf3",
        "border": "#161b22",
        "heading_color": "#58a6ff", "bold_color": "#d29922",
        "italic_color": "#3fb950",
        "code_bg": "#161b22", "code_fg": "#3fb950",
        "link_color": "#58a6ff",
        "button_bg": "#161b22", "button_fg": "#c9d1d9",
        "button_active": "#1f2937",
        "line_num_fg": "#21262d", "cursor_color": "#58a6ff",
        "statusbar_bg": "#060a10", "statusbar_fg": "#484f58",
        "popup_bg": "#161b22", "popup_fg": "#c9d1d9",
        "error": "#f85149", "warning": "#d29922", "success": "#3fb950",
        "muted": "#30363d", "divider": "#161b22",
        "input_bg": "#161b22", "input_fg": "#e6edf3",
        "input_border": "#21262d",
    },
    "Monokai": {
        "bg": "#272822", "fg": "#f8f8f2",
        "sidebar_bg": "#1e1f1c", "sidebar_fg": "#b0b0a0",
        "sidebar_hover": "#3e3d32", "sidebar_active": "#49483e",
        "editor_bg": "#272822", "editor_fg": "#f8f8f2",
        "accent": "#66d9ef", "accent2": "#f92672",
        "accent3": "#a6e22e", "accent4": "#e6db74",
        "toolbar_bg": "#1e1f1c", "toolbar_fg": "#75715e",
        "toolbar_hover": "#333328",
        "select_bg": "#49483e", "select_fg": "#f8f8f2",
        "border": "#3e3d32",
        "heading_color": "#66d9ef", "bold_color": "#e6db74",
        "italic_color": "#a6e22e",
        "code_bg": "#3e3d32", "code_fg": "#a6e22e",
        "link_color": "#66d9ef",
        "button_bg": "#3e3d32", "button_fg": "#f8f8f2",
        "button_active": "#49483e",
        "line_num_fg": "#49483e", "cursor_color": "#f8f8f0",
        "statusbar_bg": "#1e1f1c", "statusbar_fg": "#75715e",
        "popup_bg": "#3e3d32", "popup_fg": "#f8f8f2",
        "error": "#f92672", "warning": "#e6db74", "success": "#a6e22e",
        "muted": "#75715e", "divider": "#3e3d32",
        "input_bg": "#3e3d32", "input_fg": "#f8f8f2",
        "input_border": "#49483e",
    },
    "Nord": {
        "bg": "#2e3440", "fg": "#d8dee9",
        "sidebar_bg": "#272d38", "sidebar_fg": "#7a8594",
        "sidebar_hover": "#3b4252", "sidebar_active": "#434c5e",
        "editor_bg": "#2e3440", "editor_fg": "#eceff4",
        "accent": "#88c0d0", "accent2": "#bf616a",
        "accent3": "#a3be8c", "accent4": "#ebcb8b",
        "toolbar_bg": "#232830", "toolbar_fg": "#5a6370",
        "toolbar_hover": "#333a48",
        "select_bg": "#434c5e", "select_fg": "#eceff4",
        "border": "#3b4252",
        "heading_color": "#88c0d0", "bold_color": "#ebcb8b",
        "italic_color": "#a3be8c",
        "code_bg": "#3b4252", "code_fg": "#a3be8c",
        "link_color": "#81a1c1",
        "button_bg": "#3b4252", "button_fg": "#d8dee9",
        "button_active": "#434c5e",
        "line_num_fg": "#434c5e", "cursor_color": "#88c0d0",
        "statusbar_bg": "#232830", "statusbar_fg": "#4c566a",
        "popup_bg": "#3b4252", "popup_fg": "#d8dee9",
        "error": "#bf616a", "warning": "#ebcb8b", "success": "#a3be8c",
        "muted": "#4c566a", "divider": "#3b4252",
        "input_bg": "#3b4252", "input_fg": "#eceff4",
        "input_border": "#434c5e",
    },
    "Solarized": {
        "bg": "#002b36", "fg": "#93a1a1",
        "sidebar_bg": "#001e27", "sidebar_fg": "#657b83",
        "sidebar_hover": "#073642", "sidebar_active": "#094959",
        "editor_bg": "#002b36", "editor_fg": "#839496",
        "accent": "#268bd2", "accent2": "#dc322f",
        "accent3": "#859900", "accent4": "#b58900",
        "toolbar_bg": "#001820", "toolbar_fg": "#586e75",
        "toolbar_hover": "#04313e",
        "select_bg": "#073642", "select_fg": "#fdf6e3",
        "border": "#073642",
        "heading_color": "#268bd2", "bold_color": "#b58900",
        "italic_color": "#2aa198",
        "code_bg": "#073642", "code_fg": "#859900",
        "link_color": "#268bd2",
        "button_bg": "#073642", "button_fg": "#93a1a1",
        "button_active": "#094959",
        "line_num_fg": "#586e75", "cursor_color": "#268bd2",
        "statusbar_bg": "#001820", "statusbar_fg": "#586e75",
        "popup_bg": "#073642", "popup_fg": "#93a1a1",
        "error": "#dc322f", "warning": "#b58900", "success": "#859900",
        "muted": "#586e75", "divider": "#073642",
        "input_bg": "#073642", "input_fg": "#93a1a1",
        "input_border": "#094959",
    },
}

TEMPLATES = {
    "Blank": "",
    "Meeting Notes": "# Meeting Notes\n\n**Date:** {date}\n**Attendees:** \n\n## Agenda\n\n1. \n\n## Discussion\n\n\n## Action Items\n\n- [ ] \n- [ ] \n",
    "To-Do List": "# To-Do List - {date}\n\n## High Priority\n- [ ] \n\n## Medium\n- [ ] \n\n## Low\n- [ ] \n\n## Done\n- [x] \n",
    "Journal": "# Journal - {date}\n\n## Thoughts\n\n\n## Grateful For\n1. \n2. \n3. \n\n## Tomorrow\n- [ ] \n",
    "Project Plan": "# Project: \n\n**Start:** {date}  |  **Deadline:** \n\n## Overview\n\n\n## Milestones\n- [ ] Phase 1\n- [ ] Phase 2\n\n## Notes\n\n",
    "Code Snippet": "# Snippet: \n\n**Language:**   |  **Date:** {date}\n\n## Code\n```\n\n```\n\n## Notes\n\n",
    "Weekly Review": "# Week of {date}\n\n## Accomplishments\n- \n\n## Challenges\n- \n\n## Next Week\n- [ ] \n\n## Reflections\n\n",
}


# ═══════════════════════════════════════════
# DATA MANAGER
# ═══════════════════════════════════════════

class DataManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.data = self._load(DATA_FILE, self._defaults)
        self.settings = self._load(SETTINGS_FILE, self._def_settings)

    def _load(self, path, default_fn):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return default_fn()

    def _save(self, path, d):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _defaults(self):
        rid = str(uuid.uuid4())
        wid = str(uuid.uuid4())
        return {
            "folders": {
                rid: {
                    "name": "My Notes", "parent": None, "children": [],
                    "notes": [wid], "color": "#7c9cde", "expanded": True,
                }
            },
            "notes": {
                wid: {
                    "title": "Welcome to QuickNote",
                    "content": (
                        "# Welcome to QuickNote\n\n"
                        "Your premium markdown notepad.\n\n"
                        "## Features\n\n"
                        "- **Markdown** with live syntax highlighting\n"
                        "- Password lock protection\n"
                        "- 8 beautiful themes\n"
                        "- Folder organization\n"
                        "- Global hotkey: `Win+Shift+Q`\n"
                        "- Tab system with session memory\n"
                        "- Focus mode for distraction-free writing\n"
                        "- Templates for quick note creation\n"
                        "- Version history with snapshots\n"
                        "- Note statistics and reading time\n\n"
                        "## Try Markdown\n\n"
                        "```python\nprint('Hello QuickNote!')\n```\n\n"
                        "- [x] Beautiful UI\n"
                        "- [x] Smooth hover effects\n"
                        "- [ ] World domination\n\n"
                        "> Start writing something amazing.\n\n"
                        "---\n*Built with care.*\n"
                    ),
                    "folder": rid, "created": datetime.now().isoformat(),
                    "modified": datetime.now().isoformat(),
                    "color": None, "pinned": False, "bookmarked": False,
                    "tags": ["welcome"], "word_goal": 0, "snapshots": [],
                }
            },
            "root_folder": rid, "trash": [],
            "favorites": [wid], "recent": [wid],
        }

    def _def_settings(self):
        return {
            "theme": "Pastel Dark", "font_family": "Consolas", "font_size": 13,
            "geometry": "1300x800", "auto_save": True, "auto_save_ms": 3000,
            "line_numbers": True, "word_wrap": True,
            "password_hash": PWD_HASH, "locked": True,
            "last_note": None, "show_toolbar": True,
            "show_statusbar": True, "tab_size": 4, "highlight_line": True,
            "auto_bracket": True, "auto_indent": True, "reading_wpm": 200,
            "sidebar_sort": "name", "snap_interval": 30,
            "open_tabs": [], "active_tab": None,
            "sidebar_width": 260, "recent_limit": 25,
        }

    def save_data(self):
        self._save(DATA_FILE, self.data)

    def save_settings(self):
        self._save(SETTINGS_FILE, self.settings)

    def create_folder(self, name, parent=None, color="#7c9cde"):
        fid = str(uuid.uuid4())
        parent = parent or self.data["root_folder"]
        self.data["folders"][fid] = {
            "name": name, "parent": parent, "children": [],
            "notes": [], "color": color, "expanded": False,
        }
        if parent in self.data["folders"]:
            self.data["folders"][parent]["children"].append(fid)
        self.save_data()
        return fid

    def create_note(self, title="Untitled", folder=None, content="", template=None):
        nid = str(uuid.uuid4())
        folder = folder or self.data["root_folder"]
        if template and template in TEMPLATES:
            content = TEMPLATES[template].replace("{date}", datetime.now().strftime("%Y-%m-%d"))
        now = datetime.now().isoformat()
        self.data["notes"][nid] = {
            "title": title, "content": content, "folder": folder,
            "created": now, "modified": now, "color": None,
            "pinned": False, "bookmarked": False,
            "tags": [], "word_goal": 0, "snapshots": [],
        }
        if folder in self.data["folders"]:
            self.data["folders"][folder]["notes"].append(nid)
        self._add_recent(nid)
        self.save_data()
        return nid

    def update_note(self, nid, **kw):
        if nid in self.data["notes"]:
            for k, v in kw.items():
                if k in self.data["notes"][nid]:
                    self.data["notes"][nid][k] = v
            self.data["notes"][nid]["modified"] = datetime.now().isoformat()
            self.save_data()

    def delete_note(self, nid):
        n = self.data["notes"].get(nid)
        if not n:
            return
        fid = n["folder"]
        if fid in self.data["folders"] and nid in self.data["folders"][fid]["notes"]:
            self.data["folders"][fid]["notes"].remove(nid)
        self.data.setdefault("trash", []).append(nid)
        for lst in ("favorites", "recent"):
            if nid in self.data.get(lst, []):
                self.data[lst].remove(nid)
        self.save_data()

    def delete_folder(self, fid):
        if fid == self.data["root_folder"]:
            return False
        f = self.data["folders"].get(fid)
        if not f:
            return False
        for c in list(f["children"]):
            self.delete_folder(c)
        for n in f["notes"]:
            self.data.setdefault("trash", []).append(n)
        p = f["parent"]
        if p and p in self.data["folders"] and fid in self.data["folders"][p]["children"]:
            self.data["folders"][p]["children"].remove(fid)
        del self.data["folders"][fid]
        self.save_data()
        return True

    def duplicate_note(self, nid):
        n = self.data["notes"].get(nid)
        if not n:
            return None
        return self.create_note(n["title"] + " (copy)", n["folder"], n["content"])

    def move_note(self, nid, new_fid):
        n = self.data["notes"].get(nid)
        if not n or new_fid not in self.data["folders"]:
            return
        old = n["folder"]
        if old in self.data["folders"] and nid in self.data["folders"][old]["notes"]:
            self.data["folders"][old]["notes"].remove(nid)
        n["folder"] = new_fid
        self.data["folders"][new_fid]["notes"].append(nid)
        self.save_data()

    def restore_note(self, nid):
        if nid not in self.data.get("trash", []):
            return
        n = self.data["notes"].get(nid)
        if not n:
            return
        fid = n["folder"]
        if fid not in self.data["folders"]:
            fid = self.data["root_folder"]
            n["folder"] = fid
        self.data["folders"][fid]["notes"].append(nid)
        self.data["trash"].remove(nid)
        self.save_data()

    def take_snapshot(self, nid):
        n = self.data["notes"].get(nid)
        if not n:
            return
        s = n.setdefault("snapshots", [])
        s.append({"content": n["content"], "ts": datetime.now().isoformat()})
        if len(s) > 50:
            n["snapshots"] = s[-50:]
        self.save_data()

    def search(self, q):
        q = q.lower()
        results = []
        for nid, n in self.data["notes"].items():
            if nid in self.data.get("trash", []):
                continue
            if (q in n["title"].lower() or q in n["content"].lower()
                    or any(q in t.lower() for t in n.get("tags", []))):
                results.append(nid)
        return results

    def get_stats(self, nid):
        n = self.data["notes"].get(nid)
        if not n:
            return {}
        c = n["content"]
        w = len(c.split()) if c.strip() else 0
        return {
            "words": w, "chars": len(c),
            "chars_ns": len(c.replace(" ", "").replace("\n", "")),
            "lines": c.count("\n") + 1,
            "sentences": len(re.split(r"[.!?]+", c)),
            "paragraphs": len([p for p in c.split("\n\n") if p.strip()]),
            "reading": max(1, w // self.settings.get("reading_wpm", 200)) if w > 0 else 0,
        }

    def _add_recent(self, nid):
        r = self.data.setdefault("recent", [])
        if nid in r:
            r.remove(nid)
        r.insert(0, nid)
        self.data["recent"] = r[: self.settings.get("recent_limit", 25)]


# ═══════════════════════════════════════════
# WIDGETS - Python 3.14 safe
# ═══════════════════════════════════════════

class HoverButton(tk.Label):
    """
    Animated button using tk.Label to avoid all Canvas/Frame
    widget-name issues in Python 3.14.
    """

    def __init__(self, parent, text="", command=None,
                 bg="#2a2a3a", fg="#d0d0e0",
                 hover_bg="#3a3a50", hover_fg=None,
                 active_bg=None,
                 font_spec=("Segoe UI", 10),
                 padx=12, pady=4, **kw):
        kw.pop("width", None)
        kw.pop("height", None)
        kw.pop("corner_radius", None)
        super().__init__(
            parent, text=text, bg=bg, fg=fg,
            font=font_spec, padx=padx, pady=pady,
            cursor="hand2", relief="flat", bd=0, **kw,
        )
        self._cmd = command
        self._bg = bg
        self._fg = fg
        self._hover_bg = hover_bg
        self._hover_fg = hover_fg or fg
        self._active_bg = active_bg or hover_bg
        self._anim_id = None

        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<Button-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)

    @staticmethod
    def _hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(r, g, b):
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    def _lerp(self, c1, c2, t):
        r1 = self._hex_to_rgb(c1)
        r2 = self._hex_to_rgb(c2)
        return self._rgb_to_hex(*(r1[i] + (r2[i] - r1[i]) * t for i in range(3)))

    def _animate(self, tbg, tfg, step=0):
        if step > 5:
            self.configure(bg=tbg, fg=tfg)
            return
        t = (step + 1) / 6.0
        try:
            cur_bg = self.cget("bg")
            cur_fg = self.cget("fg")
            self.configure(bg=self._lerp(cur_bg, tbg, t), fg=self._lerp(cur_fg, tfg, t))
        except Exception:
            self.configure(bg=tbg, fg=tfg)
            return
        self._anim_id = self.after(16, self._animate, tbg, tfg, step + 1)

    def _cancel(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None

    def _enter(self, e):
        self._cancel()
        self._animate(self._hover_bg, self._hover_fg)

    def _leave(self, e):
        self._cancel()
        self._animate(self._bg, self._fg)

    def _press(self, e):
        self._cancel()
        self.configure(bg=self._active_bg)

    def _release(self, e):
        if self._cmd:
            self._cmd()
        self._cancel()
        self._animate(self._hover_bg, self._hover_fg)


class ToolTip:
    def __init__(self, widget, text, bg="#222", fg="#eee", delay=400):
        self.w = widget
        self.text = text
        self._bg = bg
        self._fg = fg
        self.tw = None
        self._id = None
        self._delay = delay
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<Button-1>", self._hide, add="+")

    def _schedule(self, e=None):
        self._hide()
        self._id = self.w.after(self._delay, self._show)

    def _show(self):
        if self.tw:
            return
        x = self.w.winfo_rootx() + self.w.winfo_width() // 2
        y = self.w.winfo_rooty() + self.w.winfo_height() + 4
        self.tw = t = tk.Toplevel(self.w)
        t.wm_overrideredirect(True)
        try:
            t.attributes("-alpha", 0.92)
        except Exception:
            pass
        t.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(t, text=self.text, bg=self._bg, fg=self._fg,
                       font=("Segoe UI", 9), padx=8, pady=4, relief="solid", bd=1)
        lbl.pack()

    def _hide(self, e=None):
        if self._id:
            self.w.after_cancel(self._id)
            self._id = None
        if self.tw:
            self.tw.destroy()
            self.tw = None


# ═══════════════════════════════════════════
# MARKDOWN HIGHLIGHTER
# ═══════════════════════════════════════════

class MDHighlighter:
    TAGS = [
        "h1", "h2", "h3", "h4", "bold", "ital", "bold_ital",
        "code_i", "code_b", "fence", "link", "url", "img",
        "quote", "lst", "hr", "strike", "chk_done", "chk_undone",
        "tbl", "highlight",
    ]

    def __init__(self, w, c, ff="Consolas", fs=13):
        self.w = w
        self.c = c
        self.ff = ff
        self.fs = fs
        self._setup()

    def _setup(self):
        c, ff, fs = self.c, self.ff, self.fs
        cfg = self.w.tag_configure
        cfg("h1", foreground=c["heading_color"], font=(ff, fs + 11, "bold"))
        cfg("h2", foreground=c["heading_color"], font=(ff, fs + 7, "bold"))
        cfg("h3", foreground=c["heading_color"], font=(ff, fs + 3, "bold"))
        cfg("h4", foreground=c["heading_color"], font=(ff, fs + 1, "bold"))
        cfg("bold", foreground=c["bold_color"], font=(ff, fs, "bold"))
        cfg("ital", foreground=c["italic_color"], font=(ff, fs, "italic"))
        cfg("bold_ital", foreground=c["bold_color"], font=(ff, fs, "bold italic"))
        cfg("code_i", foreground=c["code_fg"], background=c["code_bg"], font=("Courier New", fs - 1))
        cfg("code_b", foreground=c["code_fg"], background=c["code_bg"], font=("Courier New", fs - 1), lmargin1=16, lmargin2=16)
        cfg("fence", foreground=c["muted"], font=("Courier New", fs - 1))
        cfg("link", foreground=c["link_color"], underline=True)
        cfg("url", foreground=c["link_color"])
        cfg("img", foreground=c.get("accent4", c["accent"]))
        cfg("quote", foreground=c["italic_color"], font=(ff, fs, "italic"), lmargin1=24, lmargin2=24, background=c["code_bg"])
        cfg("lst", foreground=c["accent"])
        cfg("hr", foreground=c["muted"], justify="center", font=(ff, 3))
        cfg("strike", foreground=c["muted"], overstrike=True)
        cfg("chk_done", foreground=c["success"])
        cfg("chk_undone", foreground=c["error"])
        cfg("tbl", foreground=c["muted"])
        cfg("highlight", background=c.get("accent4", "#bfa86c"), foreground=c["bg"])
        cfg("cur_line", background=c["code_bg"])
        self.w.tag_lower("cur_line")

    def update(self, c, ff, fs):
        self.c, self.ff, self.fs = c, ff, fs
        self._setup()

    def highlight(self):
        for t in self.TAGS:
            self.w.tag_remove(t, "1.0", "end")
        content = self.w.get("1.0", "end-1c")
        lines = content.split("\n")
        in_code = False
        for i, line in enumerate(lines):
            ln = i + 1
            ls = f"{ln}.0"
            le = f"{ln}.end"
            if line.strip().startswith("```"):
                self.w.tag_add("fence", ls, le)
                in_code = not in_code
                continue
            if in_code:
                self.w.tag_add("code_b", ls, le)
                continue
            m = re.match(r"^(#{1,4})\s+", line)
            if m:
                self.w.tag_add(f"h{min(len(m.group(1)),4)}", ls, le)
                continue
            if re.match(r"^(\s*[-*_]{3,}\s*)$", line):
                self.w.tag_add("hr", ls, le)
                continue
            if line.lstrip().startswith(">"):
                self.w.tag_add("quote", ls, le)
                continue
            if re.match(r"^\s*\|", line) and "|" in line:
                for m2 in re.finditer(r"\|", line):
                    self.w.tag_add("tbl", f"{ln}.{m2.start()}", f"{ln}.{m2.end()}")
                if re.match(r"^\s*\|[\s\-:|]+\|", line):
                    self.w.tag_add("tbl", ls, le)
                    continue
            m = re.match(r"^(\s*)([-*+]|\d+\.)\s", line)
            if m:
                self.w.tag_add("lst", f"{ln}.{m.start(2)}", f"{ln}.{m.end(2)}")
            m = re.match(r"^(\s*[-*+]\s)\[([xX ])\]", line)
            if m:
                tag = "chk_done" if m.group(2).lower() == "x" else "chk_undone"
                self.w.tag_add(tag, f"{ln}.{m.start(0)}", f"{ln}.{m.end(0)}")
            # inline
            for m in re.finditer(r"`([^`]+)`", line):
                self.w.tag_add("code_i", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"(\*{3}|_{3})(.+?)\1", line):
                self.w.tag_add("bold_ital", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"(\*{2}|_{2})(.+?)\1", line):
                self.w.tag_add("bold", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", line):
                self.w.tag_add("ital", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"~~(.+?)~~", line):
                self.w.tag_add("strike", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"==(.+?)==", line):
                self.w.tag_add("highlight", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", line):
                self.w.tag_add("img", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
                self.w.tag_add("link", f"{ln}.{m.start()}", f"{ln}.{m.end()}")
            for m in re.finditer(r"https?://\S+", line):
                self.w.tag_add("url", f"{ln}.{m.start()}", f"{ln}.{m.end()}")


# ═══════════════════════════════════════════
# LINE NUMBERS
# ═══════════════════════════════════════════

class LineNumbers(tk.Canvas):
    def __init__(self, parent, tw, **kw):
        super().__init__(parent, **kw)
        self.configure(width=50)
        self.tw = tw
        self._fg = "#3f3f50"

    def redraw(self, _=None):
        self.delete("all")
        if not self.tw:
            return
        idx = self.tw.index("@0,0")
        while True:
            dl = self.tw.dlineinfo(idx)
            if dl is None:
                break
            self.create_text(
                42, dl[1], anchor="ne",
                text=str(idx).split(".")[0],
                fill=self._fg, font=("Consolas", 10),
            )
            idx = self.tw.index(f"{idx}+1line")


# ═══════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════

class QuickNoteApp:
    def __init__(self):
        self.dm = DataManager()
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title(APP)
        self.root.geometry(self.dm.settings.get("geometry", "1300x800"))
        self.root.minsize(900, 550)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Dark title bar on Windows
        try:
            import ctypes
            self.root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            val = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(val), ctypes.sizeof(val))
        except Exception:
            pass

        # State
        self.current_note = None
        self.current_folder = self.dm.data["root_folder"]
        self.is_locked = self.dm.settings.get("locked", True)
        self.is_visible = True
        self.highlighter = None
        self.focus_mode = False
        self.sidebar_items = {}
        self._snap_counter = 0
        self._open_tabs = OrderedDict()
        self._find_win = None

        # Detect serif font
        self._serif = "Georgia"
        try:
            import tkinter.font as tkfont
            avail = [f.lower() for f in tkfont.families()]
            for sf in SERIF_FONTS:
                if sf.lower() in avail:
                    self._serif = sf
                    break
        except Exception:
            pass

        # Theme
        self.theme_name = self.dm.settings.get("theme", "Pastel Dark")
        self.C = THEMES.get(self.theme_name, THEMES["Pastel Dark"])

        if self.is_locked:
            self._show_lock_screen()
        else:
            self._build_ui()

        self._start_hotkey()
        self.root.deiconify()

        # Fade in
        try:
            self.root.attributes("-alpha", 0.0)
            def fade(a=0.0):
                if a <= 1.0:
                    self.root.attributes("-alpha", a)
                    self.root.after(18, fade, round(a + 0.1, 2))
                else:
                    self.root.attributes("-alpha", 1.0)
            fade()
        except Exception:
            pass

        self.root.mainloop()

    # ═══════════════════════════
    # LOCK SCREEN
    # ═══════════════════════════

    def _show_lock_screen(self):
        C = self.C
        self.root.configure(bg=C["bg"])
        self.lock_frame = tk.Frame(self.root, bg=C["bg"])
        self.lock_frame.pack(fill="both", expand=True)

        center = tk.Frame(self.lock_frame, bg=C["bg"])
        center.place(relx=0.5, rely=0.42, anchor="center")

        # Animated lock icon
        self.lock_canvas = tk.Canvas(center, bg=C["bg"], highlightthickness=0)
        self.lock_canvas.configure(width=80, height=80)
        self.lock_canvas.pack(pady=(0, 16))
        self._lock_phase = 0
        self._draw_lock(0)
        self._anim_lock()

        # Title
        tk.Label(center, text=APP, font=(self._serif, 32, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=(0, 4))
        tk.Label(center, text="Your secure markdown notepad",
                 font=(self._serif, 12, "italic"),
                 bg=C["bg"], fg=C["muted"]).pack(pady=(0, 32))

        # Password entry
        pw_border = tk.Frame(center, bg=C["input_border"])
        pw_border.pack(pady=(0, 12))
        pw_inner = tk.Frame(pw_border, bg=C["input_bg"])
        pw_inner.pack(padx=2, pady=2)
        self.pass_var = tk.StringVar()
        self.pass_entry = tk.Entry(
            pw_inner, textvariable=self.pass_var, show=I.DOT,
            bg=C["input_bg"], fg=C["input_fg"],
            insertbackground=C["cursor_color"],
            font=(self._serif, 14), relief="flat", bd=0, width=22,
        )
        self.pass_entry.pack(padx=10, pady=8)
        self.pass_entry.focus_set()
        self.pass_entry.bind("<Return>", self._try_unlock)
        self.pass_entry.bind("<FocusIn>", lambda e: pw_border.configure(bg=C["accent"]))
        self.pass_entry.bind("<FocusOut>", lambda e: pw_border.configure(bg=C["input_border"]))

        # Error
        self.lock_msg = tk.Label(center, text="", font=(self._serif, 10),
                                 bg=C["bg"], fg=C["error"])
        self.lock_msg.pack(pady=(0, 8))

        # Unlock button
        HoverButton(
            center, text="  Unlock  ", command=self._try_unlock,
            bg=C["accent"], fg=C["bg"],
            hover_bg=C.get("link_color", C["accent"]),
            font_spec=(self._serif, 12, "bold"),
            padx=24, pady=8,
        ).pack()

        # Hint
        tk.Label(self.lock_frame, text="Win+Shift+Q to toggle",
                 font=("Segoe UI", 9), bg=C["bg"],
                 fg=C["muted"]).place(relx=0.5, rely=0.95, anchor="center")

    def _draw_lock(self, phase):
        c = self.lock_canvas
        c.delete("all")
        cx, cy = 40, 40
        color = self.C["accent"]
        bw, bh = 32, 24
        bx = cx - bw // 2
        by = cy
        c.create_rectangle(bx, by, bx + bw, by + bh, fill=color, outline="")
        offset = math.sin(phase * 0.05) * 2
        sw, sh = 20, 16 + offset
        c.create_arc(cx - sw // 2, by - sh, cx + sw // 2, by + 2,
                     start=0, extent=180, outline=color, width=4, style="arc")
        kr = 4
        c.create_oval(cx - kr, by + bh // 2 - kr - 2, cx + kr, by + bh // 2 + kr - 2,
                      fill=self.C["bg"], outline="")
        c.create_polygon(cx - 2, by + bh // 2 + 2, cx + 2, by + bh // 2 + 2,
                         cx, by + bh - 4, fill=self.C["bg"], outline="")

    def _anim_lock(self):
        if not hasattr(self, "lock_canvas"):
            return
        try:
            if not self.lock_canvas.winfo_exists():
                return
        except Exception:
            return
        self._lock_phase += 1
        self._draw_lock(self._lock_phase)
        self.root.after(50, self._anim_lock)

    def _try_unlock(self, e=None):
        pwd = self.pass_var.get()
        h = hashlib.sha256(pwd.encode()).hexdigest()
        if h == self.dm.settings["password_hash"]:
            self.is_locked = False
            self.dm.settings["locked"] = False
            self.dm.save_settings()
            self.lock_frame.destroy()
            if hasattr(self, "lock_canvas"):
                del self.lock_canvas
            self._build_ui()
        else:
            self.lock_msg.config(text="Incorrect password. Try again.")
            self.pass_var.set("")
            self.pass_entry.focus_set()

    # ═══════════════════════════
    # BUILD UI
    # ═══════════════════════════

    def _build_ui(self):
        C = self.C
        self.root.configure(bg=C["bg"])
        self._build_menu()

        self.main_frame = tk.Frame(self.root, bg=C["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.hpane = tk.PanedWindow(self.main_frame, orient="horizontal",
                                    bg=C["border"], sashwidth=2,
                                    sashrelief="flat", opaqueresize=True)
        self.hpane.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_right_pane()
        self._build_statusbar()
        self._bind_keys()

        # Restore tabs
        saved = self.dm.settings.get("open_tabs", [])
        active = self.dm.settings.get("active_tab")
        last = self.dm.settings.get("last_note")

        opened = False
        for nid in saved:
            if nid in self.dm.data["notes"] and nid not in self.dm.data.get("trash", []):
                self._add_tab(nid, switch=False)
                opened = True

        if active and active in self._open_tabs:
            self._switch_tab(active)
        elif last and last in self.dm.data["notes"] and last not in self.dm.data.get("trash", []):
            if last not in self._open_tabs:
                self._add_tab(last, switch=True)
            else:
                self._switch_tab(last)
            opened = True

        if not opened:
            for nid in self.dm.data["notes"]:
                if nid not in self.dm.data.get("trash", []):
                    self._add_tab(nid, switch=True)
                    break

        if self.dm.settings.get("auto_save"):
            self._auto_save_loop()

    # ── Menu ──

    def _build_menu(self):
        C = self.C
        mkw = dict(bg=C["toolbar_bg"], fg=C["toolbar_fg"],
                    activebackground=C["accent"], activeforeground=C["bg"],
                    font=("Segoe UI", 10), bd=0, relief="flat")
        self.menubar = tk.Menu(self.root, **mkw)
        self.root.config(menu=self.menubar)

        def M():
            return tk.Menu(self.menubar, tearoff=0, **mkw)

        fm = M()
        fm.add_command(label=f" {I.ADD}  New Note          Ctrl+N", command=self._new_note)
        fm.add_command(label=f" {I.TEMPLATE}  From Template", command=self._template_dlg)
        fm.add_command(label=f" {I.ADD}  New Folder       Ctrl+Shift+F", command=self._new_folder)
        fm.add_separator()
        fm.add_command(label=f" {I.SAVE}  Save                Ctrl+S", command=self._save_current)
        fm.add_command(label=f" {I.DUP}  Duplicate", command=self._dup_current)
        fm.add_separator()
        fm.add_command(label=f" {I.EXPORT}  Export .md", command=self._export_md)
        fm.add_command(label=f" {I.EXPORT}  Export .html", command=self._export_html)
        fm.add_command(label=f" {I.IMPORT}  Import .md", command=self._import_md)
        fm.add_separator()
        fm.add_command(label=f" {I.LOCK}  Lock                 Ctrl+L", command=self._lock_app)
        fm.add_separator()
        fm.add_command(label=f" {I.CLOSE}  Exit", command=self._on_close)
        self.menubar.add_cascade(label="File", menu=fm)

        em = M()
        em.add_command(label=f" {I.UNDO}  Undo     Ctrl+Z", command=lambda: self.editor.event_generate("<<Undo>>"))
        em.add_command(label=f" {I.REDO}  Redo     Ctrl+Y", command=lambda: self.editor.event_generate("<<Redo>>"))
        em.add_separator()
        em.add_command(label=f" {I.FIND}  Find        Ctrl+F", command=self._show_find)
        em.add_separator()
        em.add_command(label=f" {I.SORT}  Sort Lines", command=self._sort_lines)
        em.add_command(label="    Remove Duplicates", command=self._dedup_lines)
        em.add_command(label="    Trim Whitespace", command=self._trim_ws)
        self.menubar.add_cascade(label="Edit", menu=em)

        im = M()
        im.add_command(label=f" {I.BOLD}  Bold       Ctrl+B", command=lambda: self._wrap("**"))
        im.add_command(label=f" {I.ITALIC}  Italic     Ctrl+I", command=lambda: self._wrap("*"))
        im.add_command(label="    Strike", command=lambda: self._wrap("~~"))
        im.add_command(label="    Highlight", command=lambda: self._wrap("=="))
        im.add_command(label=f" {I.CODE}  Code", command=lambda: self._wrap("`"))
        im.add_separator()
        im.add_command(label="    Code Block", command=self._ins_codeblock)
        im.add_command(label=f" {I.LINK}  Link", command=self._ins_link)
        im.add_command(label=f" {I.HEADING}  Heading", command=self._cycle_heading)
        im.add_command(label=f" {I.HRULE}  Rule", command=lambda: self._ins("\n---\n"))
        im.add_separator()
        im.add_command(label=f" {I.CHECK}  Checkbox", command=lambda: self._ins("- [ ] "))
        im.add_command(label=f" {I.BULLET}  Bullet", command=lambda: self._ins("- "))
        im.add_command(label="    Table", command=self._ins_table)
        im.add_command(label=f" {I.CLOCK}  Date/Time", command=lambda: self._ins(datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.menubar.add_cascade(label="Insert", menu=im)

        vm = M()
        vm.add_command(label=f" {I.PREVIEW}  Preview    Ctrl+P", command=self._toggle_preview)
        vm.add_command(label=f" {I.FOCUS}  Focus Mode", command=self._toggle_focus)
        vm.add_separator()
        vm.add_command(label="  A+  Zoom In    Ctrl+=", command=lambda: self._font_delta(1))
        vm.add_command(label="  A-  Zoom Out   Ctrl+-", command=lambda: self._font_delta(-1))
        vm.add_separator()
        tm = M()
        for t in THEMES:
            mark = I.FILLED + " " if t == self.theme_name else I.RING + " "
            tm.add_command(label=f" {mark} {t}", command=lambda t=t: self._apply_theme(t))
        vm.add_cascade(label=f" {I.THEME}  Themes", menu=tm)
        vm.add_separator()
        vm.add_command(label=f" {I.STATS}  Statistics", command=self._show_stats)
        vm.add_command(label=f" {I.HISTORY}  Version History", command=self._show_history)
        vm.add_command(label=f" {I.TRASH}  Trash", command=self._show_trash)
        vm.add_command(label=f" {I.STAR}  Favorites", command=self._show_favorites)
        vm.add_command(label=f" {I.CLOCK}  Recent", command=self._show_recent)
        self.menubar.add_cascade(label="View", menu=vm)

        sm = M()
        sm.add_command(label=f" {I.LOCK}  Change Password", command=self._change_pwd)
        sm.add_command(label=f" {I.GEAR}  Preferences", command=self._show_prefs)
        self.menubar.add_cascade(label="Settings", menu=sm)

    # ── Sidebar ──

    def _build_sidebar(self):
        C = self.C
        self.sidebar = tk.Frame(self.hpane, bg=C["sidebar_bg"])
        self.sidebar.configure(width=self.dm.settings.get("sidebar_width", 260))
        self.hpane.add(self.sidebar, minsize=180)

        # Search
        sf = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        sf.pack(fill="x", padx=8, pady=(10, 4))

        sb = tk.Frame(sf, bg=C["input_border"])
        sb.pack(fill="x")
        si = tk.Frame(sb, bg=C["input_bg"])
        si.pack(fill="x", padx=1, pady=1)
        tk.Label(si, text=I.SEARCH, bg=C["input_bg"], fg=C["muted"],
                 font=("Segoe UI", 10)).pack(side="left", padx=(6, 2))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._on_search())
        self.search_entry = tk.Entry(si, textvariable=self.search_var,
                                     bg=C["input_bg"], fg=C["input_fg"],
                                     insertbackground=C["cursor_color"],
                                     font=("Segoe UI", 11), relief="flat", bd=0)
        self.search_entry.pack(fill="x", side="left", expand=True, padx=(0, 6), ipady=5)

        # Buttons
        bf = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        bf.pack(fill="x", padx=8, pady=(6, 4))
        for text, cmd, tip in [
            (f"{I.ADD} Note", self._new_note, "New Note  Ctrl+N"),
            (f"{I.ADD} Folder", self._new_folder, "New Folder"),
            (I.TEMPLATE, self._template_dlg, "Template"),
        ]:
            b = HoverButton(bf, text=text, command=cmd,
                            bg=C["button_bg"], fg=C["button_fg"],
                            hover_bg=C["button_active"],
                            font_spec=("Segoe UI", 9), padx=8, pady=2)
            b.pack(side="left", padx=(0, 4))
            ToolTip(b, tip, bg=C["popup_bg"], fg=C["popup_fg"])

        # Sort
        sort_mb = tk.Menubutton(bf, text=I.SORT, bg=C["button_bg"],
                                fg=C["button_fg"], font=("Segoe UI", 10),
                                relief="flat", cursor="hand2", bd=0, padx=6)
        sort_m = tk.Menu(sort_mb, tearoff=0, bg=C["popup_bg"], fg=C["popup_fg"],
                         activebackground=C["accent"], activeforeground=C["bg"],
                         font=("Segoe UI", 10))
        for label, val in [("Name", "name"), ("Modified", "modified"), ("Created", "created")]:
            sort_m.add_command(label=label, command=lambda v=val: self._set_sort(v))
        sort_mb.config(menu=sort_m)
        sort_mb.pack(side="right")

        tk.Frame(self.sidebar, bg=C["divider"], height=1).pack(fill="x", padx=8, pady=4)

        # Tree
        tf = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        tf.pack(fill="both", expand=True, padx=4, pady=2)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("SB.Treeview", background=C["sidebar_bg"],
                         foreground=C["sidebar_fg"],
                         fieldbackground=C["sidebar_bg"],
                         borderwidth=0, font=("Segoe UI", 11), rowheight=30)
        style.map("SB.Treeview",
                   background=[("selected", C["sidebar_active"])],
                   foreground=[("selected", C["fg"])])
        style.layout("SB.Treeview", [("SB.Treeview.treearea", {"sticky": "nswe"})])

        self.tree = ttk.Treeview(tf, style="SB.Treeview", show="tree", selectmode="browse")
        tsb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_sel)
        self.tree.bind("<Button-3>", self._on_tree_ctx)
        self.tree.bind("<Double-1>", self._on_tree_dbl)
        self._populate_tree()

    def _populate_tree(self, search=None):
        self.tree.delete(*self.tree.get_children())
        self.sidebar_items.clear()
        if search is not None:
            for nid in search:
                n = self.dm.data["notes"].get(nid)
                if n:
                    pin = I.PIN + " " if n.get("pinned") else ""
                    bm = I.BOOKMARK + " " if n.get("bookmarked") else ""
                    iid = self.tree.insert("", "end", text=f"   {I.NOTE} {pin}{bm}{n['title']}")
                    self.sidebar_items[iid] = ("note", nid)
            return
        self._add_folder("", self.dm.data["root_folder"])

    def _add_folder(self, parent, fid):
        f = self.dm.data["folders"].get(fid)
        if not f:
            return
        icon = I.FOLDER_OPEN if f.get("expanded") else I.FOLDER
        iid = self.tree.insert(parent, "end", text=f"  {icon} {f['name']}",
                               open=f.get("expanded", False))
        self.sidebar_items[iid] = ("folder", fid)
        for c in f.get("children", []):
            self._add_folder(iid, c)

        sk = self.dm.settings.get("sidebar_sort", "name")
        nids = [n for n in f.get("notes", [])
                if n in self.dm.data["notes"] and n not in self.dm.data.get("trash", [])]

        def sort_fn(nid):
            nt = self.dm.data["notes"][nid]
            if sk == "modified":
                return nt.get("modified", "")
            if sk == "created":
                return nt.get("created", "")
            return nt["title"].lower()

        nids.sort(key=sort_fn, reverse=(sk in ("modified", "created")))
        pinned = [n for n in nids if self.dm.data["notes"][n].get("pinned")]
        rest = [n for n in nids if not self.dm.data["notes"][n].get("pinned")]

        for nid in pinned + rest:
            n = self.dm.data["notes"][nid]
            pin = I.PIN + " " if n.get("pinned") else ""
            bm = I.BOOKMARK + " " if n.get("bookmarked") else ""
            niid = self.tree.insert(iid, "end", text=f"     {I.NOTE} {pin}{bm}{n['title']}")
            self.sidebar_items[niid] = ("note", nid)

    def _sel_in_tree(self, nid):
        for iid, info in self.sidebar_items.items():
            if info == ("note", nid):
                self.tree.selection_set(iid)
                self.tree.see(iid)
                return

    def _set_sort(self, v):
        self.dm.settings["sidebar_sort"] = v
        self.dm.save_settings()
        self._populate_tree()
        if self.current_note:
            self._sel_in_tree(self.current_note)

    # ── Right Pane ──

    def _build_right_pane(self):
        C = self.C
        self.right_pane = tk.Frame(self.hpane, bg=C["bg"])
        self.hpane.add(self.right_pane)

        # Tab bar
        self.tab_bar = tk.Frame(self.right_pane, bg=C["toolbar_bg"])
        self.tab_bar.pack(fill="x")
        self.tab_bar.configure(height=34)

        self.tab_container = tk.Frame(self.tab_bar, bg=C["toolbar_bg"])
        self.tab_container.pack(side="left", fill="both", expand=True)

        new_tab = HoverButton(self.tab_bar, text=I.ADD, command=self._new_note,
                              bg=C["toolbar_bg"], fg=C["toolbar_fg"],
                              hover_bg=C["toolbar_hover"],
                              font_spec=("Segoe UI", 12), padx=6, pady=2)
        new_tab.pack(side="right", padx=4, pady=3)
        ToolTip(new_tab, "New Tab  Ctrl+N", bg=C["popup_bg"], fg=C["popup_fg"])

        # Toolbar
        self.toolbar = tk.Frame(self.right_pane, bg=C["toolbar_bg"])
        if self.dm.settings.get("show_toolbar", True):
            self.toolbar.pack(fill="x")

        tb = [
            (I.BOLD, lambda: self._wrap("**"), "Bold Ctrl+B"),
            (I.ITALIC, lambda: self._wrap("*"), "Italic Ctrl+I"),
            ("S", lambda: self._wrap("~~"), "Strikethrough"),
            (I.CODE, lambda: self._wrap("`"), "Code"),
            (None, None, None),
            ("H1", lambda: self._prefix("# "), "Heading 1"),
            ("H2", lambda: self._prefix("## "), "Heading 2"),
            ("H3", lambda: self._prefix("### "), "Heading 3"),
            (None, None, None),
            (I.BULLET, lambda: self._ins("- "), "Bullet"),
            (I.NUM, lambda: self._ins("1. "), "Number"),
            (I.CHECK, lambda: self._ins("- [ ] "), "Checkbox"),
            (I.QUOTE, lambda: self._prefix("> "), "Quote"),
            (None, None, None),
            (I.LINK, self._ins_link, "Link"),
            (I.HRULE, lambda: self._ins("\n---\n"), "Rule"),
            ("{ }", self._ins_codeblock, "Code Block"),
            ("T", self._ins_table, "Table"),
            (None, None, None),
            (I.PREVIEW, self._toggle_preview, "Preview Ctrl+P"),
            (I.FOCUS, self._toggle_focus, "Focus Mode"),
        ]
        for item in tb:
            if item[0] is None:
                tk.Frame(self.toolbar, bg=C["divider"], width=1).pack(
                    side="left", fill="y", padx=3, pady=6)
                continue
            text, cmd, tip = item
            b = HoverButton(self.toolbar, text=text, command=cmd,
                            bg=C["toolbar_bg"], fg=C["toolbar_fg"],
                            hover_bg=C["toolbar_hover"],
                            font_spec=("Segoe UI", 10), padx=6, pady=2)
            b.pack(side="left", padx=1, pady=4)
            ToolTip(b, tip, bg=C["popup_bg"], fg=C["popup_fg"])

        # Title
        tf = tk.Frame(self.right_pane, bg=C["bg"])
        tf.pack(fill="x", padx=16, pady=(10, 0))
        self.title_var = tk.StringVar()
        self.title_var.trace_add("write", self._on_title_chg)
        self.title_entry = tk.Entry(tf, textvariable=self.title_var,
                                    bg=C["bg"], fg=C["accent"],
                                    insertbackground=C["accent"],
                                    font=("Segoe UI", 20, "bold"),
                                    relief="flat", bd=0)
        self.title_entry.pack(fill="x")

        # Tags
        meta = tk.Frame(self.right_pane, bg=C["bg"])
        meta.pack(fill="x", padx=16, pady=(2, 4))
        tk.Label(meta, text=I.TAG, bg=C["bg"], fg=C["muted"], font=("Segoe UI", 10)).pack(side="left")
        self.tags_var = tk.StringVar()
        self.tags_entry = tk.Entry(meta, textvariable=self.tags_var,
                                   bg=C["bg"], fg=C["muted"],
                                   insertbackground=C["cursor_color"],
                                   font=("Segoe UI", 10), relief="flat", bd=0)
        self.tags_entry.pack(side="left", fill="x", expand=True, padx=4)
        self.tags_entry.bind("<Return>", self._save_tags)
        self.meta_label = tk.Label(meta, text="", bg=C["bg"], fg=C["muted"], font=("Segoe UI", 9))
        self.meta_label.pack(side="right")

        tk.Frame(self.right_pane, bg=C["divider"], height=1).pack(fill="x", padx=16)

        # Editor
        ec = tk.Frame(self.right_pane, bg=C["bg"])
        ec.pack(fill="both", expand=True, padx=6, pady=4)

        self.line_nums = LineNumbers(ec, None, bg=C["editor_bg"], highlightthickness=0)
        self.line_nums._fg = C["line_num_fg"]
        if self.dm.settings.get("line_numbers", True):
            self.line_nums.pack(side="left", fill="y")

        esb = tk.Scrollbar(ec, orient="vertical", bg=C["border"],
                           troughcolor=C["editor_bg"], width=10)
        esb.pack(side="right", fill="y")

        ff = self.dm.settings.get("font_family", "Consolas")
        fs = self.dm.settings.get("font_size", 13)
        wr = "word" if self.dm.settings.get("word_wrap", True) else "none"

        self.editor = tk.Text(ec, bg=C["editor_bg"], fg=C["editor_fg"],
                              insertbackground=C["cursor_color"],
                              selectbackground=C["select_bg"],
                              selectforeground=C["select_fg"],
                              font=(ff, fs), wrap=wr, undo=True,
                              autoseparators=True, relief="flat", bd=0,
                              padx=14, pady=10, spacing1=2, spacing3=2,
                              insertwidth=2,
                              tabs=(f"{self.dm.settings.get('tab_size', 4)}c",),
                              yscrollcommand=esb.set)
        self.editor.pack(fill="both", expand=True)
        esb.config(command=self.editor.yview)

        self.line_nums.tw = self.editor
        self.highlighter = MDHighlighter(self.editor, C, ff, fs)

        self.editor.bind("<KeyRelease>", self._on_key_release)
        self.editor.bind("<MouseWheel>", lambda e: self.root.after(10, self.line_nums.redraw))
        self.editor.bind("<<Modified>>", self._on_modified)
        self.editor.bind("<Tab>", self._on_tab)
        self.editor.bind("<Return>", self._on_return)
        self.editor.bind("<BackSpace>", self._on_backspace)
        self.editor.bind("<Button-1>", lambda e: self.root.after(10, self._hl_cur_line))

        if self.dm.settings.get("auto_bracket", True):
            for o, c in [("(", ")"), ("[", "]"), ("{", "}"), ('"', '"'), ("'", "'")]:
                self.editor.bind(o, lambda e, p=(o, c): self._auto_close(e, p))

    # ── Tabs ──

    def _add_tab(self, nid, switch=True):
        if nid in self._open_tabs:
            if switch:
                self._switch_tab(nid)
            return
        note = self.dm.data["notes"].get(nid)
        if not note:
            return

        C = self.C
        tab = tk.Frame(self.tab_container, bg=C["toolbar_bg"])

        title_short = note["title"][:20] + ("..." if len(note["title"]) > 20 else "")
        pin_mark = I.PIN + " " if note.get("pinned") else ""

        lbl = tk.Label(tab, text=f" {pin_mark}{title_short} ",
                       bg=C["toolbar_bg"], fg=C["toolbar_fg"],
                       font=("Segoe UI", 9), cursor="hand2")
        lbl.pack(side="left", padx=(6, 0), pady=4)

        close_lbl = tk.Label(tab, text=I.TAB_CLOSE,
                             bg=C["toolbar_bg"], fg=C["muted"],
                             font=("Segoe UI", 9), cursor="hand2", padx=4)
        close_lbl.pack(side="right", padx=(0, 4), pady=4)

        accent_line = tk.Frame(tab, bg=C["toolbar_bg"], height=2)
        accent_line.pack(fill="x", side="bottom")

        # Hover effects
        def enter(e, _nid=nid):
            if self.current_note != _nid:
                tab.configure(bg=C["toolbar_hover"])
                lbl.configure(bg=C["toolbar_hover"])
                close_lbl.configure(bg=C["toolbar_hover"])

        def leave(e, _nid=nid):
            bg = C["sidebar_active"] if self.current_note == _nid else C["toolbar_bg"]
            tab.configure(bg=bg)
            lbl.configure(bg=bg)
            close_lbl.configure(bg=bg)

        def enter_close(e):
            close_lbl.configure(fg=C["error"])

        def leave_close(e):
            close_lbl.configure(fg=C["muted"])

        for w in (tab, lbl):
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)

        lbl.bind("<Button-1>", lambda e, n=nid: self._switch_tab(n))
        close_lbl.bind("<Enter>", enter_close)
        close_lbl.bind("<Leave>", leave_close)
        close_lbl.bind("<Button-1>", lambda e, n=nid: self._close_tab(n))

        tab.pack(side="left", padx=(0, 1))
        self._open_tabs[nid] = {"frame": tab, "label": lbl, "close": close_lbl, "accent": accent_line}

        if switch:
            self._switch_tab(nid)

    def _switch_tab(self, nid):
        if nid not in self._open_tabs:
            return
        C = self.C
        self._save_current()

        for tid, tw in self._open_tabs.items():
            bg = C["toolbar_bg"]
            tw["frame"].configure(bg=bg)
            tw["label"].configure(bg=bg, fg=C["toolbar_fg"])
            tw["close"].configure(bg=bg)
            tw["accent"].configure(bg=bg)

        tw = self._open_tabs[nid]
        bg = C["sidebar_active"]
        tw["frame"].configure(bg=bg)
        tw["label"].configure(bg=bg, fg=C["fg"])
        tw["close"].configure(bg=bg)
        tw["accent"].configure(bg=C["accent"])
        self._open_note(nid)

    def _close_tab(self, nid):
        if nid not in self._open_tabs:
            return
        self._save_current()
        self._open_tabs[nid]["frame"].destroy()
        del self._open_tabs[nid]
        if self.current_note == nid:
            self.current_note = None
            if self._open_tabs:
                self._switch_tab(list(self._open_tabs.keys())[-1])
            else:
                self.editor.delete("1.0", "end")
                self.title_var.set("")
                self.tags_var.set("")

    def _update_tab_title(self, nid):
        if nid not in self._open_tabs:
            return
        note = self.dm.data["notes"].get(nid, {})
        title = note.get("title", "")[:20]
        if len(note.get("title", "")) > 20:
            title += "..."
        pin = I.PIN + " " if note.get("pinned") else ""
        self._open_tabs[nid]["label"].configure(text=f" {pin}{title} ")

    # ── Status Bar ──

    def _build_statusbar(self):
        C = self.C
        self.statusbar = tk.Frame(self.root, bg=C["statusbar_bg"], height=24)
        if self.dm.settings.get("show_statusbar", True):
            self.statusbar.pack(fill="x", side="bottom")
        self.statusbar.pack_propagate(False)

        self.st_left = tk.Label(self.statusbar, text="Ready", bg=C["statusbar_bg"],
                                fg=C["statusbar_fg"], font=("Segoe UI", 9), anchor="w")
        self.st_left.pack(side="left", padx=10)
        self.st_right = tk.Label(self.statusbar, text="", bg=C["statusbar_bg"],
                                 fg=C["statusbar_fg"], font=("Segoe UI", 9), anchor="e")
        self.st_right.pack(side="right", padx=10)
        self.st_pos = tk.Label(self.statusbar, text="", bg=C["statusbar_bg"],
                               fg=C["accent"], font=("Segoe UI", 9))
        self.st_pos.pack(side="right", padx=10)
        self.st_read = tk.Label(self.statusbar, text="", bg=C["statusbar_bg"],
                                fg=C["statusbar_fg"], font=("Segoe UI", 9))
        self.st_read.pack(side="right", padx=10)
        self.st_theme = tk.Label(self.statusbar, text=self.theme_name, bg=C["statusbar_bg"],
                                 fg=C["muted"], font=("Segoe UI", 9))
        self.st_theme.pack(side="right", padx=10)

    def _update_status(self):
        if not self.current_note:
            return
        stats = self.dm.get_stats(self.current_note)
        note = self.dm.data["notes"].get(self.current_note, {})
        try:
            dt = datetime.fromisoformat(note.get("modified", ""))
            ms = dt.strftime("%b %d, %Y  %I:%M %p")
        except Exception:
            ms = ""
        self.st_left.config(text=f"Modified: {ms}")
        self.st_right.config(text=f"Words: {stats['words']}  |  Lines: {stats['lines']}  |  Chars: {stats['chars']}")
        try:
            ln, col = self.editor.index("insert").split(".")
            self.st_pos.config(text=f"Ln {ln}, Col {int(col) + 1}")
        except Exception:
            pass
        goal = note.get("word_goal", 0)
        if goal > 0:
            pct = min(100, int(stats["words"] / goal * 100))
            self.st_read.config(text=f"Goal: {stats['words']}/{goal} ({pct}%)")
        else:
            rt = stats.get("reading", 0)
            self.st_read.config(text=f"~{rt} min read" if rt > 0 else "")

    # ── Keys ──

    def _bind_keys(self):
        r = self.root
        for k, c in {
            "<Control-n>": lambda e: self._new_note(),
            "<Control-N>": lambda e: self._new_note(),
            "<Control-s>": lambda e: self._save_current(),
            "<Control-S>": lambda e: self._save_current(),
            "<Control-l>": lambda e: self._lock_app(),
            "<Control-L>": lambda e: self._lock_app(),
            "<Control-f>": lambda e: self._show_find(),
            "<Control-F>": lambda e: self._show_find(),
            "<Control-b>": lambda e: self._wrap("**"),
            "<Control-B>": lambda e: self._wrap("**"),
            "<Control-i>": lambda e: self._wrap("*"),
            "<Control-I>": lambda e: self._wrap("*"),
            "<Control-p>": lambda e: self._toggle_preview(),
            "<Control-P>": lambda e: self._toggle_preview(),
            "<Control-equal>": lambda e: self._font_delta(1),
            "<Control-plus>": lambda e: self._font_delta(1),
            "<Control-minus>": lambda e: self._font_delta(-1),
            "<Control-w>": lambda e: self._close_tab(self.current_note) if self.current_note else None,
            "<Control-W>": lambda e: self._close_tab(self.current_note) if self.current_note else None,
            "<Control-Shift-F>": lambda e: self._new_folder(),
            "<Control-Shift-f>": lambda e: self._new_folder(),
            "<Control-Shift-S>": lambda e: self._show_stats(),
            "<Control-Shift-s>": lambda e: self._show_stats(),
            "<Escape>": lambda e: self._toggle_focus() if self.focus_mode else None,
        }.items():
            r.bind(k, c)

    # ── Editor Events ──

    def _on_key_release(self, e=None):
        self.root.after(80, self._do_hl)
        self.root.after(50, self.line_nums.redraw)
        self._hl_cur_line()
        self._update_status()

    def _on_modified(self, e=None):
        if self.editor.edit_modified():
            if self.current_note:
                self.dm.data["notes"][self.current_note]["content"] = self.editor.get("1.0", "end-1c")
            self.editor.edit_modified(False)
            self._snap_counter += 1
            if self._snap_counter >= self.dm.settings.get("snap_interval", 30):
                self._snap_counter = 0
                if self.current_note:
                    self.dm.take_snapshot(self.current_note)

    def _on_title_chg(self, *a):
        if self.current_note:
            self.dm.data["notes"][self.current_note]["title"] = self.title_var.get().strip() or "Untitled"
            self._update_tab_title(self.current_note)

    def _on_tab(self, e):
        self.editor.insert("insert", " " * self.dm.settings.get("tab_size", 4))
        return "break"

    def _on_return(self, e):
        if not self.dm.settings.get("auto_indent", True):
            return None
        line = self.editor.get("insert linestart", "insert")
        m = re.match(r"^(\s*)([-*+])\s(\[[ xX]\]\s)?", line)
        if m:
            full = self.editor.get("insert linestart", "insert lineend")
            if full.strip() in ["-", "*", "+", "- [ ]", "- [x]", "- [X]"]:
                self.editor.delete("insert linestart", "insert lineend")
                self.editor.insert("insert", "\n")
                return "break"
            self.editor.insert("insert", "\n" + m.group(0))
            return "break"
        m = re.match(r"^(\s*)(\d+)\.\s", line)
        if m:
            full = self.editor.get("insert linestart", "insert lineend")
            if re.match(r"^\s*\d+\.\s*$", full):
                self.editor.delete("insert linestart", "insert lineend")
                self.editor.insert("insert", "\n")
                return "break"
            self.editor.insert("insert", f"\n{m.group(1)}{int(m.group(2)) + 1}. ")
            return "break"
        m = re.match(r"^(\s+)", line)
        if m:
            self.editor.insert("insert", "\n" + m.group(1))
            return "break"
        return None

    def _on_backspace(self, e):
        col = int(self.editor.index("insert").split(".")[1])
        ts = self.dm.settings.get("tab_size", 4)
        if col > 0 and col % ts == 0:
            before = self.editor.get("insert linestart", "insert")
            if before == " " * len(before):
                self.editor.delete(f"insert-{ts}c", "insert")
                return "break"
        return None

    def _auto_close(self, e, pair):
        try:
            sel = self.editor.get("sel.first", "sel.last")
            self.editor.delete("sel.first", "sel.last")
            self.editor.insert("insert", pair[0] + sel + pair[1])
            return "break"
        except tk.TclError:
            pass
        self.editor.insert("insert", pair[0] + pair[1])
        self.editor.mark_set("insert", "insert-1c")
        return "break"

    def _hl_cur_line(self):
        if not self.dm.settings.get("highlight_line", True):
            return
        self.editor.tag_remove("cur_line", "1.0", "end")
        self.editor.tag_add("cur_line", "insert linestart", "insert lineend+1c")

    def _do_hl(self):
        if self.highlighter:
            try:
                self.highlighter.highlight()
            except tk.TclError:
                pass

    # ── Tree Events ──

    def _on_tree_sel(self, e=None):
        sel = self.tree.selection()
        if not sel:
            return
        info = self.sidebar_items.get(sel[0])
        if not info:
            return
        typ, did = info
        if typ == "note":
            if did not in self._open_tabs:
                self._add_tab(did, switch=True)
            else:
                self._switch_tab(did)
        elif typ == "folder":
            self.current_folder = did

    def _on_tree_dbl(self, e=None):
        sel = self.tree.selection()
        if not sel:
            return
        info = self.sidebar_items.get(sel[0])
        if info and info[0] == "folder":
            f = self.dm.data["folders"].get(info[1])
            if f:
                f["expanded"] = not f.get("expanded", False)
                self.dm.save_data()

    def _on_tree_ctx(self, e):
        iid = self.tree.identify_row(e.y)
        if not iid:
            return
        self.tree.selection_set(iid)
        info = self.sidebar_items.get(iid)
        if not info:
            return
        C = self.C
        mkw = dict(bg=C["popup_bg"], fg=C["popup_fg"],
                    activebackground=C["accent"], activeforeground=C["bg"],
                    font=("Segoe UI", 10), bd=0)
        menu = tk.Menu(self.root, tearoff=0, **mkw)
        typ, did = info

        if typ == "folder":
            menu.add_command(label=f" {I.ADD}  New Note Here", command=lambda: self._new_note(folder_id=did))
            menu.add_command(label=f" {I.ADD}  Subfolder", command=lambda: self._new_folder(parent=did))
            menu.add_separator()
            menu.add_command(label="   Rename", command=lambda: self._rename_folder(did))
            menu.add_command(label=f" {I.COLOR}  Color", command=lambda: self._folder_color(did))
            if did != self.dm.data["root_folder"]:
                menu.add_separator()
                menu.add_command(label=f" {I.DELETE}  Delete", command=lambda: self._del_folder(did))
        else:
            n = self.dm.data["notes"].get(did, {})
            menu.add_command(label=f" {I.UNPIN if n.get('pinned') else I.PIN}  {'Unpin' if n.get('pinned') else 'Pin'}", command=lambda: self._toggle_pin(did))
            menu.add_command(label=f" {I.BOOKMARK}  {'Remove' if n.get('bookmarked') else 'Bookmark'}", command=lambda: self._toggle_bm(did))
            fav = did in self.dm.data.get("favorites", [])
            menu.add_command(label=f" {I.STAR}  {'Unfavorite' if fav else 'Favorite'}", command=lambda: self._toggle_fav(did))
            menu.add_separator()
            menu.add_command(label="   Rename", command=lambda: self._rename_note(did))
            menu.add_command(label=f" {I.DUP}  Duplicate", command=lambda: self._dup(did))
            menu.add_command(label=f" {I.COLOR}  Color", command=lambda: self._note_color(did))
            menu.add_command(label="   Word Goal", command=lambda: self._word_goal(did))
            menu.add_separator()
            mv = tk.Menu(menu, tearoff=0, **mkw)
            for fid, fo in self.dm.data["folders"].items():
                mv.add_command(label=f"  {I.FOLDER} {fo['name']}", command=lambda f=fid: self._move(did, f))
            menu.add_cascade(label=f" {I.FOLDER}  Move to...", menu=mv)
            menu.add_separator()
            menu.add_command(label=f" {I.DELETE}  Delete", command=lambda: self._del_note(did))
        menu.post(e.x_root, e.y_root)

    # ── Note Ops ──

    def _open_note(self, nid):
        n = self.dm.data["notes"].get(nid)
        if not n:
            return
        self.current_note = nid
        self.dm.settings["last_note"] = nid
        self.dm._add_recent(nid)
        self.title_var.set(n["title"])
        self.tags_var.set(", ".join(n.get("tags", [])))
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", n["content"])
        self.editor.edit_reset()
        self.editor.edit_modified(False)
        self._snap_counter = 0
        try:
            cdt = datetime.fromisoformat(n.get("created", ""))
            self.meta_label.config(text=cdt.strftime("Created %b %d, %Y"))
        except Exception:
            pass
        self.root.after(50, self._do_hl)
        self.root.after(50, self.line_nums.redraw)
        self._update_status()

    def _save_current(self, e=None):
        if not self.current_note:
            return
        content = self.editor.get("1.0", "end-1c")
        title = self.title_var.get().strip() or "Untitled"
        self.dm.update_note(self.current_note, content=content, title=title)
        self.editor.edit_modified(False)
        self._update_status()
        self.st_left.config(text=f"{I.SAVE} Saved")
        self.root.after(2000, self._update_status)
        self._populate_tree()
        self._sel_in_tree(self.current_note)
        self._update_tab_title(self.current_note)

    def _new_note(self, folder_id=None):
        self._save_current()
        fid = folder_id or self.current_folder
        nid = self.dm.create_note("Untitled", fid, "# New Note\n\n")
        self._populate_tree()
        self._add_tab(nid, switch=True)
        self._sel_in_tree(nid)
        self.title_entry.focus_set()
        self.title_entry.select_range(0, "end")

    def _template_dlg(self):
        C = self.C
        w = tk.Toplevel(self.root)
        w.title("New from Template")
        w.geometry("440x420")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        w.grab_set()
        tk.Label(w, text="Choose Template", font=("Segoe UI", 16, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=14)
        lb = tk.Listbox(w, bg=C["input_bg"], fg=C["input_fg"], font=("Segoe UI", 12),
                        selectbackground=C["select_bg"], selectforeground=C["select_fg"],
                        relief="flat", bd=0, highlightthickness=0, activestyle="none")
        lb.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        names = list(TEMPLATES.keys())
        for n in names:
            lb.insert("end", f"   {I.TEMPLATE}  {n}")

        def create():
            sel = lb.curselection()
            if sel:
                self._save_current()
                nid = self.dm.create_note(names[sel[0]], self.current_folder, template=names[sel[0]])
                self._populate_tree()
                self._add_tab(nid, switch=True)
                self._sel_in_tree(nid)
                w.destroy()

        HoverButton(w, text="  Create  ", command=create,
                    bg=C["accent"], fg=C["bg"],
                    hover_bg=C.get("link_color", C["accent"]),
                    font_spec=("Segoe UI", 11, "bold"), padx=20, pady=6).pack(pady=10)
        lb.bind("<Double-1>", lambda e: create())

    def _dup_current(self):
        if self.current_note:
            self._dup(self.current_note)

    def _dup(self, nid):
        new = self.dm.duplicate_note(nid)
        if new:
            self._populate_tree()
            self._add_tab(new, switch=True)
            self._sel_in_tree(new)

    def _del_note(self, nid):
        n = self.dm.data["notes"].get(nid)
        if not n:
            return
        if messagebox.askyesno("Delete", f'Move "{n["title"]}" to trash?', parent=self.root):
            self.dm.delete_note(nid)
            if nid in self._open_tabs:
                self._close_tab(nid)
            self._populate_tree()

    def _rename_note(self, nid):
        n = self.dm.data["notes"].get(nid)
        if not n:
            return
        name = simpledialog.askstring("Rename", "New name:", initialvalue=n["title"], parent=self.root)
        if name and name.strip():
            self.dm.update_note(nid, title=name.strip())
            if self.current_note == nid:
                self.title_var.set(name.strip())
            self._populate_tree()
            self._sel_in_tree(self.current_note)
            self._update_tab_title(nid)

    def _toggle_pin(self, nid):
        n = self.dm.data["notes"].get(nid)
        if n:
            self.dm.update_note(nid, pinned=not n.get("pinned", False))
            self._populate_tree()
            self._sel_in_tree(self.current_note)
            self._update_tab_title(nid)

    def _toggle_bm(self, nid):
        n = self.dm.data["notes"].get(nid)
        if n:
            self.dm.update_note(nid, bookmarked=not n.get("bookmarked", False))
            self._populate_tree()
            self._sel_in_tree(self.current_note)

    def _toggle_fav(self, nid):
        favs = self.dm.data.setdefault("favorites", [])
        if nid in favs:
            favs.remove(nid)
        else:
            favs.append(nid)
        self.dm.save_data()

    def _note_color(self, nid):
        c = colorchooser.askcolor(title="Note Color", parent=self.root)
        if c[1]:
            self.dm.update_note(nid, color=c[1])

    def _word_goal(self, nid):
        n = self.dm.data["notes"].get(nid)
        if not n:
            return
        g = simpledialog.askinteger("Word Goal", "Set goal (0=disable):",
                                     initialvalue=n.get("word_goal", 0),
                                     minvalue=0, maxvalue=100000, parent=self.root)
        if g is not None:
            self.dm.update_note(nid, word_goal=g)
            self._update_status()

    def _move(self, nid, fid):
        self.dm.move_note(nid, fid)
        self._populate_tree()
        self._sel_in_tree(self.current_note)

    def _save_tags(self, e=None):
        if self.current_note:
            tags = [t.strip() for t in self.tags_var.get().split(",") if t.strip()]
            self.dm.update_note(self.current_note, tags=tags)
            self.st_left.config(text=f"{I.TAG} Tags saved")
            self.root.after(2000, self._update_status)

    # ── Folder Ops ──

    def _new_folder(self, parent=None):
        name = simpledialog.askstring("New Folder", "Name:", parent=self.root)
        if name and name.strip():
            c = colorchooser.askcolor(title="Color", initialcolor="#7c9cde", parent=self.root)
            self.dm.create_folder(name.strip(), parent, c[1] if c[1] else "#7c9cde")
            self._populate_tree()

    def _rename_folder(self, fid):
        f = self.dm.data["folders"].get(fid)
        if not f:
            return
        name = simpledialog.askstring("Rename", "New name:", initialvalue=f["name"], parent=self.root)
        if name and name.strip():
            f["name"] = name.strip()
            self.dm.save_data()
            self._populate_tree()

    def _del_folder(self, fid):
        f = self.dm.data["folders"].get(fid)
        if not f:
            return
        if messagebox.askyesno("Delete", f'Delete "{f["name"]}" and contents?', parent=self.root):
            self.dm.delete_folder(fid)
            self.current_folder = self.dm.data["root_folder"]
            self._populate_tree()

    def _folder_color(self, fid):
        f = self.dm.data["folders"].get(fid)
        if not f:
            return
        c = colorchooser.askcolor(title="Color", initialcolor=f.get("color", "#7c9cde"), parent=self.root)
        if c[1]:
            f["color"] = c[1]
            self.dm.save_data()
            self._populate_tree()

    # ── Search ──

    def _on_search(self):
        q = self.search_var.get().strip()
        if q:
            self._populate_tree(search=self.dm.search(q))
        else:
            self._populate_tree()
            if self.current_note:
                self._sel_in_tree(self.current_note)

    # ── Markdown Ops ──

    def _wrap(self, w):
        try:
            s = self.editor.get("sel.first", "sel.last")
            self.editor.delete("sel.first", "sel.last")
            self.editor.insert("insert", f"{w}{s}{w}")
        except tk.TclError:
            self.editor.insert("insert", f"{w}{w}")
            pos = self.editor.index("insert")
            ln, col = pos.split(".")
            self.editor.mark_set("insert", f"{ln}.{int(col) - len(w)}")
        self.root.after(50, self._do_hl)

    def _ins(self, text):
        self.editor.insert("insert", text)
        self.root.after(50, self._do_hl)

    def _prefix(self, pre):
        ln = self.editor.index("insert").split(".")[0]
        self.editor.insert(f"{ln}.0", pre)
        self.root.after(50, self._do_hl)

    def _ins_codeblock(self):
        try:
            s = self.editor.get("sel.first", "sel.last")
            self.editor.delete("sel.first", "sel.last")
            self.editor.insert("insert", f"\n```\n{s}\n```\n")
        except tk.TclError:
            self.editor.insert("insert", "\n```\n\n```\n")
            pos = self.editor.index("insert")
            ln = int(pos.split(".")[0]) - 2
            self.editor.mark_set("insert", f"{ln}.0")
        self.root.after(50, self._do_hl)

    def _ins_link(self):
        try:
            s = self.editor.get("sel.first", "sel.last")
            self.editor.delete("sel.first", "sel.last")
            self.editor.insert("insert", f"[{s}](url)")
        except tk.TclError:
            self.editor.insert("insert", "[text](url)")
        self.root.after(50, self._do_hl)

    def _ins_table(self):
        self.editor.insert("insert", "\n| Col 1 | Col 2 | Col 3 |\n|-------|-------|-------|\n|       |       |       |\n")
        self.root.after(50, self._do_hl)

    def _cycle_heading(self):
        ln = self.editor.index("insert").split(".")[0]
        line = self.editor.get(f"{ln}.0", f"{ln}.end")
        m = re.match(r"^(#{0,4})\s*", line)
        lvl = len(m.group(1)) if m else 0
        new = (lvl % 4) + 1
        stripped = re.sub(r"^#{0,6}\s*", "", line)
        self.editor.delete(f"{ln}.0", f"{ln}.end")
        self.editor.insert(f"{ln}.0", "#" * new + " " + stripped)
        self.root.after(50, self._do_hl)

    # ── Text Tools ──

    def _sort_lines(self):
        try:
            s = self.editor.get("sel.first", "sel.last")
            lines = sorted(s.split("\n"))
            self.editor.delete("sel.first", "sel.last")
            self.editor.insert("insert", "\n".join(lines))
        except tk.TclError:
            c = self.editor.get("1.0", "end-1c")
            lines = sorted(c.split("\n"))
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", "\n".join(lines))
        self.root.after(50, self._do_hl)

    def _dedup_lines(self):
        c = self.editor.get("1.0", "end-1c")
        lines = c.split("\n")
        seen = set()
        res = []
        for l in lines:
            if l not in seen:
                seen.add(l)
                res.append(l)
        rm = len(lines) - len(res)
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", "\n".join(res))
        self.st_left.config(text=f"Removed {rm} duplicate(s)")
        self.root.after(50, self._do_hl)

    def _trim_ws(self):
        c = self.editor.get("1.0", "end-1c")
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", "\n".join(l.rstrip() for l in c.split("\n")))
        self.st_left.config(text="Trimmed whitespace")
        self.root.after(50, self._do_hl)

    # ── Find ──

    def _show_find(self):
        if self._find_win and self._find_win.winfo_exists():
            self._find_win.lift()
            return
        C = self.C
        self._find_win = w = tk.Toplevel(self.root)
        w.title("Find & Replace")
        w.geometry("480x230")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        w.attributes("-topmost", True)

        f = tk.Frame(w, bg=C["bg"])
        f.pack(fill="both", expand=True, padx=16, pady=12)

        tk.Label(f, text="Find:", bg=C["bg"], fg=C["fg"], font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", pady=5, padx=4)
        fv = tk.StringVar()
        fe = tk.Entry(f, textvariable=fv, bg=C["input_bg"], fg=C["input_fg"],
                      insertbackground=C["cursor_color"], font=("Segoe UI", 11), relief="flat", width=34)
        fe.grid(row=0, column=1, columnspan=3, pady=5, ipady=3, sticky="ew")
        fe.focus_set()

        tk.Label(f, text="Replace:", bg=C["bg"], fg=C["fg"], font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", pady=5, padx=4)
        rv = tk.StringVar()
        tk.Entry(f, textvariable=rv, bg=C["input_bg"], fg=C["input_fg"],
                 insertbackground=C["cursor_color"], font=("Segoe UI", 11), relief="flat", width=34).grid(row=1, column=1, columnspan=3, pady=5, ipady=3, sticky="ew")

        opts = tk.Frame(f, bg=C["bg"])
        opts.grid(row=2, column=0, columnspan=4, pady=4)
        regex_v = tk.BooleanVar(value=False)
        case_v = tk.BooleanVar(value=False)
        for text, var in [("Regex", regex_v), ("Case Sensitive", case_v)]:
            tk.Checkbutton(opts, text=text, variable=var, bg=C["bg"], fg=C["fg"],
                           selectcolor=C["input_bg"], activebackground=C["bg"],
                           font=("Segoe UI", 10)).pack(side="left", padx=8)

        rl = tk.Label(f, text="", bg=C["bg"], fg=C["accent"], font=("Segoe UI", 9))
        rl.grid(row=3, column=0, columnspan=4, pady=2)

        bf2 = tk.Frame(f, bg=C["bg"])
        bf2.grid(row=4, column=0, columnspan=4, pady=6)

        def _find():
            self.editor.tag_remove("fhl", "1.0", "end")
            q = fv.get()
            if not q:
                return
            kw2 = {"nocase": not case_v.get(), "stopindex": "end"}
            if regex_v.get():
                kw2["regexp"] = True
            start = self.editor.index("insert+1c")
            pos = self.editor.search(q, start, **kw2)
            if not pos:
                pos = self.editor.search(q, "1.0", **kw2)
            if pos:
                end_p = f"{pos}+{len(q)}c"
                self.editor.tag_add("fhl", pos, end_p)
                self.editor.tag_configure("fhl", background=C["accent"], foreground=C["bg"])
                self.editor.mark_set("insert", end_p)
                self.editor.see(pos)
                rl.config(text=f"Found at {pos}")
            else:
                rl.config(text="Not found")

        def _rep():
            q = fv.get()
            r = rv.get()
            try:
                sel = self.editor.get("sel.first", "sel.last")
                match = (sel.lower() == q.lower()) if not case_v.get() else (sel == q)
                if match:
                    self.editor.delete("sel.first", "sel.last")
                    self.editor.insert("insert", r)
            except tk.TclError:
                pass
            _find()

        def _rep_all():
            q = fv.get()
            r = rv.get()
            if not q:
                return
            c = self.editor.get("1.0", "end-1c")
            fl = 0 if case_v.get() else re.IGNORECASE
            pattern = q if regex_v.get() else re.escape(q)
            new, cnt = re.subn(pattern, r, c, flags=fl)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", new)
            rl.config(text=f"Replaced {cnt}")
            self.root.after(50, self._do_hl)

        for text, cmd in [("Find", _find), ("Replace", _rep), ("Replace All", _rep_all)]:
            HoverButton(bf2, text=f" {text} ", command=cmd,
                        bg=C["button_bg"], fg=C["button_fg"],
                        hover_bg=C["button_active"],
                        font_spec=("Segoe UI", 10), padx=10, pady=3).pack(side="left", padx=3)
        fe.bind("<Return>", lambda e: _find())
        w.bind("<Escape>", lambda e: w.destroy())

    # ── Preview ──

    def _toggle_preview(self):
        C = self.C
        w = tk.Toplevel(self.root)
        w.title("Preview")
        w.geometry("720x600")
        w.configure(bg=C["bg"])
        content = self.editor.get("1.0", "end-1c")
        ff = self.dm.settings.get("font_family", "Consolas")
        fs = self.dm.settings.get("font_size", 13)

        pv = tk.Text(w, bg=C["editor_bg"], fg=C["editor_fg"], font=(ff, fs),
                     wrap="word", padx=24, pady=16, relief="flat", bd=0,
                     spacing1=3, spacing3=3)
        pv.pack(fill="both", expand=True, padx=6, pady=6)
        pv.tag_configure("ph1", foreground=C["heading_color"], font=("Segoe UI", 24, "bold"), spacing3=10)
        pv.tag_configure("ph2", foreground=C["heading_color"], font=("Segoe UI", 20, "bold"), spacing3=8)
        pv.tag_configure("ph3", foreground=C["heading_color"], font=("Segoe UI", 16, "bold"), spacing3=6)
        pv.tag_configure("pcode", font=("Courier New", 12), background=C["code_bg"], foreground=C["code_fg"])
        pv.tag_configure("pquote", font=("Segoe UI", 13, "italic"), foreground=C["italic_color"], lmargin1=30, lmargin2=30, background=C["code_bg"])
        pv.tag_configure("pbullet", foreground=C["accent"])
        pv.tag_configure("phr", foreground=C["divider"], justify="center")
        pv.tag_configure("pdone", foreground=C["success"])
        pv.tag_configure("pundone", foreground=C["error"])

        in_code = False
        for line in content.split("\n"):
            if line.strip().startswith("```"):
                in_code = not in_code
                pv.insert("end", "\n", "phr")
                continue
            if in_code:
                pv.insert("end", line + "\n", "pcode")
                continue
            m = re.match(r"^(#{1,3})\s+(.*)", line)
            if m:
                pv.insert("end", re.sub(r"[*_`~=]+", "", m.group(2)) + "\n", f"ph{len(m.group(1))}")
                continue
            if re.match(r"^[-_*]{3,}\s*$", line.strip()):
                pv.insert("end", "\u2500" * 50 + "\n", "phr")
                continue
            if line.lstrip().startswith(">"):
                pv.insert("end", "\u2502 " + line.lstrip("> ") + "\n", "pquote")
                continue
            m = re.match(r"^(\s*[-*+]\s)\[([xX])\](.*)", line)
            if m:
                pv.insert("end", "  " + I.CHECK_DONE + m.group(3) + "\n", "pdone")
                continue
            m = re.match(r"^(\s*[-*+]\s)\[ \](.*)", line)
            if m:
                pv.insert("end", "  " + I.CHECK + m.group(2) + "\n", "pundone")
                continue
            m = re.match(r"^(\s*)([-*+])\s+(.*)", line)
            if m:
                pv.insert("end", m.group(1) + "  " + I.BULLET + " " + m.group(3) + "\n", "pbullet")
                continue
            pv.insert("end", line + "\n")
        pv.config(state="disabled")

    # ── Focus ──

    def _toggle_focus(self):
        self.focus_mode = not self.focus_mode
        if self.focus_mode:
            try:
                self.hpane.forget(self.sidebar)
            except Exception:
                self.sidebar.pack_forget()
            self.toolbar.pack_forget()
            self.statusbar.pack_forget()
            self.tab_bar.pack_forget()
        else:
            for w in self.root.winfo_children():
                w.destroy()
            self._build_ui()

    # ── Stats ──

    def _show_stats(self):
        if not self.current_note:
            return
        C = self.C
        stats = self.dm.get_stats(self.current_note)
        note = self.dm.data["notes"].get(self.current_note, {})
        w = tk.Toplevel(self.root)
        w.title("Statistics")
        w.geometry("400x450")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        tk.Label(w, text=f"{I.STATS}  Note Statistics", font=("Segoe UI", 16, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=14)
        f = tk.Frame(w, bg=C["bg"])
        f.pack(padx=28, fill="x")

        items = [("Words", stats["words"]), ("Characters", stats["chars"]),
                 ("Chars (no spaces)", stats["chars_ns"]), ("Lines", stats["lines"]),
                 ("Sentences", stats["sentences"]), ("Paragraphs", stats["paragraphs"]),
                 ("Reading Time", f"~{stats['reading']} min"), ("", ""),
                 ("Snapshots", len(note.get("snapshots", []))),
                 ("Tags", ", ".join(note.get("tags", [])) or "None")]
        try:
            items.insert(8, ("Modified", datetime.fromisoformat(note["modified"]).strftime("%b %d %Y %I:%M %p")))
        except Exception:
            pass
        try:
            items.insert(8, ("Created", datetime.fromisoformat(note["created"]).strftime("%b %d %Y %I:%M %p")))
        except Exception:
            pass

        for i, (l, v) in enumerate(items):
            if not l:
                tk.Frame(f, bg=C["divider"], height=1).grid(row=i, column=0, columnspan=2, sticky="ew", pady=6)
                continue
            tk.Label(f, text=l, bg=C["bg"], fg=C["muted"], font=("Segoe UI", 11), anchor="e").grid(row=i, column=0, sticky="e", padx=(0, 14), pady=3)
            tk.Label(f, text=str(v), bg=C["bg"], fg=C["fg"], font=("Segoe UI", 11, "bold"), anchor="w").grid(row=i, column=1, sticky="w", pady=3)

        goal = note.get("word_goal", 0)
        if goal > 0:
            pct = min(100, int(stats["words"] / goal * 100))
            r = len(items) + 1
            tk.Label(f, text=f"Goal: {stats['words']}/{goal} ({pct}%)", bg=C["bg"], fg=C["accent"], font=("Segoe UI", 11, "bold")).grid(row=r, column=0, columnspan=2, pady=8)
            bar = tk.Frame(f, bg=C["divider"], height=10)
            bar.grid(row=r + 1, column=0, columnspan=2, sticky="ew", pady=4)
            tk.Frame(bar, bg=C["success"] if pct >= 100 else C["accent"], height=10).place(relwidth=min(1.0, pct / 100), relheight=1.0)

    # ── History ──

    def _show_history(self):
        if not self.current_note:
            return
        C = self.C
        note = self.dm.data["notes"].get(self.current_note, {})
        snaps = note.get("snapshots", [])
        w = tk.Toplevel(self.root)
        w.title("Version History")
        w.geometry("700x500")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        tk.Label(w, text=f"{I.HISTORY}  Version History", font=("Segoe UI", 14, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=10)
        if not snaps:
            tk.Label(w, text="No snapshots yet.", bg=C["bg"], fg=C["muted"], font=("Segoe UI", 12)).pack(pady=40)
            return
        pane = tk.PanedWindow(w, orient="horizontal", bg=C["border"], sashwidth=2)
        pane.pack(fill="both", expand=True, padx=8, pady=8)
        lf = tk.Frame(pane, bg=C["sidebar_bg"])
        pane.add(lf, minsize=180)
        lb = tk.Listbox(lf, bg=C["sidebar_bg"], fg=C["sidebar_fg"], font=("Segoe UI", 10),
                        selectbackground=C["select_bg"], selectforeground=C["select_fg"],
                        relief="flat", bd=0, highlightthickness=0)
        lb.pack(fill="both", expand=True)
        for i2, s in enumerate(reversed(snaps)):
            try:
                lb.insert("end", "  " + datetime.fromisoformat(s["ts"]).strftime("%b %d %I:%M %p"))
            except Exception:
                lb.insert("end", f"  Snapshot {len(snaps) - i2}")
        pf = tk.Frame(pane, bg=C["bg"])
        pane.add(pf)
        preview = tk.Text(pf, bg=C["editor_bg"], fg=C["editor_fg"], font=("Consolas", 12),
                          wrap="word", relief="flat", padx=10, pady=8)
        preview.pack(fill="both", expand=True)

        def on_sel(e=None):
            sel2 = lb.curselection()
            if not sel2:
                return
            idx = len(snaps) - 1 - sel2[0]
            preview.config(state="normal")
            preview.delete("1.0", "end")
            preview.insert("1.0", snaps[idx]["content"])
            preview.config(state="disabled")
        lb.bind("<<ListboxSelect>>", on_sel)

        def restore():
            sel2 = lb.curselection()
            if not sel2:
                return
            idx = len(snaps) - 1 - sel2[0]
            if messagebox.askyesno("Restore", "Restore this version?", parent=w):
                self.dm.take_snapshot(self.current_note)
                self.dm.update_note(self.current_note, content=snaps[idx]["content"])
                self._open_note(self.current_note)
                w.destroy()

        HoverButton(w, text="  Restore Selected  ", command=restore,
                    bg=C["accent"], fg=C["bg"],
                    hover_bg=C.get("link_color", C["accent"]),
                    font_spec=("Segoe UI", 10, "bold"), padx=16, pady=6).pack(pady=8)

    # ── Trash / Favorites / Recent ──

    def _show_list_dlg(self, title, icon, items, extra_btns=None):
        C = self.C
        w = tk.Toplevel(self.root)
        w.title(title)
        w.geometry("480x400")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        tk.Label(w, text=f"{icon}  {title}", font=("Segoe UI", 16, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=10)
        lb = tk.Listbox(w, bg=C["input_bg"], fg=C["input_fg"], font=("Segoe UI", 11),
                        selectbackground=C["select_bg"], selectforeground=C["select_fg"],
                        relief="flat", bd=0, highlightthickness=0, activestyle="none")
        lb.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        ids = []
        for nid in items:
            n = self.dm.data["notes"].get(nid)
            if n:
                lb.insert("end", f"   {I.NOTE}  {n['title']}")
                ids.append(nid)
        if not ids:
            lb.insert("end", "   Empty")

        def open_sel(e=None):
            sel2 = lb.curselection()
            if sel2 and sel2[0] < len(ids):
                self._save_current()
                nid2 = ids[sel2[0]]
                if nid2 not in self._open_tabs:
                    self._add_tab(nid2, switch=True)
                else:
                    self._switch_tab(nid2)
                self._populate_tree()
                self._sel_in_tree(nid2)
                w.destroy()
        lb.bind("<Double-1>", open_sel)
        bf2 = tk.Frame(w, bg=C["bg"])
        bf2.pack(pady=8)
        HoverButton(bf2, text="  Open  ", command=open_sel,
                    bg=C["accent"], fg=C["bg"],
                    hover_bg=C.get("link_color", C["accent"]),
                    font_spec=("Segoe UI", 10, "bold"), padx=14, pady=4).pack(side="left", padx=4)

        if extra_btns:
            for text, cmd_fn, bg_c in extra_btns:
                def make(fn2):
                    def action():
                        sel2 = lb.curselection()
                        if sel2 and sel2[0] < len(ids):
                            fn2(ids[sel2[0]], lb, ids, w)
                    return action
                HoverButton(bf2, text=f"  {text}  ", command=make(cmd_fn),
                            bg=bg_c, fg="#ffffff",
                            hover_bg=bg_c,
                            font_spec=("Segoe UI", 10), padx=10, pady=4).pack(side="left", padx=4)

    def _show_trash(self):
        C = self.C

        def restore(nid2, lb2, ids2, w2):
            self.dm.restore_note(nid2)
            idx = ids2.index(nid2)
            lb2.delete(idx)
            ids2.remove(nid2)
            self._populate_tree()

        def perm_del(nid2, lb2, ids2, w2):
            if messagebox.askyesno("Delete", "Permanently delete?", parent=w2):
                if nid2 in self.dm.data["notes"]:
                    del self.dm.data["notes"][nid2]
                if nid2 in self.dm.data.get("trash", []):
                    self.dm.data["trash"].remove(nid2)
                self.dm.save_data()
                idx = ids2.index(nid2)
                lb2.delete(idx)
                ids2.remove(nid2)

        self._show_list_dlg("Trash", I.TRASH, self.dm.data.get("trash", []),
                             extra_btns=[
                                 (f"{I.HISTORY} Restore", restore, C["success"]),
                                 (f"{I.DELETE} Delete", perm_del, C["error"]),
                             ])

    def _show_favorites(self):
        self._show_list_dlg("Favorites", I.STAR,
                             [n for n in self.dm.data.get("favorites", [])
                              if n not in self.dm.data.get("trash", [])])

    def _show_recent(self):
        self._show_list_dlg("Recent", I.CLOCK,
                             [n for n in self.dm.data.get("recent", [])
                              if n not in self.dm.data.get("trash", [])])

    # ── Export / Import ──

    def _export_md(self):
        if not self.current_note:
            return
        n = self.dm.data["notes"][self.current_note]
        p = filedialog.asksaveasfilename(defaultextension=".md",
                                         filetypes=[("Markdown", "*.md")],
                                         initialfile=f"{n['title']}.md", parent=self.root)
        if p:
            with open(p, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", "end-1c"))
            self.st_left.config(text=f"{I.EXPORT} Exported: {os.path.basename(p)}")

    def _export_html(self):
        if not self.current_note:
            return
        n = self.dm.data["notes"][self.current_note]
        c = self.editor.get("1.0", "end-1c")
        body = markdown2.markdown(c, extras=["fenced-code-blocks", "tables", "strike", "task_list"]) if HAS_MD else f"<pre>{c}</pre>"
        C = self.C
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{n['title']}</title>
<style>body{{font-family:'Segoe UI',sans-serif;max-width:800px;margin:40px auto;padding:20px;background:{C['bg']};color:{C['fg']};line-height:1.8}}
h1,h2,h3{{color:{C['heading_color']};border-bottom:1px solid {C['divider']};padding-bottom:6px}}
code{{background:{C['code_bg']};color:{C['code_fg']};padding:2px 6px;border-radius:3px}}
pre{{background:{C['code_bg']};padding:16px;border-radius:6px;overflow-x:auto}}pre code{{padding:0;background:none}}
blockquote{{border-left:4px solid {C['accent']};margin:0;padding:8px 16px;color:{C['italic_color']}}}
a{{color:{C['link_color']}}}hr{{border:1px solid {C['divider']}}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid {C['divider']};padding:8px 12px;text-align:left}}
th{{background:{C['code_bg']}}}</style></head><body><h1>{n['title']}</h1>{body}</body></html>"""
        p = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")],
                                         initialfile=f"{n['title']}.html", parent=self.root)
        if p:
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            self.st_left.config(text=f"{I.EXPORT} HTML exported")

    def _import_md(self):
        p = filedialog.askopenfilename(filetypes=[("Markdown", "*.md"), ("Text", "*.txt"), ("All", "*.*")], parent=self.root)
        if p:
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            title = os.path.splitext(os.path.basename(p))[0]
            nid = self.dm.create_note(title, self.current_folder, content)
            self._populate_tree()
            self._add_tab(nid, switch=True)
            self._sel_in_tree(nid)
            self.st_left.config(text=f"{I.IMPORT} Imported: {os.path.basename(p)}")

    # ── Theme ──

    def _apply_theme(self, name):
        if name not in THEMES:
            return
        self.theme_name = name
        self.C = THEMES[name]
        self.dm.settings["theme"] = name
        self.dm.save_settings()
        for w in self.root.winfo_children():
            w.destroy()
        self._build_ui()

    # ── Font ──

    def _font_delta(self, d):
        s = max(8, min(32, self.dm.settings.get("font_size", 13) + d))
        self.dm.settings["font_size"] = s
        self.dm.save_settings()
        ff = self.dm.settings.get("font_family", "Consolas")
        self.editor.configure(font=(ff, s))
        if self.highlighter:
            self.highlighter.update(self.C, ff, s)
            self.root.after(50, self._do_hl)
        self.st_left.config(text=f"Font: {s}pt")

    # ── Preferences ──

    def _show_prefs(self):
        C = self.C
        w = tk.Toplevel(self.root)
        w.title("Preferences")
        w.geometry("520x580")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        w.grab_set()
        tk.Label(w, text=f"{I.GEAR}  Preferences", font=("Segoe UI", 16, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=14)
        f = tk.Frame(w, bg=C["bg"])
        f.pack(fill="both", expand=True, padx=28)
        s = self.dm.settings
        row = [0]

        def add_row(label):
            tk.Label(f, text=label, bg=C["bg"], fg=C["fg"], font=("Segoe UI", 11), anchor="e").grid(row=row[0], column=0, sticky="e", padx=(0, 12), pady=5)
            r = row[0]
            row[0] += 1
            return r

        r = add_row("Font:")
        font_v = tk.StringVar(value=s.get("font_family", "Consolas"))
        ttk.Combobox(f, textvariable=font_v, values=FONT_FAMILIES, state="readonly", width=22).grid(row=r, column=1, sticky="w", pady=5)

        r = add_row("Size:")
        size_v = tk.IntVar(value=s.get("font_size", 13))
        tk.Spinbox(f, from_=8, to=32, textvariable=size_v, width=6, bg=C["input_bg"], fg=C["input_fg"], font=("Segoe UI", 11)).grid(row=r, column=1, sticky="w", pady=5)

        r = add_row("Tab Size:")
        tab_v = tk.IntVar(value=s.get("tab_size", 4))
        tk.Spinbox(f, from_=2, to=8, textvariable=tab_v, width=6, bg=C["input_bg"], fg=C["input_fg"], font=("Segoe UI", 11)).grid(row=r, column=1, sticky="w", pady=5)

        r = add_row("Reading WPM:")
        wpm_v = tk.IntVar(value=s.get("reading_wpm", 200))
        tk.Spinbox(f, from_=100, to=500, textvariable=wpm_v, width=6, bg=C["input_bg"], fg=C["input_fg"], font=("Segoe UI", 11)).grid(row=r, column=1, sticky="w", pady=5)

        r = add_row("Snapshot Interval:")
        snap_v = tk.IntVar(value=s.get("snap_interval", 30))
        tk.Spinbox(f, from_=5, to=200, textvariable=snap_v, width=6, bg=C["input_bg"], fg=C["input_fg"], font=("Segoe UI", 11)).grid(row=r, column=1, sticky="w", pady=5)

        tk.Frame(f, bg=C["divider"], height=1).grid(row=row[0], column=0, columnspan=2, sticky="ew", pady=8)
        row[0] += 1

        checks = {}
        for label, key in [("Word Wrap", "word_wrap"), ("Line Numbers", "line_numbers"),
                            ("Auto Save", "auto_save"), ("Highlight Line", "highlight_line"),
                            ("Auto Brackets", "auto_bracket"), ("Auto Indent", "auto_indent"),
                            ("Show Toolbar", "show_toolbar"), ("Show Status Bar", "show_statusbar")]:
            v = tk.BooleanVar(value=s.get(key, True))
            checks[key] = v
            tk.Checkbutton(f, text=label, variable=v, bg=C["bg"], fg=C["fg"],
                           selectcolor=C["input_bg"], activebackground=C["bg"],
                           font=("Segoe UI", 11)).grid(row=row[0], column=0, columnspan=2, sticky="w", pady=2)
            row[0] += 1

        def apply():
            s["font_family"] = font_v.get()
            s["font_size"] = size_v.get()
            s["tab_size"] = tab_v.get()
            s["reading_wpm"] = wpm_v.get()
            s["snap_interval"] = snap_v.get()
            for k2, v2 in checks.items():
                s[k2] = v2.get()
            self.dm.save_settings()
            w.destroy()
            for child in self.root.winfo_children():
                child.destroy()
            self._build_ui()

        HoverButton(w, text="  Apply  ", command=apply,
                    bg=C["accent"], fg=C["bg"],
                    hover_bg=C.get("link_color", C["accent"]),
                    font_spec=("Segoe UI", 11, "bold"), padx=20, pady=6).pack(pady=14)

    # ── Password ──

    def _change_pwd(self):
        C = self.C
        w = tk.Toplevel(self.root)
        w.title("Change Password")
        w.geometry("420x300")
        w.configure(bg=C["bg"])
        w.transient(self.root)
        w.grab_set()
        tk.Label(w, text=f"{I.LOCK}  Change Password", font=(self._serif, 15, "bold"),
                 bg=C["bg"], fg=C["fg"]).pack(pady=14)
        f = tk.Frame(w, bg=C["bg"])
        f.pack(padx=24)
        vars_list = []
        for lbl in ["Current:", "New:", "Confirm:"]:
            tk.Label(f, text=lbl, bg=C["bg"], fg=C["fg"], font=("Segoe UI", 11)).grid(row=len(vars_list), column=0, sticky="e", padx=6, pady=6)
            v = tk.StringVar()
            tk.Entry(f, textvariable=v, show=I.DOT, bg=C["input_bg"], fg=C["input_fg"],
                     font=("Segoe UI", 12), relief="flat", width=20).grid(row=len(vars_list), column=1, pady=6, ipady=3)
            vars_list.append(v)
        msg = tk.Label(w, text="", bg=C["bg"], fg=C["error"], font=("Segoe UI", 10))
        msg.pack(pady=4)

        def change():
            if hashlib.sha256(vars_list[0].get().encode()).hexdigest() != self.dm.settings["password_hash"]:
                msg.config(text="Incorrect current password")
                return
            if vars_list[1].get() != vars_list[2].get():
                msg.config(text="Passwords don't match")
                return
            if len(vars_list[1].get()) < 4:
                msg.config(text="Min 4 characters")
                return
            self.dm.settings["password_hash"] = hashlib.sha256(vars_list[1].get().encode()).hexdigest()
            self.dm.save_settings()
            messagebox.showinfo("Done", "Password changed!", parent=w)
            w.destroy()

        HoverButton(w, text="  Change  ", command=change,
                    bg=C["accent"], fg=C["bg"],
                    hover_bg=C.get("link_color", C["accent"]),
                    font_spec=("Segoe UI", 11, "bold"), padx=16, pady=6).pack(pady=10)

    # ── Lock ──

    def _lock_app(self):
        self._save_current()
        self.dm.settings["locked"] = True
        self.dm.save_settings()
        self.is_locked = True
        for w in self.root.winfo_children():
            w.destroy()
        self._show_lock_screen()

    # ── Auto Save ──

    def _auto_save_loop(self):
        if self.dm.settings.get("auto_save") and not self.is_locked:
            self._save_current()
        self.root.after(self.dm.settings.get("auto_save_ms", 3000), self._auto_save_loop)

    # ── Global Hotkey: Win+Shift+Q ──

    def _start_hotkey(self):
        if not HAS_PYNPUT:
            return
        pressed = set()

        def on_press(key):
            pressed.add(key)
            win_keys = {pynput_kb.Key.cmd, pynput_kb.Key.cmd_l, pynput_kb.Key.cmd_r}
            shift_keys = {pynput_kb.Key.shift, pynput_kb.Key.shift_l, pynput_kb.Key.shift_r}
            win_p = bool(pressed & win_keys)
            shift_p = bool(pressed & shift_keys)
            q_p = False
            try:
                for k in pressed:
                    if hasattr(k, "char") and k.char and k.char.lower() == "q":
                        q_p = True
                        break
            except Exception:
                pass
            if win_p and shift_p and q_p:
                self.root.after(0, self._toggle_vis)
                pressed.clear()

        def on_release(key):
            pressed.discard(key)

        listener = pynput_kb.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    def _toggle_vis(self):
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
        else:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.is_visible = True
            if self.is_locked:
                try:
                    self.pass_entry.focus_set()
                except Exception:
                    pass
            else:
                try:
                    self.editor.focus_set()
                except Exception:
                    pass

    # ── Close ──

    def _on_close(self):
        if not self.is_locked:
            self._save_current()
            self.dm.settings["open_tabs"] = list(self._open_tabs.keys())
            self.dm.settings["active_tab"] = self.current_note
        try:
            self.dm.settings["geometry"] = self.root.geometry()
        except Exception:
            pass
        self.dm.save_settings()
        self.dm.save_data()
        self.root.destroy()


if __name__ == "__main__":
    app = QuickNoteApp()
