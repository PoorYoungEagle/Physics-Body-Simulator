import utils.create_uicomponents as create

from PyQt5 import QtCore, QtWidgets

class GraphSettings_UI:
    def __init__(self, reset_variables, show_graph_display):
        self.reset_variables = reset_variables
        self.show_graph_display = show_graph_display
        self.number_of_plots = 1
        self.dimension = "2D"

    def _set_number_of_plots(self, plot):
        self.number_of_plots = int(plot)
        self.number_of_plots_button.setText(plot)

    def _show_plots_dialog(self):
        menu = QtWidgets.QMenu(self.number_of_plots_button)

        plot_1 = menu.addAction("1")
        plot_2 = menu.addAction("2") 
        plot_3 = menu.addAction("3")
        plot_4 = menu.addAction("4")

        plot_1.triggered.connect(lambda: self._set_number_of_plots("1"))
        plot_2.triggered.connect(lambda: self._set_number_of_plots("2"))
        plot_3.triggered.connect(lambda: self._set_number_of_plots("3"))
        plot_4.triggered.connect(lambda: self._set_number_of_plots("4"))

        menu.exec_(self.number_of_plots_button.mapToGlobal(self.number_of_plots_button.rect().bottomLeft()))    

    def _show_dimension_dialog(self):
        menu = QtWidgets.QMenu(self.dimension_button)

        two_dimension = menu.addAction("2D")
        three_dimension = menu.addAction("3D")

        two_dimension.triggered.connect(lambda: self._set_dimension("2D"))
        three_dimension.triggered.connect(lambda: self._set_dimension("3D"))

        menu.exec_(self.dimension_button.mapToGlobal(self.dimension_button.rect().bottomLeft()))    

    def _set_dimension(self, dimension):
        self.dimension = dimension
        self.dimension_button.setText(dimension)

    def setup_graphing_settings(self, control_information_frame):
        """Configure Graph Settings"""
            
        self.graph_seperation_line = create.create_line(
        parent = control_information_frame,
        geometry = QtCore.QRect(10, 350, 931, 20),
        fshadow = QtWidgets.QFrame.Plain,
        width = 2,
        fshape = QtWidgets.QFrame.HLine,
        objname = "graph_seperation_line"
        )
        self.graph_settings_group = create.create_group_box(
            parent = control_information_frame,
            geometry = QtCore.QRect(0, 360, 950, 170),
            font_size = 18,
            objname = "graph_settings_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Graph Settings"
        )

        self.plots_dimension_frame = create.create_frame(
            parent = self.graph_settings_group,
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            geometry = QtCore.QRect(0, 20, 280, 100),
            objname = "plots_dimension_frame"
        )
        self.plots_dimension_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plots_dimension_grid = create.create_grid_layout(
            parent = self.plots_dimension_frame,
            objname = "plots_dimension_grid"
        )

        self.number_of_plots_label = create.create_name_label(
            parent = self.plots_dimension_frame,
            font_size = 16,
            text = "Number of Plots: ",
            objname = "number_of_plots_label"
        )
        self.dimension_label = create.create_name_label(
            parent = self.plots_dimension_frame,
            font_size = 16,
            text = "Dimension: ",
            objname = "dimension_label"
        )
        self.number_of_plots_button = create.create_button(
            parent = self.plots_dimension_frame,
            font_size = 16,
            text = "1",
            objname = "number_of_plots_button"
        )
        self.dimension_button = create.create_button(
            parent = self.plots_dimension_frame,
            font_size = 16,
            text = "2D",
            objname = "dimension_button"
        )

        self.plots_dimension_grid.addWidget(self.number_of_plots_label, 0, 0, 1, 1)
        self.plots_dimension_grid.addWidget(self.number_of_plots_button, 0, 1, 1, 1)
        self.plots_dimension_grid.addWidget(self.dimension_label, 1, 0, 1, 1)
        self.plots_dimension_grid.addWidget(self.dimension_button, 1, 1, 1, 1)

        self.number_of_plots_button.clicked.connect(self._show_plots_dialog)
        self.dimension_button.clicked.connect(self._show_dimension_dialog)

        self.axis_frame = create.create_frame(
            parent = self.graph_settings_group,
            fshape = QtWidgets.QFrame.WinPanel,
            fshadow = QtWidgets.QFrame.Plain,
            geometry = QtCore.QRect(280, 20, 670, 160),
            objname = "plots_dimension_frame"
        )
        self.axis_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.axis_grid = create.create_hlayout(
            parent = self.axis_frame,
            objname = "axis_grid"
        )

        self.x_axis_groupbox = create.create_group_box(
            parent = self.axis_frame,
            font_size = 16,
            objname = "x_axis_groupbox",
            title = "X Axis:",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
        )
        self.x_axis_scroll = create.create_scroll(
            parent = self.x_axis_groupbox,
            objname = "x_axis_scroll",
            geometry = QtCore.QRect(0, 30, 213, 107),
            resizable = True
        )
        self.x_axis_scrollcontents = create.create_widget(
            geometry = QtCore.QRect(0, 0, 211, 105),
            objname = "x_axis_scrollcontents"
        )
        self.x_axis_vlayout = create.create_grid_layout(
            parent = self.x_axis_scrollcontents,
            objname = "x_axis_vlayout",
            alignment = True
        )
        self.x_axis_scroll.setWidget(self.x_axis_scrollcontents)

        self.y_axis_groupbox = create.create_group_box(
            parent = self.axis_frame,
            font_size = 16,
            objname = "y_axis_groupbox",
            title = "Y Axis:",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
        )
        self.y_axis_scroll = create.create_scroll(
            parent = self.y_axis_groupbox,
            objname = "y_axis_scroll",
            geometry = QtCore.QRect(0, 30, 213, 107),
            resizable = True
        )
        self.y_axis_scrollcontents = create.create_widget(
            geometry = QtCore.QRect(0, 0, 211, 105),
            objname = "y_axis_scrollcontents"
        )
        self.y_axis_vlayout = create.create_grid_layout(
            parent = self.y_axis_scrollcontents,
            objname = "y_axis_vlayout",
            alignment = True
        )
        self.y_axis_scroll.setWidget(self.y_axis_scrollcontents)

        self.z_axis_groupbox = create.create_group_box(
            parent = self.axis_frame,
            font_size = 16,
            objname = "z_axis_groupbox",
            title = "Z Axis:",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
        )
        self.z_axis_scroll = create.create_scroll(
            parent = self.z_axis_groupbox,
            objname = "z_axis_scroll",
            geometry = QtCore.QRect(0, 30, 213, 107),
            resizable = True
        )
        self.z_axis_scrollcontents = create.create_widget(
            geometry = QtCore.QRect(0, 0, 211, 105),
            objname = "z_axis_scrollcontents"
        )
        self.z_axis_vlayout = create.create_grid_layout(
            parent = self.z_axis_scrollcontents,
            objname = "z_axis_vlayout",
            alignment = True
        )
        self.z_axis_scroll.setWidget(self.z_axis_scrollcontents)

        self.axis_grid.addWidget(self.x_axis_groupbox)
        self.axis_grid.addWidget(self.y_axis_groupbox)
        self.axis_grid.addWidget(self.z_axis_groupbox)

        self.create_graph_button = create.create_button(
            parent = self.graph_settings_group,
            objname = "create_graph_button",
            font_size = 16,
            geometry = QtCore.QRect(5, 120, 156, 40),
            text = "Create Graph"
        )
        self.reset_graph_button = create.create_button(
            parent = self.graph_settings_group,
            objname = "reset_graph_button",
            font_size = 16,
            geometry = QtCore.QRect(160, 120, 121, 40),
            text = "Reset"
        )

        self.create_graph_button.clicked.connect(lambda: self.show_graph_display(self.number_of_plots, self.dimension))
        self.reset_graph_button.clicked.connect(self.reset_variables)