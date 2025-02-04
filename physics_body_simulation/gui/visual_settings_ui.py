import utils.create_uicomponents as create
import constants.visual_settings as visual_settings
import utils.dark_mode as dark_mode

from PyQt5 import QtCore, QtGui, QtWidgets

class VisualSettings_UI:
    def __init__(self):
        self.current_background_color = QtGui.QColor(1, 10, 38)
        self.current_grid_color = QtGui.QColor(102, 102, 255)
        self.current_default_particle_color = QtGui.QColor(255, 255, 255)
        self.current_connecting_lines_color = QtGui.QColor(255, 255, 255)

    def _show_background_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_background_color = color
            self.background_color_button.setStyleSheet(f"background-color: {color.name()}")  
    
    def _show_grid_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_grid_color = color
            self.grid_color_button.setStyleSheet(f"background-color: {color.name()}")
    
    def _show_default_particle_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_default_particle_color = color
            self.default_particle_color_button.setStyleSheet(f"background-color: {color.name()}")
    
    def _show_connecting_lines_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_connecting_lines_color = color
            self.connecting_lines_color_button.setStyleSheet(f"background-color: {color.name()}")
    
    def setup_visual_settings(self, settings_stacked_widget, placeholder_widget):
        """Configure Visual Settings"""

        self.settings_stacked_widget = settings_stacked_widget
        self.placeholder_widget = placeholder_widget
        self.visual_settings_group = create.create_group_box(
            parent = self.settings_stacked_widget, 
            geometry = QtCore.QRect(9, 9, 931, 511),
            objname = "visual_settings_group",
            title = "Visual Settings",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )

        # Visibility Options

        self.visibility_options_group = create.create_group_box(
            parent = self.visual_settings_group, 
            geometry = QtCore.QRect(20, 100, 250, 230),
            objname = "visibility_options_group",
            title = "Visibility Options:",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.visibility_options_grid = create.create_grid_layout(
            parent = self.visibility_options_group,
            objname = "visibility_options_grid"
        )

        self.xyz_lines_checkbox = create.create_checkbox(
            parent = self.visibility_options_group,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "xyz_lines_checkbox",
            text = "Show XYZ Lines : "
        )
        self.xyz_lines_checkbox.setChecked(True)
        self.grid_checkbox = create.create_checkbox(
            parent = self.visibility_options_group,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "grid_checkbox",
            text = "Show 3D Grid : "
        )
        self.grid_checkbox.setChecked(True)
        self.particle_trail_checkbox = create.create_checkbox(
            parent = self.visibility_options_group,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "particle_trail_checkbox",
            text = "Show Particle Trail : "
        )
        self.connecting_lines_checkbox = create.create_checkbox(
            parent = self.visibility_options_group,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "connecting_lines_checkbox",
            text = "Connecting Lines : "
        )

        self.visibility_options_grid.addWidget(self.xyz_lines_checkbox)
        self.visibility_options_grid.addWidget(self.grid_checkbox)
        self.visibility_options_grid.addWidget(self.particle_trail_checkbox)
        self.visibility_options_grid.addWidget(self.connecting_lines_checkbox)

        # Color Options

        self.color_options_group = create.create_group_box(
            parent = self.visual_settings_group, 
            geometry = QtCore.QRect(300, 100, 330, 230),
            objname = "color_options_group",
            title = "Color Options:",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.color_options_grid = create.create_grid_layout(
            parent = self.color_options_group,
            objname = "color_options_grid"
        )

        self.background_color_label = create.create_name_label(
            parent = self.color_options_group,
            objname = "background_color_label",
            font_size = 16,
            text = "Background Color : "
        )
        self.grid_color_label = create.create_name_label(
            parent = self.color_options_group,
            objname = "grid_color_label",
            font_size = 16,
            text = "3D Color Grid : "
        )
        self.default_particle_color_label = create.create_name_label(
            parent = self.color_options_group,
            objname = "default_particle_color_label",
            font_size = 16,
            text = "Default Particle\nColor :"
        )
        self.connecting_lines_color_label = create.create_name_label(
            parent = self.color_options_group,
            objname = "connecting_lines_color_label",
            font_size = 16,
            text = "Connecting Lines\nColor :"
        )
        self.background_color_button = create.create_button(
            parent = self.color_options_group,
            font_size = 16,
            objname = "background_color_button",
            text = ""
        )
        self.grid_color_button = create.create_button(
            parent = self.color_options_group,
            font_size = 16,
            objname = "grid_color_button",
            text = ""
        )
        self.default_particle_color_button = create.create_button(
            parent = self.color_options_group,
            font_size = 16,
            objname = "default_particle_color_button",
            text = ""
        )
        self.connecting_lines_color_button = create.create_button(
            parent = self.color_options_group,
            font_size = 16,
            objname = "connecting_lines_color_button",
            text = ""
        )

        self.background_color_button.setStyleSheet("background-color: rgb(1, 10, 38)")
        self.grid_color_button.setStyleSheet("background-color: rgb(102, 102, 255)")
        self.default_particle_color_button.setStyleSheet("background-color: white")
        self.connecting_lines_color_button.setStyleSheet("background-color: white")

        self.background_color_button.clicked.connect(self._show_background_color_dialog)
        self.grid_color_button.clicked.connect(self._show_grid_color_dialog)
        self.default_particle_color_button.clicked.connect(self._show_default_particle_color_dialog)
        self.connecting_lines_color_button.clicked.connect(self._show_connecting_lines_color_dialog)

        
        self.color_options_grid.addWidget(self.background_color_label, 0, 0, 1, 1)
        self.color_options_grid.addWidget(self.background_color_button, 0, 1, 1, 1)
        self.color_options_grid.addWidget(self.grid_color_label, 1, 0, 1, 1)
        self.color_options_grid.addWidget(self.grid_color_button, 1, 1, 1, 1)
        self.color_options_grid.addWidget(self.default_particle_color_label, 2, 0, 1, 1)
        self.color_options_grid.addWidget(self.default_particle_color_button, 2, 1, 1, 1)
        self.color_options_grid.addWidget(self.connecting_lines_color_label, 3, 0, 1, 1)
        self.color_options_grid.addWidget(self.connecting_lines_color_button, 3, 1, 1, 1)

        # GUI Options

        self.gui_options_group = create.create_group_box(
            parent = self.visual_settings_group, 
            geometry = QtCore.QRect(670, 100, 180, 90),
            objname = "gui_options_group",
            title = "GUI Options:",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )
        self.gui_options_grid = create.create_grid_layout(
            parent = self.gui_options_group,
            objname = "gui_options_grid"
        )

        self.dark_mode_checkbox = create.create_checkbox(
            parent = self.gui_options_group,
            font_size = 16,
            layout = QtCore.Qt.RightToLeft,
            objname = "dark_mode_checkbox",
            text = "Dark Mode : "
        )
        self.dark_mode_checkbox.setChecked(True)

        self.gui_options_grid.addWidget(self.dark_mode_checkbox)

        # Save and Reset Buttons
        
        self.save_visual_button = create.create_button(
            parent = self.visual_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            objname = "save_visual_button",
            font_size = 20,
            text = "Save"
        )
        self.reset_visual_button = create.create_button(
            parent = self.visual_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            objname = "reset_visual_button",
            font_size = 20,
            text = "Reset"
        )

        self.save_visual_button.clicked.connect(self.update_visual_settings)
        self.reset_visual_button.clicked.connect(self.reset_visual_settings)

    def update_visual_settings(self):
        """Updates the values when save button is clicked"""
        
        app = QtWidgets.QApplication.instance()
        if self.dark_mode_checkbox.isChecked():
            dark_mode.set_dark_theme(app)
        else:
            dark_mode.set_light_theme(app)

        xyz_lines = int(self.xyz_lines_checkbox.isChecked())
        grid = int(self.grid_checkbox.isChecked())
        particle_trail = int(self.particle_trail_checkbox.isChecked())
        connecting_lines = int(self.connecting_lines_checkbox.isChecked())
        
        bg_color = [self.current_background_color.redF(), self.current_background_color.greenF(), self.current_background_color.blueF()]
        grid_color = [self.current_grid_color.redF(), self.current_grid_color.greenF(), self.current_grid_color.blueF()]
        default_color = [self.current_default_particle_color.redF(), self.current_default_particle_color.greenF(), self.current_default_particle_color.blueF()]
        connecting_color = [self.current_connecting_lines_color.redF(), self.current_connecting_lines_color.greenF(), self.current_connecting_lines_color.blueF()]

        visual_settings.set_3d_grid(grid)
        visual_settings.set_xyz_lines(xyz_lines)
        visual_settings.set_particle_trail(particle_trail)
        visual_settings.set_connecting_lines(connecting_lines)

        visual_settings.set_background_color(bg_color)
        visual_settings.set_3d_grid_color(grid_color)
        visual_settings.set_default_particle(default_color)
        visual_settings.set_connecting_lines_color(connecting_color)

        self.placeholder_widget()

    def reset_visual_settings(self):
        """Resets to placeholder values"""
        
        self.xyz_lines_checkbox.setChecked(True)
        self.grid_checkbox.setChecked(True)
        self.particle_trail_checkbox.setChecked(False)
        self.connecting_lines_checkbox.setChecked(False)

        self.background_color_button.setStyleSheet("background-color: rgb(1, 10, 38)")
        self.grid_color_button.setStyleSheet("background-color: rgb(102, 102, 255)")
        self.default_particle_color_button.setStyleSheet("background-color: white")
        self.connecting_lines_color_button.setStyleSheet("background-color: white")
        
        self.current_background_color = QtGui.QColor(1, 10, 38)
        self.current_grid_color = QtGui.QColor(102, 102, 255)
        self.current_default_particle_color = QtGui.QColor(255, 255, 255)
        self.current_connecting_lines_color = QtGui.QColor(255, 255, 255)