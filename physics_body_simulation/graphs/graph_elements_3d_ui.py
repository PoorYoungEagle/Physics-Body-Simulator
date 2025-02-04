import utils.create_uicomponents as create
from graphs.graph_plot_3d_ui import Plot3D

from PyQt5 import QtCore, QtGui, QtWidgets

class Group3D:
    def __init__(self, displayed_checkboxes, index):
        self.displayed_checkboxes = displayed_checkboxes.copy()
        self.index = index
        self.plot_3d = Plot3D(
            index = self.index
        )

        self.type = "Line Graph"
        self.current_background_color = QtGui.QColor(1, 10, 38)
        self.current_grid_lines_color = QtGui.QColor(255, 255, 255)

        self.timer_graph = QtCore.QTimer()
        self.timer_interaction = QtCore.QTimer()

        # self.displayed_checkboxes[key] = [value['axis'], False, value['value'], value['color']]
        self.displayed_elements = {} # [axis, checkbox, line button, scatter button]
        self.y_limit = []
        self.time_step = 500

    def _checkbox_limits(self, checkbox, name):
        """
        Updates whether a value is checked
        The Y axis can contain upto a maximum of four values and will block out any new values from being checked
        """

        if checkbox and (self.displayed_checkboxes[name][0] == "x" or self.displayed_checkboxes[name][0] == "z"):
            self.displayed_checkboxes[name] = [self.displayed_checkboxes[name][0], True, self.displayed_checkboxes[name][2]]
        elif self.displayed_checkboxes[name][0] == "x"  or self.displayed_checkboxes[name][0] == "z":
            self.displayed_checkboxes[name] = [self.displayed_checkboxes[name][0], False, self.displayed_checkboxes[name][2]]

        if checkbox and self.displayed_checkboxes[name][0] == "y":
            checked_boxes = [checkbox for checkbox in self.y_limit if checkbox.isChecked()]
            self.displayed_checkboxes[name] = [self.displayed_checkboxes[name][0], True, *self.displayed_checkboxes[name][2:6]]
            if len(checked_boxes) == 4:
                for key, value in self.displayed_elements.items():
                    if value[0] == "y":
                        value[1].setEnabled(False)
                for value in checked_boxes:
                    value.setEnabled(True)                
        elif self.displayed_checkboxes[name][0] == "y":
            for key, value in self.displayed_elements.items():
                self.displayed_checkboxes[name] = [self.displayed_checkboxes[name][0], False, *self.displayed_checkboxes[name][2:6]]
                value[1].setEnabled(True)

    def _show_type_dialog(self):
        menu = QtWidgets.QMenu(self.type_button)

        type_line = menu.addAction("Line Graph")
        type_scatter = menu.addAction("Scatter Graph")

        type_line.triggered.connect(lambda: self._set_type("Line Graph"))
        type_scatter.triggered.connect(lambda: self._set_type("Scatter Graph"))

        menu.exec_(self.type_button.mapToGlobal(self.type_button.rect().bottomLeft()))    

    def _set_type(self, type):
        self.type = type
        self.type_button.setText(type)

    def _show_background_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_background_color = color
            self.background_color_button.setStyleSheet(f"background-color: {color.name()}")

    def _show_grid_lines_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.current_grid_lines_color = color
            self.show_grid_lines_color_button.setStyleSheet(f"background-color: {color.name()}")

    def create_group_elements(self, graph_settings_scroll_widget, graph_display_layout):
        """Configure Main Group Graphing Elements"""

        self.graph_group = create.create_group_box(
            parent = graph_settings_scroll_widget,
            geometry = QtCore.QRect(10, 10, 911, 291),
            font_size = 18,
            objname = "graph_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = f"Graph {self.index}"
        )
        self.graph_group.setFixedSize(QtCore.QSize(911, 301))
        
        self.x_axis_group = create.create_group_box(
            parent = self.graph_group,
            geometry = QtCore.QRect(10, 70, 170, 220),
            font_size = 16,
            objname = "graph_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "X Axis:"
        )
        self.x_axis_scrollarea = create.create_scroll(
            parent = self.x_axis_group,
            objname = "x_axis_scrollarea",
            geometry = QtCore.QRect(0, 30, 170, 190),
            resizable = True
        )
        self.x_axis_scroll_widget = create.create_widget(
            parent = self.x_axis_group,
            objname = "x_axis_scroll_widget",
            geometry = QtCore.QRect(0, 0, 170, 190)
        )
        self.x_axis_grid = create.create_grid_layout(
            parent = self.x_axis_scroll_widget,
            objname = "x_axis_grid"
        )

        self.x_buttongroup = QtWidgets.QButtonGroup()
        self.x_buttongroup.setExclusive(True)

        self.y_axis_group = create.create_group_box(
            parent = self.graph_group,
            geometry = QtCore.QRect(190, 70, 190, 220),
            font_size = 16,
            objname = "graph_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Y Axis:"
        )
        self.y_axis_scrollarea = create.create_scroll(
            parent = self.y_axis_group,
            objname = "y_axis_scrollarea",
            geometry = QtCore.QRect(0, 30, 190, 190),
            resizable = True
        )
        self.y_axis_scroll_widget = create.create_widget(
            parent = self.y_axis_group,
            objname = "y_axis_scroll_widget",
            geometry = QtCore.QRect(0, 0, 190, 190)
        )
        self.y_axis_grid = create.create_grid_layout(
            parent = self.y_axis_scroll_widget,
            objname = "y_axis_grid"
        )

        self.z_axis_group = create.create_group_box(
            parent = self.graph_group,
            geometry = QtCore.QRect(390, 70, 170, 220),
            font_size = 16,
            objname = "graph_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Z Axis:"
        )
        self.z_axis_scrollarea = create.create_scroll(
            parent = self.z_axis_group,
            objname = "z_axis_scrollarea",
            geometry = QtCore.QRect(0, 30, 170, 190),
            resizable = True
        )
        self.z_axis_scroll_widget = create.create_widget(
            parent = self.z_axis_group,
            objname = "z_axis_scroll_widget",
            geometry = QtCore.QRect(0, 0, 170, 190)
        )
        self.z_axis_grid = create.create_grid_layout(
            parent = self.z_axis_scroll_widget,
            objname = "z_axis_grid"
        )

        self.z_buttongroup = QtWidgets.QButtonGroup()
        self.z_buttongroup.setExclusive(True)

        self.x_axis_scrollarea.setWidget(self.x_axis_scroll_widget)
        self.y_axis_scrollarea.setWidget(self.y_axis_scroll_widget)
        self.z_axis_scrollarea.setWidget(self.z_axis_scroll_widget)

        self.settings_group = create.create_group_box(
            parent = self.graph_group,
            geometry = QtCore.QRect(570, 50, 340, 240),
            font_size = 16,
            objname = "settings_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Settings:"
        )
        self.settings_grid = create.create_grid_layout(
            parent = self.settings_group,
            objname = "settings_grid"
        )

        self.type_label = create.create_name_label(
            parent = self.settings_group,
            font_size = 14,
            objname = "type_label",
            text = "Type : "
        )
        self.type_button = create.create_button(
            parent = self.settings_group,
            font_size = 14,
            objname = "type_button",
            text = "Line Graph"
        )
        self.time_step_label = create.create_name_label(
            parent = self.settings_group,
            font_size = 14,
            objname = "time_step_label",
            text = "Time Step :"
        )
        self.time_step_spinbox = create.create_double_spinbox(
            parent = self.settings_group,
            font_size = 14,
            objname = "time_step_spinbox",
            max = 1000.0,
            min = 0.01,
            step = 0.1,
            value = 0.5
        )
        self.background_color_label = create.create_name_label(
            parent = self.settings_group,
            font_size = 14,
            objname = "background_color_label",
            text = "Background Color : "
        )
        self.background_color_button = create.create_button(
            parent = self.settings_group,
            font_size = 14,
            objname = "background_color_button",
            text = ""
        )
        self.show_grid_lines_checkbox = create.create_checkbox(
            parent = self.settings_group,
            font_size = 14,
            layout = QtCore.Qt.LeftToRight,
            objname = "show_grid_lines_checkbox",
            text = "Show Grid Lines : "
        )
        self.show_grid_lines_color_button = create.create_button(
            parent = self.settings_group,
            font_size = 14,
            objname = "show_grid_lines_color_button",
            text = ""
        )
        self.show_legend_checkbox = create.create_checkbox(
            parent = self.settings_group,
            font_size = 14,
            layout = QtCore.Qt.LeftToRight,
            objname = "show_legend_checkbox",
            text = "Show Legend"
        )

        self.settings_grid.addWidget(self.type_label, 1, 0, 1, 1)
        self.settings_grid.addWidget(self.type_button, 1, 1, 1, 1)
        self.settings_grid.addWidget(self.time_step_label, 2, 0, 1, 1)
        self.settings_grid.addWidget(self.time_step_spinbox, 2, 1, 1, 1)
        self.settings_grid.addWidget(self.background_color_label, 3, 0, 1, 1)
        self.settings_grid.addWidget(self.background_color_button, 3, 1, 1, 1)
        self.settings_grid.addWidget(self.show_grid_lines_checkbox, 4, 0, 1, 1)
        self.settings_grid.addWidget(self.show_grid_lines_color_button, 4, 1, 1, 1)
        self.settings_grid.addWidget(self.show_legend_checkbox, 5, 0, 1, 1)

        self.type_button.clicked.connect(self._show_type_dialog)
        self.background_color_button.clicked.connect(self._show_background_color_dialog)
        self.background_color_button.setStyleSheet("background-color: rgb(1, 10, 38)")
        self.show_grid_lines_color_button.clicked.connect(self._show_grid_lines_color_dialog)
        self.show_grid_lines_color_button.setStyleSheet("background-color: white")

        self.show_grid_lines_checkbox.setChecked(True)

        self.settings_group.setLayout(self.settings_grid)

        self.graph_title_label = create.create_name_label(
            parent = self.graph_group,
            geometry = QtCore.QRect(10, 30, 131, 31),
            font_size = 16,
            objname = "graph_title_label",
            text = "Graph Title : "
        )
        self.graph_title_lineedit = create.create_line_edit(
            parent = self.graph_group,
            geometry = QtCore.QRect(140, 34, 130, 25),
            font_size = 16,
            objname = "graph_title_lineedit"
        )

        self.create_labels()

        graph_display_layout.addWidget(self.plot_3d.container)

    def create_labels(self):
        """Creates each label for X, Y and Z axis"""

        for key, value in self.displayed_checkboxes.items():
            checkbox = create.create_checkbox(
                text = "",
                layout = QtCore.Qt.LeftToRight,
                objname = "checkbox",
                font_size = 12
            )
            checkbox.setText(key)
            checkbox.toggled.connect(lambda state, key=key: self._checkbox_limits(state, key))
            if value[0] == "x":
                row_position = self.x_axis_grid.rowCount()
                self.x_axis_grid.addWidget(checkbox, row_position, 0)
                self.displayed_elements[key] = [value[0], checkbox]
                self.x_buttongroup.addButton(checkbox)
                if key == "Time X":
                    checkbox.setChecked(True)
            elif value[0] == "y":
                checkbox.setStyleSheet(f"color: {value[3].name()};")
                row_position = self.y_axis_grid.rowCount()
                self.y_axis_grid.addWidget(checkbox, row_position, 0)
                self.displayed_elements[key] = [value[0], checkbox]
                self.y_limit.append(checkbox)
            elif value[0] == "z":
                row_position = self.z_axis_grid.rowCount()
                self.z_axis_grid.addWidget(checkbox, row_position, 0)
                self.displayed_elements[key] = [value[0], checkbox]
                self.z_buttongroup.addButton(checkbox)

    def save_settings(self):
        """Updates the constants for the graph"""
        
        # self.displayed_checkboxes[key] = [value['axis'], False, value['value'], "Solid", "Circle", value['color']]
        x_value = []
        y_values = []
        z_value = []
        for key, value in self.displayed_checkboxes.items():
            if value[1] and value[0] == "y":
                y_values.append([key, value])  # Just store the key and value directly
            elif value[1] and value[0] == "x":
                x_value.append([key, value])
            elif value[1] and value[0] == "z":
                z_value.append([key, value])

        type = self.type
        background_color_input = self.current_background_color.name()
        grid_line_check = self.show_grid_lines_checkbox.isChecked()
        grid_line_color_input = self.current_grid_lines_color
        legend_check = self.show_legend_checkbox.isChecked()

        graph_title = self.graph_title_lineedit.text() if self.graph_title_lineedit.text() else f"Graph {self.index}"
        
        self.plot_3d.update(
            type = type,
            background_color = background_color_input,
            grid_line_check = grid_line_check,
            grid_line_color = grid_line_color_input,
            legend_check = legend_check,
            graph_title = graph_title,
            x_value = x_value,
            y_values = y_values,
            z_value = z_value
        )

        self.time_step = self.time_step_spinbox.value() * 1000

    def start_simulation(self):
        """
        Starts the simulation by connecting the timer to the plot update and starting the timer.
        Ensures the signal is connected only once
        """
        try:
            self.timer_graph.timeout.disconnect()  # Disconnect all existing connections
        except:
            pass
        
        self.timer_graph.timeout.connect(self.plot_3d.update_plot)
        self.timer_graph.start(int(self.time_step))

    def stop_simulation(self):
        """Stops the timer/graphing simulation"""

        self.timer_graph.stop()

    def reset_simulation(self):
        """
        Resets the simulation by stopping the timer and clearing the plot data.
        Ensures the signal is disconnected to avoid multiple connection
        """
        self.timer_graph.stop()
        try:
            self.timer_graph.timeout.disconnect()  # Disconnect all existing connections
        except:
            pass
        self.plot_3d.reset_plot()

    def remove_simulation(self):
        """
        Removes the graph's values present by resetting the values and stopping the timer.
        Ensures the signal is disconnected to avoid multiple connections.
        """
        self.timer_graph.stop()
        try:
            self.timer_graph.timeout.disconnect()  # Disconnect all existing connections
        except:
            pass
        self.plot_3d.reset_values()