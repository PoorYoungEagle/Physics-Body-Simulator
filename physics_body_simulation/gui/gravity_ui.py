import utils.create_uicomponents as create
from utils.resolution_scaler import ResolutionScaler
import properties.gravity_property as gravity_property

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Gravity_UI:
    """Gravity Plane UI and Logic"""

    def __init__(self):
        self.gravity = {}
        self.no_of_gravity = 0
        self.initial_name_gravity = 'G' + str(self.no_of_gravity)
        self.current_gravity_command_id = None
        self.command_link_gravity_buttons = {}
        self.gravity_classes = {}

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        self.gravity_icon_path = os.path.join(base_dir, "pictures", "gravity_command.png").replace('\\','/')
        self.scaler = ResolutionScaler()

    def _show_plane_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_plane_color = color
            self.plane_color_button.setStyleSheet(f'background-color: {color.name()}')
    
    def _show_line_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_line_color = color
            self.line_color_button.setStyleSheet(f'background-color: {color.name()}')

    def _set_plane_design(self, design):
        self.plane_design = design
        self.plane_design_button.setText(design)

    def _show_design_plane_dialog(self):
        menu = QtWidgets.QMenu(self.plane_design_button)

        fill_action = menu.addAction("Fill")
        outline_action = menu.addAction("Outline")

        fill_action.triggered.connect(lambda: self._set_plane_design("Fill"))
        outline_action.triggered.connect(lambda: self._set_plane_design("Outline"))
            
        menu.exec_(self.plane_design_button.mapToGlobal(self.plane_design_button.rect().bottomLeft()))    

    def setup_gravity_settings(
            self,
            settings_stacked_widget,
            universe_verticalLayout,
            universe_vlayout_widget,
            placeholder_widget,
            gravity_command_settings_function
        ):
        """Configure Gravity Settings"""

        self.settings_stacked_widget = settings_stacked_widget
        self.universe_verticalLayout = universe_verticalLayout
        self.universe_vlayout_widget = universe_vlayout_widget
        self.placeholder_widget = placeholder_widget
        self.gravity_command_settings_function = gravity_command_settings_function

        self.gravity_settings_group = create.create_group_box(
            parent = self.settings_stacked_widget,
            geometry = QtCore.QRect(9, 9, 931, 511),
            font_size = 20,
            objname = "add_matter_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Gravity Settings"
        )
        self.name_gravity_label = create.create_name_label(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(40, 40, 81, 41),
            font_size = 16,
            text = "Name :",
            objname = "name_gravity_label"
        )
        self.name_gravity_lineedit = create.create_line_edit(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(130, 40, 151, 41),
            font_size = 14,
            objname = "name_gravity_lineedit"
        )

        # Position of Gravity Plane

        self.position_gravity_groupbox = create.create_group_box(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(0, 110, 180, 180),
            font_size = 18,
            objname = "add_matter_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft,
            title = "Position (m) :"
        )
        self.position_grid_layout = create.create_grid_layout(
            parent = self.position_gravity_groupbox,
            objname = "position_grid_layout"
        )
        self.x_axis_gravity_label = create.create_name_label(
            parent = self.position_gravity_groupbox,
            font_size = 16,
            objname = "x_axis_gravity_label",
            text = "X Axis :"
        )
        self.y_axis_gravity_label = create.create_name_label(
            parent = self.position_gravity_groupbox,
            font_size = 16,
            objname = "y_axis_gravity_label",
            text = "Y Axis :"
        )
        self.z_axis_gravity_label = create.create_name_label(
            parent = self.position_gravity_groupbox,
            font_size = 16,
            objname = "z_axis_gravity_label",
            text = "Z Axis :"
        )
        self.x_axis_gravity_lineedit = create.create_line_edit(
            parent = self.position_gravity_groupbox,
            font_size = 16,
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 2),
            objname = "x_axiz_gravity_lineedit",
            placeholder = "0.0"
        )
        self.y_axis_gravity_lineedit = create.create_line_edit(
            parent = self.position_gravity_groupbox,
            font_size = 16,
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 2),
            objname = "y_axiz_gravity_lineedit",
            placeholder = "0.0"
        )
        self.z_axis_gravity_lineedit = create.create_line_edit(
            parent = self.position_gravity_groupbox,
            font_size = 16,
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 2),
            objname = "z_axiz_gravity_lineedit",
            placeholder = "0.0"
        )
        
        self.position_grid_layout.addWidget(self.x_axis_gravity_label, 0, 0, 1, 1)
        self.position_grid_layout.addWidget(self.y_axis_gravity_label, 1, 0, 1, 2)
        self.position_grid_layout.addWidget(self.z_axis_gravity_label, 2, 0, 1, 2)
        self.position_grid_layout.addWidget(self.x_axis_gravity_lineedit, 0, 2, 1, 1)
        self.position_grid_layout.addWidget(self.y_axis_gravity_lineedit, 1, 2, 1, 1)
        self.position_grid_layout.addWidget(self.z_axis_gravity_lineedit, 2, 2, 1, 1)

        # Normal for Plane

        self.normal_gravity_groupbox = create.create_group_box(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(200, 110, 180, 180),
            font_size = 18,
            objname = "normal_gravity_groupbox",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft,
            title = "Normal (m) :"
        )
        self.normal_grid_layout = create.create_grid_layout(
            parent = self.normal_gravity_groupbox,
            objname = "normal_grid_layout"
        )
        self.x_normal_gravity_label = create.create_name_label(
            parent = self.normal_gravity_groupbox,
            font_size = 16,
            text = "X Axis",
            objname = "x_normal_gravity_label"
        )
        self.y_normal_gravity_label = create.create_name_label(
            parent = self.normal_gravity_groupbox,
            font_size = 16,
            text = "Y Axis",
            objname = "y_normal_gravity_label"
        )
        self.z_normal_gravity_label = create.create_name_label(
            parent = self.normal_gravity_groupbox,
            font_size = 16,
            text = "Z Axis",
            objname = "z_normal_gravity_label"
        )
        self.x_normal_gravity_spinbox = create.create_double_spinbox(
            parent = self.normal_gravity_groupbox,
            font_size = 16,
            max = 1.0,
            min = -1.0,
            step = 0.01,
            objname = "x_normal_gravity_spinbox",
            value = 0.0
        )
        self.y_normal_gravity_spinbox = create.create_double_spinbox(
            parent = self.normal_gravity_groupbox,
            font_size = 16,
            max = 1.0,
            min = -1.0,
            step = 0.01,
            objname = "y_normal_gravity_spinbox",
            value = 1.0
        )
        self.z_normal_gravity_spinbox = create.create_double_spinbox(
            parent = self.normal_gravity_groupbox,
            font_size = 16,
            max = 1.0,
            min = -1.0,
            step = 0.01,
            objname = "z_normal_gravity_spinbox",
            value = 0.0
        )

        self.normal_grid_layout.addWidget(self.x_normal_gravity_label, 0, 0, 1, 1)
        self.normal_grid_layout.addWidget(self.y_normal_gravity_label, 1, 0, 1, 2)
        self.normal_grid_layout.addWidget(self.z_normal_gravity_label, 2, 0, 1, 2)
        self.normal_grid_layout.addWidget(self.x_normal_gravity_spinbox, 0, 2, 1, 1)
        self.normal_grid_layout.addWidget(self.y_normal_gravity_spinbox, 1, 2, 1, 1)
        self.normal_grid_layout.addWidget(self.z_normal_gravity_spinbox, 2, 2, 1, 1)

        # Size of Gravity Plane

        self.gravity_size_groupbox = create.create_group_box(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(390, 110, 190, 180),
            font_size = 18,
            objname = "gravity_size_groupbox",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft,
            title = "Size (m) :"
        )
        self.gravity_size_grid = create.create_grid_layout(
            parent = self.gravity_size_groupbox,
            objname = "gravity_size_grid"
        )
        self.width_label = create.create_name_label(
            parent = self.gravity_size_groupbox,
            font_size = 16,
            objname = "width_label",
            text = "Width :"
        )
        self.depth_label = create.create_name_label(
            parent = self.gravity_size_groupbox,
            font_size = 16,
            objname = "depth_label",
            text = "Depth :"
        )
        self.width_lineedit = create.create_line_edit(
            parent = self.gravity_size_groupbox,
            font_size = 16,
            objname = "width_lineedit",
            placeholder = "5.0",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 2)
        )
        self.depth_lineedit = create.create_line_edit(
            parent = self.gravity_size_groupbox,
            font_size = 16,
            objname = "depth_lineedit",
            placeholder = "5.0",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 2)
        )

        self.gravity_size_grid.addWidget(self.width_label, 0, 0, 1, 1)
        self.gravity_size_grid.addWidget(self.depth_label, 1, 0, 1, 1)
        self.gravity_size_grid.addWidget(self.width_lineedit, 0, 1, 1, 1)
        self.gravity_size_grid.addWidget(self.depth_lineedit, 1, 1, 1, 1)


        # Gravity Basic Functions

        self.gravity_basic_frame = create.create_frame(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(590, 80, 340, 410),
            font_size = 16,
            fshape = QtWidgets.QFrame.StyledPanel,
            fshadow = QtWidgets.QFrame.Raised,
            objname = "gravity_basic_frame"
        )
        self.gravity_basic_grid = create.create_grid_layout(
            parent = self.gravity_basic_frame,
            objname = "gravity_basic_grid"
        )
        self.collision_gravity_checkbox = create.create_checkbox(
            parent = self.gravity_basic_frame,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "collision_gravity_checkbox",
            text = "Collision"
        )
        self.gravity_strength_label = create.create_name_label(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Gravity Strength : ",
            objname = "gravity_strength_label"
        )
        self.gravity_strength_lineedit = create.create_line_edit(
            parent = self.gravity_basic_frame,
            font_size = 16,
            validator = QtGui.QDoubleValidator(0, 999.99, 2),
            objname = "gravity_strength_lineedit",
            placeholder = "9.8"
        )
        self.plane_design_label = create.create_name_label(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Plane Design : ",
            objname = "plane_design_label"
        )
        self.plane_design_button = create.create_button(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Design",
            objname = "plane_design_button"
        )
        self.plane_color_label = create.create_name_label(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Plane Color : ",
            objname = "plane_opacity_label"
        )
        self.plane_color_button = create.create_button(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "",
            objname = "plane_design_button"
        )
        self.plane_opacity_label = create.create_name_label(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Plane Opacity : ",
            objname = "plane_opacity_label"
        )
        self.plane_opacity_slider = create.create_slider(
            parent = self.gravity_basic_frame,
            objname = "plane_opacity_slider",
            orientation = QtCore.Qt.Horizontal
        )
        self.line_color_label = create.create_name_label(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Line Color : ",
            objname = "line_color_label"
        )
        self.line_color_button = create.create_button(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "",
            objname = "line_color_button"
        )
        self.line_opacity_label = create.create_name_label(
            parent = self.gravity_basic_frame,
            font_size = 16,
            text = "Line Opacity : ",
            objname = "line_opacity_label"
        )
        self.line_opacity_slider = create.create_slider(
            parent = self.gravity_basic_frame,
            objname = "line_opacity_slider",
            orientation = QtCore.Qt.Horizontal
        )

        self.plane_color_button.setStyleSheet("background-color: white")
        self.line_color_button.setStyleSheet("background-color: white")

        self.current_plane_color = QtGui.QColor(255, 255, 255)
        self.current_line_color = QtGui.QColor(255, 255, 255)

        self.plane_design_button.clicked.connect(self._show_design_plane_dialog)
        self.plane_color_button.clicked.connect(self._show_plane_color_dialog)
        self.line_color_button.clicked.connect(self._show_line_color_dialog)

        self.gravity_basic_grid.addWidget(self.collision_gravity_checkbox, 0, 0, 1, 1)
        self.gravity_basic_grid.addWidget(self.gravity_strength_label, 1, 0, 1, 2)
        self.gravity_basic_grid.addWidget(self.gravity_strength_lineedit, 1, 2, 1, 1)
        self.gravity_basic_grid.addWidget(self.plane_design_label, 2, 0, 1, 1)
        self.gravity_basic_grid.addWidget(self.plane_design_button, 2, 1, 1, 2)
        self.gravity_basic_grid.addWidget(self.plane_color_label, 3, 0, 1, 1)
        self.gravity_basic_grid.addWidget(self.plane_color_button, 3, 1, 1, 2)
        self.gravity_basic_grid.addWidget(self.plane_opacity_label, 4, 0, 1, 1)
        self.gravity_basic_grid.addWidget(self.plane_opacity_slider, 4, 2, 1, 1)
        self.gravity_basic_grid.addWidget(self.line_color_label, 5, 0, 1, 1)
        self.gravity_basic_grid.addWidget(self.line_color_button, 5, 1, 1, 2)
        self.gravity_basic_grid.addWidget(self.line_opacity_label, 6, 0, 1, 1)
        self.gravity_basic_grid.addWidget(self.line_opacity_slider, 6, 2, 1, 1)


        # Save, Reset and Delete Buttons

        self.save_gravity_button = create.create_button(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            objname = "save_gravity_button",
            font_size = 20,
            text = "Save"
        )
        self.reset_gravity_button = create.create_button(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            objname = "reset_gravity_button",
            font_size = 20,
            text = "Reset"
        )
        self.delete_gravity_button = create.create_button(
            parent = self.gravity_settings_group,
            geometry = QtCore.QRect(300, 460, 150, 50),
            objname = "delete_gravity_button",
            font_size = 20,
            text = "Delete"
        )

        self.save_gravity_button.clicked.connect(self.add_gravity_details)
        self.reset_gravity_button.clicked.connect(self.reset_gravity)
        self.delete_gravity_button.clicked.connect(lambda: self.delete_gravity())

    def add_gravity_details(self):
        """Adds a Gravity Plane to the simulation"""

        x_gravity_value = float(self.x_axis_gravity_lineedit.text()) if self.x_axis_gravity_lineedit.text() else 0.0
        y_gravity_value = float(self.y_axis_gravity_lineedit.text()) if self.y_axis_gravity_lineedit.text() else 0.0
        z_gravity_value = float(self.z_axis_gravity_lineedit.text()) if self.z_axis_gravity_lineedit.text() else 0.0

        x_normal_value = float(self.x_normal_gravity_spinbox.value()) if self.x_normal_gravity_spinbox.value() else 0.0
        y_normal_value = float(self.y_normal_gravity_spinbox.value()) if self.y_normal_gravity_spinbox.value() else 0.0
        z_normal_value = float(self.z_normal_gravity_spinbox.value()) if self.z_normal_gravity_spinbox.value() else 0.0

        width_value = float(self.width_lineedit.text()) if self.width_lineedit.text() else 5.0
        depth_value = float(self.depth_lineedit.text()) if self.depth_lineedit.text() else 5.0

        name_input = self.name_gravity_lineedit.text() if self.name_gravity_lineedit.text() else 'G' + str(self.current_gravity_command_id)
        collision_input = self.collision_gravity_checkbox.isChecked()
        gravity_strength_input = self.gravity_strength_lineedit.text() if self.gravity_strength_lineedit.text() else 9.8
        
        plane_color_input = [self.current_plane_color.redF(), self.current_plane_color.greenF(), self.current_plane_color.blueF()]
        line_color_input = [self.current_line_color.redF(), self.current_line_color.greenF(), self.current_line_color.blueF()]
        design_input = self.plane_design_button.text() if self.plane_design_button.text() else "Fill"
        plane_slider_value = self.plane_opacity_slider.value()
        line_slider_value = self.line_opacity_slider.value()
        position_input = [x_gravity_value, y_gravity_value, z_gravity_value]
        normal_input = [x_normal_value, y_normal_value, z_normal_value]

        if normal_input == [0, 0, 0]:
            normal_input = [0, 1, 0]

        gravity = gravity_property.Gravity(
            name = name_input,
            collision = collision_input,
            position = position_input,
            normal = normal_input,
            width = width_value,
            depth = depth_value,
            gravity_strength = gravity_strength_input,
            design = design_input,
            plane_color = plane_color_input,
            plane_opacity = plane_slider_value,
            line_color = line_color_input,
            line_opacity = line_slider_value
        )

        gravity.create_plane()
        self.gravity[self.current_gravity_command_id] = [name_input, gravity]
        self.gravity_classes[self.current_gravity_command_id] = gravity
        name_update = self.command_link_gravity_buttons[self.current_gravity_command_id]
        name_update.setText(name_input)
        
        self.placeholder_widget()

    def reset_gravity(self):
        """Resets the UI back to its placeholder values"""
        
        try:
            gravity_details = self.gravity.get(self.current_gravity_command_id)
            name = gravity_details[0]
            self.name_gravity_lineedit.setText(name)
            self.current_plane_color = QtGui.QColor(255, 255, 255)
            self.current_line_color = QtGui.QColor(255, 255, 255)
            self.plane_color_button.setStyleSheet("background-color: white")
            self.line_color_button.setStyleSheet("background-color: white")
        except:
            self.name_gravity_lineedit.setPlaceholderText('G' + str(self.current_gravity_command_id))

        self.x_axis_gravity_lineedit.clear()
        self.y_axis_gravity_lineedit.clear()
        self.z_axis_gravity_lineedit.clear()

        self.x_normal_gravity_spinbox.setValue(0.0)
        self.y_normal_gravity_spinbox.setValue(1.0)
        self.z_normal_gravity_spinbox.setValue(0.0)

        self.width_lineedit.clear()
        self.depth_lineedit.clear()
        self.name_gravity_lineedit.clear()
        self.gravity_strength_lineedit.clear()

        self.plane_design_button.setText("Fill")
        self.plane_opacity_slider.setValue(100)
        self.line_opacity_slider.setValue(100)
        self.collision_gravity_checkbox.setChecked(False)

    def delete_all_gravity(self):
        """Removes all gravity plane details and logic"""

        try:
            id_keys = list(self.command_link_gravity_buttons.keys())
            for id in id_keys:
                try:
                    button_remove = self.command_link_gravity_buttons.pop(id)
                    self.universe_verticalLayout.removeWidget(button_remove)
                    button_remove.hide()
                    button_remove.deleteLater()
                    self.gravity.pop(id)
                    try:
                        self.gravity_classes.pop(id)
                    except:
                        pass
                except:
                    pass
            self.no_of_gravity = 0
            self.current_gravity_command_id = None
            self.placeholder_widget()
            self.reset_gravity()
        except:
            pass

    def delete_gravity(self):
        """Removes specified gravity plane details and logic"""

        button_remove = self.command_link_gravity_buttons.pop(self.current_gravity_command_id)
        self.universe_verticalLayout.removeWidget(button_remove)
        button_remove.hide()
        button_remove.deleteLater()
        self.gravity.pop(self.current_gravity_command_id)

        try:
            self.gravity_classes.pop(self.current_gravity_command_id)
        except:
            pass

        self.placeholder_widget()
        self.reset_gravity()

    def add_gravity_universe(self):
        """Adds a command link button to the universe stack"""

        self.no_of_gravity += 1
        self.current_gravity_command_id = self.no_of_gravity
        self.initial_name_gravity = 'G' + str(self.no_of_gravity)

        self.universe_gravity = create.create_command_link(
            parent = self.universe_vlayout_widget,
            objname = "gravity_universe_particle",
            font_size = 16,
            text = self.initial_name_gravity
        )

        if os.path.exists(self.gravity_icon_path):
            self.universe_gravity.setIcon(QtGui.QIcon(self.gravity_icon_path))
            self.universe_gravity.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))
        self.universe_verticalLayout.addWidget(self.universe_gravity)
        self.universe_gravity.clicked.connect(lambda _, num = self.current_gravity_command_id: self.command_button_details_gravity(num))
        self.command_link_gravity_buttons[self.no_of_gravity] = self.universe_gravity

        self.current_plane_color = QtGui.QColor(255, 255, 255)
        self.current_line_color = QtGui.QColor(255, 255, 255)

    def load_gravity_universe(self, gravity_dicts):
        """
        A different way of loading gravity plane values by passing a dictionary based on it.
        Used in saving and loading universes if a gravity plane exists in the saved universe
        """

        self.delete_all_gravity()

        for gravity_details in gravity_dicts:

            self.no_of_gravity += 1
            self.current_gravity_command_id = self.no_of_gravity

            name_input = gravity_details["name"]
            position_input = gravity_details["position"]
            normal_input = gravity_details["normal"]
            gravity_strength_input = gravity_details["gravity_strength"]
            width_input = gravity_details["width"]
            depth_input = gravity_details["depth"]
            design_input = gravity_details["design"]
            plane_color_input = gravity_details["plane_color"]
            plane_opacity_input = gravity_details["plane_opacity"]
            line_color_input = gravity_details["line_color"]
            line_opacity_input = gravity_details["line_opacity"]
            collision_input = gravity_details["collision"]

            self.universe_gravity = create.create_command_link(
                parent = self.universe_vlayout_widget,
                objname = "gravity_universe_particle",
                font_size = 16,
                text = name_input
            )

            if os.path.exists(self.gravity_icon_path):
                self.universe_gravity.setIcon(QtGui.QIcon(self.gravity_icon_path))
                self.universe_gravity.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))

            gravity = gravity_property.Gravity(
                name = name_input,
                collision = collision_input,
                position = position_input,
                normal = normal_input,
                width = width_input,
                depth = depth_input,
                gravity_strength = gravity_strength_input,
                design = design_input,
                plane_color = plane_color_input,
                plane_opacity = plane_opacity_input,
                line_color = line_color_input,
                line_opacity = line_opacity_input
            )
            gravity.create_plane()
            self.gravity[self.current_gravity_command_id] = [name_input, gravity]
            self.gravity_classes[self.current_gravity_command_id] = gravity

            self.universe_verticalLayout.addWidget(self.universe_gravity)
            self.universe_gravity.clicked.connect(lambda _, num = self.current_gravity_command_id: self.command_button_details_gravity(num))
            self.command_link_gravity_buttons[self.no_of_gravity] = self.universe_gravity

    def command_button_details_gravity(self, command_id):
        """Displays specific gravity plane details when the command link button is clicked"""

        self.current_gravity_command_id = command_id
        self.gravity_command_settings_function()
        details = None
        try:
            
            gravity_details = self.gravity.get(command_id)
            name = gravity_details[0]
            details = vars(gravity_details[1])
            if command_id in self.gravity.keys():

                self.name_gravity_lineedit.setText(name)
                self.collision_gravity_checkbox.setChecked(True) if details['collision'] else self.collision_gravity_checkbox.setChecked(False)
                self.gravity_strength_lineedit.setText(str(details['gravity_strength']))

                position = details['position']
                self.x_axis_gravity_lineedit.setText(str(position[0]))
                self.y_axis_gravity_lineedit.setText(str(position[1]))
                self.z_axis_gravity_lineedit.setText(str(position[2]))

                normal = details['normal']
                self.x_normal_gravity_spinbox.setValue(normal[0])
                self.y_normal_gravity_spinbox.setValue(normal[1])
                self.z_normal_gravity_spinbox.setValue(normal[2])

                width = details['width']
                depth = details['depth']
                self.width_lineedit.setText(str(width))
                self.depth_lineedit.setText(str(depth))

                self.plane_design_button.setText(details['design'])
                self.plane_opacity_slider.setValue(details['plane_opacity'])
                self.line_opacity_slider.setValue(details['line_opacity'])

                if 'plane_color' in details:
                    color = details['plane_color']
                    self.current_plane_color = QtGui.QColor.fromRgbF(color[0], color[1], color[2])
                    self.plane_color_button.setStyleSheet(f"background-color: {self.current_plane_color.name()}")
                else:
                    self.current_plane_color = QtGui.QColor(255, 255, 255)
                    self.plane_color_button.setStyleSheet("background-color: white")
                
                if 'line_color' in details:
                    color = details['line_color']
                    self.current_line_color = QtGui.QColor.fromRgbF(color[0], color[1], color[2])
                    self.line_color_button.setStyleSheet(f"background-color: {self.current_line_color.name()}")
                else:
                    self.current_line_color = QtGui.QColor(255, 255, 255)
                    self.line_color_button.setStyleSheet(f"background-color: {self.current_line_color.name()}")

            else:
                raise
        except:
            self.gravity[command_id] = ['G' + str(command_id), None]
            self.name_gravity_lineedit.setPlaceholderText('G' + str(command_id))
            self.name_gravity_lineedit.clear()
            self.collision_gravity_checkbox.setChecked(False)
            self.gravity_strength_lineedit.clear()
            self.plane_color_button.setStyleSheet("background-color: white")
            self.line_color_button.setStyleSheet("background-color: white")

            self.x_axis_gravity_lineedit.clear()
            self.y_axis_gravity_lineedit.clear()
            self.z_axis_gravity_lineedit.clear()

            self.x_normal_gravity_spinbox.setValue(0.0)
            self.y_normal_gravity_spinbox.setValue(1.0)
            self.z_normal_gravity_spinbox.setValue(0.0)

            self.plane_design_button.setText("Fill")
            self.plane_opacity_slider.setValue(100)
            self.line_opacity_slider.setValue(100)

            self.width_lineedit.clear()
            self.depth_lineedit.clear()