import utils.create_uicomponents as create
from utils.resolution_scaler import ResolutionScaler

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json

class SavedUniverses_UI:
    def __init__(self):
        self.save_folder = None

        self.file_id = 0
        self.no_of_files = 0
        self.file_classes = {}
        self.command_link_buttons = {}
        self.current_file_details = None
        self.current_file_path = None

        self.scaler = ResolutionScaler()

    def setup_saved_universes(self, settings_stacked_widget, placeholder_widget, particle_ui, gravity_ui, boundary_ui, universe_settings_ui):
        """Configure Saved Universes Setup"""

        self.placeholder_widget = placeholder_widget
        self.particle_ui = particle_ui
        self.gravity_ui = gravity_ui
        self.boundary_ui = boundary_ui
        self.universe_settings_ui = universe_settings_ui

        self.saved_universes_group = create.create_group_box(
            parent = settings_stacked_widget,
            geometry = QtCore.QRect(9, 9, 931, 511),
            font_size = 20,
            objname = "saved_universes_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Saved Universes"
        )
        self.universe_details_group = create.create_group_box(
            parent = self.saved_universes_group,
            geometry = QtCore.QRect(480, 40, 441, 461),
            font_size = 18,
            objname = "universe_details_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignLeft,
            title = "Details"
        )

        self.universe_name_label = create.create_name_label(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(10, 38, 421, 24),
            font_size = 16,
            text = "Name :  -",
            objname = "universe_name_label"
        )

        self.values_frame = create.create_frame(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(10, 70, 421, 121),
            font_size = 16,
            fshape = QtWidgets.QFrame.StyledPanel,
            fshadow = QtWidgets.QFrame.Raised,
            objname = "values_frame"
        )
        self.values_grid = create.create_grid_layout(
            parent = self.values_frame,
            objname = "values_grid"
        )

        self.no_of_particles_label = create.create_name_label(
            parent = self.values_frame,
            font_size = 16,
            text = "Number of\nParticles : -",
            objname = "no_of_particles_label"
        )
        self.no_of_gravity_planes_label = create.create_name_label(
            parent = self.values_frame,
            font_size = 16,
            text = "Number of\nGravity Planes : -",
            objname = "no_of_gravity_planes_label"
        )
        self.boundary_label = create.create_name_label(
            parent = self.values_frame,
            font_size = 16,
            text = "Boundary : -",
            objname = "boundary_label"
        )
        self.g_value_label = create.create_name_label(
            parent = self.values_frame,
            font_size = 16,
            text = "G Value : -",
            objname = "g_value_label"
        )

        self.values_grid.addWidget(self.no_of_particles_label, 0, 0, 1, 1)
        self.values_grid.addWidget(self.no_of_gravity_planes_label, 0, 1, 1, 1)
        self.values_grid.addWidget(self.boundary_label, 1, 0, 1, 1)
        self.values_grid.addWidget(self.g_value_label, 1, 1, 1, 1)

        self.universe_description_label = create.create_name_label(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(10, 190, 151, 24),
            font_size = 16,
            text = "Description :",
            objname = "universe_description_label"
        )
        self.universe_description_textedit = create.create_text_edit(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(10, 220, 421, 141),
            font_size = 15,
            placeholder = "-",
            objname = "universe_description_textedit"
        )
        self.universe_description_textedit.setReadOnly(True)

        self.creation_date_label = create.create_name_label(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(10, 370, 391, 24),
            font_size = 16,
            text = "Date : -",
            objname = "creation_date_label"
        )

        self.universe_load_button = create.create_button(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(10, 400, 171, 51),
            font_size = 16,
            text = "Load",
            objname = "universe_load_button"
        )
        self.universe_delete_button = create.create_button(
            parent = self.universe_details_group,
            geometry = QtCore.QRect(260, 400, 171, 51),
            font_size = 16,
            text = "Delete",
            objname = "universe_delete_button"
        )

        self.universe_display_scrollarea = create.create_scroll(
            parent = self.saved_universes_group,
            geometry = QtCore.QRect(10, 40, 461, 461),
            objname = "universe_display_scrollarea",
            resizable = True
        )
        self.universe_display_widget = create.create_widget(
            geometry = QtCore.QRect(0, 0, 459, 459),
            objname = "universe_display_widget"
        )
        self.universe_display_vlayout = create.create_vlayout(
            parent = self.universe_display_widget,
            objname = "universe_display_vlayout",
            alignment = True
        )

        self.universe_display_scrollarea.setWidget(self.universe_display_widget)
        self.universe_details_group.hide()

        self.universe_load_button.clicked.connect(lambda: self.load_selected_universe())
        self.universe_delete_button.clicked.connect(lambda: self.delete_selected_universe())

    def display_saved_universes(self):
        """Displays each save file as a command link button"""

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        self.save_folder = os.path.join(base_dir, "saves")
        json_files = [file for file in os.listdir(self.save_folder) if file.endswith(".json")]
        self.no_of_files = len(json_files)
        self.file_id = 0

        # Clear all existing command link buttons before displaying new saves
 
        while self.universe_display_vlayout.count():
            item = self.universe_display_vlayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.file_classes.clear()
        self.command_link_buttons.clear()
        
        # Display Saves
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        saves_icon_path = os.path.join(base_dir, "pictures", "arrow.png").replace('\\','/')

        for file in json_files:
            self.file_id += 1

            self.saved_universe_file_command = create.create_command_link(
                parent = self.universe_display_widget,
                objname = "universe_particle",
                font_size = 16,
                text = file[0:-5]
            )
            self.saved_universe_file_command.setIcon(QtGui.QIcon(saves_icon_path))
            self.saved_universe_file_command.setIconSize(QtCore.QSize(*self.scaler.scale_size(20, 20)))

            file_path = os.path.join(self.save_folder, file)
            with open(file_path, "r") as file_color:
                details = json.load(file_color)
            color = details["color"]
            rgb_color = f"rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)})"
            self.saved_universe_file_command.setStyleSheet(f"QCommandLinkButton {{ color: {rgb_color}; }}")

            self.universe_display_vlayout.addWidget(self.saved_universe_file_command)
            self.saved_universe_file_command.clicked.connect(lambda _, num = self.file_id: self.display_universe_details(num))

            self.file_classes[self.file_id] = file
            self.command_link_buttons[self.file_id] = self.saved_universe_file_command

    def display_universe_details(self, display_id):
        """Displays details of each save"""

        file = self.file_classes[display_id]
        file_path = os.path.join(self.save_folder, file)
        self.current_file_path = file_path
        self.current_display_id = display_id

        with open(file_path, "r") as file:
            self.current_file_details = json.load(file)

        self.universe_name_label.setText("Name : " + self.current_file_details["universe_name"])
        self.no_of_particles_label.setText("Number of\nParticles : " + str(self.current_file_details["no_of_particles"]))
        self.no_of_gravity_planes_label.setText("Number of\nGravity Planes : " + str(self.current_file_details["no_of_gravity_planes"]))
        self.boundary_label.setText("Boundary : " + str(self.current_file_details["boundary"]))
        self.g_value_label.setText("G Value : " + str(self.current_file_details["g_value"]))
        self.universe_description_textedit.setText(self.current_file_details["description"])
        self.creation_date_label.setText("Date : " + str(self.current_file_details["date"]))

        self.universe_details_group.show()

    def load_selected_universe(self):
        """Loads all elements specified within the save details"""

        self.particle_ui.delete_all_particles()
        self.gravity_ui.delete_all_gravity()
        self.boundary_ui.delete_boundary()
        if self.current_file_details["particles"]:
            particles_dicts = self.current_file_details["particles"]
            self.particle_ui.load_particles_universe(particles_dicts)
        
        if self.current_file_details["gravity_planes"]:
            gravity_dicts = self.current_file_details["gravity_planes"]
            self.gravity_ui.load_gravity_universe(gravity_dicts)

        if self.current_file_details["boundary_details"]:
            boundary_dict = self.current_file_details["boundary_details"]
            self.boundary_ui.load_boundary_universe(boundary_dict)

        g_value = self.current_file_details["g_value"]
        self.universe_settings_ui.load_g_value(g_value)

        self.placeholder_widget()

    def delete_selected_universe(self):
        """Deletes a save from the folder when specified"""

        if os.path.exists(self.current_file_path) and self.current_file_path.endswith(".json"):
            os.remove(self.current_file_path)

            button_remove = self.command_link_buttons.pop(self.current_display_id)
            self.universe_display_vlayout.removeWidget(button_remove)
            button_remove.hide()
            button_remove.deleteLater()
            self.file_classes.pop(self.current_display_id)
            self.universe_details_group.hide()