"""
Main window module for the Pastro application.
"""

import shutil
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ..core.classifier import AutoClassifier
from .dialogs import CategoryDialog, PreviewDialog, ProgressDialog

class FolderOrganizer(QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Organizador de Pastas")
        self.setGeometry(100, 100, 1000, 600)
        
        # Set window icon
        icon_path = Path(__file__).parent.parent.parent / "resources" / "logo.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Initialize auto classifier
        self.classifier = AutoClassifier()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create top section with folder selection
        top_section = QHBoxLayout()
        self.folder_label = QLabel("Nenhuma pasta selecionada")
        top_section.addWidget(self.folder_label)
        select_button = QPushButton("Selecionar Pasta")
        select_button.clicked.connect(self.select_folder)
        top_section.addWidget(select_button)
        layout.addLayout(top_section)
        
        # Create main section with categories and files
        main_section = QHBoxLayout()
        
        # Categories section
        categories_section = QVBoxLayout()
        categories_section.addWidget(QLabel("Categorias:"))
        self.categories_list = QListWidget()
        categories_section.addWidget(self.categories_list)
        add_category_button = QPushButton("Adicionar Categoria")
        add_category_button.clicked.connect(self.add_category)
        categories_section.addWidget(add_category_button)
        main_section.addLayout(categories_section)
        
        # Files section
        files_section = QVBoxLayout()
        files_section.addWidget(QLabel("Arquivos:"))
        self.files_list = QListWidget()
        files_section.addWidget(self.files_list)
        main_section.addLayout(files_section)
        
        layout.addLayout(main_section)
        
        # Create bottom section with organize button
        bottom_section = QHBoxLayout()
        organize_button = QPushButton("Organizar")
        organize_button.clicked.connect(self.organize_files)
        bottom_section.addWidget(organize_button)
        layout.addLayout(bottom_section)
        
        # Load default categories
        self.load_default_categories()
        self.selected_folder = None
    
    def load_default_categories(self):
        """Load default categories from the classifier."""
        self.classifier.load_default_categories()
        self.update_categories_list()
    
    def update_categories_list(self):
        """Update the categories list widget."""
        self.categories_list.clear()
        for category in self.classifier.categories:
            self.categories_list.addItem(category)
    
    def select_folder(self):
        """Open dialog to select a folder."""
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if folder:
            self.selected_folder = Path(folder)
            self.folder_label.setText(str(self.selected_folder))
            self.update_files_list()
    
    def update_files_list(self):
        """Update the files list widget."""
        self.files_list.clear()
        if self.selected_folder:
            for file_path in self.selected_folder.glob("*"):
                if file_path.is_file():
                    self.files_list.addItem(file_path.name)
    
    def add_category(self):
        """Open dialog to add a new category."""
        dialog = CategoryDialog(self)
        if dialog.exec():
            name, extensions = dialog.get_data()
            if name and extensions:
                self.classifier.add_category(name, extensions)
                self.update_categories_list()
    
    def auto_classify(self):
        """Classify files in the selected folder."""
        if not self.selected_folder:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta primeiro!")
            return None
        
        files = [f for f in self.selected_folder.glob("*") if f.is_file()]
        if not files:
            QMessageBox.warning(self, "Erro", "Nenhum arquivo encontrado na pasta!")
            return None
        
        return self.classifier.classify_files(files)
    
    def organize_files_by_classification(self, classification):
        """Organize files according to the classification."""
        total_files = sum(len(files) for files in classification.values())
        progress_dialog = ProgressDialog(total_files, self)
        progress_dialog.show()
        
        try:
            # Create category folders and move files
            for category, files in classification.items():
                if not files:
                    continue
                
                # Create category folder
                category_path = self.selected_folder / category
                category_path.mkdir(exist_ok=True)
                
                # Move files
                for file_path in files:
                    target_path = category_path / file_path.name
                    shutil.move(str(file_path), str(target_path))
                    progress_dialog.update_progress(file_path.name, category)
            
            QMessageBox.information(self, "Sucesso", "Arquivos organizados com sucesso!")
            self.update_files_list()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao organizar arquivos: {str(e)}")
        finally:
            progress_dialog.close()
    
    def organize_files(self):
        """Start the organization process."""
        classification = self.auto_classify()
        if classification:
            preview = PreviewDialog(classification, self)
            if preview.exec():
                self.organize_files_by_classification(classification) 