"""
Auto classifier module for the Folder Organizer System.
"""

from pathlib import Path
from typing import Dict, List, Set
import mimetypes
import re

class AutoClassifier:
    def __init__(self):
        # Default categories with their file extensions and patterns
        self.categories = {
            "Imagens": {
                "extensions": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"},
                "patterns": []
            },
            "Documentos": {
                "extensions": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx"},
                "patterns": []
            },
            "Vídeos": {
                "extensions": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
                "patterns": []
            },
            "Áudio": {
                "extensions": {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"},
                "patterns": []
            },
            "Compactados": {
                "extensions": {".zip", ".rar", ".7z", ".tar", ".gz"},
                "patterns": []
            },
            "Códigos": {
                "extensions": {".py", ".js", ".html", ".css", ".java", ".cpp", ".php", ".sql"},
                "patterns": []
            },
            "Downloads": {
                "extensions": {".crdownload", ".part", ".download"},
                "patterns": [r"^download_\d+"]
            }
        }

    def classify_file(self, file_path: Path) -> str:
        """
        Classify a single file based on its extension and name pattern.
        Returns the category name.
        """
        file_ext = file_path.suffix.lower()
        file_name = file_path.name.lower()

        # Try to classify by extension first
        for category, rules in self.categories.items():
            if file_ext in rules["extensions"]:
                return category

            # Check patterns if no extension match
            for pattern in rules["patterns"]:
                if re.search(pattern, file_name):
                    return category

        # If no match found, try to get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith("image/"):
                return "Imagens"
            elif mime_type.startswith("video/"):
                return "Vídeos"
            elif mime_type.startswith("audio/"):
                return "Áudio"
            elif mime_type.startswith("text/"):
                return "Documentos"
            elif mime_type.startswith("application/"):
                if "compressed" in mime_type or "zip" in mime_type:
                    return "Compactados"
                return "Documentos"

        # If still no match, classify as "Outros"
        return "Outros"

    def classify_files(self, folder_path: Path) -> Dict[str, List[Path]]:
        """
        Classify all files in a folder.
        Returns a dictionary with categories as keys and lists of file paths as values.
        """
        classification = {}
        
        for file_path in folder_path.glob("*"):
            if file_path.is_file():
                category = self.classify_file(file_path)
                if category not in classification:
                    classification[category] = []
                classification[category].append(file_path)
        
        return classification

    def get_categories(self) -> Set[str]:
        """Return all available categories"""
        return set(self.categories.keys()) | {"Outros"} 