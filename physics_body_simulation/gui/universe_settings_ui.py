import utils.create_uicomponents as create
import constants.universe_settings as universe_settings

from PyQt5 import QtCore, QtGui

class UniverseSettings_UI:
    def __init__(self):
        pass

    def setup_universe_settings(self, settings_stacked_widget, placeholder_widget):
        """Configure Universe Settings"""

        self.settings_stacked_widget = settings_stacked_widget
        self.placeholder_widget = placeholder_widget

        self.universe_settings_group = create.create_group_box(
            parent = self.settings_stacked_widget, 
            geometry = QtCore.QRect(9, 9, 931, 511),
            objname = "universe_settings_group",
            title = "Universe Settings",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )

        # Camera Settings

        self.camera_settings_group = create.create_group_box(
            parent = self.universe_settings_group, 
            geometry = QtCore.QRect(20, 100, 310, 180),
            objname = "universe_settings_group",
            title = "Universe Settings:",
            font_size = 18,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.camera_settings_grid = create.create_grid_layout(
            parent = self.camera_settings_group,
            objname = "camera_settings_grid"
        )
        self.mouse_sensitivity_label = create.create_name_label(
            parent = self.camera_settings_group,
            objname = "mouse_sensitivity_label",
            font_size = 16,
            text = "Mouse Sensitivity : "
        )
        self.camera_speed_label = create.create_name_label(
            parent = self.camera_settings_group,
            objname = "camera_speed_label",
            font_size = 16,
            text = "Camera Speed : "
        )
        self.mouse_sensitivity_spinbox = create.create_double_spinbox(
            parent = self.camera_settings_group,
            font_size = 16,
            objname = "mouse_sensitivity_spinbox",
            max = 5.0,
            min = 0.1,
            step = 0.1,
            value = 0.25
        )
        self.camera_speed_spinbox = create.create_double_spinbox(
            parent = self.camera_settings_group,
            font_size = 16,
            objname = "camera_speed_spinbox",
            max = 5.0,
            min = 0.01,
            step = 0.01,
            value = 0.05
        )

        self.camera_settings_grid.addWidget(self.mouse_sensitivity_label, 0, 0, 1, 1)
        self.camera_settings_grid.addWidget(self.mouse_sensitivity_spinbox, 0, 1, 1, 1)
        self.camera_settings_grid.addWidget(self.camera_speed_label, 1, 0, 1, 1)
        self.camera_settings_grid.addWidget(self.camera_speed_spinbox, 1, 1, 1, 1)

        # Simulation Settings

        self.simulation_settings_group = create.create_group_box(
            parent = self.universe_settings_group, 
            geometry = QtCore.QRect(340, 100, 290, 180),
            objname = "simulation_settings_group",
            title = "Simulation Settings:",
            font_size = 18,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.simulation_settings_grid = create.create_grid_layout(
            parent = self.simulation_settings_group,
            objname = "simulation_settings_grid"
        )

        self.particle_gravity_checkbox = create.create_checkbox(
            parent = self.simulation_settings_group,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "particle_gravity_checkbox",
            text = "Particle Gravity : "
        )
        self.particle_gravity_checkbox.setChecked(True)
        self.render_distance_label = create.create_name_label(
            parent = self.simulation_settings_group,
            objname = "render_distance_label",
            font_size = 16,
            text = "Render Distance : "
        )
        self.render_distance_lineedit = create.create_line_edit(
            parent = self.simulation_settings_group,
            font_size = 16,
            objname = "render_distance_lineedit",
            validator = QtGui.QDoubleValidator(0, 999.99, 2),
            placeholder = "1000.0"
        )

        self.simulation_settings_grid.addWidget(self.particle_gravity_checkbox, 0, 0, 1, 1)
        self.simulation_settings_grid.addWidget(self.render_distance_label, 1, 0, 1, 1)
        self.simulation_settings_grid.addWidget(self.render_distance_lineedit, 1, 1, 1, 1)

        # Constants

        self.constants_group = create.create_group_box(
            parent = self.universe_settings_group, 
            geometry = QtCore.QRect(640, 100, 270, 220),
            objname = "constants_group",
            title = "Constants:",
            font_size = 18,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.constants_grid = create.create_grid_layout(
            parent = self.constants_group,
            objname = "constants_grid"
        )

        self.time_step_label = create.create_name_label(
            parent = self.constants_group,
            objname = "time_step_label",
            font_size = 16,
            text = "Time Step (dt) : "
        )
        self.gravitational_constant_label = create.create_name_label(
            parent = self.constants_group,
            objname = "gravitational_constant_label",
            font_size = 16,
            text = "Gravitational\nConstant (G) : "
        )
        self.time_multiplier_label = create.create_name_label(
            parent = self.constants_group,
            objname = "time_multiplier_label",
            font_size = 16,
            text = "Time\nMultiplier : "
        )
        self.time_multiplier_spinbox = create.create_double_spinbox(
            parent = self.constants_group,
            font_size = 16,
            objname = "time_multiplier_spinbox",
            max = 5.0,
            min = 0.1,
            step = 0.1,
            value = 1.0
        )
        self.time_step_spinbox = create.create_double_spinbox(
            parent = self.constants_group,
            font_size = 16,
            objname = "time_step_spinbox",
            max = 5.0,
            min = 0,
            step = 0.01,
            value = 0.016
        )
        self.gravitational_constant_lineedit = create.create_line_edit(
            parent = self.constants_group,
            font_size = 16,
            objname = "gravitational_constant_lineedit",
            validator = QtGui.QDoubleValidator(0, 999.99, 10),
            placeholder = "0.01"
        )

        self.constants_grid.addWidget(self.time_step_label, 0, 0, 1, 1)
        self.constants_grid.addWidget(self.time_multiplier_label, 1, 0, 1, 1)
        self.constants_grid.addWidget(self.gravitational_constant_label, 2, 0, 1, 1)
        self.constants_grid.addWidget(self.time_step_spinbox, 0, 1, 1, 1)
        self.constants_grid.addWidget(self.time_multiplier_spinbox, 1, 1, 1, 1)
        self.constants_grid.addWidget(self.gravitational_constant_lineedit, 2, 1, 1, 1)

        # Save and Reset

        self.save_universe_button = create.create_button(
            parent = self.universe_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            objname = "save_universe_button",
            font_size = 20,
            text = "Save"
        )
        self.reset_universe_button = create.create_button(
            parent = self.universe_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            objname = "reset_universe_button",
            font_size = 20,
            text = "Reset"
        )

        self.save_universe_button.clicked.connect(self.update_settings)
        self.reset_universe_button.clicked.connect(self.reset_universe_settings)

    def update_settings(self):
        """Updates the constants present in <universe_settings.py>"""

        mouse_sensitivity = float(self.mouse_sensitivity_spinbox.value())
        camera_speed = float(self.camera_speed_spinbox.value())

        particle_gravity = int(self.particle_gravity_checkbox.isChecked())
        render_distance = float(self.render_distance_lineedit.text()) if self.render_distance_lineedit.text() else 1000

        time_step = float(self.time_step_spinbox.value())
        time_multiplier = float(self.time_multiplier_spinbox.value())
        gravitational_constant = float(self.gravitational_constant_lineedit.text()) if self.gravitational_constant_lineedit.text() else 0.01
        self.gravitational_constant_lineedit.setText(str(gravitational_constant))

        universe_settings.set_mouse_sensitivity(mouse_sensitivity)
        universe_settings.set_camera_speed(camera_speed)

        universe_settings.set_render_distance(render_distance)
        universe_settings.set_particle_gravity(particle_gravity)
        
        universe_settings.set_time_multiplier(time_multiplier)
        universe_settings.set_time_step(time_step)
        universe_settings.set_gravitational_constant(gravitational_constant)

        self.placeholder_widget()

    def load_g_value(self, g_value):
        """Sets the gravitational constant value"""

        self.gravitational_constant_lineedit.setText(str(g_value))
        universe_settings.set_gravitational_constant(g_value)

    def reset_universe_settings(self):
        """Resets back to placeholder values"""
        
        self.render_distance_lineedit.clear()
        self.gravitational_constant_lineedit.clear()

        self.particle_gravity_checkbox.setChecked(True)

        self.mouse_sensitivity_spinbox.setValue(0.25)
        self.camera_speed_spinbox.setValue(0.05)
        self.time_step_spinbox.setValue(0.016)
        self.time_multiplier_spinbox.setValue(1.0)