from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt
from main import Game
import sys

class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Load the PNG image
        image_path = "launcher/splash.jpg"
        image = QImage(image_path)

        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(image)

        # Create a QBrush with the QPixmap
        brush = QBrush(pixmap)

        # Create a palette and set the background image using the QBrush
        palette = self.palette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # Make sure the widget automatically fills its background with the palette
        self.setAutoFillBackground(True)

        # Set window properties
        self.setWindowTitle('Game Launcher')
        self.setFixedSize(1280,720)

        # Create a vertical layout
        layout = QVBoxLayout(self)

        # Create a button
        launch = QPushButton('Launch', self)
        launch.setFixedSize(200, 60)
        launch.setStyleSheet('background-color: #ffc709; border-radius: 3px; font-size: 18px; font-weight: 300;')
        launch.clicked.connect(self.launchGame)

        # Add the button to the layout and align it to the bottom right corner
        layout.addWidget(launch, alignment=Qt.AlignBottom | Qt.AlignRight)

        # Center the window
        self.center()

        # Show the window
        self.show()

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def launchGame(self):
        # Launch the Pygame window from the main module
        self.close
        game = Game()
        game.run()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Launcher()
    sys.exit(app.exec_())