import sys
import os
import json
import winreg
import ctypes
import ctypes.wintypes
from pathlib import Path
import threading
import uuid
import difflib

from PySide6.QtCore import (
    Qt, QPoint, Signal, QFileSystemWatcher, QTimer, QEvent, QRect, QMimeData
)
from PySide6.QtGui import (
    QColor, QCursor, QFont, QIcon, QPainter, QPainterPath, QKeySequence, QShortcut, QPixmap
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QCheckBox, QPushButton, QSpacerItem, 
    QSizePolicy, QFrame, QGraphicsDropShadowEffect, QTreeWidget, QTreeWidgetItem,
    QMessageBox, QInputDialog, QAbstractItemView, QMenu,
    QSizeGrip, QDialog, QFormLayout, QComboBox, QFontComboBox, QSpinBox,
    QFileDialog, QTextEdit, QListWidget, QListWidgetItem, QTextBrowser, QColorDialog
)

import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".foldercheck_settings.json"

DEFAULT_SETTINGS = {
    "font_family": "Segoe UI Variable Display",
    "font_size": 13,
    "default_lines": 15,
    "theme": "Dark"
}

THEMES = {
    "Dark": {
        "bg_color": "rgba(30, 30, 34, 0.95)",
        "text_color": "#E0E0E0",
        "border_color": "rgba(255, 255, 255, 0.1)",
        "input_bg": "rgba(255, 255, 255, 0.05)",
        "input_focus_border": "#4DAAF2",
        "menu_bg": "#2b2b2b",
        "menu_selected": "rgba(77, 170, 242, 0.5)",
        "accent": "#4DAAF2",
        "hover_bg": "rgba(255, 255, 255, 0.03)",
        "btn_hover": "rgba(255, 255, 255, 0.1)",
        "checkbox_border": "rgba(255, 255, 255, 0.3)",
        "checkbox_bg": "rgba(0, 0, 0, 0.2)",
        "title_color": "#FFFFFF",
        "faint_text": "rgba(255, 255, 255, 0.4)",
        "faint_icon": "rgba(255, 255, 255, 0.3)",
        "bar_color": "rgba(77, 170, 242, 30)",
        "sel_border": "rgba(77, 170, 242, 200)",
        "sel_fill": "rgba(77, 170, 242, 20)",
        "shadow": "rgba(0, 0, 0, 150)",
    },
    "Light": {
        "bg_color": "rgba(250, 250, 250, 0.95)",
        "text_color": "#2E2E2E",
        "border_color": "rgba(0, 0, 0, 0.1)",
        "input_bg": "rgba(0, 0, 0, 0.05)",
        "input_focus_border": "#0078D4",
        "menu_bg": "#F5F5F5",
        "menu_selected": "rgba(0, 120, 212, 0.3)",
        "accent": "#0078D4",
        "hover_bg": "rgba(0, 0, 0, 0.03)",
        "btn_hover": "rgba(0, 0, 0, 0.08)",
        "checkbox_border": "rgba(0, 0, 0, 0.3)",
        "checkbox_bg": "rgba(255, 255, 255, 0.5)",
        "title_color": "#111111",
        "faint_text": "rgba(0, 0, 0, 0.4)",
        "faint_icon": "rgba(0, 0, 0, 0.3)",
        "bar_color": "rgba(0, 120, 212, 30)",
        "sel_border": "rgba(0, 120, 212, 200)",
        "sel_fill": "rgba(0, 120, 212, 20)",
        "shadow": "rgba(0, 0, 0, 50)",
    },
    "Dracula": {
        "bg_color": "rgba(40, 42, 54, 0.95)",
        "text_color": "#F8F8F2",
        "border_color": "rgba(98, 114, 164, 0.5)",
        "input_bg": "rgba(68, 71, 90, 0.5)",
        "input_focus_border": "#FF79C6",
        "menu_bg": "#282A36",
        "menu_selected": "rgba(255, 121, 198, 0.5)",
        "accent": "#FF79C6",
        "hover_bg": "rgba(68, 71, 90, 0.3)",
        "btn_hover": "rgba(68, 71, 90, 0.5)",
        "checkbox_border": "rgba(98, 114, 164, 0.8)",
        "checkbox_bg": "rgba(40, 42, 54, 0.5)",
        "title_color": "#50FA7B",
        "faint_text": "rgba(248, 248, 242, 0.4)",
        "faint_icon": "rgba(248, 248, 242, 0.3)",
        "bar_color": "rgba(255, 121, 198, 40)",
        "sel_border": "rgba(255, 121, 198, 200)",
        "sel_fill": "rgba(255, 121, 198, 20)",
        "shadow": "rgba(0, 0, 0, 180)",
    },
    "Nord": {
        "bg_color": "rgba(46, 52, 64, 0.95)",
        "text_color": "#D8DEE9",
        "border_color": "rgba(76, 86, 106, 0.5)",
        "input_bg": "rgba(59, 66, 82, 0.5)",
        "input_focus_border": "#88C0D0",
        "menu_bg": "#3B4252",
        "menu_selected": "rgba(136, 192, 208, 0.5)",
        "accent": "#88C0D0",
        "hover_bg": "rgba(67, 76, 94, 0.3)",
        "btn_hover": "rgba(67, 76, 94, 0.5)",
        "checkbox_border": "rgba(76, 86, 106, 0.8)",
        "checkbox_bg": "rgba(46, 52, 64, 0.5)",
        "title_color": "#ECEFF4",
        "faint_text": "rgba(216, 222, 233, 0.4)",
        "faint_icon": "rgba(216, 222, 233, 0.3)",
        "bar_color": "rgba(136, 192, 208, 40)",
        "sel_border": "rgba(136, 192, 208, 200)",
        "sel_fill": "rgba(136, 192, 208, 20)",
        "shadow": "rgba(0, 0, 0, 150)",
    }
}

class SettingsManager:
    @staticmethod
    def load():
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in DEFAULT_SETTINGS.items():
                        if k not in data:
                            data[k] = v
                    return data
            except Exception:
                pass
        return DEFAULT_SETTINGS.copy()

    @staticmethod
    def save(settings):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

