from PyQt5 import QtGui, QtCore

def set_dark_theme(app):
    app.setStyle('Fusion')
    
    # Set up for dark theme
    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(127, 127, 127))
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(42, 42, 42))
    darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(66, 66, 66))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(127, 127, 127))
    darkPalette.setColor(QtGui.QPalette.Dark, QtGui.QColor(35, 35, 35))
    darkPalette.setColor(QtGui.QPalette.Shadow, QtGui.QColor(20, 20, 20))
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(127, 127, 127))
    darkPalette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(80, 80, 80))
    darkPalette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, QtGui.QColor(127, 127, 127))
    
    app.setPalette(darkPalette)

def set_light_theme(app):
    app.setStyle('Fusion')
    
    # Set up for light theme
    lightPalette = QtGui.QPalette()
    lightPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
    lightPalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
    lightPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(128, 128, 128))
    lightPalette.setColor(QtGui.QPalette.Base, QtCore.Qt.white)
    lightPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(233, 233, 233))
    lightPalette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
    lightPalette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
    lightPalette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
    lightPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(128, 128, 128))
    lightPalette.setColor(QtGui.QPalette.Dark, QtGui.QColor(160, 160, 160))
    lightPalette.setColor(QtGui.QPalette.Shadow, QtGui.QColor(201, 201, 201))
    lightPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(240, 240, 240))
    lightPalette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.black)
    lightPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(128, 128, 128))
    lightPalette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    lightPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(0, 122, 204))
    lightPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 120, 215))
    lightPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(200, 200, 200))
    lightPalette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)
    lightPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, QtGui.QColor(128, 128, 128))
    
    app.setPalette(lightPalette)