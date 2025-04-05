"""
Splash screen module for displaying loading progress.
"""

from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QSplashScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        # Criar um widget para o splash
        self.splash_widget = QWidget()
        layout = QVBoxLayout(self.splash_widget)
        
        # Logo
        logo_path = Path(__file__).parent.parent.parent / "resources" / "logo.png"
        if logo_path.exists():
            logo_label = QLabel()
            logo_pixmap = QPixmap(str(logo_path))
            # Redimensionar a logo para um tamanho adequado
            scaled_logo = logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_logo)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Título
        title = QLabel("Organizador de Pastas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                height: 200px;
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
        self.splash_widget.setFixedSize(400, 300)
        
        # Criar um pixmap do widget
        pixmap = QPixmap(self.splash_widget.size())
        self.splash_widget.render(pixmap)
        
        # Inicializar o splash screen com o pixmap
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    
    def update_status(self, message, value):
        """Update the status message and progress bar value."""
        if hasattr(self, 'status') and self.status is not None:
            self.status.setText(message)
            self.progress.setValue(value)
            self.repaint() 