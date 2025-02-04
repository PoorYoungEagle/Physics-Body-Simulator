from utils.resolution_scaler import ResolutionScaler

from PyQt5 import QtGui
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import QSize

class Plot2D:
    def __init__(
            self,
            index=0
        ):
        pg.setConfigOptions(antialias=True)

        self.type = "Line Graph"
        self.index = index

        scaler = ResolutionScaler()
        scaled_width, scaled_height = scaler.scale_size(900, 380)

        self.plot_widget = pg.PlotWidget(background=QtGui.QColor(1, 10, 38))  # Dark blue background
        self.plot_widget.setFixedSize(QSize(scaled_width, scaled_height))
        
        self.plot_widget.setTitle(f"Graph {self.index}", color='w', size='16pt')
        self.plot_widget.setLabel('bottom', "X Axis", color='#D3D3D3', size='14pt')
        self.plot_widget.setLabel('left', "Y Axis", color='#D3D3D3', size='14pt')
        
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)

        self.scatter_plot = pg.ScatterPlotItem(size = 10)
        self.plot_widget.addItem(self.scatter_plot)

        self.x_value = []
        self.data_y_values = {}

        self.line_type = {
            "Solid" : None,
            "Dashed" : QtCore.Qt.DashLine,
            "Dot" : QtCore.Qt.DotLine,
            "Dashed Dot" : QtCore.Qt.DashDotLine
        }
        self.scatter_type = {
            "Circle" : 'o',
            "Square" : 's',
            "Triangle" : 't',
            "Diamond" : 'd',
            "Plus" : '+',
            "Cross" : 'x',
            "Pentagon" : 'p',
            "Hexagon" : 'h'
        }

        self.legend = None
        self.show_legend = False

        self.counter = 0

    def reset_plot(self):
        """Resets the plot values"""

        for data in self.data_y_values.values():
            data["x_list"].clear()
            data["y_list"].clear()
            data["plot"].setData([],[])

        self.counter = 0

    def update_plot(self):
        """Update the plot with new data points in real time"""

        self.counter += 1

        if self.x_value[0][0] == "Time X":
            x_data = self.counter
        else:
            x = self.x_value[0]
            x_data = x[1][2]()

        if self.type == "Line Graph":
            for name, data in self.data_y_values.items():
                value = data["data"]()
                data["x_list"].append(x_data)
                data["y_list"].append(value)
                data["plot"].setData(data["x_list"], data["y_list"])
        else:
            for name, data in self.data_y_values.items():
                value = data["data"]()
                data["x_list"].append(x_data)
                data["y_list"].append(value)
                data["plot"].setData(x=data["x_list"], y=data["y_list"])

    def update(
            self,
            type,
            background_color,
            grid_line_check,
            grid_line_color,
            legend_check,
            graph_title,
            x_input,
            y_input,
            x_value,
            y_values
        ):
        """Update plot styling and labels"""
        
        self.type = type

        self.plot_widget.setTitle(graph_title, color='w', size='16pt')
        
        # Configure grid
        grid_color_pen = pg.mkPen(color=(grid_line_color.red(), grid_line_color.green(), grid_line_color.blue()), width=0.5)
        self.plot_widget.showGrid(x=grid_line_check, y=grid_line_check, alpha=0.3)
        self.plot_widget.getAxis('bottom').setPen(grid_color_pen)
        self.plot_widget.getAxis('left').setPen(grid_color_pen)

        self.plot_widget.setLabel('bottom', x_input, color='#D3D3D3')
        self.plot_widget.setLabel('left', y_input, color='#D3D3D3')

        # Convert hex to RGB
        bg_color = QtGui.QColor(int(background_color[1:3], 16), 
                          int(background_color[3:5], 16), 
                          int(background_color[5:7], 16))
        self.plot_widget.setBackground(bg_color)

        self.x_value = x_value
        self.y_values = y_values

        self.plots = []
        for name, data in y_values:
            if self.type == "Line Graph":
                plot = self.plot_widget.plot(
                    pen = pg.mkPen(color=(data[5].red(), data[5].green(), data[5].blue()), width=2, style = self.line_type[data[3]]),
                    name=name
                )
                self.plots.append(plot)

                self.data_y_values[name] = {
                    "data" : data[2],
                    "line_type" : data[3],
                    "plot" : plot,
                    "x_list" : [],
                    "y_list" : []
                }
            else:
                scatter = pg.ScatterPlotItem(
                    brush=pg.mkBrush(data[5].red(), data[5].green(), data[5].blue(), 120),
                    symbol = self.scatter_type[data[4]],
                    size = 10,
                    name=name
                )
                self.plots.append(scatter)

                self.data_y_values[name] = {
                    "data" : data[2],
                    "line_type" : data[3],
                    "plot" : scatter,
                    "x_list" : [],
                    "y_list" : []
                }
                self.plot_widget.addItem(scatter)

        if self.show_legend:
            if self.legend is not None:
                self.legend.scene().removeItem(self.legend)
                self.legend = None
            self.show_legend = False

        if legend_check:
            if not self.show_legend:
                self.legend = pg.LegendItem(offset=(70, 30))
                self.legend.setParentItem(self.plot_widget.graphicsItem())
                for plot in self.plots:
                    self.legend.addItem(plot, plot.name())
                self.show_legend = True

        self.counter = 0