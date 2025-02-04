import utils.create_uicomponents as create
from graphs.graph_plot_2d_ui import Plot2D

from PyQt5 import QtCore, QtGui, QtWidgets

class Group2D:
    def __init__(self, displayed_checkboxes, index):
        self.displayed_checkboxes = displayed_checkboxes.copy()
        self.index = index
        self.plot_2d = Plot2D(
            index = self.index
        )

        self.type = "Line Graph"
        self.current_background_color = QtGui.QColor(1, 10, 38)
        self.current_grid_lines_color = QtGui.QColor(255, 255, 255)

        self.timer_graph = QtCore.QTimer()

        # self.displayed_checkboxes[key] = [value['axis'], False, value['value'], "Solid", "Circle", value['color']]
        self.displayed_elements = {} # [axis, checkbox, line button, scatter button]
        self.y_limit = []
        self.time_step = 500

    def _show_line_menu(self, line, name):
        menu = QtWidgets.QMenu()

        line_solid = menu.addAction("Solid")
        line_dash = menu.addAction("Dashed")
        line_dot = menu.addAction("Dot")
        line_dasheddot = menu.addAction("Dashed Dot")

        line_solid.triggered.connect(lambda: self._set_line("Solid", name))
        line_dash.triggered.connect(lambda: self._set_line("Dashed", name))
        line_dot.triggered.connect(lambda: self._set_line("Dot", name))
        line_dasheddot.triggered.connect(lambda: self._set_line("Dashed Dot", name))

        menu.exec_(self.displayed_elements[name][2].mapToGlobal(self.displayed_elements[name][2].rect().bottomLeft()))  

    def _set_line(self, line, name):
        self.displayed_elements[name][2].setText(line)
        self.displayed_checkboxes[name][3] = line
    
    def _show_scatter_menu(self, scatter, name):
        menu = QtWidgets.QMenu()

        scatter_circle = menu.addAction("Circle")
        scatter_square = menu.addAction("Square")
        scatter_triangle = menu.addAction("Triangle")
        scatter_diamond = menu.addAction("Diamond")
        scatter_plus = menu.addAction("Plus")
        scatter_cross = menu.addAction("Cross")
        scatter_pentagon = menu.addAction("Pentagon")
        scatter_hexagon = menu.addAction("Hexagon")

        scatter_circle.triggered.connect(lambda: self._set_scatter("Circle", name))
        scatter_square.triggered.connect(lambda: self._set_scatter("Square", name))
        scatter_triangle.triggered.connect(lambda: self._set_scatter("Triangle", name))
        scatter_diamond.triggered.connect(lambda: self._set_scatter("Diamond", name))
        scatter_plus.triggered.connect(lambda: self._set_scatter("Plus", name))
        scatter_cross.triggered.connect(lambda: self._set_scatter("Cross", name))
        scatter_pentagon.triggered.connect(lambda: self._set_scatter("Pentagon", name))
        scatter_hexagon.triggered.connect(lambda: self._set_scatter("Hexagon", name))

        menu.exec_(self.displayed_elements[name][3].mapToGlobal(self.displayed_elements[name][3].rect().bottomLeft()))  

    def _set_scatter(self, scatter, name):
        self.displayed_elements[name][3].setText(scatter)
        self.displayed_checkboxes[name][4] = scatter
        
    def _checkbox_limits(self, checkbox, name):
        """
        Updates whether a value is checked
        The Y axis can contain upto a maximum of four values and will block out any new values from being checked
        """

        if checkbox and self.displayed_checkboxes[name][0] == "x":
            self.displayed_checkboxes[name] = [self.displayed_checkboxes[name][0], True, self.displayed_checkboxes[name][2]]
        elif self.displayed_checkboxes[name][0] == "x":
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
        if self.type == type:
            return

        self.type = type
        self.type_button.setText(type)

        line = []
        scatter = []
        for list in self.displayed_elements.values():
            if len(list) > 2:
                line.append(list[2])
                scatter.append(list[3])

        if self.type == "Line Graph":
            for i in range(1, len(line) + 1):
                self.y_axis_grid.removeWidget(scatter[i - 1])  # Remove scatter widget
                scatter[i - 1].hide()  # Hide scatter widget
                self.y_axis_grid.addWidget(line[i - 1], i, 1)  # Add line widget
                line[i - 1].show()  # Show line widget

        if self.type == "Scatter Graph":
            for i in range(1, len(scatter) + 1):
                self.y_axis_grid.removeWidget(line[i - 1])  # Remove line widget
                line[i - 1].hide()  # Hide line widget
                self.y_axis_grid.addWidget(scatter[i - 1], i, 1)  # Add scatter widget
                scatter[i - 1].show()  # Show scatter widget

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
            geometry = QtCore.QRect(10, 68, 221, 171),
            font_size = 16,
            objname = "graph_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "X Axis:"
        )
        self.x_axis_scrollarea = create.create_scroll(
            parent = self.x_axis_group,
            objname = "x_axis_scrollarea",
            geometry = QtCore.QRect(0, 29, 221, 141),
            resizable = True
        )
        self.x_axis_scroll_widget = create.create_widget(
            parent = self.x_axis_group,
            objname = "x_axis_scroll_widget",
            geometry = QtCore.QRect(0, 0, 219, 139)
        )
        self.x_axis_grid = create.create_grid_layout(
            parent = self.x_axis_scroll_widget,
            objname = "x_axis_grid"
        )

        self.x_buttongroup = QtWidgets.QButtonGroup()
        self.x_buttongroup.setExclusive(True)

        self.y_axis_group = create.create_group_box(
            parent = self.graph_group,
            geometry = QtCore.QRect(263, 68, 221, 171),
            font_size = 16,
            objname = "graph_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Y Axis:"
        )
        self.y_axis_scrollarea = create.create_scroll(
            parent = self.y_axis_group,
            objname = "y_axis_scrollarea",
            geometry = QtCore.QRect(0, 30, 221, 141),
            resizable = True
        )
        self.y_axis_scroll_widget = create.create_widget(
            parent = self.y_axis_group,
            objname = "y_axis_scroll_widget",
            geometry = QtCore.QRect(0, 0, 219, 139)
        )
        self.y_axis_grid = create.create_grid_layout(
            parent = self.y_axis_scroll_widget,
            objname = "y_axis_grid"
        )

        self.x_axis_scrollarea.setWidget(self.x_axis_scroll_widget)
        self.y_axis_scrollarea.setWidget(self.y_axis_scroll_widget)

        self.settings_group = create.create_group_box(
            parent = self.graph_group,
            geometry = QtCore.QRect(520, 50, 370, 240),
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
        self.x_axis_name_label = create.create_name_label(
            parent = self.graph_group,
            font_size = 16,
            geometry = QtCore.QRect(10, 250, 141, 31),
            objname = "x_axis_name_label",
            text = "X Axis Name :"
        )
        self.x_axis_name_lineedit = create.create_line_edit(
            parent = self.graph_group,
            geometry = QtCore.QRect(149, 254, 81, 25),
            font_size = 16,
            objname = "x_axis_name_lineedit"
        )
        self.y_axis_name_label = create.create_name_label(
            parent = self.graph_group,
            geometry = QtCore.QRect(265, 250, 141, 31),
            font_size = 16,
            objname = "y_axis_name_label",
            text = "Y Axis Name :"
        )
        self.y_axis_name_lineedit = create.create_line_edit(
            parent = self.graph_group,
            geometry = QtCore.QRect(405, 255, 81, 25),
            font_size = 16,
            objname = "y_axis_name_lineedit"
        )

        self.create_labels()
    
        graph_display_layout.addWidget(self.plot_2d.plot_widget)

    def create_labels(self):
        """
        Creates each label for X, Y and Z axis.
        Creates a line and scatter style buttons for Y axis only
        """

        for key, value in self.displayed_checkboxes.items():
            checkbox = create.create_checkbox(
                text = "",
                layout = QtCore.Qt.LeftToRight,
                objname = "checkbox",
                font_size = 12
            )
            line_button = create.create_button(
                text = "Solid",
                objname = "line_button",
                font_size = 12
            )
            scatter_button = create.create_button(
                text = "Circle",
                objname = "scatter_button",
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
                line_button.clicked.connect(lambda state, key=key: self._show_line_menu(state, key))
                scatter_button.clicked.connect(lambda state, key=key: self._show_scatter_menu(state, key))
                checkbox.setStyleSheet(f"color: {value[5].name()};")
                row_position = self.y_axis_grid.rowCount()
                self.y_axis_grid.addWidget(checkbox, row_position, 0)
                self.y_axis_grid.addWidget(line_button, row_position, 1)
                self.displayed_elements[key] = [value[0], checkbox, line_button, scatter_button]
                self.y_limit.append(checkbox)

    def save_settings(self):
        """Updates the constants for the graph"""

        # self.displayed_checkboxes[key] = [value['axis'], False, value['value'], "Solid", "Circle", value['color']]
        x_value = []
        y_values = []
        for key, value in self.displayed_checkboxes.items():
            if value[1] and value[0] == "y":
                y_values.append([key, value])  # Just store the key and value directly
            elif value[1] and value[0] == "x":
                x_value.append([key, value])  # Just store the key and value directly

        type = self.type
        background_color_input = self.current_background_color.name()
        grid_line_check = self.show_grid_lines_checkbox.isChecked()
        grid_line_color_input = self.current_grid_lines_color
        legend_check = self.show_legend_checkbox.isChecked()

        graph_title = self.graph_title_lineedit.text() if self.graph_title_lineedit.text() else f"Graph {self.index}"
        x_input = self.x_axis_name_lineedit.text() if self.x_axis_name_lineedit.text() else "X Axis"
        y_input = self.y_axis_name_lineedit.text()if self.y_axis_name_lineedit.text() else "Y Axis"
        
        self.plot_2d.update(
            type = type,
            background_color = background_color_input,
            grid_line_check = grid_line_check,
            grid_line_color = grid_line_color_input,
            legend_check = legend_check,
            graph_title = graph_title,
            x_input = x_input,
            y_input = y_input,
            x_value = x_value,
            y_values = y_values
        )

        self.time_step = self.time_step_spinbox.value() * 1000

    def start_simulation(self):
        """
        Starts the simulation by connecting the timer to the plot update and starting the timer.
        Ensures the signal is connected only once.
        """
        try:
            self.timer_graph.timeout.disconnect()  # Disconnect all existing connections
        except:
            pass

        self.timer_graph.timeout.connect(self.plot_2d.update_plot)
        self.timer_graph.start(int(self.time_step))

    def stop_simulation(self):
        """Stops the timer/graphing simulation"""
        
        self.timer_graph.stop()

    def reset_simulation(self):
        """
        Resets the simulation by stopping the timer and clearing the plot data.
        Ensures the signal is disconnected to avoid multiple connections.
        """
        self.timer_graph.stop()
        try:
            self.timer_graph.timeout.disconnect()  # Disconnect all existing connections
        except:
            pass
        self.plot_2d.reset_plot()
