import utils.create_uicomponents as create
from utils.resolution_scaler import ResolutionScaler

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class GroupManager:
    """Manages UI groups and their interactions for the particle simulation interface"""

    def __init__(
            self,

            # UI groups
            
            particle_ui,
            random_particle_ui,
            gravity_ui,
            boundary_ui,
            visual_settings_ui,
            universe_settings_ui,
            saved_universes_ui,
            save_universe_settings_ui,

            # Arbitrary Values

            centralwidget,
            universe_verticalLayout,
            universe_vlayout_widget,
            universe_matter_frame,
            control_information_frame,
            add_boundary_button
        ):
        """Initialize UI components and setup all group interfaces"""

        self.particle_ui = particle_ui
        self.random_particle_ui = random_particle_ui
        self.gravity_ui = gravity_ui
        self.boundary_ui = boundary_ui
        self.visual_settings_ui = visual_settings_ui
        self.universe_settings_ui = universe_settings_ui
        self.saved_universes_ui = saved_universes_ui
        self.save_universe_settings_ui = save_universe_settings_ui

        self.centralwidget = centralwidget
        self.universe_verticalLayout = universe_verticalLayout
        self.universe_vlayout_widget = universe_vlayout_widget
        self.universe_matter_frame = universe_matter_frame
        self.control_information_frame = control_information_frame
        self.add_boundary_button = add_boundary_button

        self.setup_placeholder_group()
        self.particle_ui.setup_particle_settings(
            self.centralwidget,
            self.settings_stacked_widget,
            self.universe_verticalLayout,
            self.control_information_frame,
            self.universe_matter_frame,
            self.universe_vlayout_widget,
            self.placeholder_widget,
            self.particle_command_settings_function
        )
        self.random_particle_ui.setup_random_particle_settings(
            self.settings_stacked_widget,
            self.particle_ui
        )
        self.gravity_ui.setup_gravity_settings(
            self.settings_stacked_widget,
            self.universe_verticalLayout,
            self.universe_vlayout_widget,
            self.placeholder_widget,
            self.gravity_command_settings_function
        )
        self.boundary_ui.setup_boundary_settings(
            self.settings_stacked_widget,
            self.universe_verticalLayout,
            self.add_boundary_button,
            self.universe_vlayout_widget,
            self.placeholder_widget,
            self.boundary_command_settings_function
        )
        self.visual_settings_ui.setup_visual_settings(
            self.settings_stacked_widget,
            self.placeholder_widget
        )
        self.universe_settings_ui.setup_universe_settings(
            self.settings_stacked_widget,
            self.placeholder_widget
        )
        self.saved_universes_ui.setup_saved_universes(
            self.settings_stacked_widget,
            self.placeholder_widget,
            self.particle_ui,
            self.gravity_ui,
            self.boundary_ui,
            self.universe_settings_ui
        )
        self.save_universe_settings_ui.setup_save_universe_settings(
            self.settings_stacked_widget,
            self.placeholder_widget,
            self.particle_ui.particle_classes,
            self.gravity_ui.gravity_classes,
            self.boundary_ui.boundary
        )

        self.settings_stacked_widget.addWidget(self.settings_opening_groupbox)
        self.settings_stacked_widget.addWidget(self.particle_ui.particle_settings_group)
        self.settings_stacked_widget.addWidget(self.random_particle_ui.random_particle_settings_group)
        self.settings_stacked_widget.addWidget(self.gravity_ui.gravity_settings_group)
        self.settings_stacked_widget.addWidget(self.boundary_ui.boundary_settings_group)
        self.settings_stacked_widget.addWidget(self.visual_settings_ui.visual_settings_group)
        self.settings_stacked_widget.addWidget(self.universe_settings_ui.universe_settings_group)
        self.settings_stacked_widget.addWidget(self.saved_universes_ui.saved_universes_group)
        self.settings_stacked_widget.addWidget(self.save_universe_settings_ui.save_universe_settings_group)

    def setup_placeholder_group(self):
        self.settings_stacked_widget = create.create_stacked_widget(
            parent = self.centralwidget,
            geometry = QtCore.QRect(9, 9, 948, 528),
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "settings_stacked_widget"
        )
        self.settings_opening_groupbox = create.create_group_box(
            parent = self.settings_stacked_widget,
            geometry = QtCore.QRect(9, 9, 931, 511),
            objname = "particles_group",
            title = "Placeholder",
            font_size = 20,
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter
        )

        self.ooze = create.create_name_label(
            parent = self.settings_opening_groupbox,
            geometry = QtCore.QRect(0, 270, 830, 47),
            objname = "ooze",
            font_size = 16,
            text = "_______________________________________________________________________________________________________"
        )
        self.ooze.setStyleSheet("color: #b8b8b8;")
        self.something = create.create_name_label(
            parent = self.settings_opening_groupbox,
            geometry = QtCore.QRect(290, 270, 240, 30),
            objname = "something",
            font_size = 16,
            text = "Something goes here..."
        )
        self.something.setStyleSheet("color: #b8b8b8;")

        placeholder_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures", "placeholder.png").replace('\\','/')
        self.snail = create.create_button(
            parent = self.settings_opening_groupbox,
            geometry = QtCore.QRect(820, 220, 100, 100),
            objname = "snail",
            font_size = 18,
            text = ""
        )
        self.snail.setStyleSheet("border: none; background: transparent;")
        scaler = ResolutionScaler()
        self.snail.setIcon(QtGui.QIcon(placeholder_icon_path))
        self.snail.setIconSize(QtCore.QSize(*scaler.scale_size(90, 90)))

    def placeholder_widget(self):
        """Display placeholder opening screen"""
        
        self.settings_stacked_widget.setCurrentWidget(self.settings_opening_groupbox)

    def particle_command_settings_function(self):
        """Switch to particle settings group"""

        self.settings_stacked_widget.setCurrentWidget(self.particle_ui.particle_settings_group)

    def random_particle_command_settings_function(self):
        """Switch to random particle generator group"""

        self.random_particle_ui.set_default_parent()
        self.settings_stacked_widget.setCurrentWidget(self.random_particle_ui.random_particle_settings_group)

    def gravity_command_settings_function(self):
        """Switch to gravity settings group"""

        self.settings_stacked_widget.setCurrentWidget(self.gravity_ui.gravity_settings_group)

    def boundary_command_settings_function(self):
        """Switch to boundary settings group"""

        self.settings_stacked_widget.setCurrentWidget(self.boundary_ui.boundary_settings_group)

    def visual_settings_function(self):
        """Switch to visual settings group"""

        self.settings_stacked_widget.setCurrentWidget(self.visual_settings_ui.visual_settings_group)

    def universe_settings_function(self):
        """Switch to universe settings group"""

        self.settings_stacked_widget.setCurrentWidget(self.universe_settings_ui.universe_settings_group)

    def saved_universes_function(self):
        """Switch to saved universes group which displays all the saves present in "save" file"""

        self.settings_stacked_widget.setCurrentWidget(self.saved_universes_ui.saved_universes_group)
        self.saved_universes_ui.display_saved_universes()
        self.saved_universes_ui.universe_details_group.hide()

    def save_universe_settings_function(self):
        """Switch to save universe settings group"""

        self.settings_stacked_widget.setCurrentWidget(self.save_universe_settings_ui.save_universe_settings_group)

    def clear_universe_function(self):
        """Deletes all matter present in universe"""

        self.particle_ui.delete_all_particles()
        self.gravity_ui.delete_all_gravity()
        self.boundary_ui.delete_boundary()

    def particle_settings_group(self):
        """Adds a particle to the universe list"""

        self.particle_ui.add_particle_universe()
    
    def gravity_settings_group(self):
        """Adds a gravity plane to the universe list"""

        self.gravity_ui.add_gravity_universe()

    def boundary_settings_group(self):
        """Adds a boundary to the universe list"""
        
        self.boundary_ui.add_boundary_universe()