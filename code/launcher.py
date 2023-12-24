from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from main import Game
import sys

class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a button
        launch = QPushButton('Launch', self)
        launch.clicked.connect(self.launchGame)

        # Set window properties
        self.setWindowTitle('Game Launcher')
        self.resize(1080, 700)
        self.center()  # Center the window

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
        game = Game()
        game.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Launcher()
    sys.exit(app.exec_())