STYLESHEET_TEMPLATE = """
QWidget {{
    font-family: '{font_family}', 'Segoe UI', 'Inter', sans-serif;
    font-size: {font_size}px;
    color: {text_color};
}}

QTreeWidget {{
    background: transparent;
    border: none;
    outline: none;
}}

QTreeWidget::item {{
    background: transparent;
    padding: 2px 0px;
    border-radius: 4px;
}}

QTreeWidget::item:hover {{
    background: transparent;
}}

QTreeWidget::item:selected {{
    background: transparent;
}}

QTreeWidget::branch:has-siblings:!adjoins-item {{
    border-image: none;
}}
QTreeWidget::branch:has-siblings:adjoins-item {{
    border-image: none;
}}
QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {{
    border-image: none;
}}
QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {{
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNhYWFhYWEiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNOSAxOGw2LTZtMCwwbC02LTYiLz48L3N2Zz4=);
}}
QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings  {{
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNhYWFhYWEiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNiA5bDYgNm0wLDBsNi02Ii8+PC9zdmc+);
}}

QScrollBar:vertical {{
    border: none;
    background: transparent;
    width: 6px;
    margin: 0px 0px 0px 0px;
}}
QScrollBar::handle:vertical {{
    background: {border_color};
    min-height: 20px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical:hover {{
    background: {accent};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QLineEdit {{
    background-color: {input_bg};
    border: 1px solid {border_color};
    border-radius: 6px;
    padding: 8px 12px;
    color: {text_color};
}}
QLineEdit:focus {{
    border: 1px solid {input_focus_border};
    background-color: {input_bg};
}}

QPushButton.icon-btn {{
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 4px;
    color: {text_color};
}}
QPushButton.icon-btn:hover {{
    background: {btn_hover};
}}

QPushButton.generate-btn {{
    background: {btn_hover};
    color: {accent};
    border: 1px solid {border_color};
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 11px;
}}
QPushButton.generate-btn:hover {{
    background: {menu_selected};
}}

QCheckBox {{
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid {checkbox_border};
    background: {checkbox_bg};
}}
QCheckBox::indicator:hover {{
    border: 1px solid {accent};
    background: {btn_hover};
}}
QCheckBox::indicator:checked {{
    background: {accent};
    border: 1px solid {accent};
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0yMCA2TDEwIDE3bS01LTVsNS01Ii8+PC9zdmc+);
}}

QMenu {{ 
    background-color: {menu_bg}; 
    color: {text_color}; 
    border: 1px solid {border_color}; 
    border-radius: 4px; 
    padding: 4px;
}}
QMenu::item {{
    padding: 6px 24px 6px 24px;
    border-radius: 4px;
}}
QMenu::item:selected {{ 
    background-color: {menu_selected}; 
}}

QDialog {{
    background-color: {menu_bg};
    color: {text_color};
}}
QLabel {{
    color: {text_color};
}}
QComboBox, QFontComboBox, QSpinBox {{
    background-color: {input_bg};
    border: 1px solid {border_color};
    border-radius: 4px;
    padding: 4px;
    color: {text_color};
}}
QComboBox:focus, QFontComboBox:focus, QSpinBox:focus {{
    border: 1px solid {input_focus_border};
}}
"""
PRESET_COLORS = {
    "Default (Clear)": "transparent",
    "Red": "rgba(255, 89, 94, 0.25)",
    "Orange": "rgba(255, 202, 58, 0.25)",
    "Yellow": "rgba(243, 222, 138, 0.25)",
    "Green": "rgba(138, 201, 38, 0.25)",
    "Cyan": "rgba(25, 130, 196, 0.25)",
    "Blue": "rgba(66, 135, 245, 0.25)",
    "Purple": "rgba(106, 76, 147, 0.25)",
    "Pink": "rgba(255, 153, 200, 0.25)",
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_registry():
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(pythonw_path):
            pythonw_path = sys.executable
        exe_path = f'"{pythonw_path}" "{os.path.abspath(__file__)}"'
    
    prog_id = "FolderCheck.File"
    ext = ".check"

    try:
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, prog_id) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "FolderCheck Checklist")
            with winreg.CreateKey(key, "DefaultIcon") as icon_key:
                winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, f"{sys.executable},0")
            with winreg.CreateKey(key, r"shell\open\command") as cmd_key:
                if getattr(sys, 'frozen', False):
                    command = f'"{exe_path}" "%1"'
                else:
                    command = f'{exe_path} "%1"'
                winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, command)

        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, prog_id)
            with winreg.CreateKey(key, "ShellNew") as shellnew_key:
                winreg.SetValueEx(shellnew_key, "Data", 0, winreg.REG_SZ, '{"items": []}')

        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        return True
    except Exception as e:
        print(e)
        return False


