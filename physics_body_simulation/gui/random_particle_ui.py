import utils.create_uicomponents as create

from PyQt5 import QtCore, QtGui, QtWidgets
import random

class RandomParticle_UI:
    def __init__(self):
        self.color_type = "Random"
        self.current_color_lower = QtGui.QColor(255, 255, 255)
        self.current_color_upper = QtGui.QColor(255, 255, 255)
        self.current_command_id = None
        self.current_parent_particle = "None"

    def _show_color_types_dialog(self):
        menu = QtWidgets.QMenu(self.color_menu_button)

        random_action = menu.addAction("Random")
        custom_action = menu.addAction("Custom")

        random_action.triggered.connect(lambda: self._set_color_type("Random"))
        custom_action.triggered.connect(lambda: self._set_color_type("Custom"))

        menu.exec_(self.color_menu_button.mapToGlobal(self.color_menu_button.rect().bottomLeft()))

    def _set_color_type(self, type):
        self.color_type = type
        self.color_menu_button.setText(type)

        if type == "Custom":
            self.rules_single_variable_frame.setGeometry(QtCore.QRect(630, 120, 301, 365))
            self.color_button_lower.show()
            self.color_button_upper.show()
            self.color_hyphen_label.show()
        else:
            self.rules_single_variable_frame.setGeometry(QtCore.QRect(630, 120, 301, 321))
            self.color_button_lower.hide()
            self.color_button_upper.hide()
            self.color_hyphen_label.hide()

    def _show_color_lower_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_color_lower = color
            self.color_button_lower.setStyleSheet(f"background-color: {color.name()}")
    
    def _show_color_upper_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_color_upper = color
            self.color_button_upper.setStyleSheet(f"background-color: {color.name()}")

    def _show_particle_parent_menu(self):
        menu = QtWidgets.QMenu()

        none = menu.addAction("None")
        for particle in self.particle_ui.particle_classes.values():
            add_name = menu.addAction(particle.name)
            add_name.triggered.connect(lambda checked, option=particle: self._set_particle_parent(option))
        none.triggered.connect(lambda checked, option="None": self._set_particle_parent(option))
        menu.exec_(self.parent_particle_button.mapToGlobal(self.parent_particle_button.rect().bottomLeft()))  

    def _set_particle_parent(self, particle):
        if particle == "None":
            self.current_parent_particle = "None"
            self.parent_particle_button.setText(particle)
        else:
            self.current_parent_particle = particle.id
            self.parent_particle_button.setText(particle.name)

    def set_default_parent(self):
        self.current_parent_particle = "None"
        self.parent_particle_button.setText(self.current_parent_particle)

    def setup_random_particle_settings(self, settings_stacked_widget, particle_ui):
        """Configure Random Particle Settings"""

        self.settings_stacked_widget = settings_stacked_widget
        self.particle_ui = particle_ui

        self.random_particle_settings_group = create.create_group_box(
            parent = self.settings_stacked_widget, 
            geometry = QtCore.QRect(9, 9, 931, 511),
            objname = "random_particle_settings_group",
            title = "Random Particle Settings",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        ) 
        
        self.no_of_particles_label = create.create_name_label(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(10, 40, 221, 40),
            font_size = 16,
            text = "Number of Particles :",
            objname = "no_of_particles_label"
        )
        self.no_of_particles_spinbox = create.create_spinbox(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(230, 40, 111, 40),
            font_size = 16,
            min = 1,
            max = 200,
            step = 1,
            value = 1,
            objname = "no_of_particles_spinbox"
        )

        self.parent_particle_label = create.create_name_label(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(380, 40, 171, 40),
            font_size = 16,
            text = "Parent Particle :",
            objname = "parent_particle_label"
        ) 
        self.parent_particle_button = create.create_button(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(550, 40, 150, 41),
            objname = "parent_particle_button",
            font_size = 16,
            text = "None"
        )

        self.create_particles_button = create.create_button(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            objname = "create_particles_button",
            font_size = 20,
            text = "Create"
        )
        self.reset_particles_button = create.create_button(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            objname = "reset_particles_button",
            font_size = 20,
            text = "Reset"
        )

        # Particle Single Valued Properties

        self.rules_single_variable_frame = create.create_frame(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(630, 120, 301, 321),
            fshape = QtWidgets.QFrame.StyledPanel,
            fshadow = QtWidgets.QFrame.Raised,
            objname = "rules_single_variable_frame",
            font_size = 16
        )
        self.rules_single_variable_grid = create.create_grid_layout(
            parent = self.rules_single_variable_frame,
            objname = "rules_single_variable_grid"
        )

        self.mass_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "mass_label",
            font_size = 16,
            text = "Mass (m) :"
        )
        self.mass_hyphen_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "mass_hyphen_label",
            font_size = 16,
            text = "-"
        )
        self.mass_lineedit_lower = create.create_line_edit(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "mass_lineedit_lower",
            validator = QtGui.QDoubleValidator(0, 999.99, 5),
            placeholder = "1.0"
        )
        self.mass_lineedit_upper = create.create_line_edit(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "mass_lineedit_upper",
            validator = QtGui.QDoubleValidator(0, 999.99, 5),
            placeholder = "1.0"
        )

        self.radius_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "radius_label",
            font_size = 16,
            text = "Radius (r) :"
        )
        self.radius_hyphen_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "radius_hyphen_label",
            font_size = 16,
            text = "-"
        )
        self.radius_lineedit_lower = create.create_line_edit(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "radius_lineedit_lower",
            validator = QtGui.QDoubleValidator(0, 999.99, 5),
            placeholder = "1.0"
        )
        self.radius_lineedit_upper = create.create_line_edit(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "radius_lineedit_upper",
            validator = QtGui.QDoubleValidator(0, 999.99, 5),
            placeholder = "1.0"
        )

        self.collision_chance_label = create.create_name_label(
            parent = self.random_particle_settings_group,
            font_size = 16,
            text = "Collision Chance :",
            objname = "collision_chance_label"
        )
        self.collision_chance_spinbox = create.create_spinbox(
            parent = self.random_particle_settings_group,
            font_size = 16,
            min = 0,
            max = 100,
            step = 1,
            value = 0,
            objname = "collision_chance_spinbox"
        )

        self.elasticity_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "elasticity_label",
            font_size = 16,
            text = "Elasticity :"
        )
        self.elasticity_hyphen_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "elasticity_hyphen_label",
            font_size = 16,
            text = "-"
        )
        self.elasticity_spinbox_lower = create.create_double_spinbox(
            parent = self.random_particle_settings_group,
            font_size = 16,
            min = 0,
            max = 1,
            step = 0.1,
            value = 0,
            objname = "elasticity_spinbox_lower"
        )
        self.elasticity_spinbox_upper = create.create_double_spinbox(
            parent = self.random_particle_settings_group,
            font_size = 16,
            min = 0,
            max = 1,
            step = 0.1,
            value = 0,
            objname = "elasticity_spinbox_upper"
        )

        self.toggle_gravity_plane_chance_label = create.create_name_label(
            parent = self.random_particle_settings_group,
            font_size = 16,
            text = "Toggle Gravity\nPlane Chance :",
            objname = "toggle_gravity_plane_chance_label"
        )
        self.toggle_gravity_plane_spinbox = create.create_spinbox(
            parent = self.random_particle_settings_group,
            font_size = 16,
            min = 0,
            max = 100,
            step = 1,
            value = 100,
            objname = "toggle_gravity_plane_spinbox"
        )

        self.color_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "color_label",
            font_size = 16,
            text = "Color :"
        )
        self.color_menu_button = create.create_button(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "color_menu_button",
            text = "Random"
        )
        self.color_hyphen_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "color_hyphen_label",
            font_size = 16,
            text = "-"
        )
        self.color_button_lower = create.create_button(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "color_button_lower",
            text = ""
        )
        self.color_button_upper = create.create_button(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "color_button_upper",
            text = ""
        )

        self.rules_single_variable_grid.addWidget(self.mass_label, 0, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.mass_lineedit_lower, 0, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.mass_hyphen_label, 0, 2, 1, 1)
        self.rules_single_variable_grid.addWidget(self.mass_lineedit_upper, 0, 3, 1, 1)

        self.rules_single_variable_grid.addWidget(self.radius_label, 1, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.radius_lineedit_lower, 1, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.radius_hyphen_label, 1, 2, 1, 1)
        self.rules_single_variable_grid.addWidget(self.radius_lineedit_upper, 1, 3, 1, 1)

        self.rules_single_variable_grid.addWidget(self.collision_chance_label, 2, 0, 1, 2)
        self.rules_single_variable_grid.addWidget(self.collision_chance_spinbox, 2, 3, 1, 1)

        self.rules_single_variable_grid.addWidget(self.elasticity_label, 3, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.elasticity_spinbox_lower, 3, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.elasticity_hyphen_label, 3, 2, 1, 1)
        self.rules_single_variable_grid.addWidget(self.elasticity_spinbox_upper, 3, 3, 1, 1)

        self.rules_single_variable_grid.addWidget(self.toggle_gravity_plane_chance_label, 4, 0, 1, 2)
        self.rules_single_variable_grid.addWidget(self.toggle_gravity_plane_spinbox, 4, 3, 1, 1)

        self.rules_single_variable_grid.addWidget(self.color_label, 5, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.color_menu_button, 5, 1, 1, 3)
        self.rules_single_variable_grid.addWidget(self.color_button_lower, 6, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.color_hyphen_label, 6, 2, 1, 1)
        self.rules_single_variable_grid.addWidget(self.color_button_upper, 6, 3, 1, 1)

        self.color_button_lower.hide()
        self.color_button_upper.hide()
        self.color_hyphen_label.hide()

        self.color_menu_button.clicked.connect(self._show_color_types_dialog)
        self.color_button_lower.clicked.connect(self._show_color_lower_dialog)
        self.color_button_lower.setStyleSheet("background-color: white")
        self.color_button_upper.clicked.connect(self._show_color_upper_dialog)
        self.color_button_upper.setStyleSheet("background-color: white")
        self.parent_particle_button.clicked.connect(self._show_particle_parent_menu)

        self.create_particles_button.clicked.connect(self.add_random_particle_details)
        self.reset_particles_button.clicked.connect(self.reset_random_particle_details)

        # Position

        self.random_position_groupbox = create.create_group_box(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(10, 110, 180, 180),
            font_size = 18,
            objname = "random_position_groupbox",
            title = "Position (m) :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft
        )
        self.position_grid = create.create_grid_layout(
            parent = self.random_position_groupbox,
            objname = "position_grid"
        )

        self.x_axis_label = create.create_name_label(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "x_axis_label",
            text = "X :"
        )
        self.x_hyphen_label = create.create_name_label(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "x_axis_label",
            text = "-"
        )
        self.x_axis_lineedit_lower = create.create_line_edit(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "x_axis_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.x_axis_lineedit_upper = create.create_line_edit(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "x_axis_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.y_axis_label = create.create_name_label(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "y_axis_label",
            text = "Y :"
        )
        self.y_hyphen_label = create.create_name_label(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "y_axis_label",
            text = "-"
        )
        self.y_axis_lineedit_lower = create.create_line_edit(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "y_axis_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.y_axis_lineedit_upper = create.create_line_edit(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "y_axis_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.z_axis_label = create.create_name_label(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "z_axis_label",
            text = "Z :"
        )
        self.z_hyphen_label = create.create_name_label(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "z_axis_label",
            text = "-"
        )
        self.z_axis_lineedit_lower = create.create_line_edit(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "z_axis_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.z_axis_lineedit_upper = create.create_line_edit(
            parent = self.random_position_groupbox,
            font_size = 16,
            objname = "z_axis_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.position_grid.addWidget(self.x_axis_label, 0, 0, 1, 1)
        self.position_grid.addWidget(self.x_axis_lineedit_lower, 0, 1, 1, 1)
        self.position_grid.addWidget(self.x_hyphen_label, 0, 2, 1, 1)
        self.position_grid.addWidget(self.x_axis_lineedit_upper, 0, 3, 1, 1)

        self.position_grid.addWidget(self.y_axis_label, 1, 0, 1, 1)
        self.position_grid.addWidget(self.y_axis_lineedit_lower, 1, 1, 1, 1)
        self.position_grid.addWidget(self.y_hyphen_label, 1, 2, 1, 1)
        self.position_grid.addWidget(self.y_axis_lineedit_upper, 1, 3, 1, 1)

        self.position_grid.addWidget(self.z_axis_label, 2, 0, 1, 1)
        self.position_grid.addWidget(self.z_axis_lineedit_lower, 2, 1, 1, 1)
        self.position_grid.addWidget(self.z_hyphen_label, 2, 2, 1, 1)
        self.position_grid.addWidget(self.z_axis_lineedit_upper, 2, 3, 1, 1)

        # Velocity

        self.random_velocity_groupbox = create.create_group_box(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(200, 110, 190, 180),
            font_size = 18,
            objname = "velocity_groupbox",
            title = "  Velocity (v) :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft
        )
        self.velocity_grid = create.create_grid_layout(
            parent = self.random_velocity_groupbox,
            objname = "velocity_grid"
        )

        self.vx_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vx_label",
            text = "Vx :"
        )
        self.vx_hyphen_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vx_hyphen_label",
            text = "-"
        )
        self.vx_lineedit_lower = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vx_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.vx_lineedit_upper = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vx_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.vy_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vy_label",
            text = "Vy :"
        )
        self.vy_hyphen_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vy_hyphen_label",
            text = "-"
        )
        self.vy_lineedit_lower = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vy_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.vy_lineedit_upper = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vy_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        
        self.vz_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vz_label",
            text = "Vz :"
        )
        self.vz_hyphen_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vz_hyphen_label",
            text = "-"
        )
        self.vz_lineedit_lower = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vz_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.vz_lineedit_upper = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "vz_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        
        self.velocity_grid.addWidget(self.vx_label, 0, 0, 1, 1)
        self.velocity_grid.addWidget(self.vx_lineedit_lower, 0, 1, 1, 1)
        self.velocity_grid.addWidget(self.vx_hyphen_label, 0, 2, 1, 1)
        self.velocity_grid.addWidget(self.vx_lineedit_upper, 0, 3, 1, 1)

        self.velocity_grid.addWidget(self.vy_label, 1, 0, 1, 1)
        self.velocity_grid.addWidget(self.vy_lineedit_lower, 1, 1, 1, 1)
        self.velocity_grid.addWidget(self.vy_hyphen_label, 1, 2, 1, 1)
        self.velocity_grid.addWidget(self.vy_lineedit_upper, 1, 3, 1, 1)

        self.velocity_grid.addWidget(self.vz_label, 2, 0, 1, 1)
        self.velocity_grid.addWidget(self.vz_lineedit_lower, 2, 1, 1, 1)
        self.velocity_grid.addWidget(self.vz_hyphen_label, 2, 2, 1, 1)
        self.velocity_grid.addWidget(self.vz_lineedit_upper, 2, 3, 1, 1)

        # Acceleration

        self.random_acceleration_groupbox = create.create_group_box(
            parent = self.random_particle_settings_group,
            geometry = QtCore.QRect(400, 110, 220, 180),
            font_size = 18,
            objname = "random_acceleration_groupbox",
            title = "Acceleration (a) :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft
        )
        self.acceleration_grid = create.create_grid_layout(
            parent = self.random_acceleration_groupbox,
            objname = "acceleration_grid"
        )

        self.ax_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ax_label",
            text = "Ax :"
        )
        self.ax_hyphen_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ax_hyphen_label",
            text = "-"
        )
        self.ax_lineedit_lower = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ax_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.ax_lineedit_upper = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ax_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.ay_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ay_label",
            text = "Ay :"
        )
        self.ay_hyphen_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ay_hyphen_label",
            text = "-"
        )
        self.ay_lineedit_lower = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ay_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.ay_lineedit_upper = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "ay_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.az_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "az_label",
            text = "Ax :"
        )
        self.az_hyphen_label = create.create_name_label(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "az_hyphen_label",
            text = "-"
        )
        self.az_lineedit_lower = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "az_lineedit_lower",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.az_lineedit_upper = create.create_line_edit(
            parent = self.random_velocity_groupbox,
            font_size = 16,
            objname = "az_lineedit_upper",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.acceleration_grid.addWidget(self.ax_label, 0, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ax_lineedit_lower, 0, 1, 1, 1)
        self.acceleration_grid.addWidget(self.ax_hyphen_label, 0, 2, 1, 1)
        self.acceleration_grid.addWidget(self.ax_lineedit_upper, 0, 3, 1, 1)

        self.acceleration_grid.addWidget(self.ay_label, 1, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ay_lineedit_lower, 1, 1, 1, 1)
        self.acceleration_grid.addWidget(self.ay_hyphen_label, 1, 2, 1, 1)
        self.acceleration_grid.addWidget(self.ay_lineedit_upper, 1, 3, 1, 1)

        self.acceleration_grid.addWidget(self.az_label, 2, 0, 1, 1)
        self.acceleration_grid.addWidget(self.az_lineedit_lower, 2, 1, 1, 1)
        self.acceleration_grid.addWidget(self.az_hyphen_label, 2, 2, 1, 1)
        self.acceleration_grid.addWidget(self.az_lineedit_upper, 2, 3, 1, 1)

    def reset_random_particle_details(self):
        """Resets the UI back to its placeholder values"""

        self.no_of_particles_spinbox.setValue(1)
        self.parent_particle_button.setText("None")
        self.current_parent_particle = "None"
        self.mass_lineedit_lower.clear()
        self.mass_lineedit_upper.clear()
        self.radius_lineedit_lower.clear()
        self.radius_lineedit_upper.clear()
        self.collision_chance_spinbox.setValue(0)
        self.elasticity_spinbox_lower.setValue(0.0)
        self.elasticity_spinbox_upper.setValue(0.0)
        self.toggle_gravity_plane_spinbox.setValue(100)

        self.color_button_lower.setStyleSheet("background-color: white")
        self.color_button_upper.setStyleSheet("background-color: white")
        self.current_color_lower = QtGui.QColor(255, 255, 255)
        self.current_color_upper = QtGui.QColor(255, 255, 255)

        self.x_axis_lineedit_lower.clear()
        self.x_axis_lineedit_upper.clear()
        self.y_axis_lineedit_lower.clear()
        self.y_axis_lineedit_upper.clear()
        self.z_axis_lineedit_lower.clear()
        self.z_axis_lineedit_upper.clear()

        self.vx_lineedit_lower.clear()
        self.vx_lineedit_upper.clear()
        self.vy_lineedit_lower.clear()
        self.vy_lineedit_upper.clear()
        self.vz_lineedit_lower.clear()
        self.vz_lineedit_upper.clear()

        self.ax_lineedit_lower.clear()
        self.ax_lineedit_upper.clear()
        self.ay_lineedit_lower.clear()
        self.ay_lineedit_upper.clear()
        self.az_lineedit_lower.clear()
        self.az_lineedit_upper.clear()

    def add_random_particle_details(self):
        """The particle details get sent over to <particle_ui.py> as a dictionary to be added into the universe stack"""

        self.current_command_id = self.particle_ui.no_of_particles

        x_lower_value = float(self.x_axis_lineedit_lower.text()) if self.x_axis_lineedit_lower.text() else 0.0
        x_upper_value = float(self.x_axis_lineedit_upper.text()) if self.x_axis_lineedit_upper.text() else 0.0
        if x_lower_value > x_upper_value:
            x_lower_value, x_upper_value = x_upper_value, x_lower_value

        y_lower_value = float(self.y_axis_lineedit_lower.text()) if self.y_axis_lineedit_lower.text() else 0.0
        y_upper_value = float(self.y_axis_lineedit_upper.text()) if self.y_axis_lineedit_upper.text() else 0.0
        if y_lower_value > y_upper_value:
            y_lower_value, y_upper_value = y_upper_value, y_lower_value

        z_lower_value = float(self.z_axis_lineedit_lower.text()) if self.z_axis_lineedit_lower.text() else 0.0
        z_upper_value = float(self.z_axis_lineedit_upper.text()) if self.z_axis_lineedit_upper.text() else 0.0
        if z_lower_value > z_upper_value:
            z_lower_value, z_upper_value = z_upper_value, z_lower_value

        vx_lower_value = float(self.vx_lineedit_lower.text()) if self.vx_lineedit_lower.text() else 0.0
        vx_upper_value = float(self.vx_lineedit_upper.text()) if self.vx_lineedit_upper.text() else 0.0
        if vx_lower_value > vx_upper_value:
            vx_lower_value, vx_upper_value = vx_upper_value, vx_lower_value

        vy_lower_value = float(self.vy_lineedit_lower.text()) if self.vy_lineedit_lower.text() else 0.0
        vy_upper_value = float(self.vy_lineedit_upper.text()) if self.vy_lineedit_upper.text() else 0.0
        if vy_lower_value > vy_upper_value:
            vy_lower_value, vy_upper_value = vy_upper_value, vy_lower_value

        vz_lower_value = float(self.vz_lineedit_lower.text()) if self.vz_lineedit_lower.text() else 0.0
        vz_upper_value = float(self.vz_lineedit_upper.text()) if self.vz_lineedit_upper.text() else 0.0
        if vz_lower_value > vz_upper_value:
            vz_lower_value, vz_upper_value = vz_upper_value, vz_lower_value

        ax_lower_value = float(self.ax_lineedit_lower.text()) if self.ax_lineedit_lower.text() else 0.0
        ax_upper_value = float(self.ax_lineedit_upper.text()) if self.ax_lineedit_upper.text() else 0.0
        if ax_lower_value > ax_upper_value:
            ax_lower_value, ax_upper_value = ax_upper_value, ax_lower_value

        ay_lower_value = float(self.ay_lineedit_lower.text()) if self.ay_lineedit_lower.text() else 0.0
        ay_upper_value = float(self.ay_lineedit_upper.text()) if self.ay_lineedit_upper.text() else 0.0
        if ay_lower_value > ay_upper_value:
            ay_lower_value, ay_upper_value = ay_upper_value, ay_lower_value

        az_lower_value = float(self.az_lineedit_lower.text()) if self.az_lineedit_lower.text() else 0.0
        az_upper_value = float(self.az_lineedit_upper.text()) if self.az_lineedit_upper.text() else 0.0
        if az_lower_value > az_upper_value:
            az_lower_value, az_upper_value = az_upper_value, az_lower_value

        mass_lower_input = float(self.mass_lineedit_lower.text()) if self.mass_lineedit_lower.text() else 1.0
        mass_upper_input = float(self.mass_lineedit_upper.text()) if self.mass_lineedit_upper.text() else 1.0
        if mass_lower_input > mass_upper_input:
            mass_lower_input, mass_upper_input = mass_upper_input, mass_lower_input

        radius_lower_input = float(self.radius_lineedit_lower.text()) if self.radius_lineedit_lower.text() else 1.0
        radius_upper_input = float(self.radius_lineedit_upper.text()) if self.radius_lineedit_upper.text() else 1.0
        if radius_lower_input > radius_upper_input:
            radius_lower_input, radius_upper_input = radius_upper_input, radius_lower_input

        elasticity_lower_input = self.elasticity_spinbox_lower.value()
        elasticity_upper_input = self.elasticity_spinbox_upper.value()
        if elasticity_lower_input > elasticity_upper_input:
            elasticity_lower_input, elasticity_upper_input = elasticity_upper_input, elasticity_lower_input

        no_of_particles_input = self.no_of_particles_spinbox.value()
        collision_chance_input = self.collision_chance_spinbox.value() / 100
        toggle_gravity_chance_input = self.toggle_gravity_plane_spinbox.value() / 100

        if self.color_type == "Custom":
            color_lower_input = [
            self.current_color_lower.redF(), 
            self.current_color_lower.greenF(), 
            self.current_color_lower.blueF()
            ]
            color_upper_input = [
                self.current_color_upper.redF(), 
                self.current_color_upper.greenF(), 
                self.current_color_upper.blueF()
            ]

            for i in range(3):  # 0: red, 1: green, 2: blue
                if color_lower_input[i] > color_upper_input[i]:
                    color_lower_input[i], color_upper_input[i] = color_upper_input[i], color_lower_input[i]

        particles = []

        for _ in range(no_of_particles_input):
            self.current_command_id += 1
            if self.color_type == "Random":
                color_input = [round(random.uniform(0.0, 1.0), 4) for _ in range(3)]
            else:
                color_input = [round(random.uniform(color_lower_input[i], color_upper_input[i]), 4) for i in range(3)]

            data = {
                "id" : self.current_command_id,
                "name" : 'P' + str(self.current_command_id),
                "mass" : round(random.uniform(mass_lower_input, mass_upper_input), 4),
                "radius" : round(random.uniform(radius_lower_input, radius_upper_input), 4),
                "position" : [
                    round(random.uniform(x_lower_value, x_upper_value), 4),
                    round(random.uniform(y_lower_value, y_upper_value), 4),
                    round(random.uniform(z_lower_value, z_upper_value), 4)
                ],
                "velocity" : [
                    round(random.uniform(vx_lower_value, vx_upper_value), 4),
                    round(random.uniform(vy_lower_value, vy_upper_value), 4),
                    round(random.uniform(vz_lower_value, vz_upper_value), 4)
                ],
                "acceleration" : [
                    round(random.uniform(ax_lower_value, ax_upper_value), 4),
                    round(random.uniform(ay_lower_value, ay_upper_value), 4),
                    round(random.uniform(az_lower_value, az_upper_value), 4)
                ],
                "elasticity" : round(random.uniform(elasticity_lower_input, elasticity_upper_input), 2),
                "collision" : random.random() <= collision_chance_input,
                "toggle_gravity" : random.random() <= toggle_gravity_chance_input,
                "color" : color_input,
                "parent_particle_id" : self.current_parent_particle
            }
            particles.append(data)

        self.particle_ui.load_particles_universe(particles)