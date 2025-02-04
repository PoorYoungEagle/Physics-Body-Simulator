from utils.resolution_scaler import ResolutionScaler

from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

class Plot3D:
    def __init__(
            self,
            index=0
        ):
        pg.setConfigOptions(antialias=True)

        self.type = "Line Graph"
        self.index = index

        scaler = ResolutionScaler()
        scaled_width, scaled_height = scaler.scale_size(900, 380)

        self.container = QtWidgets.QWidget()
        self.container.setFixedSize(QtCore.QSize(scaled_width, scaled_height))
        
        self.plot_widget = gl.GLViewWidget()
        self.plot_widget.setBackgroundColor(QtGui.QColor(1, 10, 38))  # Dark blue background
        self.plot_widget.setCameraPosition(distance=40, elevation=30)
        
        layout = QtWidgets.QVBoxLayout(self.container)
        layout.addWidget(self.plot_widget)

        self.title_label = QtWidgets.QLabel(self.container)
        self.title_label.setFont(QtGui.QFont("Arial Rounded MT Bold", 12, QtGui.QFont.Bold))
        self.title_label.setStyleSheet("color: white; background-color: transparent;")
        self.title_label.setGeometry(400, 0, 150, 50)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.hide()
        
        self.legend = QtWidgets.QLabel(self.container)
        self.legend.setFont(QtGui.QFont("Arial Rounded MT Bold", 10))
        self.legend.setStyleSheet("color: white; background-color: transparent; padding: 5px; border-radius: 5px;")
        self.legend.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.legend.hide()
        
        self.axes = gl.GLAxisItem()
        self.axes.setSize(x=20, y=20, z=20)
        self.plot_widget.addItem(self.axes)
        
        self.grid = gl.GLGridItem()
        self.grid.setSize(x=40, y=40)
        self.grid.setSpacing(x=1, y=1)
        self.grid.translate(0, 0, 0)
        self.plot_widget.addItem(self.grid)

        self.plots = {}
        self.x_value = []
        self.data_y_values = {}
        self.z_value = []

        self.show_legend = False
        self.counter = 0

    def reset_plot(self):
        """Resets the plot values"""

        pts = np.vstack([
            np.array([]),
            np.array([]),
            np.array([])
        ]).T.astype(np.float32)
        for name in self.plots:
            self.plots[name].setData(pos=pts)

        for data in self.data_y_values.values():
            data["x_list"].clear()
            data["y_list"].clear()
            data["z_list"].clear()
            data["plot"].setData(pos=pts)
        self.counter = 0

    def reset_values(self):
        """Removes plots from the graph"""

        for name in self.plots:
            self.plot_widget.removeItem(self.plots[name])
        self.plots.clear()
        self.data_y_values.clear()
        self.counter = 0

    def update_plot(self):
        """Update the plot with new data points in real time"""

        self.counter += 1
        try:
            if self.x_value[0][0] == "Time X":
                x_data = self.counter
            else:
                x = self.x_value[0]
                x_data = x[1][2]()
            
            z = self.z_value[0]
            z_data = z[1][2]()

            for name, data in self.data_y_values.items():
                y_data = data["data"]()
                data["x_list"].append(x_data)
                data["y_list"].append(y_data)
                data["z_list"].append(z_data)
                
                # Ensure we have at least 2 points for line plots
                if len(data["x_list"]) < 2:
                    continue
                
                # Create 3D points
                pts = np.vstack([
                    np.array(data["x_list"]),
                    np.array(data["y_list"]),
                    np.array(data["z_list"])
                ]).T.astype(np.float32)  # Ensure float32 type

                self.plots[name].setData(pos=pts)
                    
        except Exception as e:
            print(f"Error updating plot: {str(e)}")
            pass

    def update(
            self,
            type,
            background_color,
            grid_line_check,
            grid_line_color,
            legend_check,
            graph_title,
            x_value,
            y_values,
            z_value
        ):
        """Update plot styling and labels"""
        self.type = type
        
        # Set background color
        bg_color = QtGui.QColor(int(background_color[1:3], 16), 
                         int(background_color[3:5], 16), 
                         int(background_color[5:7], 16))
        self.plot_widget.setBackgroundColor(bg_color)

        self.grid.setVisible(grid_line_check)
        self.grid.setColor((grid_line_color.red(), grid_line_color.green(), grid_line_color.blue(), 75))

        
        self.x_value = x_value
        self.y_values = y_values
        self.z_value = z_value

        # Initialize with two points to avoid OpenGL errors
        initial_pts = np.array([[0, 0, 0], [0, 0, 0]], dtype=np.float32)

        self.title_label.setText(graph_title)
        self.title_label.show()

        self.reset_values()

        legend_text = "<span style='color: white;'>Legend:</span><br>"
        for name, data in y_values:
            color = data[3]
            color_tuple = (color.red()/255, color.green()/255, color.blue()/255, 1.0)
            
            if self.type == "Line Graph":
                line_plot = gl.GLLinePlotItem(
                    pos=initial_pts,
                    color=color_tuple,
                    width=2.0,
                    antialias=True,
                    mode='line_strip'  # Explicitly set the drawing mode
                )
                self.plots[name] = line_plot
                self.plot_widget.addItem(line_plot)
                self.data_y_values[name] = {
                    "data": data[2],
                    "plot": line_plot,
                    "x_list": [],
                    "y_list": [],
                    "z_list": []
                }
            else:
                scatter_plot = gl.GLScatterPlotItem(
                    pos=initial_pts,
                    color=color_tuple,
                    size=10.0,
                    pxMode=True
                )
                self.plots[name] = scatter_plot
                self.plot_widget.addItem(scatter_plot)
            
                self.data_y_values[name] = {
                    "data": data[2],
                    "plot": scatter_plot,
                    "x_list": [],
                    "y_list": [],
                    "z_list": []
                }
            
            legend_text += f"<span style='color: {color.name()};'>- {name}</span><br>"

        if legend_check:
            self.legend.setText(legend_text)
            self.legend.setGeometry(20, 20, 200, 30 + 20 * len(y_values))
            self.legend.show()
            self.show_legend = True
        else:
            self.legend.hide()
            self.show_legend = False

        self.counter = 0