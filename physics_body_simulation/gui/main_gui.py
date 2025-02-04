import utils.create_uicomponents as create
from utils.groupbox_manager import GroupManager
from utils.resolution_scaler import ResolutionScaler
from simulation.opengl_widget import OpenGLWidget
from gui.particle_ui import Particle_UI
from gui.random_particle_ui import RandomParticle_UI
from gui.gravity_ui import Gravity_UI
from gui.boundary_ui import Boundary_UI
from gui.universe_settings_ui import UniverseSettings_UI
from gui.visual_settings_ui import VisualSettings_UI
from gui.saved_universes_ui import SavedUniverses_UI
from gui.save_universe_settings_ui import SaveUniverseSettings_UI

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class ParticleSimulatorGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.particle_ui = Particle_UI()
        self.random_particle_ui = RandomParticle_UI()
        self.gravity_ui = Gravity_UI()
        self.boundary_ui = Boundary_UI()
        self.visual_settings_ui = VisualSettings_UI()
        self.universe_settings_ui = UniverseSettings_UI()
        self.saved_universes_ui = SavedUniverses_UI()
        self.save_universe_settings_ui = SaveUniverseSettings_UI()

        self.binary_indicator = 0

        self.openGLWidget = OpenGLWidget()

        self.number_of_plots = 1
        self.dimension = "2D"

    def setupGUI(self, MainWindow):
        """Sets up the Group Manager from <group_manager.py> which creates all the ui functions"""

        self._setup_main_window(MainWindow)
        self._setup_central_widget(MainWindow)
        
        self._setup_information_settings()
        self._setup_universe_settings()

        self.group_manager = GroupManager(
            # UI groups

            particle_ui = self.particle_ui,
            random_particle_ui = self.random_particle_ui,
            gravity_ui = self.gravity_ui,
            boundary_ui = self.boundary_ui,
            visual_settings_ui = self.visual_settings_ui,
            universe_settings_ui = self.universe_settings_ui,
            saved_universes_ui = self.saved_universes_ui,
            save_universe_settings_ui = self.save_universe_settings_ui,

            # Arbitrary Values

            centralwidget = self.centralwidget,
            universe_verticalLayout = self.universe_verticalLayout,
            universe_vlayout_widget = self.universe_vlayout_widget,
            universe_matter_frame = self.universe_matter_frame,
            control_information_frame = self.control_information_frame,
            add_boundary_button = self.add_boundary_button

        )

        self._setup_opengl_settings()
        
        self.start_simulation_button.clicked.connect(self.start_simulation)
        self.stop_simulation_button.clicked.connect(self.stop_simulation)
        self.reset_simulation_button.clicked.connect(self.reset_simulation)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_simulation(self):
        """
        Starts the timer which updates and starts the simulation.
        Also starts 2D or 3D graphs updates
        """
        self.openGLWidget.timer_simulation.start(16)
        try:
            if self.particle_ui.graph_settings_ui.dimension == "2D":
                self.particle_ui.graph_display_2d_ui.start_graph()
            elif self.particle_ui.graph_settings_ui.dimension == "3D":
                self.particle_ui.graph_display_3d_ui.start_graph()
        except:
            pass

    def stop_simulation(self):
        """
        Stops the timer which stops the simulation.
        Also stops 2D or 3D graphs updates
        """
        self.openGLWidget.timer_simulation.stop()
        if self.particle_ui.graph_settings_ui.dimension == "2D":
            self.particle_ui.graph_display_2d_ui.stop_graph()
        elif self.particle_ui.graph_settings_ui.dimension == "3D":
            self.particle_ui.graph_display_3d_ui.stop_graph()

    def reset_simulation(self):
        """
        Resets the simulation back to its original state.
        Also resets the 2D or 3D graphs back to its original state
        """
        self.openGLWidget.reset_simulation()
        try:
            if self.particle_ui.graph_settings_ui.dimension == "2D":
                self.particle_ui.graph_display_2d_ui.reset_graph()
            elif self.particle_ui.graph_settings_ui.dimension == "3D":
                self.particle_ui.graph_display_3d_ui.reset_graph()
        except:
            pass

    def _setup_main_window(self, MainWindow):
        """Configure Main Window Settings"""

        MainWindow.setObjectName("Hello Particle")
        MainWindow.showFullScreen()

        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        MainWindow.setFont(font)

    def _setup_central_widget(self, MainWindow):
        """Configure Central Widget Settings"""

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

    def _setup_universe_settings(self):
        """Sets up the "Add Matter" and "Universe" frames on the lower left side of the screen"""

        self.universe_matter_frame = create.create_frame(
            parent = self.centralwidget,
            geometry = QtCore.QRect(9, 543, 951, 531),
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "universe_matter_frame",
        )
        self.universe_matter_grid = create.create_hlayout(
            parent = self.universe_matter_frame,
            objname = "universe_matter_grid"
        )
        self.add_matter_frame = create.create_frame(
            parent = self.universe_matter_frame,
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "add_matter_frame"
        )
        self.add_matter_group = create.create_group_box(
            parent = self.add_matter_frame,
            geometry = QtCore.QRect(10, 10, 441, 491),
            font_size = 20,
            objname = "add_matter_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Add Matter"
        )
        
        self.add_particle_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(30, 50, 150, 150),
            objname = "add_particle_button",
            font_size = 18,
            text = ""
        )
        self.random_particle_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(30, 50, 40, 40),
            objname = "random_particle_button",
            font_size = 18,
            text = ""
        )
        self.add_gravity_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(260, 50, 150, 150),
            objname = "add_gravity_button",
            font_size = 18,
            text = ""
        )
        self.add_boundary_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(30, 220, 150, 150),
            objname = "add_boundary_button",
            font_size = 18,
            text = ""
        )
        self.visual_settings_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(260, 220, 150, 150),
            objname = "visual_settings_button",
            font_size = 18,
            text = ""
        )
        self.quit_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(30, 410, 71, 61),
            objname = "quit_button",
            font_size = 18,
            text = ""
        )
        self.saved_universes_button = create.create_button(
            parent = self.add_matter_group,
            geometry = QtCore.QRect(130, 410, 71, 61),
            objname = "saved_universes_button",
            font_size = 18,
            text = ""
        )
        
        scaler = ResolutionScaler()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        
        particle_icon_path = os.path.join(base_dir, "pictures", "particle.png").replace('\\','/')
        random_particle_icon_path = os.path.join(base_dir, "pictures", "random.png").replace('\\','/')
        gravity_icon_path = os.path.join(base_dir, "pictures", "gravity.png").replace('\\','/')
        boundary_icon_path = os.path.join(base_dir, "pictures", "boundary.png").replace('\\','/')
        visual_icon_path = os.path.join(base_dir, "pictures", "visual.png").replace('\\','/')
        save_icon_path = os.path.join(base_dir, "pictures", "save.png").replace('\\','/')
        exit_icon_path = os.path.join(base_dir, "pictures", "exit.png").replace('\\','/')

        if not os.path.exists(particle_icon_path):
            print("Icon file does not exist!")
        else:
            self.add_particle_button.setIcon(QtGui.QIcon(particle_icon_path))
            self.add_particle_button.setIconSize(QtCore.QSize(*scaler.scale_size(150, 150)))

            self.random_particle_button.setIcon(QtGui.QIcon(random_particle_icon_path))
            self.random_particle_button.setIconSize(QtCore.QSize(*scaler.scale_size(30, 30)))

            self.add_gravity_button.setIcon(QtGui.QIcon(gravity_icon_path))
            self.add_gravity_button.setIconSize(QtCore.QSize(*scaler.scale_size(150,150)))

            self.add_boundary_button.setIcon(QtGui.QIcon(boundary_icon_path))
            self.add_boundary_button.setIconSize(QtCore.QSize(*scaler.scale_size(150,150)))

            self.visual_settings_button.setIcon(QtGui.QIcon(visual_icon_path))
            self.visual_settings_button.setIconSize(QtCore.QSize(*scaler.scale_size(150,150)))

            self.saved_universes_button.setIcon(QtGui.QIcon(save_icon_path))
            self.saved_universes_button.setIconSize(QtCore.QSize(*scaler.scale_size(35,35)))

            self.quit_button.setIcon(QtGui.QIcon(exit_icon_path))
            self.quit_button.setIconSize(QtCore.QSize(*scaler.scale_size(40,40)))

        self.universe_matter_grid.addWidget(self.add_matter_frame)


        self.universe_frame = create.create_frame(
            parent = self.universe_matter_frame,
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "universe_frame"
        )
        self.universe_group = create.create_group_box(
            parent = self.universe_frame,
            geometry = QtCore.QRect(10, 10, 441, 491),
            font_size = 20,
            objname = "universe_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Universe"
        )
        self.save_universe_button = create.create_button(
            parent = self.universe_frame,
            geometry = QtCore.QRect(10, 10, 111, 31),
            font_size = 16,
            text = "Save",
            objname = "save_universe_button"
        )
        self.clear_universe_button = create.create_button(
            parent = self.universe_frame,
            geometry = QtCore.QRect(340, 10, 111, 31),
            font_size = 16,
            text = "Clear",
            objname = "clear_universe_button"
        )

        self.universe_scrollarea = create.create_scroll(
            parent = self.universe_group,
            geometry = QtCore.QRect(10, 40, 420, 400),
            resizable = True,
            objname = "universe_scrollarea"
        )
        self.universe_vlayout_widget = create.create_widget(
            parent = self.universe_scrollarea,
            objname = "universe_vlayout_widget"
        )
        self.universe_verticalLayout = create.create_vlayout(
            parent = self.universe_vlayout_widget,
            objname = "universe_verticalLayout",
            alignment = True
        )

        self.universe_scrollarea.setWidget(self.universe_vlayout_widget)
        self.universe_scrollarea.setWidgetResizable(True)

        self.universe_settings_commandlink = create.create_command_link(
            parent = self.universe_group,
            geometry = QtCore.QRect(70, 440, 300, 40),
            font_size = 18,
            objname = "universe_settings_commandlink",
            text = "Universe Settings"
        )
        universe_icon_path = os.path.join(base_dir, "pictures", "universe.png").replace('\\','/')
        if os.path.exists(universe_icon_path):
            self.universe_settings_commandlink.setIcon(QtGui.QIcon(universe_icon_path))
            self.universe_settings_commandlink.setIconSize(QtCore.QSize(*scaler.scale_size(30, 30)))
        
        
        self.universe_matter_grid.addWidget(self.universe_frame)
        
        self.add_particle_button.clicked.connect(lambda: self.group_manager.particle_settings_group())
        self.random_particle_button.clicked.connect(lambda: self.group_manager.random_particle_command_settings_function())
        self.add_gravity_button.clicked.connect(lambda: self.group_manager.gravity_settings_group())
        self.add_boundary_button.clicked.connect(lambda: self.group_manager.boundary_settings_group())
        self.visual_settings_button.clicked.connect(lambda: self.group_manager.visual_settings_function())
        self.universe_settings_commandlink.clicked.connect(lambda: self.group_manager.universe_settings_function())

        self.saved_universes_button.clicked.connect(lambda: self.group_manager.saved_universes_function())
        self.save_universe_button.clicked.connect(lambda: self.group_manager.save_universe_settings_function())
        self.clear_universe_button.clicked.connect(lambda: self.group_manager.clear_universe_function())
        self.quit_button.clicked.connect(lambda: QtWidgets.QApplication.quit())
    
    def _setup_opengl_settings(self):
        """Sets up the OpenGL Widget present on the top right area of the screen"""

        self.openGLWidget = OpenGLWidget(
            parent = self.centralwidget,
            fullscreen_signal = self.fullscreen_signal,
            start_simulation = self.start_simulation,
            stop_simulation = self.stop_simulation,
            reset_simulation = self.reset_simulation,
            particle_variables = self.particle_ui.particle_variables,
            particle_classes = self.particle_ui.particle_classes,
            gravity_classes = self.gravity_ui.gravity_classes,
            boundary = self.boundary_ui.boundary
        )
        self.openGLWidget.setEnabled(True)
        geometry = create.create_openGL_geometry(QtCore.QRect(960, 0, 960, 540))
        self.openGLWidget.setGeometry(geometry)
        self.openGLWidget.setObjectName("openGLWidget")

    def _setup_information_settings(self):
        """Sets up the start/stop/reset buttons present on the lower right side of the screen"""

        self.control_information_frame = create.create_frame(
            parent = self.centralwidget,
            geometry = QtCore.QRect(963, 543, 948, 533),
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "control_information_frame"
        )
        self.seperation_line = create.create_line(
            parent = self.control_information_frame,
            fshape = QtWidgets.QFrame.HLine,
            fshadow = QtWidgets.QFrame.Plain,
            width = 2,
            objname = "seperation_line",
            geometry = QtCore.QRect(10, 70, 931, 20)
        )        
        self.simulation_control_frame = create.create_frame(
            parent = self.control_information_frame,
            geometry = QtCore.QRect(10, 9, 931, 71),
            fshape = QtWidgets.QFrame.StyledPanel,
            fshadow = QtWidgets.QFrame.Raised,
            objname = "simulation_control_frame"
        )
        self.control_hlayout = create.create_hlayout(
            parent = self.simulation_control_frame,
            objname = "control_hlayout"
        )
        
        self.start_simulation_button = create.create_button(
            parent = self.simulation_control_frame,
            font_size = 20,
            text = "Start Simulation",
            objname = "start_simulation_button"
        )
        self.stop_simulation_button = create.create_button(
            parent = self.simulation_control_frame,
            font_size = 20,
            text = "Stop Simulation",
            objname = "stop_simulation_button"
        )
        self.reset_simulation_button = create.create_button(
            parent = self.simulation_control_frame,
            font_size = 20,
            text = "Reset Simulation",
            objname = "reset_simulation_button"
        )

        self.control_hlayout.addWidget(self.start_simulation_button)
        self.control_hlayout.addWidget(self.stop_simulation_button)
        self.control_hlayout.addWidget(self.reset_simulation_button)
        
    def fullscreen_signal(self):
        """Key press to enlarge the OpenGL Widget"""

        if self.binary_indicator == 0:
            geometry = create.create_openGL_geometry(QtCore.QRect(0, 0, 1920, 1080))
            self.openGLWidget.setGeometry(geometry)
            self.openGLWidget.raise_()
            self.binary_indicator = 1
        else:
            geometry = create.create_openGL_geometry(QtCore.QRect(960, 0, 960, 540))
            self.openGLWidget.setGeometry(geometry)
            self.binary_indicator = 0