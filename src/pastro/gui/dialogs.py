"""
Dialog windows for the Pastro application.
"""

from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QScrollArea, QTreeWidget,
    QTreeWidgetItem, QProgressBar, QPlainTextEdit
)
from PyQt6.QtCore import Qt

class CategoryDialog(QDialog):
    """Dialog for creating a new category."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nova Categoria")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Category name
        layout.addWidget(QLabel("Nome da Categoria:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        
        # Extensions
        layout.addWidget(QLabel("Extensões (separadas por vírgula):"))
        self.extensions_input = QLineEdit()
        layout.addWidget(self.extensions_input)
        
        # Buttons
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
    
    def get_data(self):
        """Return the category name and extensions."""
        name = self.name_input.text().strip()
        extensions = [ext.strip() for ext in self.extensions_input.text().split(",") if ext.strip()]
        return name, extensions

class PreviewDialog(QDialog):
    """Dialog for previewing the organization before applying."""
    def __init__(self, classification, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prévia da Organização")
        self.setModal(True)
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Summary label
        summary = QLabel("Resumo da Organização:")
        layout.addWidget(summary)
        
        # Create scroll area for the tree
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Create tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Categoria", "Arquivos"])
        self.tree.setColumnCount(2)
        scroll.setWidget(self.tree)
        
        # Populate tree
        for category, files in classification.items():
            if files:  # Only show categories with files
                category_item = QTreeWidgetItem(self.tree)
                category_item.setText(0, category)
                category_item.setText(1, f"{len(files)} arquivo(s)")
                
                for file_path in files:
                    file_item = QTreeWidgetItem(category_item)
                    file_item.setText(0, file_path.name)
                    file_item.setText(1, str(file_path.parent))
        
        self.tree.expandAll()
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        
        # Buttons
        buttons = QHBoxLayout()
        ok_button = QPushButton("Organizar")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

class ProgressDialog(QDialog):
    """Dialog for showing organization progress."""
    def __init__(self, total_files, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Organizando Arquivos")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Log area
        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        # Status label
        self.status_label = QLabel("Preparando...")
        layout.addWidget(self.status_label)
        
        self.current_progress = 0
        self.total_files = total_files
    
    def update_progress(self, file_name, category):
        """Update progress bar and log."""
        self.current_progress += 1
        self.progress_bar.setValue(self.current_progress)
        
        # Add log entry with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] Movendo '{file_name}' para categoria '{category}'"
        self.log_area.appendPlainText(log_entry)
        
        # Update status
        progress_percent = (self.current_progress / self.total_files) * 100
        self.status_label.setText(f"Progresso: {progress_percent:.1f}% ({self.current_progress}/{self.total_files})")
        
        # Auto scroll to bottom
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        ) 