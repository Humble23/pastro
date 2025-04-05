#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for the Pastro application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from pastro.gui import SplashScreen, FolderOrganizer

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Create and show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Simulate loading
    splash.update_status("Inicializando interface...", 20)
    QTimer.singleShot(100, lambda: splash.update_status("Carregando componentes...", 40))
    QTimer.singleShot(200, lambda: splash.update_status("Preparando classificador...", 60))
    QTimer.singleShot(300, lambda: splash.update_status("Finalizando...", 80))
    
    # Create the main window
    window = FolderOrganizer()
    
    # Finish splash and show main window
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