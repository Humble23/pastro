"""
File classifier module for automatically categorizing files.
"""

from pathlib import Path
from typing import Dict, List, Set

class AutoClassifier:
    """Automatic file classifier based on extensions."""
    
    def __init__(self):
        self.categories: Dict[str, Set[str]] = {}
    
    def load_default_categories(self):
        """Load default categories and their extensions."""
        self.categories = {
            "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
            "Documentos": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"},
            "Planilhas": {".xls", ".xlsx", ".csv", ".ods"},
            "Apresentações": {".ppt", ".pptx", ".odp"},
            "Vídeos": {".mp4", ".avi", ".mkv", ".mov", ".wmv"},
            "Áudios": {".mp3", ".wav", ".ogg", ".m4a", ".wma"},
            "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
            "Códigos": {".py", ".js", ".html", ".css", ".php", ".java", ".cpp"},
            "Executáveis": {".exe", ".msi", ".bat", ".sh"},
            "Outros": set()  # Categoria padrão para extensões não reconhecidas
        }
    
    def add_category(self, name: str, extensions: List[str]) -> None:
        """Add a new category with its extensions."""
        # Ensure extensions start with dot
        extensions_set = {ext if ext.startswith(".") else f".{ext}" for ext in extensions}
        self.categories[name] = extensions_set
    
    def get_category_for_extension(self, extension: str) -> str:
        """Get the category for a given file extension."""
        extension = extension.lower()
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return "Outros"
    
    def classify_files(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Classify a list of files into categories."""
        classification: Dict[str, List[Path]] = {category: [] for category in self.categories}
        
        for file_path in files:
            extension = file_path.suffix.lower()
            category = self.get_category_for_extension(extension)
            classification[category].append(file_path)
        
        return classification 