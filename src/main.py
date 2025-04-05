#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main application file for the Folder Organizer System.
"""

import sys
import shutil
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QDialog,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QScrollArea,
    QProgressBar,
    QPlainTextEdit,
    QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from pathlib import Path
from auto_classifier import AutoClassifier
from datetime import datetime

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        # Criar um widget para o splash
        self.splash_widget = QWidget()
        layout = QVBoxLayout(self.splash_widget)
        
        # Logo
        logo_path = Path(__file__).parent / "resources" / "logo.png"
        if logo_path.exists():
            logo_label = QLabel()
            logo_pixmap = QPixmap(str(logo_path))
            # Redimensionar a logo para um tamanho adequado
            scaled_logo = logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_logo)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Título
        title = QLabel("Sistema Organizador\nde Pastas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                margin: 20px;
            }
        """)
        layout.addWidget(title)
        
        # Mensagem de carregamento
        self.status = QLabel("Carregando...")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.status)
        
        # Barra de progresso
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                margin: 10px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                width: 10px;
                margin: 0.5px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Configurar o widget
        self.splash_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
            }
        """)
        self.splash_widget.setFixedSize(400, 300)  # Aumentei a altura para acomodar a logo
        
        # Criar um pixmap do widget
        pixmap = QPixmap(self.splash_widget.size())
        self.splash_widget.render(pixmap)
        
        # Inicializar o splash screen com o pixmap
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    
    def update_status(self, message, value):
        if hasattr(self, 'status') and self.status is not None:
            self.status.setText(message)
            self.progress.setValue(value)
            self.repaint()

class CategoryDialog(QDialog):
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
        name = self.name_input.text().strip()
        extensions = [ext.strip() for ext in self.extensions_input.text().split(",") if ext.strip()]
        return name, extensions

class PreviewDialog(QDialog):
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
        """Update progress bar and log"""
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
        
        # Process events to update UI
        QApplication.processEvents()

class FolderOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Organizador de Pastas")
        self.setGeometry(100, 100, 1000, 600)
        
        # Set window icon
        icon_path = Path(__file__).parent / "resources" / "logo.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Initialize auto classifier
        self.auto_classifier = AutoClassifier()
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left panel - Categories
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Categorias:"))
        self.categories_list = QListWidget()
        left_layout.addWidget(self.categories_list)
        
        # Category buttons
        cat_buttons = QHBoxLayout()
        add_category_btn = QPushButton("Adicionar Categoria")
        add_category_btn.clicked.connect(self.add_category)
        auto_classify_btn = QPushButton("Classificar Automaticamente")
        auto_classify_btn.clicked.connect(self.auto_classify)
        cat_buttons.addWidget(add_category_btn)
        cat_buttons.addWidget(auto_classify_btn)
        left_layout.addLayout(cat_buttons)
        
        layout.addWidget(left_panel)
        
        # Right panel - Files and Folders
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Folder selection
        folder_btn = QPushButton("Selecionar Pasta")
        folder_btn.clicked.connect(self.select_folder)
        right_layout.addWidget(folder_btn)
        
        # Files list
        right_layout.addWidget(QLabel("Arquivos:"))
        self.files_list = QListWidget()
        right_layout.addWidget(self.files_list)
        
        # Organize button
        organize_btn = QPushButton("Organizar")
        organize_btn.clicked.connect(self.organize_files)
        right_layout.addWidget(organize_btn)
        
        layout.addWidget(right_panel)
        
        # Initialize variables
        self.selected_folder = None
        self.categories = {}
        
        # Load default categories from auto classifier
        self.load_default_categories()
        
        self.show()
    
    def load_default_categories(self):
        """Load default categories from auto classifier"""
        self.categories = self.auto_classifier.categories.copy()
        self.update_categories_list()
    
    def update_categories_list(self):
        """Update the categories list widget"""
        self.categories_list.clear()
        for category in sorted(self.categories.keys()):
            self.categories_list.addItem(category)
    
    def select_folder(self):
        """Open dialog to select folder to organize"""
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if folder:
            self.selected_folder = Path(folder)
            self.update_files_list()
    
    def update_files_list(self):
        """Update the files list with contents of selected folder"""
        if not self.selected_folder:
            return
            
        self.files_list.clear()
        for file_path in self.selected_folder.glob("*"):
            if file_path.is_file():
                self.files_list.addItem(file_path.name)
    
    def add_category(self):
        """Add a new category with custom rules"""
        dialog = CategoryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, extensions = dialog.get_data()
            if name and extensions:
                self.categories[name] = {
                    "extensions": set(extensions),
                    "patterns": []
                }
                self.update_categories_list()
    
    def auto_classify(self):
        """Automatically classify files in the selected folder"""
        if not self.selected_folder:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma pasta primeiro!")
            return
        
        # Get classification
        classification = self.auto_classifier.classify_files(self.selected_folder)
        
        # Show preview dialog
        preview = PreviewDialog(classification, self)
        if preview.exec() == QDialog.DialogCode.Accepted:
            self.organize_files_by_classification(classification)
    
    def organize_files_by_classification(self, classification):
        """Organize files according to the given classification"""
        try:
            # Count total files
            total_files = sum(len(files) for files in classification.values())
            
            # Create and show progress dialog
            progress_dialog = ProgressDialog(total_files, self)
            progress_dialog.show()
            
            for category, files in classification.items():
                # Create category folder
                category_path = self.selected_folder / category
                category_path.mkdir(exist_ok=True)
                
                # Add log entry for category creation
                progress_dialog.log_area.appendPlainText(f"\n[{datetime.now().strftime('%H:%M:%S')}] Criando pasta '{category}'")
                
                # Move files
                for file_path in files:
                    target_path = category_path / file_path.name
                    if target_path.exists():
                        # If file exists, add number to filename
                        base = target_path.stem
                        suffix = target_path.suffix
                        counter = 1
                        while target_path.exists():
                            target_path = category_path / f"{base}_{counter}{suffix}"
                            counter += 1
                    
                    # Move file and update progress
                    shutil.move(str(file_path), str(target_path))
                    progress_dialog.update_progress(file_path.name, category)
            
            # Final log entry
            progress_dialog.log_area.appendPlainText(f"\n[{datetime.now().strftime('%H:%M:%S')}] Organização concluída com sucesso!")
            
            # Wait a moment before closing
            QTimer.singleShot(2000, progress_dialog.accept)
            
            self.update_files_list()
        
        except Exception as e:
            error_msg = f"Erro ao organizar arquivos: {str(e)}"
            progress_dialog.log_area.appendPlainText(f"\n[{datetime.now().strftime('%H:%M:%S')}] ERRO: {error_msg}")
            QMessageBox.critical(self, "Erro", error_msg)
    
    def organize_files(self):
        """Organize files based on selected categories"""
        if not self.selected_folder:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma pasta primeiro!")
            return
        
        # Use auto classifier to organize files
        self.auto_classify()

def main():
    app = QApplication(sys.argv)
    
    # Criar e mostrar splash screen
    splash = SplashScreen()
    splash.show()
    
    # Simular carregamento
    splash.update_status("Inicializando interface...", 20)
    QTimer.singleShot(100, lambda: splash.update_status("Carregando componentes...", 40))
    QTimer.singleShot(200, lambda: splash.update_status("Preparando classificador...", 60))
    QTimer.singleShot(300, lambda: splash.update_status("Finalizando...", 80))
    
    # Criar a janela principal
    window = FolderOrganizer()
    
    # Finalizar splash e mostrar janela principal
    QTimer.singleShot(400, lambda: (
        splash.update_status("Pronto!", 100),
        QTimer.singleShot(200, lambda: (
            splash.finish(window),
            window.show()
        ))
    ))
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 