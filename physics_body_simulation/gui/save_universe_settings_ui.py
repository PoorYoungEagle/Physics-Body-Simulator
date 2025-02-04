import utils.create_uicomponents as create
import constants.universe_settings as universe_settings

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os
from datetime import datetime

class SaveUniverseSettings_UI:
    def __init__(self):
        self.current_color = QtGui.QColor(255, 255, 255)

    def _show_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_color = color
            self.save_universe_color_button.setStyleSheet(f"background-color: {color.name()}")

    def setup_save_universe_settings(self, settings_stacked_widget, placeholder_widget, particle_classes, gravity_classes, boundary):
        """Configure Save Settings Setup"""

        self.placeholder_widget = placeholder_widget

        self.particle_classes = particle_classes
        self.gravity_classes = gravity_classes
        self.boundary = boundary

        self.save_universe_settings_group = create.create_group_box(
            parent = settings_stacked_widget,
            geometry = QtCore.QRect(9, 9, 931, 511),
            font_size = 20,
            objname = "save_universe_settings_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Save Universe Settings"
        )

        self.save_universe_name_label = create.create_name_label(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(20, 50, 81, 31),
            font_size = 16,
            text = "Name :",
            objname = "save_universe_name_label"
        )
        self.save_universe_name_lineedit = create.create_line_edit(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(110, 50, 181, 31),
            font_size = 16,
            objname = "save_universe_name_lineedit",
            placeholder = "Required"
        )
        self.save_universe_color_label = create.create_name_label(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(320, 50, 81, 31),
            font_size = 16,
            text = "Color :",
            objname = "save_universe_color_label"
        )
        self.save_universe_color_button = create.create_button(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(399, 50, 131, 30),
            font_size = 16,
            text = "",
            objname = "save_universe_color_button"
        )
        self.save_universe_color_button.setStyleSheet("background-color: white")

        self.save_universe_description_label = create.create_name_label(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(20, 100, 161, 31),
            font_size = 16,
            text = "Description :",
            objname = "save_universe_description_label"
        )
        self.save_universe_description_textedit = create.create_text_edit(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(20, 140, 891, 291),
            font_size = 14,
            placeholder = "-",
            objname = "save_universe_description_textedit"
        )

        self.save_universe_button = create.create_button(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(0, 460, 150, 50),
            font_size = 20,
            text = "Save",
            objname = "self.save_universe_button"
        )
        self.reset_universe_button = create.create_button(
            parent = self.save_universe_settings_group,
            geometry = QtCore.QRect(150, 460, 150, 50),
            font_size = 20,
            text = "Reset",
            objname = "reset_universe_button"
        )

        self.save_universe_color_button.clicked.connect(self._show_color_dialog)
        self.save_universe_button.clicked.connect(lambda: self.save_current_universe())
        self.reset_universe_button.clicked.connect(lambda: self.reset_details())

    def convert_particle_to_dict(self, particle):
        try:
            return {
            "id" : particle.id,
            "name" : particle.name,
            "mass" : particle.mass,
            "radius" : particle.radius,
            "position" : particle.position.tolist(),
            "velocity" : particle.velocity.tolist(),
            "acceleration" : particle.acceleration.tolist(),
            "elasticity" : particle.elasticity,
            "collision" : particle.collision,
            "toggle_gravity" : particle.gravity_plane,
            "color" : particle.color,
            "parent_particle_id" : particle.parent_particle.id
            }
        except:
            return {
            "id" : particle.id,
            "name" : particle.name,
            "mass" : particle.mass,
            "radius" : particle.radius,
            "position" : particle.position.tolist(),
            "velocity" : particle.velocity.tolist(),
            "acceleration" : particle.acceleration.tolist(),
            "elasticity" : particle.elasticity,
            "collision" : particle.collision,
            "toggle_gravity" : particle.gravity_plane,
            "color" : particle.color,
            "parent_particle_id" : "None"
            }

    def convert_gravity_to_dict(self, gravity):
        return {
            "name" : gravity.name,
            "position" : gravity.position.tolist(),
            "normal" : gravity.normal.tolist(),
            "gravity_strength" : gravity.gravity_strength,
            "width" : gravity.width,
            "depth" : gravity.depth,
            "design" : gravity.design,
            "plane_color" : gravity.plane_color,
            "plane_opacity" : gravity.plane_opacity,
            "line_color" : gravity.line_color,
            "line_opacity" : gravity.line_opacity,
            "collision" : gravity.collision
        }
    
    def convert_boundary_to_dict(self, boundary):
        return {
            "width" : boundary.width,
            "depth" : boundary.depth,
            "height" : boundary.height,
            "color" : boundary.color.tolist(),
            "restitution" : boundary.restitution,
            "opacity" : boundary.opacity
        }

    def save_current_universe(self):
        """Converts values to a json file when saved"""

        name_input = self.save_universe_name_lineedit.text()
        if name_input:
            color_input = [self.current_color.redF(), self.current_color.greenF(), self.current_color.blueF()]
            description_input = self.save_universe_description_textedit.toPlainText() if self.save_universe_description_textedit.toPlainText() else "-"
            no_of_particles = len(self.particle_classes)
            no_of_gravity_planes = len(self.gravity_classes)
            if self.boundary:
                boundary = True
            else:
                boundary = False

            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p")

            data = {
                "universe_name" : name_input,
                "description" : description_input,
                "color" : color_input,
                "no_of_particles" : no_of_particles,
                "no_of_gravity_planes" : no_of_gravity_planes,
                "boundary" : boundary,
                "g_value" : universe_settings.GRAVITATIONAL_CONSTANT,
                "date" : formatted_time,
                "particles" : None,
                "gravity_planes" : None,
                "boundary_details" : None
            }
            if self.particle_classes:
                data["particles"] = [self.convert_particle_to_dict(particle) for particle in self.particle_classes.values()]
            if self.gravity_classes:
                data["gravity_planes"] = [self.convert_gravity_to_dict(gravity) for gravity in self.gravity_classes.values()]
            if self.boundary:
                data["boundary_details"] = self.convert_boundary_to_dict(self.boundary[1])

            # script_dir = os.path.dirname(os.path.abspath(__file__))
            # base_dir = os.path.dirname(script_dir)
            # self.boundary_icon_path = os.path.join(base_dir, "pictures", "boundary2.png").replace('\\','/')

            filename = name_input+".json"

            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(script_dir)
            saves_path = os.path.join(base_dir, "saves").replace('\\', '/')
            file_path = os.path.join(saves_path, filename)

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            self.reset_details()
            self.placeholder_widget()

    def reset_details(self):
        """Resets back to its placeholder values"""

        self.save_universe_name_lineedit.clear()
        self.save_universe_description_textedit.clear()
        self.current_color = QtGui.QColor(255, 255, 255)
        self.save_universe_color_button.setStyleSheet("background-color: white")