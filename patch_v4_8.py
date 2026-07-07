import sys

with open("foldercheck.py", "r", encoding="utf-8") as f:
    content = f.read()

title_old = """        self.templates_btn = QPushButton("📑")
        self.templates_btn.setToolTip("Templates")"""

title_new = """        self.search_btn = QPushButton("🔍")
        self.search_btn.setToolTip("Search")
        self.search_btn.setProperty("class", "icon-btn")
        self.search_btn.setFixedSize(30, 30)
        self.search_btn.clicked.connect(self.parent.open_search)

        self.templates_btn = QPushButton("📑")
        self.templates_btn.setToolTip("Templates")"""

content = content.replace(title_old, title_new)

layout_old = """        layout.addWidget(self.templates_btn)
        layout.addWidget(self.settings_btn)"""

layout_new = """        layout.addWidget(self.search_btn)
        layout.addWidget(self.templates_btn)
        layout.addWidget(self.settings_btn)"""

content = content.replace(layout_old, layout_new)

search_method = """
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

    def open_templates(self):"""

content = content.replace("    def open_templates(self):", search_method)

with open("foldercheck.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patch 8 complete")
