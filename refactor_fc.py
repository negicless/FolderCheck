import os

file_path = "foldercheck.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
content = content.replace(
    "QMessageBox, QInputDialog, QAbstractItemView, QMenu",
    "QMessageBox, QInputDialog, QAbstractItemView, QMenu,\n    QSizeGrip, QDialog, QFormLayout, QComboBox, QFontComboBox, QSpinBox"
)

# 2. Extract and Replace STYLESHEET with THEMES, SETTINGS, and STYLESHEET_TEMPLATE
start_idx = content.find("STYLESHEET = ")
end_idx = content.find("PRESET_COLORS = {")

new_stylesheet_section = '''import json
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
'''
content = content[:start_idx] + new_stylesheet_section + content[end_idx:]

# 3. SettingsDialog insertion before TitleBar
title_bar_idx = content.find("class TitleBar(QWidget):")
settings_dialog_code = '''class SettingsDialog(QDialog):
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

'''
content = content[:title_bar_idx] + settings_dialog_code + content[title_bar_idx:]

# 4. Modify TitleBar for Settings Button
content = content.replace(
    'self.export_btn.clicked.connect(self.parent.export_to_markdown)',
    '''self.export_btn.clicked.connect(self.parent.export_to_markdown)

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.setProperty("class", "icon-btn")
        self.settings_btn.setFixedSize(30, 30)
        self.settings_btn.clicked.connect(self.parent.open_settings)'''
)

content = content.replace(
    'layout.addWidget(self.export_btn)',
    'layout.addWidget(self.settings_btn)\n        layout.addWidget(self.export_btn)'
)

# 5. Modify NodeWidget logic for theme colors
content = content.replace(
    'self.progress_label.setStyleSheet("color: rgba(255, 255, 255, 0.4); font-size: 11px;")',
    'self.progress_label.setStyleSheet("font-size: 11px;") # Color set via theme'
)

# In NodeWidget.update_ui_state
content = content.replace(
    '''        if is_f:
            self.icon_label.setText("■") # Minimal square
            self.icon_label.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 10px;")
        else:
            self.icon_label.setText("●") # Minimal dot
            self.icon_label.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 8px;")''',
    '''        theme_name = self.app_ref.settings.get("theme", "Dark")
        theme = THEMES.get(theme_name, THEMES["Dark"])

        if is_f:
            self.icon_label.setText("■") # Minimal square
            self.icon_label.setStyleSheet(f"color: {theme['faint_icon']}; font-size: 10px;")
        else:
            self.icon_label.setText("●") # Minimal dot
            self.icon_label.setStyleSheet(f"color: {theme['faint_icon']}; font-size: 8px;")
        self.progress_label.setStyleSheet(f"color: {theme['faint_text']}; font-size: 11px;")'''
)

content = content.replace(
    '''        if done:
            self.label.setStyleSheet("color: rgba(255, 255, 255, 0.4);")
        elif file_exists:
            self.label.setStyleSheet("color: #4DAAF2;")
        else:
            self.label.setStyleSheet("color: #E0E0E0;")''',
    '''        if done:
            self.label.setStyleSheet(f"color: {theme['faint_text']};")
        elif file_exists:
            self.label.setStyleSheet(f"color: {theme['accent']};")
        else:
            self.label.setStyleSheet(f"color: {theme['text_color']};")'''
)

content = content.replace(
    '''    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet(STYLESHEET)''',
    '''    def contextMenuEvent(self, event):
        menu = QMenu(self)'''
)

# Paint Event in NodeWidget
content = content.replace(
    '''            painter.setBrush(QColor(77, 170, 242, 30)) # Light blue translucent''',
    '''            theme_name = self.app_ref.settings.get("theme", "Dark")
            theme = THEMES.get(theme_name, THEMES["Dark"])
            r, g, b, a = [int(x) for x in theme["bar_color"].replace("rgba(", "").replace(")", "").split(",")]
            painter.setBrush(QColor(r, g, b, a))'''
)
content = content.replace(
    '''            painter.setPen(QColor(77, 170, 242, 200)) # Blue border
            painter.setBrush(QColor(77, 170, 242, 20)) # Very faint blue fill''',
    '''            theme_name = self.app_ref.settings.get("theme", "Dark")
            theme = THEMES.get(theme_name, THEMES["Dark"])
            br, bg, bb, ba = [int(x) for x in theme["sel_border"].replace("rgba(", "").replace(")", "").split(",")]
            fr, fg, fb, fa = [int(x) for x in theme["sel_fill"].replace("rgba(", "").replace(")", "").split(",")]
            painter.setPen(QColor(br, bg, bb, ba))
            painter.setBrush(QColor(fr, fg, fb, fa))'''
)

content = content.replace(
    '''            if bg_color == "transparent":
                self.setStyleSheet("NodeWidget { background-color: rgba(255, 255, 255, 0.03); border-radius: 6px; }")''',
    '''            theme_name = self.app_ref.settings.get("theme", "Dark")
            theme = THEMES.get(theme_name, THEMES["Dark"])
            if bg_color == "transparent":
                self.setStyleSheet(f"NodeWidget {{ background-color: {theme['hover_bg']}; border-radius: 6px; }}")'''
)
content = content.replace(
    '''            else:
                self.setStyleSheet(f"NodeWidget {{ background-color: {bg_color}; border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; }}")''',
    '''            else:
                self.setStyleSheet(f"NodeWidget {{ background-color: {bg_color}; border: 1px solid {theme['border_color']}; border-radius: 6px; }}")'''
)

# 6. FolderCheckApp initialization and logic
content = content.replace(
    '''        self.init_data()
        self.init_ui()''',
    '''        self.settings = SettingsManager.load()
        self.init_data()
        self.init_ui()
        self.apply_theme()'''
)

content = content.replace(
    '''        self.resize(350, 550)
        self.setStyleSheet(STYLESHEET)''',
    '''        self.resize_based_on_lines()'''
)

content = content.replace(
    '''        self.bg_container.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 34, 0.95);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)''',
    ''
)
content = content.replace(
    '''        self.title_bar.title_label.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 14px;")''',
    ''
)

content = content.replace(
    '''        self.toast_label.hide()''',
    '''        self.toast_label.hide()

        self.size_grip_layout = QHBoxLayout()
        self.size_grip_layout.setContentsMargins(0, 0, 0, 0)
        self.size_grip_layout.addStretch()
        self.size_grip = QSizeGrip(self.bg_container)
        self.size_grip.setFixedSize(16, 16)
        self.size_grip.setStyleSheet("background: transparent;")
        self.size_grip_layout.addWidget(self.size_grip)
        self.container_layout.addLayout(self.size_grip_layout)'''
)

# Add open_settings, apply_theme, resize_based_on_lines methods
methods_code = '''    def open_settings(self):
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

'''
app_class_idx = content.find("    def show_toast(self, message):")
content = content[:app_class_idx] + methods_code + content[app_class_idx:]


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done refactoring.")
