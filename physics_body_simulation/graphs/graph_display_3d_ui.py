import utils.create_uicomponents as create
from graphs.graph_elements_3d_ui import Group3D

from PyQt5 import QtCore, QtWidgets

class GraphDisplay3D_UI(QtCore.QObject):
    def __init__(self, go_back_function):
        super().__init__()
        self.go_back_function = go_back_function
        self.displayed_checkboxes = {}
        self.graph1 = None
        self.graph2 = None
        self.graph3 = None
        self.graph4 = None

        self.number_of_plots = 0

    def setup_graph_display_3d(self, centralwidget, particle_values, number_of_plots):
        """Displays the main frame of the entire bottom left region"""

        self.number_of_plots = number_of_plots
        self.displayed_checkboxes = {
            "Time X" : ['x', True, None]
        }
        if particle_values:
            for list in particle_values:
                for key, value in list.items():
                    if value['axis'] == "y":
                        self.displayed_checkboxes[key] = [value['axis'], False, value['value'], value['color']]
                    else:
                        self.displayed_checkboxes[key] = [value['axis'], False, value['value']]

        self.graph_settings_3d_frame = create.create_frame(
            parent = centralwidget,
            geometry = QtCore.QRect(9, 540, 948, 540),
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "graph_settings_3d_frame"
        )

        self.graph_settings_3d_group = create.create_group_box(
            parent = self.graph_settings_3d_frame,
            geometry = QtCore.QRect(9, 9, 932, 481),
            font_size = 18,
            objname = "graph_settings_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Graph Settings (3D)"
        )
        self.graph_settings_scrollarea = create.create_scroll(
            parent = self.graph_settings_3d_group,
            geometry = QtCore.QRect(0, 30, 932, 451),
            objname = "graph_settings_scrollarea",
            resizable = True
        )
        self.graph_settings_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graph_settings_scroll_widget = create.create_widget(
            objname = "graph_settings_scroll_widget",
            geometry = QtCore.QRect(0, 0, 930, 449)
        )

        self.graph_display_3d_frame = create.create_frame(
            parent = centralwidget,
            geometry = QtCore.QRect(9, 9, 948, 520),
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            objname = "graph_display_3d_frame"
        )
        self.graph_display_scrollarea = create.create_scroll(
            parent = self.graph_display_3d_frame,
            geometry = QtCore.QRect(11, 2, 928, 514),
            objname = "graph_display_scrollarea",
            resizable = True
        )
        self.graph_display_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graph_display_scroll_widget = create.create_widget(
            objname = "graph_display_scroll_widget",
            geometry = QtCore.QRect(0, 0, 926, 515)
        )

        self.graph_display_layout = create.create_vlayout(
            self.graph_display_scroll_widget,
            objname = "graph_display_layout"
        )
        self.graph_group_layout = create.create_vlayout(
            self.graph_settings_scroll_widget,
            objname = "graph_group_layout"
        )
        
        if number_of_plots >= 1:
            self.graph1 = Group3D(self.displayed_checkboxes, 1)
            self.graph1.create_group_elements(self.graph_settings_scroll_widget, self.graph_display_layout)
            self.graph_group_layout.addWidget(self.graph1.graph_group)
        if number_of_plots >= 2:
            self.graph2 = Group3D(self.displayed_checkboxes, 2)
            self.graph2.create_group_elements(self.graph_settings_scroll_widget, self.graph_display_layout)
            self.graph_group_layout.addWidget(self.graph2.graph_group)
        if number_of_plots >= 3:
            self.graph3 = Group3D(self.displayed_checkboxes, 3)
            self.graph3.create_group_elements(self.graph_settings_scroll_widget, self.graph_display_layout)
            self.graph_group_layout.addWidget(self.graph3.graph_group)
        if number_of_plots == 4:
            self.graph4 = Group3D(self.displayed_checkboxes, 4)
            self.graph4.create_group_elements(self.graph_settings_scroll_widget, self.graph_display_layout)
            self.graph_group_layout.addWidget(self.graph4.graph_group)

        self.graph_settings_scrollarea.setWidget(self.graph_settings_scroll_widget)
        self.graph_display_scrollarea.setWidget(self.graph_display_scroll_widget)

        # Save and Return buttons

        self.save_graph_button = create.create_button(
            parent = self.graph_settings_3d_frame,
            font_size = 16,
            text = "Save",
            geometry = QtCore.QRect(8, 490, 151, 41),
            objname = "save_graph_button"
        )
        self.go_back_button = create.create_button(
            parent = self.graph_settings_3d_frame,
            font_size = 16,
            text = "Go Back",
            geometry = QtCore.QRect(158, 490, 141, 41),
            objname = "go_back_button"
        )

        self.save_graph_button.clicked.connect(self.update_graph)
        self.go_back_button.clicked.connect(self.go_back_function)

        self.graph_display_scrollarea.installEventFilter(self)
        self.graph_display_scrollarea.wheelEvent = self.handle_wheel_event

    def start_graph(self):
        """Starts the graphing process"""

        self.save_graph_button.setEnabled(False)
        if self.number_of_plots >= 1:
            self.graph1.start_simulation()
        if self.number_of_plots >= 2:
            self.graph2.start_simulation()
        if self.number_of_plots >= 3:
            self.graph3.start_simulation()
        if self.number_of_plots == 4:
            self.graph4.start_simulation()

    def stop_graph(self):
        """Stops the graphs"""

        if self.number_of_plots >= 1:
            self.graph1.stop_simulation()
        if self.number_of_plots >= 2:
            self.graph2.stop_simulation()
        if self.number_of_plots >= 3:
            self.graph3.stop_simulation()
        if self.number_of_plots == 4:
            self.graph4.stop_simulation()

    def reset_graph(self):
        """Resets the plots present in the graph"""

        self.save_graph_button.setEnabled(True)
        if self.number_of_plots >= 1:
            self.graph1.reset_simulation()
        if self.number_of_plots >= 2:
            self.graph2.reset_simulation()
        if self.number_of_plots >= 3:
            self.graph3.reset_simulation()
        if self.number_of_plots == 4:
            self.graph4.reset_simulation()
    
    def remove_graph(self):
        """Removes the graphs to reduce computation"""
        
        if self.number_of_plots >= 1:
            self.graph1.remove_simulation()
        if self.number_of_plots >= 2:
            self.graph2.remove_simulation()
        if self.number_of_plots >= 3:
            self.graph3.remove_simulation()
        if self.number_of_plots == 4:
            self.graph4.remove_simulation()

    def update_graph(self):
        """Updates the graph with selected information"""

        if self.number_of_plots >= 1:
            self.graph1.save_settings()
        if self.number_of_plots >= 2:
            self.graph2.save_settings()
        if self.number_of_plots >= 3:
            self.graph3.save_settings()
        if self.number_of_plots == 4:
            self.graph4.save_settings()

    def handle_wheel_event(self, event):
        """Handle wheel events here and only process zooming (disable scrolling)"""

        if event.angleDelta().y() != 0:
            event.ignore()