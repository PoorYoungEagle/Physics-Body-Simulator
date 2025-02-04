import utils.dark_mode as dark_mode
import gui.main_gui as main_gui

from PyQt5 import QtWidgets
import sys

def main():
    """Main entry point of the application"""

    app = QtWidgets.QApplication(sys.argv)

    # Appling dark theme
    dark_mode.set_dark_theme(app)
    
    MainWindow = QtWidgets.QMainWindow()
    ui = main_gui.ParticleSimulatorGUI()
    ui.setupGUI(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()