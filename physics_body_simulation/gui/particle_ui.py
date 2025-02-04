import utils.create_uicomponents as create
from utils.resolution_scaler import ResolutionScaler
import properties.particle_property as particle_property
import constants.visual_settings as visual_settings
import graphs.particle_variable_ui as particle_variable_ui
from graphs.graph_settings_ui import GraphSettings_UI
from graphs.graph_display_2d_ui import GraphDisplay2D_UI
from graphs.graph_display_3d_ui import GraphDisplay3D_UI

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import numpy as np

class Particle_UI:
    def __init__(self):
        self.particles = {}
        self.no_of_particles = 0
        self.initial_name = 'P' + str(self.no_of_particles)
        self.current_command_id = None
        self.command_link_buttons = {}
        self.particle_classes = {}
        self.particle_variables = {}
        self.current_color = QtGui.QColor(255, 255, 255)

        self.graph_settings_ui = GraphSettings_UI(self.reset_variables, self.show_graph_display)
        self.graph_display_2d_ui = GraphDisplay2D_UI(self.go_back_function)
        self.graph_display_3d_ui = GraphDisplay3D_UI(self.go_back_function)

        self.parent_particle = "None"

        self.indicator = 0

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        self.particle_icon_path = os.path.join(base_dir, "pictures", "particle2.png").replace('\\','/')
        self.scaler = ResolutionScaler()

    def _show_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()}")

    def _show_particle_parent_menu(self):
        menu = QtWidgets.QMenu()

        none = menu.addAction("None")
        for particle in self.particle_classes.values():
            try:
                if particle != self.particle_classes[self.current_command_id]:
                    add_name = menu.addAction(particle.name)
                    add_name.triggered.connect(lambda checked, option=particle: self._set_particle_parent(option))
            except:
                add_name = menu.addAction(particle.name)
                add_name.triggered.connect(lambda checked, option=particle: self._set_particle_parent(option))
        none.triggered.connect(lambda checked, option="None": self._set_particle_parent(option))
        menu.exec_(self.parent_particle_button.mapToGlobal(self.parent_particle_button.rect().bottomLeft()))  

    def _set_particle_parent(self, particle):
        self.parent_particle = particle
        if self.parent_particle == "None":
            self.parent_particle_button.setText(particle)
        else:
            self.parent_particle_button.setText(particle.name)

    def reset_variables(self):
        """Resets all selected variables present in <particle_variable_ui.py>"""

        for particle, variable in self.particle_variables.values():
            try:
                variable.reset_particle_variables()
            except:
                pass
    
    def go_back_function(self):
        """Hides graphs and displays previous settings"""

        try:
            if self.dimension == "2D":
                self.graph_display_2d_ui.graph_settings_2d_frame.hide()
                self.graph_display_2d_ui.graph_display_2d_frame.hide()
                self.graph_display_2d_ui.displayed_checkboxes = {}
            else:
                self.graph_display_3d_ui.graph_settings_3d_frame.hide()
                self.graph_display_3d_ui.graph_display_3d_frame.hide()
                self.graph_display_3d_ui.displayed_checkboxes = {}
                self.graph_display_3d_ui.remove_graph()
        except:
            pass
        self.graph_settings_ui.graph_settings_group.show()
        self.universe_matter_frame.show()
        self.settings_stacked_widget.show()
        self.placeholder_widget()

        self.hide_settings_button.hide()

    def show_graph_display(self, number_of_plots, dimension):
        """Displays either 2D or 3D graphs"""

        particle_values = []
        self.dimension = dimension

        for particle, variable in self.particle_variables.values():
            try:
                particle_values.append(variable.selected_variables)
            except:
                pass

        if self.graph_settings_ui.y_axis_vlayout.count() > 0 and dimension == "2D":          # Should always have atleast one element for the y axis
            self.particle_settings_group.hide()
            self.graph_settings_ui.graph_settings_group.hide()

            self.universe_matter_frame.hide()
            self.settings_stacked_widget.hide()

            self.graph_display_2d_ui.setup_graph_display_2d(self.centralwidget, particle_values, number_of_plots)
            self.graph_display_2d_ui.graph_settings_2d_frame.show()
            self.graph_display_2d_ui.graph_display_2d_frame.show()

        if self.graph_settings_ui.y_axis_vlayout.count() > 0 and self.graph_settings_ui.z_axis_vlayout.count() > 0 and dimension == "3D" : # Should always have atleast one element for the y and z axis 
            self.particle_settings_group.hide()
            self.graph_settings_ui.graph_settings_group.hide()

            self.universe_matter_frame.hide()
            self.settings_stacked_widget.hide()
            self.graph_display_3d_ui.setup_graph_display_3d(self.centralwidget, particle_values, number_of_plots)
            self.graph_display_3d_ui.graph_settings_3d_frame.show()
            self.graph_display_3d_ui.graph_display_3d_frame.show()

        self.hide_settings_button.show()
    
    def hide_show_settings(self):
        """Toggles between hiding or showing the graphing settings in 2D or 3D graph"""

        if self.indicator == 0:
            self.indicator = 1
            if self.dimension == "2D":
                self.graph_display_2d_ui.graph_settings_2d_frame.hide()
                self.hide_settings_button.setText("Show Settings")
                self.graph_display_2d_ui.graph_display_2d_frame.setGeometry(QtCore.QRect(10, 10, 940, 1068))
                self.graph_display_2d_ui.graph_display_scrollarea.setGeometry(QtCore.QRect(11, 2, 928, 1061))
                self.graph_display_2d_ui.graph_display_scroll_widget.setGeometry(QtCore.QRect(0, 0, 926, 1061))
            else:
                self.graph_display_3d_ui.graph_settings_3d_frame.hide()
                self.hide_settings_button.setText("Show Settings")
                self.graph_display_3d_ui.graph_display_3d_frame.setGeometry(QtCore.QRect(10, 10, 940, 1068))
                self.graph_display_3d_ui.graph_display_scrollarea.setGeometry(QtCore.QRect(11, 2, 928, 1061))
                self.graph_display_3d_ui.graph_display_scroll_widget.setGeometry(QtCore.QRect(0, 0, 926, 1061))
            return

        if self.indicator == 1:
            self.indicator = 0
            if self.dimension == "2D":
                self.graph_display_2d_ui.graph_settings_2d_frame.show()
                self.hide_settings_button.setText("Hide Settings")
                self.graph_display_2d_ui.graph_display_2d_frame.setGeometry(QtCore.QRect(9, 9, 948, 520))
                self.graph_display_2d_ui.graph_display_scrollarea.setGeometry(QtCore.QRect(11, 2, 928, 514))
                self.graph_display_2d_ui.graph_display_scroll_widget.setGeometry(QtCore.QRect(0, 0, 926, 515))
            else:
                self.graph_display_3d_ui.graph_settings_3d_frame.show()
                self.hide_settings_button.setText("Hide Settings")
                self.graph_display_3d_ui.graph_display_3d_frame.setGeometry(QtCore.QRect(9, 9, 948, 520))
                self.graph_display_3d_ui.graph_display_scrollarea.setGeometry(QtCore.QRect(11, 2, 928, 514))
                self.graph_display_3d_ui.graph_display_scroll_widget.setGeometry(QtCore.QRect(0, 0, 926, 515))
            return

    def setup_particle_settings(
            self,
            centralwidget,
            settings_stacked_widget,
            universe_verticalLayout,
            control_information_frame,
            universe_matter_frame,
            universe_vlayout_widget,
            placeholder_widget,
            particle_command_settings_function
        ):
        """Configure Particle Settings"""
        
        self.centralwidget = centralwidget
        self.settings_stacked_widget = settings_stacked_widget
        self.universe_verticalLayout = universe_verticalLayout
        self.control_information_frame = control_information_frame
        self.universe_matter_frame = universe_matter_frame
        self.universe_vlayout_widget = universe_vlayout_widget
        self.placeholder_widget = placeholder_widget
        self.particle_command_settings_function = particle_command_settings_function

        self.graph_settings_ui.setup_graphing_settings(control_information_frame)
        
        self.particle_settings_group = create.create_group_box(
            parent = self.settings_stacked_widget, 
            geometry = QtCore.QRect(9, 9, 931, 511),
            objname = "particle_settings_group",
            title = "Particle Settings",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        ) 
        
        # Particle Single Valued Properties

        self.rules_single_variable_frame = create.create_frame(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(630, 110, 290, 270),
            fshape = QtWidgets.QFrame.StyledPanel,
            fshadow = QtWidgets.QFrame.Raised,
            objname = "rules_single_variable_frame",
            font_size = 16
        )
        self.rules_single_variable_grid = create.create_grid_layout(
            parent = self.rules_single_variable_frame,
            objname = "rules_single_variable_grid"
        )
        self.name_label = create.create_name_label(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(40, 40, 81, 41),
            font_size = 16,
            text = "Name :",
            objname = "name_label"
        )
        self.parent_particle_label = create.create_name_label(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(300, 40, 171, 40),
            font_size = 16,
            text = "Parent Particle :",
            objname = "parent_particle_label"
        )
        
        self.parent_particle_button = create.create_button(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(470, 40, 150, 41),
            objname = "parent_particle_button",
            font_size = 16,
            text = "None"
        )        
        self.save_button = create.create_button(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            objname = "save_button",
            font_size = 20,
            text = "Save"
        )
        self.reset_button = create.create_button(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            objname = "reset_button",
            font_size = 20,
            text = "Reset"
        )
        self.delete_button = create.create_button(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(300, 460, 150, 50),
            objname = "delete_button",
            font_size = 20,
            text = "Delete"
        )
        
        self.mass_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "mass_label",
            font_size = 16,
            text = "Mass (m) :"
        )
        self.mass_kg_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "mass_kg_label",
            font_size = 12,
            text = "kg"
        )
        self.radius_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "radius_label",
            font_size = 16,
            text = "Radius (r) :"
        )
        self.radius_m_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "radius_m_label",
            font_size = 12,
            text = "m"
        )
        self.elasticity_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "elasticity_label",
            font_size = 16,
            text = "Elasticity :"
        )
        self.name_lineedit = create.create_line_edit(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(130, 40, 151, 41),
            font_size = 14,
            objname = "name_lineedit",
            placeholder = "P1"
        )
        self.mass_lineedit = create.create_line_edit(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "mass_lineedit",
            validator = QtGui.QDoubleValidator(0, 999.99, 5),
            placeholder = "1.0"
        )
        self.radius_lineedit = create.create_line_edit(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "radius_lineedit",
            validator = QtGui.QDoubleValidator(0.0, 999.99, 5),
            placeholder = "1.0"
        )
        self.collision_checkbox = create.create_checkbox(
            parent = self.rules_single_variable_frame,
            font_size = 16,
            layout = QtCore.Qt.LeftToRight,
            objname = "collision_checkbox",
            text = "Particle Collision"
        )
        self.elasticity_spinbox = create.create_double_spinbox(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            max = 1.0,
            step = 0.01,
            objname = "elasticity_spinbox"            
        )
        self.color_label = create.create_name_label(
            parent = self.rules_single_variable_frame,
            objname = "color_label",
            font_size = 16,
            text = "Color:"
        )
        self.color_button = create.create_button(
            parent = self.rules_single_variable_frame,
            font_size = 14,
            objname = "color_button",
            text = ""
        )
        self.gravity_plane_checkbox = create.create_checkbox(
            parent = self.rules_single_variable_frame,
            font_size = 16,
            layout = QtCore.Qt.LeftToRight,
            objname = "gravity_plane_checkbox",
            text = "Toggle Gravity\nPlane Effect"
        )
        self.gravity_plane_checkbox.setChecked(True)

        self.rules_single_variable_grid.addWidget(self.mass_label, 0, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.mass_lineedit, 0, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.mass_kg_label, 0, 2, 1, 1)
        self.rules_single_variable_grid.addWidget(self.radius_label, 1, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.radius_lineedit, 1, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.radius_m_label, 1, 2, 1, 1)
        self.rules_single_variable_grid.addWidget(self.collision_checkbox, 2, 0, 1, 2)
        self.rules_single_variable_grid.addWidget(self.elasticity_label, 3, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.elasticity_spinbox, 3, 1, 1, 1)
        self.rules_single_variable_grid.addWidget(self.gravity_plane_checkbox, 4, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.color_label, 5, 0, 1, 1)
        self.rules_single_variable_grid.addWidget(self.color_button, 5, 1, 1, 1)

        self.color_button.clicked.connect(self._show_color_dialog)

        # Position

        self.position_groupbox = create.create_group_box(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(0, 110, 180, 180),
            font_size = 18,
            objname = "position_groupbox",
            title = "Position (m) :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft
        )
        self.position_grid = create.create_grid_layout(
            parent = self.position_groupbox,
            objname = "position_grid"
        )

        self.x_axis_label = create.create_name_label(
            parent = self.position_groupbox,
            font_size = 16,
            objname = "x_axis_label",
            text = "X Axis :"
        )
        self.y_axis_label = create.create_name_label(
            parent = self.position_groupbox,
            font_size = 16,
            objname = "y_axis_label",
            text = "Y Axis :"
        )
        self.z_axis_label = create.create_name_label(
            parent = self.position_groupbox,
            font_size = 16,
            objname = "z_axis_label",
            text = "Z Axis :"
        )
        self.x_axis_lineedit = create.create_line_edit(
            parent = self.position_groupbox,
            font_size = 16,
            objname = "x_axis_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.y_axis_lineedit = create.create_line_edit(
            parent = self.position_groupbox,
            font_size = 16,
            objname = "y_axis_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.z_axis_lineedit = create.create_line_edit(
            parent = self.position_groupbox,
            font_size = 16,
            objname = "z_axis_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.position_grid.addWidget(self.x_axis_label, 0, 0, 1, 1)
        self.position_grid.addWidget(self.y_axis_label, 1, 0, 1, 2)
        self.position_grid.addWidget(self.z_axis_label, 2, 0, 1, 2)
        self.position_grid.addWidget(self.x_axis_lineedit, 0, 2, 1, 1)
        self.position_grid.addWidget(self.y_axis_lineedit, 1, 2, 1, 1)
        self.position_grid.addWidget(self.z_axis_lineedit, 2, 2, 1, 1)

        # Velocity

        self.velocity_groupbox = create.create_group_box(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(200, 110, 180, 180),
            font_size = 18,
            objname = "velocity_groupbox",
            title = "  Velocity (v) :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft
        )
        self.velocity_grid = create.create_grid_layout(
            parent = self.velocity_groupbox,
            objname = "velocity_grid"
        )

        self.vx_label = create.create_name_label(
            parent = self.velocity_groupbox,
            font_size = 16,
            objname = "vx_label",
            text = "Vx :"
        )
        self.vy_label = create.create_name_label(
            parent = self.velocity_groupbox,
            font_size = 16,
            objname = "vy_label",
            text = "Vy :"
        )
        self.vz_label = create.create_name_label(
            parent = self.velocity_groupbox,
            font_size = 16,
            objname = "vz_label",
            text = "Vz :"
        )
        self.vx_ms_label = create.create_name_label(
            parent = self.velocity_groupbox,
            font_size = 12,
            objname = "vx_ms_label",
            text = "m/s"
        )
        self.vy_ms_label = create.create_name_label(
            parent = self.velocity_groupbox,
            font_size = 12,
            objname = "vy_ms_label",
            text = "m/s"
        )
        self.vz_ms_label = create.create_name_label(
            parent = self.velocity_groupbox,
            font_size = 12,
            objname = "vz_ms_label",
            text = "m/s"
        )
        self.vx_lineedit = create.create_line_edit(
            parent = self.velocity_groupbox,
            font_size = 16,
            objname = "vx_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.vy_lineedit = create.create_line_edit(
            parent = self.velocity_groupbox,
            font_size = 16,
            objname = "vy_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.vz_lineedit = create.create_line_edit(
            parent = self.velocity_groupbox,
            font_size = 16,
            objname = "vz_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.velocity_grid.addWidget(self.vx_label, 0, 0, 1, 1)
        self.velocity_grid.addWidget(self.vy_label, 1, 0, 1, 1)
        self.velocity_grid.addWidget(self.vz_label, 2, 0, 1, 1)
        self.velocity_grid.addWidget(self.vx_ms_label, 0, 2, 1, 1)
        self.velocity_grid.addWidget(self.vy_ms_label, 1, 2, 1, 1)
        self.velocity_grid.addWidget(self.vz_ms_label, 2, 2, 1, 1)
        self.velocity_grid.addWidget(self.vx_lineedit, 0, 1, 1, 1)
        self.velocity_grid.addWidget(self.vy_lineedit, 1, 1, 1, 1)
        self.velocity_grid.addWidget(self.vz_lineedit, 2, 1, 1, 1)

        # Acceleration

        self.acceleration_groupbox = create.create_group_box(
            parent = self.particle_settings_group,
            geometry = QtCore.QRect(400, 110, 221, 180),
            font_size = 18,
            objname = "acceleration_groupbox",
            title = "Acceleration (a) :",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft
        )
        self.acceleration_grid = create.create_grid_layout(
            parent = self.acceleration_groupbox,
            objname = "acceleration_grid"
        )

        self.ax_label = create.create_name_label(
            parent = self.acceleration_groupbox,
            font_size = 16,
            objname = "ax_label",
            text = "Ax :"
        )
        self.ay_label = create.create_name_label(
            parent = self.acceleration_groupbox,
            font_size = 16,
            objname = "ay_label",
            text = "Ay :"
        )
        self.az_label = create.create_name_label(
            parent = self.acceleration_groupbox,
            font_size = 16,
            objname = "az_label",
            text = "Az :"
        )
        self.ax_ms2_label = create.create_name_label(
            parent = self.acceleration_groupbox,
            font_size = 12,
            objname = "ax_ms2_label",
            text = "m/s^2"
        )
        self.ay_ms2_label = create.create_name_label(
            parent = self.acceleration_groupbox,
            font_size = 12,
            objname = "ay_ms2_label",
            text = "m/s^2"
        )
        self.az_ms2_label = create.create_name_label(
            parent = self.acceleration_groupbox,
            font_size = 12,
            objname = "az_ms2_label",
            text = "m/s^2"
        )
        self.ax_lineedit = create.create_line_edit(
            parent = self.acceleration_groupbox,
            font_size = 16,
            objname = "ax_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.ay_lineedit = create.create_line_edit(
            parent = self.acceleration_groupbox,
            font_size = 16,
            objname = "ay_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )
        self.az_lineedit = create.create_line_edit(
            parent = self.acceleration_groupbox,
            font_size = 16,
            objname = "az_lineedit",
            validator = QtGui.QDoubleValidator(-999.99, 999.99, 5),
            placeholder = "0.0"
        )

        self.acceleration_grid.addWidget(self.ax_label, 0, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ay_label, 1, 0, 1, 1)
        self.acceleration_grid.addWidget(self.az_label, 2, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ax_lineedit, 0, 2, 1, 1)
        self.acceleration_grid.addWidget(self.ay_lineedit, 1, 2, 1, 1)
        self.acceleration_grid.addWidget(self.az_lineedit, 2, 2, 1, 1)
        self.acceleration_grid.addWidget(self.ax_ms2_label, 0, 3, 1, 1)
        self.acceleration_grid.addWidget(self.ay_ms2_label, 1, 3, 1, 1)
        self.acceleration_grid.addWidget(self.az_ms2_label, 2, 3, 1, 1)

        self.particle_settings_group.hide()
        self.save_button.clicked.connect(self.add_particle_details)
        self.parent_particle_button.clicked.connect(self._show_particle_parent_menu)
        self.reset_button.clicked.connect(self.reset_details)
        self.delete_button.clicked.connect(lambda: self.delete_particle())

        self.hide_settings_button = create.create_button(
            parent = control_information_frame,
            font_size = 16,
            text = "Hide Settings",
            geometry = QtCore.QRect(10, 480, 150, 40),
            objname = "hide_settings_button"
        )
        self.hide_settings_button.clicked.connect(self.hide_show_settings)
        self.hide_settings_button.hide()

    def add_particle_details(self):
        """Adds a particle to the simulation"""

        x_value = float(self.x_axis_lineedit.text()) if self.x_axis_lineedit.text() else 0.0
        y_value = float(self.y_axis_lineedit.text()) if self.y_axis_lineedit.text() else 0.0
        z_value = float(self.z_axis_lineedit.text()) if self.z_axis_lineedit.text() else 0.0

        vx_value = float(self.vx_lineedit.text()) if self.vx_lineedit.text() else 0.0
        vy_value = float(self.vy_lineedit.text()) if self.vy_lineedit.text() else 0.0
        vz_value = float(self.vz_lineedit.text()) if self.vz_lineedit.text() else 0.0

        ax_value = float(self.ax_lineedit.text()) if self.ax_lineedit.text() else 0.0
        ay_value = float(self.ay_lineedit.text()) if self.ay_lineedit.text() else 0.0
        az_value = float(self.az_lineedit.text()) if self.az_lineedit.text() else 0.0

        name_input = self.name_lineedit.text() if self.name_lineedit.text() else 'P' + str(self.current_command_id)
        mass_input = float(self.mass_lineedit.text()) if self.mass_lineedit.text() else 1.0
        radius_input = float(self.radius_lineedit.text()) if self.radius_lineedit.text() else 1.0
        position_input = [x_value, y_value, z_value]
        velocity_input = [vx_value, vy_value, vz_value]
        acceleration_input = [ax_value, ay_value, az_value]
        elasticity_input = self.elasticity_spinbox.value()
        collision_input = self.collision_checkbox.isChecked()
        toggle_gravity_input = self.gravity_plane_checkbox.isChecked()
        color_input = [self.current_color.redF(), self.current_color.greenF(), self.current_color.blueF()]
        
        parent_particle_old = self.particle_classes.get(self.current_command_id, "None")

        if self.current_command_id in self.particle_classes:
            particle = self.particle_classes[self.current_command_id]
            particle.name = name_input
            particle.parent_particle = self.parent_particle
            particle.position = np.array(position_input, dtype = float)
            particle.velocity = np.array(velocity_input, dtype = float)
            particle.acceleration = np.array(acceleration_input, dtype = float)
            particle.mass = mass_input
            particle.radius = radius_input
            particle.collision = collision_input
            particle.elasticity = elasticity_input
            particle.gravity_plane = toggle_gravity_input
            particle.color = color_input

            particle.reset()

        else:
            particle = particle_property.Particle(
                id=self.current_command_id,
                name=name_input,
                parent_particle=self.parent_particle,
                position=position_input,
                velocity=velocity_input,
                acceleration=acceleration_input,
                mass=mass_input,
                radius=radius_input,
                collision=collision_input,
                elasticity=elasticity_input,
                gravity_plane=toggle_gravity_input,
                color=color_input
            )

        self.particle_classes[self.current_command_id] = particle

        if self.current_command_id in self.particle_variables:
            variable = self.particle_variables[self.current_command_id][1]
        else:
            variable = particle_variable_ui.Variables(self.graph_settings_ui)
            self.particle_variables[self.current_command_id] = [None, variable]


        self.particles[self.current_command_id] = [name_input, particle]
        self.particle_variables[self.current_command_id][0] = particle
        self.particle_classes[self.current_command_id] = particle
        name_update = self.command_link_buttons[self.current_command_id]
        name_update.setText(name_input)

        for variable in self.particle_variables.values():
            var = variable[1]
            try:
                var.particle_variable_group.hide()
            except:
                pass
            
        self.placeholder_widget()

        # Graphing Updates

        try:
            particle_variables = self.particle_variables.get(self.current_command_id)[1]
            particle_variables.update_names(name_input)
        except:
            pass

        # Naming Updates for Parent Particle

        for parent in self.particle_classes.values():
            if parent.parent_particle == parent_particle_old and parent_particle_old != "None":
                parent.parent_particle = particle

    def reset_details(self):
        """Resets the UI back to its placeholder values"""
        
        try:
            particle_details = self.particles.get(self.current_command_id)
            name = particle_details[0]
            self.particle_classes[self.current_command_id].parent_particle = "None"
            self.name_lineedit.setText(name)
            self.current_color = QtGui.QColor(255, 255, 255)
            self.color_button.setStyleSheet("background-color: white")
        except:
            self.name_lineedit.setPlaceholderText('P' + str(self.current_command_id))

        self.mass_lineedit.clear()
        self.radius_lineedit.clear()
        self.collision_checkbox.setChecked(False)
        self.gravity_plane_checkbox.setChecked(True)
        self.elasticity_spinbox.setValue(0.0)
        self.color_button.setStyleSheet("background-color: white")
        self.parent_particle = "None"
        self.parent_particle_button.setText("None")
        
        self.x_axis_lineedit.clear()
        self.y_axis_lineedit.clear()
        self.z_axis_lineedit.clear()

        self.vx_lineedit.clear()
        self.vy_lineedit.clear()
        self.vz_lineedit.clear()

        self.ax_lineedit.clear()
        self.ay_lineedit.clear()
        self.az_lineedit.clear()

    def delete_all_particles(self):
        """Removes all particle details and logic"""

        try:
            id_keys = list(self.command_link_buttons.keys())
            for id in id_keys:
                try:
                    button_remove = self.command_link_buttons.pop(id)
                    self.universe_verticalLayout.removeWidget(button_remove)
                    button_remove.hide()
                    button_remove.deleteLater()
                    self.particles.pop(id)
                    parent_particle_delete = self.particle_classes[id]
                    for parent in self.particle_classes.values():
                        if parent.parent_particle == parent_particle_delete and parent_particle_delete != "None":
                            parent.parent_particle = "None"

                    particle_variables = self.particle_variables.get(id)[1]
                    particle_variables.delete_labels()
                    try:
                        self.particle_classes.pop(id)
                        self.particle_variables.pop(id)
                    except:
                        pass
                except:
                    pass
            self.no_of_particles = 0
            self.current_command_id = None
            self.reset_details()
            self.placeholder_widget()
        except:
            pass

    def delete_particle(self):
        """Removes specified particle details and logic"""

        try:
            button_remove = self.command_link_buttons.pop(self.current_command_id)
            self.universe_verticalLayout.removeWidget(button_remove)
            button_remove.hide()
            button_remove.deleteLater()
            self.particles.pop(self.current_command_id)
            parent_particle_delete = self.particle_classes[self.current_command_id]

            for parent in self.particle_classes.values():
                if parent.parent_particle == parent_particle_delete and parent_particle_delete != "None":
                    parent.parent_particle = "None"

            # Delete Graphing labels

            particle_variables = self.particle_variables.get(self.current_command_id)[1]
            particle_variables.delete_labels()

            try:
                self.particle_classes.pop(self.current_command_id)
                self.particle_variables.pop(self.current_command_id)
            except:
                pass
            
            self.reset_details()
        except:
            pass

        self.placeholder_widget()

    def add_particle_universe(self):
        """Adds a command link button to the universe stack"""

        self.no_of_particles += 1
        self.current_command_id = self.no_of_particles
        self.initial_name = 'P' + str(self.no_of_particles)

        self.universe_particle = create.create_command_link(
            parent = self.universe_vlayout_widget,
            objname = "universe_particle",
            font_size = 16,
            text = self.initial_name
        )

        if os.path.exists(self.particle_icon_path):
            self.universe_particle.setIcon(QtGui.QIcon(self.particle_icon_path))
            self.universe_particle.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))

        self.universe_verticalLayout.addWidget(self.universe_particle)
        self.universe_particle.clicked.connect(lambda _, num = self.current_command_id: self.command_button_details(num))
        self.command_link_buttons[self.no_of_particles] = self.universe_particle

        self.current_color = QtGui.QColor(255, 255, 255)

    def load_particles_universe(self, particle_dicts):
        """
        A different way of loading particle values by passing a dictionary based on it.
        Used in saving and loading universes if a particle exists in the saved universe
        """

        for particle_details in particle_dicts:

            id = particle_details['id']
            name_input = particle_details["name"]
            position_input = particle_details["position"]
            velocity_input = particle_details["velocity"]
            acceleration_input = particle_details["acceleration"]
            mass_input = particle_details["mass"]
            radius_input = particle_details["radius"]
            collision_input = particle_details["collision"]
            elasticity_input = particle_details["elasticity"]
            toggle_gravity_input = particle_details["toggle_gravity"]
            color_input = particle_details["color"]

            self.universe_particle = create.create_command_link(
                parent = self.universe_vlayout_widget,
                objname = "universe_particle",
                font_size = 16,
                text = name_input
            )

            if os.path.exists(self.particle_icon_path):
                self.universe_particle.setIcon(QtGui.QIcon(self.particle_icon_path))
                self.universe_particle.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))

            particle = particle_property.Particle(
                id=id,
                name=name_input,
                parent_particle="None",
                position=position_input,
                velocity=velocity_input,
                acceleration=acceleration_input,
                mass=mass_input,
                radius=radius_input,
                collision=collision_input,
                elasticity=elasticity_input,
                gravity_plane=toggle_gravity_input,
                color=color_input
            )

            self.particle_classes[id] = particle
            variable = particle_variable_ui.Variables(self.graph_settings_ui)
            self.particle_variables[id] = [particle, variable]

            self.particles[id] = [name_input, particle]
            self.particle_classes[id] = particle

            for variable in self.particle_variables.values():
                var = variable[1]
                try:
                    var.particle_variable_group.hide()
                except:
                    pass
            
            try:
                particle_variables = self.particle_variables.get(id)[1]
                particle_variables.update_names(name_input)
            except:
                pass
            
            self.universe_verticalLayout.addWidget(self.universe_particle)
            self.universe_particle.clicked.connect(lambda _, num = id: self.command_button_details(num))
            self.command_link_buttons[id] = self.universe_particle

        id_list = []

        for particle_details in particle_dicts:
            id = particle_details["id"]
            id_list.append(id)
            parent_id = particle_details["parent_particle_id"]
            if parent_id != "None":
                parent_particle = self.particle_classes[parent_id]                
                child_particle = self.particle_classes[id]

                child_particle.parent_particle = parent_particle
                self.particles[id][1] = child_particle
                self.particle_classes[id] = child_particle
                self.particle_variables[id][0] = child_particle

        self.no_of_particles = max(id_list)

    def command_button_details(self, command_id):
        """Displays specific particle details when the command link button is clicked"""

        self.current_command_id = command_id
        self.particle_command_settings_function()
        details = None

        for variable in self.particle_variables.values():
            var = variable[1]
            try:
                var.particle_variable_group.hide()
            except:
                pass
        
        color = visual_settings.COLOR_DEFAULT_PARTICLE
        color_rgb = f"rgb({int(color[0])}, {int(color[1])}, {int(color[2])})"
        stylesheet = f"background-color: {color_rgb}"
        self.current_color = QtGui.QColor(int(color[0]),int(color[1]),int(color[2]))
        self.parent_particle = "None"
        try:
            particle_details = self.particles.get(command_id)
            particle_variables = self.particle_variables.get(command_id)[1]
            name = particle_details[0]
            details = vars(particle_details[1])
            if command_id in self.particles.keys():
                self.name_lineedit.setText(name)
                if details['parent_particle'] != "None":
                    self.parent_particle = details['parent_particle']
                    self.parent_particle_button.setText(details['parent_particle'].name)
                else:
                    self.parent_particle = "None"
                    self.parent_particle_button.setText("None")
                self.mass_lineedit.setText(str(details['mass']))
                self.radius_lineedit.setText(str(details['radius']))
                self.collision_checkbox.setChecked(True) if details['collision'] else self.collision_checkbox.setChecked(False)
                self.gravity_plane_checkbox.setChecked(True) if details['gravity_plane'] else self.gravity_plane_checkbox.setChecked(False)
                self.elasticity_spinbox.setValue(details['elasticity'])

                position = details['position']
                self.x_axis_lineedit.setText(str(position[0]))
                self.y_axis_lineedit.setText(str(position[1]))
                self.z_axis_lineedit.setText(str(position[2]))

                velocity = details['velocity']
                self.vx_lineedit.setText(str(velocity[0]))
                self.vy_lineedit.setText(str(velocity[1]))
                self.vz_lineedit.setText(str(velocity[2]))

                acceleration = details['acceleration']
                self.ax_lineedit.setText(str(acceleration[0]))
                self.ay_lineedit.setText(str(acceleration[1]))
                self.az_lineedit.setText(str(acceleration[2]))
                if 'color' in details:
                    color = details['color']
                    self.current_color = QtGui.QColor.fromRgbF(color[0], color[1], color[2])
                    self.color_button.setStyleSheet(f"background-color: {self.current_color.name()}")
                else:
                    self.current_color = QtGui.QColor(255, 255, 255)
                    self.color_button.setStyleSheet("background-color: white")

                particle_variables.setup_particle_variable(self.control_information_frame, particle_details[1])
                particle_variables.set_title(name)
                particle_variables.particle_variable_group.show()

            else:
                raise
        except:

            self.particles[command_id] = ['P' + str(command_id), None]
            self.name_lineedit.setPlaceholderText('P' + str(command_id))
            self.name_lineedit.clear()
            self.mass_lineedit.clear()
            self.radius_lineedit.clear()
            self.collision_checkbox.setChecked(False)
            self.gravity_plane_checkbox.setChecked(True)
            self.elasticity_spinbox.setValue(0.0)
            self.color_button.setStyleSheet(stylesheet)
            self.parent_particle_button.setText("None")

            self.x_axis_lineedit.clear()
            self.y_axis_lineedit.clear()
            self.z_axis_lineedit.clear()

            self.vx_lineedit.clear()
            self.vy_lineedit.clear()
            self.vz_lineedit.clear()

            self.ax_lineedit.clear()
            self.ay_lineedit.clear()
            self.az_lineedit.clear()