from utils.resolution_scaler import ResolutionScaler

from PyQt5 import QtGui, QtWidgets, QtCore

"""The entire PyQt5 logic is created using these functions"""

scaler = ResolutionScaler()
font_family = "Arial Rounded MT Bold" 

def create_group_box(parent, font_size, objname, title, layout, alignment, geometry=None):
    group = QtWidgets.QGroupBox(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        group.setGeometry(geometry)
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    group.setFont(font)
    group.setObjectName(objname)
    group.setTitle(title)
    group.setLayoutDirection(layout)
    group.setAlignment(alignment)

    return group

def create_frame(parent, fshape, fshadow, objname, geometry=None, font_size=None):
    frame = QtWidgets.QFrame(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        frame.setGeometry(geometry)
    frame.setFrameShape(fshape)
    frame.setFrameShadow(fshadow)
    frame.setObjectName(objname)
    if font_size:
        font_size = scaler.scale_font_size(font_size)
        font = QtGui.QFont()
        font.setPointSize(font_size)

    return frame

def create_name_label(font_size, text, objname, parent=None, geometry=None, alignment=None):
    if parent:
        label = QtWidgets.QLabel(parent)
    else:
        label = QtWidgets.QLabel()
    if geometry:
        geometry = scaler.scale_rect(geometry)
        label.setGeometry(geometry)
    if alignment:
        label.setAlignment(alignment)

    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    label.setFont(font)
    label.setText(text)
    label.setObjectName(objname)
        
    return label

def create_line_edit(parent, font_size, objname, placeholder=None, geometry=None, validator=None):
    line = QtWidgets.QLineEdit(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        line.setGeometry(geometry)

    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    line.setFont(font)
    line.setObjectName(objname)
    line.setPlaceholderText(placeholder)

    if validator:
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        line.setValidator(validator)
    

    return line

def create_grid_layout(parent, objname, alignment=None):
    grid = QtWidgets.QGridLayout(parent)
    grid.setObjectName(objname)
    if alignment:
        grid.setAlignment(QtCore.Qt.AlignTop)

    return grid

def create_checkbox(font_size, layout, objname, text, parent=None, geometry=None):
    if parent:
        check = QtWidgets.QCheckBox(parent)
    else:
        check = QtWidgets.QCheckBox()
    if geometry:
        geometry = scaler.scale_rect(geometry)
        check.setGeometry(geometry)
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    check.setFont(font)
    check.setObjectName(objname)
    check.setLayoutDirection(layout)
    check.setText(text)

    return check

def create_double_spinbox(parent, font_size, objname, max, min=0, step=0.01, value=0, geometry=None):
    double = QtWidgets.QDoubleSpinBox(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        double.setGeometry(geometry)
    
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    double.setFont(font)
    double.setMaximum(max)
    double.setMinimum(min)
    double.setSingleStep(step)
    double.setObjectName(objname)
    double.setValue(value)
    return double

def create_spinbox(parent, font_size, objname, max, min=0, step=1, value=0, geometry=None):
    spin = QtWidgets.QSpinBox(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        spin.setGeometry(geometry)

    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    spin.setFont(font)
    spin.setMaximum(max)
    spin.setMinimum(min)
    spin.setSingleStep(step)
    spin.setObjectName(objname)
    spin.setValue(value)
    return spin

def create_button(objname, font_size, text, geometry=None, parent = None):
    if parent:
        button = QtWidgets.QPushButton(parent)
    else:
        button = QtWidgets.QPushButton()

    if geometry:
        geometry = scaler.scale_rect(geometry)
        button.setGeometry(geometry)
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    button.setFont(font)
    button.setObjectName(objname)
    button.setText(text)

    return button

def create_hlayout(parent, objname):
    layout = QtWidgets.QHBoxLayout(parent)
    layout.setObjectName(objname)

    return layout

def create_vlayout(parent, objname,alignment=None):
    layout = QtWidgets.QVBoxLayout(parent)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setObjectName(objname)
    if alignment:
        layout.setAlignment(QtCore.Qt.AlignTop)

    return layout

def create_scroll(parent, objname, geometry, resizable):
    scroll = QtWidgets.QScrollArea(parent)
    geometry = scaler.scale_rect(geometry)
    scroll.setGeometry(geometry)
    scroll.setWidgetResizable(resizable)
    scroll.setObjectName(objname)
    scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    return scroll

def create_widget(objname, parent=None, geometry=None):
    widget = QtWidgets.QWidget(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        widget.setGeometry(geometry)
    widget.setObjectName(objname)

    return widget

def create_command_link(parent, font_size, objname, text, geometry=None):
    command = QtWidgets.QCommandLinkButton(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        command.setGeometry(geometry)
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    command.setFont(font)
    command.setObjectName(objname)
    command.setText(text)
    
    return command

def create_line(parent, fshape, fshadow, width, objname, geometry=None):
    line = QtWidgets.QFrame(parent)
    line.setFrameShape(fshape)
    line.setFrameShadow(fshadow)
    line.setLineWidth(width)
    line.setObjectName(objname)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        line.setGeometry(geometry)

def create_openGL_geometry(geometry):
    geometry = scaler.scale_rect(geometry)

    return geometry

def create_slider(parent, objname, orientation, geometry=None):
    slider = QtWidgets.QSlider(parent)
    slider.setOrientation(orientation)
    slider.setRange(0, 100)
    slider.setValue(100)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        slider.setGeometry(geometry)
    slider.setObjectName(objname)

    return slider

def create_tabs(parent, geometry, font_size, objname):
    tabs = QtWidgets.QTabWidget(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        tabs.setGeometry(geometry)
    
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    tabs.setFont(font)
    tabs.setObjectName(objname)

    return tabs

def create_radio(parent):
    radio = QtWidgets.QRadioButton(parent)
    radio.setText("")

    return radio

def create_stacked_widget(parent, geometry, fshape, fshadow, objname):
    stacked = QtWidgets.QStackedWidget(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        stacked.setGeometry(geometry)
    stacked.setFrameShape(fshape)
    stacked.setFrameShadow(fshadow)
    stacked.setObjectName(objname)

    return stacked

def create_text_edit(parent, geometry, font_size, placeholder, objname):
    text = QtWidgets.QTextEdit(parent)
    if geometry:
        geometry = scaler.scale_rect(geometry)
        text.setGeometry(geometry)
    font_size = scaler.scale_font_size(font_size)
    font = QtGui.QFont(font_family, font_size)
    text.setFont(font)
    text.setPlaceholderText(placeholder)
    text.setObjectName(objname)

    return text