import utils.create_uicomponents as create
from utils.resolution_scaler import ResolutionScaler
import properties.boundary_property as boundary_property

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Boundary_UI:
    """Boundary UI and Logic"""

    def __init__(self):
        self.initial_name = "Boundary"
        self.boundary = {}
        self.current_boundary_color = QtGui.QColor(255, 255, 255)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        self.boundary_icon_path = os.path.join(base_dir, "pictures", "boundary2.png").replace('\\','/')
        self.scaler = ResolutionScaler()

    def _show_color_boundary_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_boundary_color = color
            self.color_boundary_button.setStyleSheet(f"background-color: {color.name()}")

    def setup_boundary_settings(
            self,
            settings_stacked_widget,
            universe_verticalLayout,
            add_boundary_button,
            universe_vlayout_widget,
            placeholder_widget,
            boundary_command_settings_function
        ):
        """Configure Boundary Settings"""

        self.settings_stacked_widget = settings_stacked_widget
        self.universe_verticalLayout = universe_verticalLayout
        self.add_boundary_button = add_boundary_button
        self.universe_vlayout_widget = universe_vlayout_widget
        self.placeholder_widget = placeholder_widget
        self.boundary_command_settings_function = boundary_command_settings_function

        self.boundary_settings_group = create.create_group_box(
            parent = self.settings_stacked_widget, 
            geometry = QtCore.QRect(9, 9, 931, 511),
            objname = "boundary_settings_group",
            title = "Boundary Settings",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )

        self.boundary_dimension_groupbox = create.create_group_box(
            parent = self.boundary_settings_group,
            geometry = QtCore.QRect(50, 80, 241, 181),
            font_size = 18,
            objname = "boundary_dimension_groupbox",
            title = "Boundary Regions :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.boundary_dimension_layout = create.create_grid_layout(
            parent = self.boundary_dimension_groupbox,
            objname = "boundary_dimension_layout"
        )

        self.boundary_width_label = create.create_name_label(
            parent = self.boundary_dimension_groupbox,
            objname = "boundary_width_label",
            font_size = 16,
            text = "Width : "
        )
        self.boundary_height_label = create.create_name_label(
            parent = self.boundary_dimension_groupbox,
            objname = "boundary_height_label",
            font_size = 16,
            text = "Height : "
        )
        self.boundary_depth_label = create.create_name_label(
            parent = self.boundary_dimension_groupbox,
            objname = "boundary_depth_label",
            font_size = 16,
            text = "Depth : "
        )
        self.boundary_width_lineedit = create.create_line_edit(
            parent = self.boundary_dimension_groupbox,
            font_size = 16,
            objname = "boundary_width_lineedit",
            validator = QtGui.QDoubleValidator(0, 999.99, 2),
            placeholder = "10.0"
        )
        self.boundary_height_lineedit = create.create_line_edit(
            parent = self.boundary_dimension_groupbox,
            font_size = 16,
            objname = "boundary_height_lineedit",
            validator = QtGui.QDoubleValidator(0, 999.99, 2),
            placeholder = "10.0"
        )
        self.boundary_depth_lineedit = create.create_line_edit(
            parent = self.boundary_dimension_groupbox,
            font_size = 16,
            objname = "boundary_depth_lineedit",
            validator = QtGui.QDoubleValidator(0, 999.99, 2),
            placeholder = "10.0"
        )
        
        self.boundary_dimension_layout.addWidget(self.boundary_width_label, 0, 0, 1, 1)
        self.boundary_dimension_layout.addWidget(self.boundary_height_label, 1, 0, 1, 2)
        self.boundary_dimension_layout.addWidget(self.boundary_depth_label, 2, 0, 1, 2)
        self.boundary_dimension_layout.addWidget(self.boundary_width_lineedit, 0, 2, 1, 1)
        self.boundary_dimension_layout.addWidget(self.boundary_height_lineedit, 1, 2, 1, 1)
        self.boundary_dimension_layout.addWidget(self.boundary_depth_lineedit, 2, 2, 1, 1)

        self.boundary_basic_frame = create.create_frame(
            parent = self.boundary_settings_group,
            font_size = 16,
            geometry = QtCore.QRect(400, 90, 311, 171),
            fshape = QtWidgets.QFrame.StyledPanel,
            fshadow = QtWidgets.QFrame.Raised,
            objname = "boundary_basic_frame"
        )
        self.boundary_basic_layout = create.create_grid_layout(
            parent = self.boundary_basic_frame,
            objname = "boundary_basic_layout"
        )

        self.restitution_boundary_label = create.create_name_label(
            parent = self.boundary_basic_frame,
            objname = "restitution_boundary_label",
            font_size = 16,
            text = "Restitution : "
        )
        self.restitution_spinbox = create.create_double_spinbox(
            parent = self.boundary_basic_frame,
            font_size = 16,
            objname = "restitution_spinbox",
            max = 1.0,
            min = 0.0,
            step = 0.1,
            value = 1.0
        )
        self.line_opacity_label = create.create_name_label(
            parent = self.boundary_basic_frame,
            objname = "line_opacity_label",
            font_size = 16,
            text = "Line_Opacity : "
        )
        self.line_opacity_slider = create.create_slider(
            parent = self.boundary_basic_frame,
            objname = "line_opacity_slider",
            orientation = QtCore.Qt.Horizontal
        )
        self.color_boundary_button = create.create_button(
            parent = self.boundary_basic_frame,
            font_size = 16,
            objname = "color_boundary_button",
            text = ""
        )
        self.color_boundary_label = create.create_name_label(
            parent = self.boundary_basic_frame,
            objname = "color_boundary_label",
            font_size = 16,
            text = "Color : "
        )
        self.color_boundary_button.setStyleSheet("background-color: white")

        self.color_boundary_button.clicked.connect(self._show_color_boundary_dialog)

        self.boundary_basic_layout.addWidget(self.restitution_boundary_label, 1, 0, 1, 1)
        self.boundary_basic_layout.addWidget(self.restitution_spinbox, 1, 1, 1, 1)
        self.boundary_basic_layout.addWidget(self.line_opacity_label, 2, 0, 1, 1)
        self.boundary_basic_layout.addWidget(self.line_opacity_slider, 3, 0, 1, 2)
        self.boundary_basic_layout.addWidget(self.color_boundary_button, 4, 1, 1, 1)
        self.boundary_basic_layout.addWidget(self.color_boundary_label, 4, 0, 1, 1)

        self.save_boundary_button = create.create_button(
            parent = self.boundary_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            objname = "save_boundary_button",
            font_size = 20,
            text = "Save"
        )
        self.reset_boundary_button = create.create_button(
            parent = self.boundary_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            objname = "reset_boundary_button",
            font_size = 20,
            text = "Reset"
        )
        self.delete_boundary_button = create.create_button(
            parent = self.boundary_settings_group,
            geometry = QtCore.QRect(300, 460, 150, 50),
            objname = "delete_boundary_button",
            font_size = 20,
            text = "Delete"
        )

        self.save_boundary_button.clicked.connect(self.add_boundary_details)
        self.reset_boundary_button.clicked.connect(self.reset_boundary)
        self.delete_boundary_button.clicked.connect(lambda: self.delete_boundary())

    def add_boundary_details(self):
        """Adds a boundary to the simulation"""

        width_value = float(self.boundary_width_lineedit.text()) if self.boundary_width_lineedit.text() else 10.0
        height_value = float(self.boundary_height_lineedit.text()) if self.boundary_height_lineedit.text() else 10.0
        depth_value = float(self.boundary_depth_lineedit.text()) if self.boundary_depth_lineedit.text() else 10.0

        restitution_value = float(self.restitution_spinbox.value())
        color_input = [self.current_boundary_color.redF(), self.current_boundary_color.greenF(), self.current_boundary_color.blueF()]
        slider_value = self.line_opacity_slider.value()

        boundary = boundary_property.Boundary(
            width = width_value,
            height = height_value,
            depth = depth_value,
            restitution = restitution_value,
            color = color_input,
            opacity = slider_value
        )
        self.boundary[1] = boundary
        self.placeholder_widget()

    def reset_boundary(self):
        """Resets the UI back to its placeholder values"""

        self.current_boundary_color = QtGui.QColor(255, 255, 255)
        self.color_boundary_button.setStyleSheet("background-color: white")

        self.boundary_width_lineedit.clear()
        self.boundary_height_lineedit.clear()
        self.boundary_depth_lineedit.clear()

        self.restitution_spinbox.setValue(1.0)
        self.line_opacity_slider.setValue(100)

    def delete_boundary(self):
        """Removes boundary details and logic"""

        try:
            self.add_boundary_button.setDisabled(False)

            if self.boundary:
                self.boundary.pop(1)

            self.universe_boundary.hide()
            self.universe_boundary.deleteLater
            self.universe_verticalLayout.removeWidget(self.universe_boundary)
            self.placeholder_widget()
            self.reset_boundary()
        except:
            pass

    def add_boundary_universe(self):
        """Adds a command link button to the universe stack"""

        
        self.add_boundary_button.setDisabled(True)

        self.universe_boundary = create.create_command_link(
            parent = self.universe_vlayout_widget,
            objname = "universe_boundary",
            font_size = 16,
            text = self.initial_name
        )

        if os.path.exists(self.boundary_icon_path):
            self.universe_boundary.setIcon(QtGui.QIcon(self.boundary_icon_path))
            self.universe_boundary.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))

        self.universe_verticalLayout.addWidget(self.universe_boundary)
        self.universe_boundary.clicked.connect(lambda: self.command_button_details_boundary())

    def load_boundary_universe(self, boundary_dict):
        """
        A different way of loading boundary values by passing a dictionary based on it.
        Used in saving and loading universes if a boundary exists in the saved universe
        """

        self.delete_boundary()
        self.add_boundary_button.setDisabled(True)

        self.universe_boundary = create.create_command_link(
            parent = self.universe_vlayout_widget,
            objname = "universe_boundary",
            font_size = 16,
            text = self.initial_name
        )

        if os.path.exists(self.boundary_icon_path):
            self.universe_boundary.setIcon(QtGui.QIcon(self.boundary_icon_path))
            self.universe_boundary.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))

        width_input = boundary_dict["width"]
        height_input = boundary_dict["height"]
        depth_input = boundary_dict["depth"]
        color_input = boundary_dict["color"]
        restitution_input = boundary_dict["restitution"]
        opacity_input = boundary_dict["opacity"]

        boundary = boundary_property.Boundary(
            width = width_input,
            height = height_input,
            depth = depth_input,
            restitution = restitution_input,
            color = color_input,
            opacity = opacity_input
        )
        self.boundary[1] = boundary
        self.universe_verticalLayout.addWidget(self.universe_boundary)
        self.universe_boundary.clicked.connect(lambda: self.command_button_details_boundary())

    def command_button_details_boundary(self):
        """Displays boundary details when the command link button is clicked"""

        self.boundary_command_settings_function()

        try:
            details = vars(self.boundary[1])
            self.boundary_width_lineedit.setText(str(details['width']))
            self.boundary_height_lineedit.setText(str(details['height']))
            self.boundary_depth_lineedit.setText(str(details['depth']))

            self.restitution_spinbox.setValue(details['restitution'])
            self.line_opacity_slider.setValue(details['opacity'])
            if 'color' in details:
                color = details['color']
                self.current_boundary_color = QtGui.QColor.fromRgbF(color[0], color[1], color[2])
                self.color_boundary_button.setStyleSheet(f"background-color: {self.current_boundary_color.name()}")
            else:
                self.current_boundary_color = QtGui.QColor(255, 255, 255)
                self.color_boundary_button.setStyleSheet("background-color: white")
        except:
            self.reset_boundary()