class NodeWidget(QWidget):
    changed = Signal()
    deleted = Signal(object) # pass self
    request_generate = Signal(object)
    request_rename = Signal(object, str, str) # self, old_name, new_name

    def __init__(self, tree_item, item_data, app_ref):
        super().__init__()
        self.tree_item = tree_item
        self.item_data = item_data
        self.app_ref = app_ref
        
        self.setAttribute(Qt.WA_Hover)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.installEventFilter(self)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 2, 8, 2)
        self.layout.setSpacing(6)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(item_data.get("done", False))
        self.checkbox.stateChanged.connect(self.on_check_changed)

        # Icon (dot for file, square for folder)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(16, 16)
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        self.label = QLabel(item_data.get("text", ""))
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.status_icons = QLabel()
        
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("font-size: 11px;") # Color set via theme

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setProperty("class", "icon-btn")
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.clicked.connect(lambda: self.deleted.emit(self))
        self.delete_btn.hide()

        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.status_icons)
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.delete_btn)

        self.progress_ratio = 0.0

    def get_target_widgets(self):
        selected_items = self.app_ref.tree.selectedItems()
        if self.tree_item in selected_items:
            return [self.app_ref.tree.itemWidget(item, 0) for item in selected_items if self.app_ref.tree.itemWidget(item, 0)]
        return [self]

    def get_relative_path(self):
        # Calculate full relative path by traversing tree parents
        parts = []
        node = self.tree_item
        while node is not None:
            w = self.app_ref.tree.itemWidget(node, 0)
            if w:
                parts.insert(0, w.item_data.get("text", ""))
            node = node.parent()
        return os.path.join(*parts) if parts else ""

    def is_folder(self):
        children = self.item_data.get("children", [])
        text = self.item_data.get("text", "")
        if children:
            return True
        if '.' not in text or text.startswith('.') or text.endswith('.'):
            return True
        return False

    def on_check_changed(self, state):
        done_state = (state == 2)
        for w in self.get_target_widgets():
            w.item_data["done"] = done_state
            w.checkbox.blockSignals(True)
            w.checkbox.setChecked(done_state)
            w.checkbox.blockSignals(False)
            w.update_ui_state()
        self.changed.emit()

    def on_generate_clicked(self):
        for w in self.get_target_widgets():
            w.request_generate.emit(w)

    def update_ui_state(self):
        text = self.item_data.get("text", "")
        done = self.item_data.get("done", False)
        children = self.item_data.get("children", [])
        
        rel_path = self.get_relative_path()
        full_path = self.app_ref.root_dir / rel_path if rel_path else None
        
        # Smart Path: If doesn't exist, try fuzzy search
        file_exists = False
        self.fuzzy_match = None
        validation_failed = False
        
        if full_path and full_path.exists():
            file_exists = True
            
            # File validation logic
            val_rule = self.item_data.get("validation", {})
            val_type = val_rule.get("type", "none")
            val_val = val_rule.get("value", "")
            
            if not self.is_folder() and val_type != "none":
                try:
                    if val_type == "not_empty":
                        if full_path.stat().st_size == 0:
                            validation_failed = True
                    elif val_type == "contains" and val_val:
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                content_txt = f.read()
                                if val_val not in content_txt:
                                    validation_failed = True
                        except UnicodeDecodeError:
                            validation_failed = True # Binary file?
                except Exception:
                    validation_failed = True
                    
        elif full_path and not full_path.exists() and full_path.parent.exists():
            # Fuzzy search in parent directory
            try:
                candidates = [f.name for f in full_path.parent.iterdir()]
                matches = difflib.get_close_matches(text, candidates, n=1, cutoff=0.7)
                if matches:
                    self.fuzzy_match = matches[0]
            except Exception:
                pass
            
        # Icon
        is_f = self.is_folder()
        theme_name = self.app_ref.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])

        if is_f:
            self.icon_label.setText("■") # Minimal square
            self.icon_label.setStyleSheet(f"color: {theme['faint_icon']}; font-size: 10px;")
        else:
            self.icon_label.setText("●") # Minimal dot
            self.icon_label.setStyleSheet(f"color: {theme['faint_icon']}; font-size: 8px;")
        self.progress_label.setStyleSheet(f"color: {theme['faint_text']}; font-size: 11px;")

        # Progress
        if children:
            total = len(children)
            completed = sum(1 for c in children if c.get("done", False))
            self.progress_label.setText(f"[{completed}/{total}]")
            self.progress_ratio = completed / total if total > 0 else 0
            
            # Auto complete parent
            if completed == total and total > 0 and not done:
                self.checkbox.setChecked(True) # will trigger changed
        else:
            self.progress_label.setText("")
            self.progress_ratio = 0.0

        # Style logic
        font = self.label.font()
        font.setBold(bool(children))
        font.setStrikeOut(done)
        self.label.setFont(font)

        if done:
            self.label.setStyleSheet(f"color: {theme['faint_text']};")
        elif hasattr(self, 'fuzzy_match') and self.fuzzy_match:
            self.label.setStyleSheet("color: #FFCA3A;") # Yellow for warning
        elif file_exists and validation_failed:
            self.label.setStyleSheet("color: #FF595E;") # Red for validation fail
        elif file_exists:
            self.label.setStyleSheet(f"color: {theme['accent']};")
        else:
            self.label.setStyleSheet(f"color: {theme['text_color']};")
            
        # Status Icons
        icons = []
        if self.item_data.get("notes", "").strip():
            icons.append("📝")
        if self.item_data.get("validation", {}).get("type", "none") != "none":
            icons.append("✔️")
        
        # Dependency locking
        dep_id = self.item_data.get("depends_on")
        is_locked = False
        if dep_id:
            # check if dependency is done
            def _find_dep(items):
                for it in items:
                    if it.get("id") == dep_id: return it
                    res = _find_dep(it.get("children", []))
                    if res: return res
                return None
            
            dep_node = _find_dep(self.app_ref.tree_data.get("items", []))
            if dep_node and not dep_node.get("done"):
                is_locked = True
                icons.append("🔒")
                
        self.checkbox.setEnabled(not is_locked)
        
        self.status_icons.setText(" ".join(icons))
        self.status_icons.setStyleSheet(f"color: {theme['faint_text']}; font-size: 11px;")
        
        notes_text = self.item_data.get("notes", "").strip()
        if notes_text:
            if "<" in notes_text and ">" in notes_text:
                self.setToolTip(notes_text)
            else:
                fs = self.app_ref.settings.get("font_size", 13) + 2
                formatted_text = notes_text.replace('\n', '<br>')
                html_tooltip = f"<div style='font-size: {fs}px;'>{formatted_text}</div>"
                self.setToolTip(html_tooltip)
        else:
            self.setToolTip("")

        # Apply background color
        bg_color = self.item_data.get("color", "transparent")
        if bg_color != "transparent":
            self.setStyleSheet(f"NodeWidget {{ background-color: {bg_color}; border-radius: 6px; }}")
        else:
            self.setStyleSheet("NodeWidget { background-color: transparent; }")

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        # Only show generate if it doesn't exist
        rel_path = self.get_relative_path()
        full_path = self.app_ref.root_dir / rel_path if rel_path else None
        
        if hasattr(self, 'fuzzy_match') and self.fuzzy_match:
            heal_action = menu.addAction(f"🩹 Auto-Heal (Link to '{self.fuzzy_match}')")
            heal_action.triggered.connect(self.heal_link)
            menu.addSeparator()

        if full_path and not full_path.exists() and not self.item_data.get("done"):
            gen_action = menu.addAction("✨ Generate Placeholder")
            gen_action.triggered.connect(self.on_generate_clicked)
            menu.addSeparator()
            
        if full_path and full_path.exists():
            reveal_action = menu.addAction("📂 Reveal in Explorer")
            reveal_action.triggered.connect(self.reveal_in_explorer)
            menu.addSeparator()
            
        notes_action = menu.addAction("📝 Edit Notes")
        notes_action.triggered.connect(self.edit_notes)
        
        dep_action = menu.addAction("🔗 Set Dependency")
        dep_action.triggered.connect(self.set_dependency)
        
        val_action = menu.addAction("✔️ Set Content Rule")
        val_action.triggered.connect(self.set_validation)
        
        menu.addSeparator()

        color_menu = menu.addMenu("🎨 Set Color")
        
        for name, rgba in PRESET_COLORS.items():
            action = color_menu.addAction(name)
            # Create a small color square icon
            if rgba != "transparent":
                pixmap = QPixmap(12, 12)
                pixmap.fill(QColor(*[int(x) for x in rgba.replace('rgba(','').replace(')','').split(',')[:3]]))
                action.setIcon(QIcon(pixmap))
            
            action.triggered.connect(lambda checked=False, c=rgba: self.set_bg_color(c))

        menu.exec(event.globalPos())

    def reveal_in_explorer(self):
        rel_path = self.get_relative_path()
        if not rel_path: return
        full_path = self.app_ref.root_dir / rel_path
        if full_path.exists():
            import subprocess
            subprocess.Popen(['explorer', '/select,', str(full_path)])
    def heal_link(self):
        if hasattr(self, 'fuzzy_match') and self.fuzzy_match:
            self.app_ref.rename_node(self, self.item_data.get("text"), self.fuzzy_match)

    def edit_notes(self):
        dialog = NotesDialog(self.item_data.get("notes", ""), self)
        theme_name = self.app_ref.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        font_family = self.app_ref.settings.get("font_family", "Segoe UI")
        font_size = self.app_ref.settings.get("font_size", 13)
        dialog.setStyleSheet(STYLESHEET_TEMPLATE.format(font_family=font_family, font_size=font_size, **theme))
        
        if dialog.exec():
            self.item_data["notes"] = dialog.get_notes()
            self.update_ui_state()
            self.changed.emit()
            
    def set_dependency(self):
        dialog = DependencyDialog(self.app_ref.tree_data, self.item_data.get("depends_on"), self.item_data.get("id"), self)
        theme_name = self.app_ref.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        font_family = self.app_ref.settings.get("font_family", "Segoe UI")
        font_size = self.app_ref.settings.get("font_size", 13)
        dialog.setStyleSheet(STYLESHEET_TEMPLATE.format(font_family=font_family, font_size=font_size, **theme))
        
        if dialog.exec():
            self.item_data["depends_on"] = dialog.get_dependency()
            self.update_ui_state()
            self.changed.emit()

    def set_validation(self):
        dialog = ValidationDialog(self.item_data.get("validation", {}), self)
        theme_name = self.app_ref.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        font_family = self.app_ref.settings.get("font_family", "Segoe UI")
        font_size = self.app_ref.settings.get("font_size", 13)
        dialog.setStyleSheet(STYLESHEET_TEMPLATE.format(font_family=font_family, font_size=font_size, **theme))
        
        if dialog.exec():
            self.item_data["validation"] = dialog.get_validation()
            self.update_ui_state()
            self.changed.emit()

    def set_bg_color(self, rgba_str):
        for w in self.get_target_widgets():
            w.item_data["color"] = rgba_str
            w.update_ui_state()
        self.changed.emit()

    def paintEvent(self, event):
        # Draw translucent progress bar for parent nodes
        if self.item_data.get("children") and self.progress_ratio > 0 and not self.item_data.get("done"):
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            theme_name = self.app_ref.settings.get("theme", "Dark")
            theme = THEMES.get(theme_name, THEMES["Dark"])
            r, g, b, a = [int(x) for x in theme["bar_color"].replace("rgba(", "").replace(")", "").split(",")]
            painter.setBrush(QColor(r, g, b, a))
            rect = self.rect()
            rect.setWidth(int(rect.width() * self.progress_ratio))
            painter.drawRoundedRect(rect, 4, 4)
            painter.end()
            
        # Draw selection highlight
        if self.tree_item.isSelected():
            painter = QPainter(self)
            theme_name = self.app_ref.settings.get("theme", "Dark")
            theme = THEMES.get(theme_name, THEMES["Dark"])
            br, bg, bb, ba = [int(x) for x in theme["sel_border"].replace("rgba(", "").replace(")", "").split(",")]
            fr, fg, fb, fa = [int(x) for x in theme["sel_fill"].replace("rgba(", "").replace(")", "").split(",")]
            painter.setPen(QColor(br, bg, bb, ba))
            painter.setBrush(QColor(fr, fg, fb, fa))
            painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 4, 4)
            painter.end()
            
        super().paintEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.delete_btn.show()
            bg_color = self.item_data.get("color", "transparent")
            theme_name = self.app_ref.settings.get("theme", "Dark")
            theme = THEMES.get(theme_name, THEMES["Dark"])
            if bg_color == "transparent":
                self.setStyleSheet(f"NodeWidget {{ background-color: {theme['hover_bg']}; border-radius: 6px; }}")
            else:
                self.setStyleSheet(f"NodeWidget {{ background-color: {bg_color}; border: 1px solid {theme['border_color']}; border-radius: 6px; }}")
        elif event.type() == QEvent.Leave:
            self.delete_btn.hide()
            bg_color = self.item_data.get("color", "transparent")
            if bg_color == "transparent":
                self.setStyleSheet("NodeWidget { background-color: transparent; }")
            else:
                self.setStyleSheet(f"NodeWidget {{ background-color: {bg_color}; border-radius: 6px; }}")
        elif event.type() == QEvent.MouseButtonDblClick:
            # Rename logic
            old_name = self.item_data.get("text", "")
            new_name, ok = QInputDialog.getText(self, "Rename", "New name:", QLineEdit.Normal, old_name)
            if ok and new_name and new_name != old_name:
                self.request_rename.emit(self, old_name, new_name)
        return super().eventFilter(obj, event)


class SettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(320, 200)
        self.current_settings = current_settings.copy()

        layout = QFormLayout(self)
        
        from PySide6.QtGui import QFont
        self.font_cb = QFontComboBox()
        self.font_cb.setCurrentFont(QFont(self.current_settings["font_family"]))
        layout.addRow("Font:", self.font_cb)

        self.size_sb = QSpinBox()
        self.size_sb.setRange(8, 36)
        self.size_sb.setValue(self.current_settings["font_size"])
        layout.addRow("Font Size:", self.size_sb)

        self.lines_sb = QSpinBox()
        self.lines_sb.setRange(5, 50)
        self.lines_sb.setValue(self.current_settings["default_lines"])
        layout.addRow("Default Lines:", self.lines_sb)

        self.theme_cb = QComboBox()
        self.theme_cb.addItems(list(THEMES.keys()))
        self.theme_cb.setCurrentText(self.current_settings["theme"])
        layout.addRow("Theme:", self.theme_cb)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        theme_name = self.current_settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        save_btn.setStyleSheet(f"padding: 6px; background-color: {theme['accent']}; color: {theme['bg_color']}; border-radius: 4px;")
        cancel_btn.setStyleSheet(f"padding: 6px; background-color: transparent; border: 1px solid {theme['border_color']}; border-radius: 4px;")

        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)

        layout.addRow(btn_layout)

    def get_settings(self):
        return {
            "font_family": self.font_cb.currentFont().family(),
            "font_size": self.size_sb.value(),
            "default_lines": self.lines_sb.value(),
            "theme": self.theme_cb.currentText()
        }


class NotesDialog(QDialog):
    def __init__(self, notes_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Notes")
        self.setFixedSize(500, 400)
        layout = QVBoxLayout(self)
        
        self.toolbar_widget = QWidget()
        toolbar = QHBoxLayout(self.toolbar_widget)
        toolbar.setContentsMargins(0, 0, 0, 0)
        
        self.font_cb = QFontComboBox()
        self.font_cb.currentFontChanged.connect(self.change_font)
        toolbar.addWidget(self.font_cb)
        
        self.size_sb = QSpinBox()
        self.size_sb.setRange(6, 72)
        self.size_sb.setValue(12)
        self.size_sb.valueChanged.connect(self.change_size)
        toolbar.addWidget(self.size_sb)
        
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.setStyleSheet("font-weight: bold;")
        self.bold_btn.clicked.connect(self.toggle_bold)
        toolbar.addWidget(self.bold_btn)
        
        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.setStyleSheet("font-style: italic;")
        self.italic_btn.clicked.connect(self.toggle_italic)
        toolbar.addWidget(self.italic_btn)
        
        self.under_btn = QPushButton("U")
        self.under_btn.setCheckable(True)
        self.under_btn.setStyleSheet("text-decoration: underline;")
        self.under_btn.clicked.connect(self.toggle_underline)
        toolbar.addWidget(self.under_btn)
        
        self.strike_btn = QPushButton("S")
        self.strike_btn.setCheckable(True)
        self.strike_btn.setStyleSheet("text-decoration: line-through;")
        self.strike_btn.clicked.connect(self.toggle_strike)
        toolbar.addWidget(self.strike_btn)
        
        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(self.change_color)
        toolbar.addWidget(self.color_btn)
        toolbar.addStretch()
        
        layout.addWidget(self.toolbar_widget)
        
        self.text_edit = QTextEdit()
        if "<" in notes_text and ">" in notes_text:
            self.text_edit.setHtml(notes_text)
        else:
            self.text_edit.setPlainText(notes_text)
            
        self.text_edit.currentCharFormatChanged.connect(self.update_toolbar_state)
        layout.addWidget(self.text_edit)
        
        btn_layout = QHBoxLayout()
        
        self.md_toggle = QPushButton("Markdown Mode")
        self.md_toggle.setCheckable(True)
        self.md_toggle.toggled.connect(self.toggle_markdown_mode)
        btn_layout.addWidget(self.md_toggle)
        
        save_btn = QPushButton("Save Notes")
        save_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def toggle_markdown_mode(self, checked):
        if checked:
            self.toolbar_widget.setVisible(False)
            md_text = self.text_edit.toMarkdown()
            self.text_edit.setPlainText(md_text)
        else:
            self.toolbar_widget.setVisible(True)
            md_text = self.text_edit.toPlainText()
            self.text_edit.setMarkdown(md_text)

    def change_font(self, font):
        self.text_edit.setCurrentFont(font)
        
    def change_size(self, size):
        self.text_edit.setFontPointSize(size)
        
    def toggle_bold(self, checked):
        from PySide6.QtGui import QFont
        self.text_edit.setFontWeight(QFont.Bold if checked else QFont.Normal)
        
    def toggle_italic(self, checked):
        self.text_edit.setFontItalic(checked)
        
    def toggle_underline(self, checked):
        self.text_edit.setFontUnderline(checked)
        
    def toggle_strike(self, checked):
        fmt = self.text_edit.currentCharFormat()
        font = fmt.font()
        font.setStrikeOut(checked)
        fmt.setFont(font)
        self.text_edit.setCurrentCharFormat(fmt)
        
    def change_color(self):
        color = QColorDialog.getColor(self.text_edit.textColor(), self)
        if color.isValid():
            self.text_edit.setTextColor(color)
            
    def update_toolbar_state(self, fmt):
        if self.md_toggle.isChecked():
            return
            
        self.font_cb.blockSignals(True)
        self.font_cb.setCurrentFont(fmt.font())
        self.font_cb.blockSignals(False)
        
        self.size_sb.blockSignals(True)
        size = fmt.fontPointSize()
        if size > 0:
            self.size_sb.setValue(int(size))
        self.size_sb.blockSignals(False)
        
        from PySide6.QtGui import QFont
        self.bold_btn.blockSignals(True)
        self.bold_btn.setChecked(fmt.font().weight() >= QFont.Bold.value)
        self.bold_btn.blockSignals(False)
        
        self.italic_btn.blockSignals(True)
        self.italic_btn.setChecked(fmt.font().italic())
        self.italic_btn.blockSignals(False)
        
        self.under_btn.blockSignals(True)
        self.under_btn.setChecked(fmt.font().underline())
        self.under_btn.blockSignals(False)
        
        self.strike_btn.blockSignals(True)
        self.strike_btn.setChecked(fmt.font().strikeOut())
        self.strike_btn.blockSignals(False)

    def get_notes(self):
        if self.md_toggle.isChecked():
            from PySide6.QtGui import QTextDocument
            doc = QTextDocument()
            doc.setMarkdown(self.text_edit.toPlainText())
            return doc.toHtml()
        return self.text_edit.toHtml()

class ValidationDialog(QDialog):
    def __init__(self, validation_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Content Validation")
        self.setFixedSize(300, 150)
        layout = QFormLayout(self)
        
        self.type_cb = QComboBox()
        self.type_cb.addItems(["none", "not_empty", "contains"])
        self.type_cb.setCurrentText(validation_data.get("type", "none"))
        layout.addRow("Rule Type:", self.type_cb)
        
        self.val_input = QLineEdit()
        self.val_input.setText(validation_data.get("value", ""))
        layout.addRow("Value:", self.val_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        layout.addRow(btn_layout)
        
    def get_validation(self):
        return {"type": self.type_cb.currentText(), "value": self.val_input.text()}

class DependencyDialog(QDialog):
    def __init__(self, tree_data, current_dep_id, current_node_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Dependency")
        self.setFixedSize(400, 400)
        layout = QVBoxLayout(self)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)
        
        self.selected_id = current_dep_id
        
        def _build(items, parent_node):
            for it in items:
                if it.get("id") == current_node_id:
                    continue
                node = QTreeWidgetItem(parent_node)
                node.setText(0, it.get("text", ""))
                node.setData(0, Qt.UserRole, it.get("id"))
                if it.get("id") == current_dep_id:
                    node.setSelected(True)
                _build(it.get("children", []), node)
                
        _build(tree_data.get("items", []), self.tree.invisibleRootItem())
        self.tree.expandAll()
        
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear Dependency")
        clear_btn.clicked.connect(self.clear_dep)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
    def clear_dep(self):
        self.selected_id = None
        self.accept()
        
    def get_dependency(self):
        selected = self.tree.selectedItems()
        if selected and self.selected_id is not None:
            return selected[0].data(0, Qt.UserRole)
        return self.selected_id

class TemplateManagerDialog(QDialog):
    def __init__(self, current_tree_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Template Library")
        self.setFixedSize(400, 300)
        self.current_tree_data = current_tree_data
        self.templates_dir = Path.home() / ".foldercheck_templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.refresh_list()
        layout.addWidget(self.list_widget)
        
        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Load Selected")
        load_btn.clicked.connect(self.accept)
        
        save_btn = QPushButton("Save Current As...")
        save_btn.clicked.connect(self.save_template)
        
        btn_layout.addWidget(load_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
    def refresh_list(self):
        self.list_widget.clear()
        for f in self.templates_dir.glob("*.json"):
            self.list_widget.addItem(f.stem)
            
    def save_template(self):
        name, ok = QInputDialog.getText(self, "Save Template", "Template Name:")
        if ok and name:
            file_path = self.templates_dir / f"{name}.json"
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.current_tree_data, f, ensure_ascii=False, indent=2)
                self.refresh_list()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save: {e}")
                
    def get_selected_template_data(self):
        selected = self.list_widget.currentItem()
        if selected:
            file_path = self.templates_dir / f"{selected.text()}.json"
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    pass
        return None

class TitleBar(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 14px;")
        
        self.export_btn = QPushButton("📄")
        self.export_btn.setToolTip("Export to Markdown")
        self.export_btn.setProperty("class", "icon-btn")
        self.export_btn.setFixedSize(30, 30)
        self.export_btn.clicked.connect(self.parent.export_to_markdown)

        self.search_btn = QPushButton("🔍")
        self.search_btn.setToolTip("Search")
        self.search_btn.setProperty("class", "icon-btn")
        self.search_btn.setFixedSize(30, 30)
        self.search_btn.clicked.connect(self.parent.open_search)

        self.templates_btn = QPushButton("📑")
        self.templates_btn.setToolTip("Templates")
        self.templates_btn.setProperty("class", "icon-btn")
        self.templates_btn.setFixedSize(30, 30)
        self.templates_btn.clicked.connect(self.parent.open_templates)

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.setProperty("class", "icon-btn")
        self.settings_btn.setFixedSize(30, 30)
        self.settings_btn.clicked.connect(self.parent.open_settings)

        self.pin_btn = QPushButton("📌")
        self.pin_btn.setProperty("class", "icon-btn")
        self.pin_btn.setFixedSize(30, 30)
        self.pin_btn.setCheckable(True)
        self.pin_btn.clicked.connect(self.toggle_pin)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setProperty("class", "icon-btn")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.parent.close)
        
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.search_btn)
        layout.addWidget(self.templates_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.pin_btn)
        layout.addWidget(self.close_btn)
        
        self.start_pos = None

    def toggle_pin(self, checked):
        self.parent.setWindowFlag(Qt.WindowStaysOnTopHint, checked)
        self.pin_btn.setStyleSheet("background: rgba(255, 255, 255, 0.2);" if checked else "")
        self.parent.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.start_pos = None


class ChecklistTreeWidget(QTreeWidget):
    def __init__(self, app_ref):
        super().__init__()
        self.app_ref = app_ref
        self.setDragDropMode(QTreeWidget.DragDrop)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setHeaderHidden(True)
        self.setIndentation(20)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.source() == self:
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls() or event.source() == self:
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # External File/Folder Drop
            event.acceptProposedAction()
            target_item = self.itemAt(event.position().toPoint())
            
            for url in event.mimeData().urls():
                path = Path(url.toLocalFile())
                if path.exists():
                    self.app_ref.add_dropped_path(path, target_item)
        elif event.source() == self:
            # Internal Move Drop
            dragged_item = self.currentItem()
            target_item = self.itemAt(event.position().toPoint())
            drop_pos = self.dropIndicatorPosition()
            
            if not dragged_item:
                return

            # Prevent dropping on itself or its children
            curr = target_item
            while curr:
                if curr == dragged_item:
                    event.ignore()
                    return
                curr = curr.parent()

            dragged_widget = self.itemWidget(dragged_item, 0)
            if not dragged_widget:
                return
                
            dragged_data = dragged_widget.item_data

            # Remove from old parent in data
            old_parent = dragged_item.parent()
            if old_parent:
                old_parent_widget = self.itemWidget(old_parent, 0)
                if dragged_data in old_parent_widget.item_data.get("children", []):
                    old_parent_widget.item_data["children"].remove(dragged_data)
            else:
                if dragged_data in self.app_ref.tree_data.get("items", []):
                    self.app_ref.tree_data["items"].remove(dragged_data)

            # Add to new parent in data
            if target_item:
                target_widget = self.itemWidget(target_item, 0)
                if drop_pos == QAbstractItemView.DropIndicatorPosition.OnItem:
                    target_widget.item_data.setdefault("children", []).append(dragged_data)
                else:
                    # Drop above or below
                    target_parent = target_item.parent()
                    target_parent_widget = self.itemWidget(target_parent, 0) if target_parent else None
                    target_list = target_parent_widget.item_data.setdefault("children", []) if target_parent_widget else self.app_ref.tree_data.setdefault("items", [])
                    try:
                        idx = target_list.index(target_widget.item_data)
                        if drop_pos == QAbstractItemView.DropIndicatorPosition.BelowItem:
                            idx += 1
                        target_list.insert(idx, dragged_data)
                    except ValueError:
                        target_list.append(dragged_data)
            else:
                self.app_ref.tree_data.setdefault("items", []).append(dragged_data)

            # Re-render to prevent setItemWidget loss
            self.app_ref.populate_tree()
            self.app_ref.request_save()
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class EdgeGrip(QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.edge = edge
        if edge in ('left', 'right'):
            self.setCursor(Qt.SizeHorCursor)
        elif edge in ('top', 'bottom'):
            self.setCursor(Qt.SizeVerCursor)
        elif edge == 'bottom_right':
            self.setCursor(Qt.SizeFDiagCursor)
            
        self.start_pos = None
        self.start_geom = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPosition().toPoint()
            self.start_geom = self.window().geometry()
            
    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            delta = event.globalPosition().toPoint() - self.start_pos
            geom = self.start_geom
            w_min = self.window().minimumWidth()
            h_min = self.window().minimumHeight()
            
            if self.edge == 'right':
                self.window().resize(max(w_min, geom.width() + delta.x()), geom.height())
            elif self.edge == 'bottom':
                self.window().resize(geom.width(), max(h_min, geom.height() + delta.y()))
            elif self.edge == 'bottom_right':
                self.window().resize(max(w_min, geom.width() + delta.x()), max(h_min, geom.height() + delta.y()))
            elif self.edge == 'left':
                new_w = max(w_min, geom.width() - delta.x())
                if geom.width() - delta.x() >= w_min:
                    self.window().setGeometry(geom.x() + delta.x(), geom.y(), new_w, geom.height())
            elif self.edge == 'top':
                new_h = max(h_min, geom.height() - delta.y())
                if geom.height() - delta.y() >= h_min:
                    self.window().setGeometry(geom.x(), geom.y() + delta.y(), geom.width(), new_h)

    def mouseReleaseEvent(self, event):
        self.start_pos = None
        self.start_geom = None

class FolderCheckApp(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = Path(file_path).resolve()
        self.root_dir = self.file_path.parent
        self.tree_data = {"items": []}
        
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(500)
        self.save_timer.timeout.connect(self.flush_save)

        self.settings = SettingsManager.load()
        self.init_data()
        self.init_ui()
        self.apply_theme()
        self.populate_tree()
        self.init_watcher()

    def init_data(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tree_data = self.migrate_v3_to_v4(data)
            except Exception as e:
                print(f"Error loading data: {e}")

    def migrate_v3_to_v4(self, data):
        items = data.get("items", [])
        # Upgrade v2 to v3 first if needed
        for item in items:
            if "children" not in item:
                item["children"] = []
                
        # Upgrade to v4: add id, notes, depends_on, validation
        def _upgrade(item_list):
            for item in item_list:
                if "id" not in item: item["id"] = str(uuid.uuid4())
                if "notes" not in item: item["notes"] = ""
                if "depends_on" not in item: item["depends_on"] = None
                if "validation" not in item: item["validation"] = {"type": "none", "value": ""}
                _upgrade(item.get("children", []))
        _upgrade(items)
        return {"items": items}

    def request_save(self):
        self.save_timer.start()
        self.update_all_nodes() # Also trigger UI updates (progress, etc)

    def flush_save(self):
        def _save():
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.tree_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Save error: {e}")
        # Threading for save to prevent UI blocking
        threading.Thread(target=_save, daemon=True).start()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize_based_on_lines()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.bg_container = QWidget()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 4)
        self.bg_container.setGraphicsEffect(shadow)

        self.container_layout = QVBoxLayout(self.bg_container)
        self.container_layout.setContentsMargins(0, 0, 0, 15)
        self.container_layout.setSpacing(0)

        self.title_bar = TitleBar(self.file_path.name, self)
        self.container_layout.addWidget(self.title_bar)

        self.tree = ChecklistTreeWidget(self)
        self.container_layout.addWidget(self.tree)

        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(15, 10, 15, 0)
        
        self.import_btn = QPushButton("📁")
        self.import_btn.setToolTip("Import Directory")
        self.import_btn.setProperty("class", "icon-btn")
        self.import_btn.setFixedSize(30, 30)
        self.import_btn.clicked.connect(self.import_directory)
        self.input_layout.addWidget(self.import_btn)

        self.new_task_input = QLineEdit()
        self.new_task_input.setPlaceholderText("Add a root task...")
        self.new_task_input.returnPressed.connect(self.add_root_task)
        self.input_layout.addWidget(self.new_task_input)
        
        self.container_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.bg_container)

        QShortcut(QKeySequence("Esc"), self, self.close)
        QShortcut(QKeySequence("Ctrl+N"), self, self.new_task_input.setFocus)
        QShortcut(QKeySequence("Delete"), self, self.delete_selected_items)
        QTimer.singleShot(100, self.new_task_input.setFocus)

        self.toast_label = QLabel(self)
        self.toast_label.setStyleSheet("background-color: rgba(77, 170, 242, 0.9); color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold; font-size: 12px;")
        self.toast_label.setAlignment(Qt.AlignCenter)
        self.toast_label.hide()
        
        self.grip_left = EdgeGrip(self, 'left')
        self.grip_right = EdgeGrip(self, 'right')
        self.grip_top = EdgeGrip(self, 'top')
        self.grip_bottom = EdgeGrip(self, 'bottom')
        self.grip_bottom_right = EdgeGrip(self, 'bottom_right')

        

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()
        t = 5 # thickness
        m = 10 # margin
        
        self.grip_left.setGeometry(m, m + t, t, h - 2*m - 2*t)
        self.grip_right.setGeometry(w - m - t, m + t, t, h - 2*m - 2*t)
        self.grip_top.setGeometry(m + t, m, w - 2*m - 2*t, t)
        self.grip_bottom.setGeometry(m + t, h - m - t, w - 2*m - 2*t, t)
        self.grip_bottom_right.setGeometry(w - m - t, h - m - t, t, t)
        
        self.grip_left.raise_()
        self.grip_right.raise_()
        self.grip_top.raise_()
        self.grip_bottom.raise_()
        self.grip_bottom_right.raise_()



    def open_search(self):
        text, ok = QInputDialog.getText(self, "Search", "Search tasks (rough match):")
        if ok and text:
            self.tree.clearSelection()
            search_text = text.lower()
            matches_found = False
            
            def search_item(item):
                nonlocal matches_found
                item_widget = self.tree.itemWidget(item, 0)
                if item_widget:
                    node_text = item_widget.item_data.get("text", "").lower()
                    notes_text = item_widget.item_data.get("notes", "").lower()
                    
                    if search_text in node_text or search_text in notes_text:
                        item.setSelected(True)
                        parent = item.parent()
                        while parent:
                            parent.setExpanded(True)
                            parent = parent.parent()
                        matches_found = True
                        
                for i in range(item.childCount()):
                    search_item(item.child(i))
                    
            for i in range(self.tree.topLevelItemCount()):
                search_item(self.tree.topLevelItem(i))
                
            if matches_found:
                selected = self.tree.selectedItems()
                if selected:
                    self.tree.scrollToItem(selected[0])
            else:
                QMessageBox.information(self, "Search Result", "No matching tasks found.")

    def open_templates(self):
        dialog = TemplateManagerDialog(self.tree_data, self)
        theme_name = self.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        font_family = self.settings.get("font_family", "Segoe UI")
        font_size = self.settings.get("font_size", 13)
        dialog.setStyleSheet(STYLESHEET_TEMPLATE.format(font_family=font_family, font_size=font_size, **theme))

        if dialog.exec():
            selected_data = dialog.get_selected_template_data()
            if selected_data:
                # Merge template items into current
                # Upgrade them to have new UUIDs so they don't conflict
                def _renew_uuids(item_list):
                    for item in item_list:
                        item["id"] = str(uuid.uuid4())
                        _renew_uuids(item.get("children", []))
                
                new_items = selected_data.get("items", [])
                _renew_uuids(new_items)
                
                self.tree_data.setdefault("items", []).extend(new_items)
                self.populate_tree()
                self.request_save()

    def import_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory to Import")
        if folder:
            path = Path(folder)
            def _build_data(p: Path):
                data = {"id": str(uuid.uuid4()), "text": p.name, "done": False, "children": [], "notes": "", "depends_on": None, "validation": {"type": "none", "value": ""}}
                if p.is_dir():
                    try:
                        for child in p.iterdir():
                            child_data = _build_data(child)
                            if child_data:
                                data["children"].append(child_data)
                    except PermissionError:
                        pass
                return data

            new_data = _build_data(path)
            if new_data:
                self.tree_data.setdefault("items", []).append(new_data)
                self.populate_tree()
                self.request_save()

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)
        theme_name = self.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        font_family = self.settings.get("font_family", "Segoe UI")
        font_size = self.settings.get("font_size", 13)
        dialog.setStyleSheet(STYLESHEET_TEMPLATE.format(font_family=font_family, font_size=font_size, **theme))

        if dialog.exec():
            self.settings = dialog.get_settings()
            SettingsManager.save(self.settings)
            self.apply_theme()
            self.resize_based_on_lines()

    def apply_theme(self):
        theme_name = self.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])
        font_family = self.settings.get("font_family", "Segoe UI")
        font_size = self.settings.get("font_size", 13)
        
        style = STYLESHEET_TEMPLATE.format(
            font_family=font_family,
            font_size=font_size,
            **theme
        )
        self.setStyleSheet(style)
        
        self.bg_container.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['bg_color']};
                border-radius: 12px;
                border: 1px solid {theme['border_color']};
            }}
        """)
        
        self.title_bar.title_label.setStyleSheet(f"color: {theme['title_color']}; font-weight: 600; font-size: 14px;")
        
        sr, sg, sb, sa = [int(x) for x in theme["shadow"].replace("rgba(", "").replace(")", "").split(",")]
        shadow = self.bg_container.graphicsEffect()
        if shadow:
            shadow.setColor(QColor(sr, sg, sb, sa))
        
        self.toast_label.setStyleSheet(f"background-color: {theme['accent']}; color: {theme['bg_color']}; padding: 8px 16px; border-radius: 6px; font-weight: bold; font-size: 12px;")
        
        self.update_all_nodes()

    def resize_based_on_lines(self):
        lines = self.settings.get("default_lines", 15)
        font_size = self.settings.get("font_size", 13)
        # 24 is roughly the base height without padding + padding + spacing
        item_height = font_size * 2 + 4
        new_height = 40 + 50 + (lines * item_height)
        self.resize(350, new_height)

    def show_toast(self, message):
        self.toast_label.setText(message)
        self.toast_label.adjustSize()
        self.toast_label.move((self.width() - self.toast_label.width()) // 2, self.height() - 80)
        self.toast_label.show()
        self.toast_label.raise_()
        QTimer.singleShot(2000, self.toast_label.hide)

    def export_to_markdown(self):
        lines = []
        def _walk(item_list, current_path, depth):
            for item in item_list:
                text = item.get("text", "")
                done = item.get("done", False)
                children = item.get("children", [])
                
                full_path = current_path / text
                status = "Exists" if full_path.exists() else "Missing"
                
                indent = "  " * depth
                checkbox = "[x]" if done else "[ ]"
                lines.append(f"{indent}- {checkbox} {text} *({status})*")
                
                _walk(children, full_path, depth + 1)
                
        _walk(self.tree_data.get("items", []), self.root_dir, 0)
        
        QApplication.clipboard().setText("\n".join(lines))
        self.show_toast("Copied to clipboard!")

    def populate_tree(self):
        self.tree.clear()
        self.build_nodes(self.tree_data.get("items", []), self.tree.invisibleRootItem())

    def build_nodes(self, item_list, parent_item):
        for data in item_list:
            node = QTreeWidgetItem(parent_item)
            node.setExpanded(True)
            widget = NodeWidget(node, data, self)
            widget.changed.connect(self.request_save)
            widget.deleted.connect(self.delete_node)
            widget.request_generate.connect(self.generate_node)
            widget.request_rename.connect(self.rename_node)
            self.tree.setItemWidget(node, 0, widget)
            
            if "children" in data and data["children"]:
                self.build_nodes(data["children"], node)

    def add_dropped_path(self, path: Path, target_item=None):
        # Build JSON recursively (max depth 3 to avoid hanging)
        def _build_data(p: Path, depth=0):
            if depth > 3: return None
            data = {"id": str(uuid.uuid4()), "text": p.name, "done": False, "children": [], "notes": "", "depends_on": None, "validation": {"type": "none", "value": ""}}
            if p.is_dir():
                try:
                    for child in p.iterdir():
                        child_data = _build_data(child, depth + 1)
                        if child_data:
                            data["children"].append(child_data)
                except PermissionError:
                    pass
            return data

        new_data = _build_data(path)
        if not new_data: return

        if target_item:
            target_widget = self.tree.itemWidget(target_item, 0)
            target_widget.item_data.setdefault("children", []).append(new_data)
            target_item.setExpanded(True)
        else:
            self.tree_data.setdefault("items", []).append(new_data)

        self.populate_tree()
        self.request_save()

    def add_root_task(self):
        text = self.new_task_input.text().strip()
        if text:
            new_data = {"id": str(uuid.uuid4()), "text": text, "done": False, "children": [], "notes": "", "depends_on": None, "validation": {"type": "none", "value": ""}}
            self.tree_data.setdefault("items", []).append(new_data)
            
            node = QTreeWidgetItem(self.tree.invisibleRootItem())
            node.setExpanded(True)
            widget = NodeWidget(node, new_data, self)
            widget.changed.connect(self.request_save)
            widget.deleted.connect(self.delete_node)
            widget.request_generate.connect(self.generate_node)
            widget.request_rename.connect(self.rename_node)
            self.tree.setItemWidget(node, 0, widget)
            
            self.request_save()
            self.new_task_input.clear()
            self.tree.scrollToBottom()

    def delete_selected_items(self):
        selected = self.tree.selectedItems()
        if selected:
            widgets = [self.tree.itemWidget(i, 0) for i in selected if self.tree.itemWidget(i, 0)]
            for w in widgets:
                if w.tree_item.treeWidget(): # Check if still in tree
                    self.delete_node(w)
        else:
            # Fallback to hovered
            pos = QCursor.pos()
            widget = QApplication.widgetAt(pos)
            while widget and not isinstance(widget, NodeWidget):
                widget = widget.parentWidget()
            if widget and isinstance(widget, NodeWidget):
                self.delete_node(widget)

    def delete_node(self, widget):
        node = widget.tree_item
        # Find in data structure and remove
        parent_node = node.parent()
        if parent_node:
            parent_widget = self.tree.itemWidget(parent_node, 0)
            if parent_widget and widget.item_data in parent_widget.item_data.get("children", []):
                parent_widget.item_data["children"].remove(widget.item_data)
        else:
            if widget.item_data in self.tree_data.get("items", []):
                self.tree_data["items"].remove(widget.item_data)
        
        # Remove from UI
        (node.parent() or self.tree.invisibleRootItem()).removeChild(node)
        self.request_save()

    def generate_node(self, widget):
        rel_path = widget.get_relative_path()
        full_path = self.root_dir / rel_path
        if not full_path: return

        # Recursively generate based on JSON structure
        def _gen(item_data, current_path: Path):
            children = item_data.get("children", [])
            # Is folder if it has children or no extension
            is_folder = bool(children) or ('.' not in item_data.get("text", ""))
            
            if is_folder:
                current_path.mkdir(parents=True, exist_ok=True)
                for c in children:
                    _gen(c, current_path / c.get("text", ""))
            else:
                current_path.parent.mkdir(parents=True, exist_ok=True)
                if not current_path.exists():
                    current_path.touch()

        try:
            _gen(widget.item_data, full_path)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate: {e}")
        
        self.update_all_nodes()

    def rename_node(self, widget, old_name, new_name):
        rel_path = widget.get_relative_path()
        full_path = self.root_dir / rel_path
        
        # Modify JSON
        widget.item_data["text"] = new_name
        
        # Physical Sync
        if full_path.exists():
            msg = QMessageBox()
            msg.setWindowTitle("Physical Sync")
            msg.setText(f"Do you also want to rename the physical file/folder on disk to '{new_name}'?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec() == QMessageBox.Yes:
                new_full_path = full_path.parent / new_name
                try:
                    full_path.rename(new_full_path)
                except Exception as e:
                    QMessageBox.warning(self, "Rename Error", str(e))
                # fuzzy search "self healing" could be implemented if it fails

        widget.update_ui_state()
        self.request_save()

    def update_all_nodes(self):
        # Traverse tree and update all UI
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            w = self.tree.itemWidget(item, 0)
            if w: w.update_ui_state()
            iterator += 1

    def init_watcher(self):
        self.watcher = QFileSystemWatcher()
        self.watcher.directoryChanged.connect(self.on_fs_changed)
        self.watcher.fileChanged.connect(self.on_fs_changed)
        
        self.refresh_timer = QTimer()
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.setInterval(300)
        self.refresh_timer.timeout.connect(self.update_all_nodes)
        
        self.update_watcher_paths()

    def update_watcher_paths(self):
        # Windows watcher doesn't do deep watching easily.
        # We add the root dir and any subdirectories mapped in the blueprint.
        paths = [str(self.root_dir)]
        
        def _add_dirs(item_list, current_path: Path):
            for data in item_list:
                cp = current_path / data.get("text", "")
                children = data.get("children", [])
                if children or ('.' not in data.get("text", "")):
                    if cp.exists() and cp.is_dir():
                        paths.append(str(cp))
                    _add_dirs(children, cp)
        
        _add_dirs(self.tree_data.get("items", []), self.root_dir)
        
        existing = self.watcher.directories() + self.watcher.files()
        if existing:
            self.watcher.removePaths(existing)
        
        # Filter duplicates and add
        unique_paths = list(set(paths))
        if unique_paths:
            self.watcher.addPaths(unique_paths)

    def on_fs_changed(self, path):
        self.refresh_timer.start()

# Needed for traversing tree
from PySide6.QtWidgets import QTreeWidgetItemIterator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    file_path = "test.check"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            if not is_admin():
                msg = QMessageBox()
                msg.setWindowTitle("FolderCheck Setup")
                msg.setText("This will register FolderCheck to your Right-Click menu.\nDo you want to proceed? (Requires Administrator privileges)")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                if msg.exec() == QMessageBox.Yes:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
                sys.exit()
            else:
                if setup_registry():
                    QMessageBox.information(None, "FolderCheck Installed", "Successfully added to the Right-Click menu!\n\nYou can now Right-Click in any folder and select 'New -> FolderCheck Checklist'.")
                sys.exit()
        else:
            file_path = sys.argv[1]

    window = FolderCheckApp(file_path)
    window.show()
    # Initial UI update
    QTimer.singleShot(50, window.update_all_nodes)
    sys.exit(app.exec())
