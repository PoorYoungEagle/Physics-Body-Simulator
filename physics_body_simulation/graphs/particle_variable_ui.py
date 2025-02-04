import utils.create_uicomponents as create

from PyQt5 import QtCore, QtWidgets, QtGui

class Variables:
    def __init__(self, graph_settings_ui):

        self.graph_settings_ui = graph_settings_ui
        self.layouts = {
            'x' : self.graph_settings_ui.x_axis_vlayout,
            'y' : self.graph_settings_ui.y_axis_vlayout,
            'z' : self.graph_settings_ui.z_axis_vlayout
        }
        self.name = "Nan"

        self.particle_variable_group = None

        # All these values are just saving which radio button is checked
        # Probably can be done better

        self.position_x = {"x": 0, "y": 0, "z": 0}
        self.position_y = {"x": 0, "y": 0, "z": 0}
        self.position_z = {"x": 0, "y": 0, "z": 0}

        self.velocity_x = {"x": 0, "y": 0, "z": 0}
        self.velocity_y = {"x": 0, "y": 0, "z": 0}
        self.velocity_z = {"x": 0, "y": 0, "z": 0}
        self.velocity_mag = {"x": 0, "y": 0, "z": 0}

        self.acceleration_x = {"x": 0, "y": 0, "z": 0}
        self.acceleration_y = {"x": 0, "y": 0, "z": 0}
        self.acceleration_z = {"x": 0, "y": 0, "z": 0}
        self.acceleration_mag = {"x": 0, "y": 0, "z": 0}

        self.momentum_x = {"x": 0, "y": 0, "z": 0}
        self.momentum_y = {"x": 0, "y": 0, "z": 0}
        self.momentum_z = {"x": 0, "y": 0, "z": 0}
        self.momentum_mag = {"x": 0, "y": 0, "z": 0}
        
        self.force_x = {"x": 0, "y": 0, "z": 0}
        self.force_y = {"x": 0, "y": 0, "z": 0}
        self.force_z = {"x": 0, "y": 0, "z": 0}
        self.force_mag = {"x": 0, "y": 0, "z": 0}

        self.energy_ke = {"x": 0, "y": 0, "z": 0}
        self.energy_pe = {"x": 0, "y": 0, "z": 0}
        self.energy_te = {"x": 0, "y": 0, "z": 0}

        self.selected_variables = {}
        self.displayed_labels = {}
        self.current_color = QtGui.QColor(255, 255, 255)

    def _show_color_dialog(self, name):
        split_name = name.split(" : ")[1]
        name = self.name + " : " + split_name
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            if name in self.displayed_labels:
                if len(self.displayed_labels[name]) == 4:  # Check if it includes a button
                    current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                    current_button.setStyleSheet(f"background-color: {color.name()}")
                    self.displayed_labels[name] = (*self.displayed_labels[name][:3], color)

                if name in self.selected_variables:
                    current_values = self.selected_variables[name]
                    if len(current_values) == 3:  # Ensure it has space for color
                        current_values["color"] = color
                    self.selected_variables[name] = current_values

    def set_position(self, axis, value, position, particle):
        """Update the position for the specified axis"""

        label = create.create_name_label(
            text = "",
            objname = "label",
            font_size = 12
        )
        color_button = create.create_button(
            text = "",
            objname = "color_button",
            font_size = 12
        )

        if position == 'x':
            for key in self.position_x:
                self.position_x[key] = 0
            self.position_x[axis] = value
            name = f"{self.name} : Position X"
            particle_axis = 0

        elif position == 'y':
            for key in self.position_y:
                self.position_y[key] = 0
            self.position_y[axis] = value
            name = f"{self.name} : Position Y"
            particle_axis = 1

        elif position == 'z':
            for key in self.position_z:
                self.position_z[key] = 0
            self.position_z[axis] = value
            name = f"{self.name} : Position Z"
            particle_axis = 2

        if name in self.displayed_labels:
            if len(self.displayed_labels[name]) == 4:
                current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_layout.removeWidget(current_button)
                current_label.deleteLater()
                current_button.deleteLater()
            elif len(self.displayed_labels[name]) == 2:
                current_label, current_layout = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_label.deleteLater()
            
        current_color = QtGui.QColor(255, 255, 255)
        label.setText(name)
        
        if axis == 'y': 
            color_button.setStyleSheet(f"background-color: {current_color.name()}")
            color_button.clicked.connect(lambda: self._show_color_dialog(name))
            row_position = self.layouts[axis].rowCount()
            self.layouts[axis].addWidget(label, row_position, 0)
            self.layouts[axis].addWidget(color_button, row_position, 1)
            self.displayed_labels[name] = (label, color_button, self.layouts[axis], current_color)
            self.selected_variables[name] = {
                'axis': axis,
                'value': lambda: particle.position_dynamic[particle_axis],  # Reference the dynamic value
                'color': current_color
            }
        else:
            row_position = self.layouts[axis].rowCount()
            self.layouts[axis].addWidget(label, row_position, 0)
            self.displayed_labels[name] = (label, self.layouts[axis])
            self.selected_variables[name] = {
                'axis': axis,
                'value': lambda: particle.position_dynamic[particle_axis],
            }

    def set_velocity(self, axis, value, velocity, particle):
        """Update the velocity for the specified axis"""

        label = create.create_name_label(
            text = "",
            objname = "label",
            font_size = 12
        )
        color_button = create.create_button(
            text = "",
            objname = "color_button",
            font_size = 12
        )

        if velocity == 'x':
            for key in self.velocity_x:
                self.velocity_x[key] = 0
            self.velocity_x[axis] = value
            name = f"{self.name} : Velocity X"
            particle_axis = 0

        elif velocity == 'y':
            for key in self.velocity_y:
                self.velocity_y[key] = 0
            self.velocity_y[axis] = value
            name = f"{self.name} : Velocity Y"
            particle_axis = 1

        elif velocity == 'z':
            for key in self.velocity_z:
                self.velocity_z[key] = 0
            self.velocity_z[axis] = value
            name = f"{self.name} : Velocity Z"
            particle_axis = 2
        
        elif velocity == 'mag':
            for key in self.velocity_mag:
                self.velocity_mag[key] = 0
            self.velocity_mag[axis] = value
            name = f"{self.name} : |Velocity|"
            particle_axis = "mag"


        if name in self.displayed_labels:
            if len(self.displayed_labels[name]) == 4:
                current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_layout.removeWidget(current_button)
                current_label.deleteLater()
                current_button.deleteLater()
            elif len(self.displayed_labels[name]) == 2:
                current_label, current_layout = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_label.deleteLater()
        
        current_color = QtGui.QColor(255, 255, 255)
        
        label.setText(name)
        row_position = self.layouts[axis].rowCount()
        if axis == 'y':
            color_button.setStyleSheet(f"background-color: {current_color.name()}")
            color_button.clicked.connect(lambda: self._show_color_dialog(name))

            self.layouts[axis].addWidget(label, row_position, 0)
            self.layouts[axis].addWidget(color_button, row_position, 1)
            self.displayed_labels[name] = (label, color_button, self.layouts[axis], current_color)
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.velocity_magnitude,
                    'color': current_color
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.velocity_dynamic[particle_axis],
                    'color': current_color
                }
        else:
            self.layouts[axis].addWidget(label, row_position, 0)
            self.displayed_labels[name] = (label, self.layouts[axis])
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.velocity_magnitude
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.velocity_dynamic[particle_axis]
                }
    
    def set_acceleration(self, axis, value, acceleration, particle):
        """Update the acceleration for the specified axis"""

        label = create.create_name_label(
            text = "",
            objname = "label",
            font_size = 12
        )
        color_button = create.create_button(
            text = "",
            objname = "color_button",
            font_size = 12
        )

        if acceleration == 'x':
            for key in self.acceleration_x:
                self.acceleration_x[key] = 0
            self.acceleration_x[axis] = value
            name = f"{self.name} : Acceleration X"
            particle_axis = 0

        elif acceleration == 'y':
            for key in self.acceleration_y:
                self.acceleration_y[key] = 0
            self.acceleration_y[axis] = value
            name = f"{self.name} : Acceleration Y"
            particle_axis = 1

        elif acceleration == 'z':
            for key in self.acceleration_z:
                self.acceleration_z[key] = 0
            self.acceleration_z[axis] = value
            name = f"{self.name} : Acceleration Z"
            particle_axis = 2
        
        elif acceleration == 'mag':
            for key in self.acceleration_mag:
                self.acceleration_mag[key] = 0
            self.acceleration_mag[axis] = value
            name = f"{self.name} : |Acceleration|"
            particle_axis = "mag"

        if name in self.displayed_labels:
            if len(self.displayed_labels[name]) == 4:
                current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_layout.removeWidget(current_button)
                current_label.deleteLater()
                current_button.deleteLater()
            elif len(self.displayed_labels[name]) == 2:
                current_label, current_layout = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_label.deleteLater()

        current_color = QtGui.QColor(255, 255, 255)
        
        label.setText(name)
        row_position = self.layouts[axis].rowCount()
        if axis == 'y':
            color_button.setStyleSheet(f"background-color: {current_color.name()}")
            color_button.clicked.connect(lambda: self._show_color_dialog(name))

            self.layouts[axis].addWidget(label, row_position, 0)
            self.layouts[axis].addWidget(color_button, row_position, 1)
            self.displayed_labels[name] = (label, color_button, self.layouts[axis], current_color)
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.acceleration_magnitude,
                    'color': current_color
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.acceleration_total[particle_axis],
                    'color': current_color
                }
        else:
            self.layouts[axis].addWidget(label, row_position, 0)
            self.displayed_labels[name] = (label, self.layouts[axis])
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.acceleration_magnitude
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.acceleration_total[particle_axis]
                }

    def set_momentum(self, axis, value, momentum, particle):
        """Update the momentum for the specified axis"""

        label = create.create_name_label(
            text = "",
            objname = "label",
            font_size = 12
        )
        color_button = create.create_button(
            text = "",
            objname = "color_button",
            font_size = 12
        )

        if momentum == 'x':
            for key in self.momentum_x:
                self.momentum_x[key] = 0
            self.momentum_x[axis] = value
            name = f"{self.name} : Momentum X"
            particle_axis = 0

        elif momentum == 'y':
            for key in self.momentum_y:
                self.momentum_y[key] = 0
            self.momentum_y[axis] = value
            name = f"{self.name} : Momentum Y"
            particle_axis = 1

        elif momentum == 'z':
            for key in self.momentum_z:
                self.momentum_z[key] = 0
            self.momentum_z[axis] = value

            name = f"{self.name} : Momentum Z"
            particle_axis = 2
        
        elif momentum == 'mag':
            for key in self.momentum_mag:
                self.momentum_mag[key] = 0
            self.momentum_mag[axis] = value
            name = f"{self.name} : |Momentum|"
            particle_axis = 'mag'

        if name in self.displayed_labels:
            if len(self.displayed_labels[name]) == 4:
                current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_layout.removeWidget(current_button)
                current_label.deleteLater()
                current_button.deleteLater()
            elif len(self.displayed_labels[name]) == 2:
                current_label, current_layout = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_label.deleteLater()

        current_color = QtGui.QColor(255, 255, 255)
        
        label.setText(name)
        row_position = self.layouts[axis].rowCount()
        if axis == 'y':
            color_button.setStyleSheet(f"background-color: {current_color.name()}")
            color_button.clicked.connect(lambda: self._show_color_dialog(name))

            self.layouts[axis].addWidget(label, row_position, 0)
            self.layouts[axis].addWidget(color_button, row_position, 1)
            self.displayed_labels[name] = (label, color_button, self.layouts[axis], current_color)
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.momentum_magnitude,
                    'color': current_color
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.momentum_dynamic[particle_axis],
                    'color': current_color
                }
        else:
            self.layouts[axis].addWidget(label, row_position, 0)
            self.displayed_labels[name] = (label, self.layouts[axis])
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.momentum_magnitude
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.momentum_dynamic[particle_axis]
                }

    def set_force(self, axis, value, force, particle):
        """Update the force for the specified axis"""

        label = create.create_name_label(
            text = "",
            objname = "label",
            font_size = 12
        )
        color_button = create.create_button(
            text = "",
            objname = "color_button",
            font_size = 12
        )

        if force == 'x':
            for key in self.force_x:
                self.force_x[key] = 0
            self.force_x[axis] = value
            name = f"{self.name} : Force X"
            particle_axis = 0

        elif force == 'y':
            for key in self.force_y:
                self.force_y[key] = 0
            self.force_y[axis] = value
            name = f"{self.name} : Force Y"
            particle_axis = 1

        elif force == 'z':
            for key in self.force_z:
                self.force_z[key] = 0
            self.force_z[axis] = value
            name = f"{self.name} : Force Z"
            particle_axis = 2
        
        elif force == 'mag':
            for key in self.force_mag:
                self.force_mag[key] = 0
            self.force_mag[axis] = value
            name = f"{self.name} : |Force|"
            particle_axis = "mag"

        if name in self.displayed_labels:
            if len(self.displayed_labels[name]) == 4:
                current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_layout.removeWidget(current_button)
                current_label.deleteLater()
                current_button.deleteLater()
            elif len(self.displayed_labels[name]) == 2:
                current_label, current_layout = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_label.deleteLater()

        current_color = QtGui.QColor(255, 255, 255)
        
        label.setText(name)
        row_position = self.layouts[axis].rowCount()
        if axis == 'y':
            color_button.setStyleSheet(f"background-color: {current_color.name()}")
            color_button.clicked.connect(lambda: self._show_color_dialog(name))

            self.layouts[axis].addWidget(label, row_position, 0)
            self.layouts[axis].addWidget(color_button, row_position, 1)
            self.displayed_labels[name] = (label, color_button, self.layouts[axis], current_color)
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.force_magnitude,
                    'color': current_color
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.force_dynamic[particle_axis],
                    'color': current_color
                }
        else:
            self.layouts[axis].addWidget(label, row_position, 0)
            self.displayed_labels[name] = (label, self.layouts[axis])
            if particle_axis == "mag":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.force_magnitude
                }
            else:
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.force_dynamic[particle_axis]
                }
        
    def set_energy(self, axis, value, energy, particle):
        """Update the energy for the specified axis"""

        label = create.create_name_label(
            text = "",
            objname = "label",
            font_size = 12
        )
        color_button = create.create_button(
            text = "",
            objname = "color_button",
            font_size = 12
        )

        if energy == 'ke':
            for key in self.energy_ke:
                self.energy_ke[key] = 0
            self.energy_ke[axis] = value
            name = f"{self.name} : Energy KE"
            particle_axis = "ke"

        elif energy == 'pe':
            for key in self.energy_pe:
                self.energy_pe[key] = 0
            self.energy_pe[axis] = value
            name = f"{self.name} : Energy PE"
            particle_axis = "pe"

        elif energy == 'te':
            for key in self.energy_te:
                self.energy_te[key] = 0
            self.energy_te[axis] = value
            name = f"{self.name} : Energy TE"
            particle_axis = "te"

        if name in self.displayed_labels:
            if len(self.displayed_labels[name]) == 4:
                current_label, current_button, current_layout, current_color = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_layout.removeWidget(current_button)
                current_label.deleteLater()
                current_button.deleteLater()
            elif len(self.displayed_labels[name]) == 2:
                current_label, current_layout = self.displayed_labels[name]
                current_layout.removeWidget(current_label)
                current_label.deleteLater()

        current_color = QtGui.QColor(255, 255, 255)
        
        label.setText(name)
        row_position = self.layouts[axis].rowCount()
        if axis == 'y':
            color_button.setStyleSheet(f"background-color: {current_color.name()}")
            color_button.clicked.connect(lambda: self._show_color_dialog(name))

            self.layouts[axis].addWidget(label, row_position, 0)
            self.layouts[axis].addWidget(color_button, row_position, 1)
            self.displayed_labels[name] = (label, color_button, self.layouts[axis], current_color)
            if particle_axis == "ke":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.kinetic_energy_dynamic,
                    'color': current_color
                }
            elif particle_axis == "pe":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.potential_energy_dynamic,
                    'color': current_color
                }            
            elif particle_axis == "te":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.total_energy_dynamic,
                    'color': current_color
                }
        else:
            self.layouts[axis].addWidget(label, row_position, 0)
            self.displayed_labels[name] = (label, self.layouts[axis])
            if particle_axis == "ke":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.kinetic_energy_dynamic
                }
            elif particle_axis == "pe":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.potential_energy_dynamic
                }            
            elif particle_axis == "te":
                self.selected_variables[name] = {
                    'axis': axis,
                    'value': lambda: particle.total_energy_dynamic
                }

    def set_title(self, new_name):
        """Update the title and propagate changes to all relevant references"""

        self.particle_variable_group.hide()

        self.particle_variable_group.setTitle(new_name + ' : ')
        self.name = new_name

    def update_names(self, new_name):
        """"Updates names and labels"""

        self.name = new_name

        updated_displayed_labels = {}
        for key, value in self.displayed_labels.items():
            updated_name = key.split(" : ")[1]
            name = self.name + " : " + updated_name
            if len(value) == 4:
                label, button, layout, color = value
            else:
                label, layout = value

            # Update the label text
            label.setText(name)

            # Update the dictionary entry with the new name
            if len(value) == 4:
                updated_displayed_labels[name] = (label, button, layout, color)
            else:
                updated_displayed_labels[name] = (label, layout)

        self.displayed_labels = updated_displayed_labels

        updated_selected_variables = {}

        for key, value in self.selected_variables.items():
            updated_name = key.split(" : ")[1]
            name = self.name + " : " + updated_name

            updated_selected_variables[name] = value

        self.selected_variables = updated_selected_variables

    def delete_labels(self):
        """Deletes all labels and buttons"""

        for key, value in self.displayed_labels.items():
            if len(value) == 4:
                label, button, layout, _ = value
                layout.removeWidget(label)
                layout.removeWidget(button)
            else:
                label, layout = value
                layout.removeWidget(label)
        self.displayed_labels = {}
        try:
            self.particle_variable_group.hide()
        except:
            pass

    def update_particle_variables(self, particle):
        """Updates all dynamic values present on the lower right side of the screen"""

        self.posx_value_label.setText("X: " + f"{particle.position_dynamic[0]:.2f}")
        self.posy_value_label.setText("Y: " + f"{particle.position_dynamic[1]:.2f}")
        self.posz_value_label.setText("Z: " + f"{particle.position_dynamic[2]:.2f}")

        self.vx_value_label.setText("X: " + f"{particle.velocity_dynamic[0]:.2f}")
        self.vy_value_label.setText("Y: " + f"{particle.velocity_dynamic[1]:.2f}")
        self.vz_value_label.setText("Z: " + f"{particle.velocity_dynamic[2]:.2f}")
        self.v_value_label.setText("|V|: " + f"{particle.velocity_magnitude:.2f}")

        self.ax_value_label.setText("X: " + f"{particle.acceleration_total[0]:.2f}")
        self.ay_value_label.setText("Y: " + f"{particle.acceleration_total[1]:.2f}")
        self.az_value_label.setText("Z: " + f"{particle.acceleration_total[2]:.2f}")
        self.a_value_label.setText("|A|: " + f"{particle.acceleration_magnitude:.2f}")

        self.px_value_label.setText("X: " + f"{particle.momentum_dynamic[0]:.2f}")
        self.py_value_label.setText("Y: " + f"{particle.momentum_dynamic[1]:.2f}")
        self.pz_value_label.setText("Z: " + f"{particle.momentum_dynamic[2]:.2f}")
        self.p_value_label.setText("|p|: " + f"{particle.momentum_magnitude:.2f}")

        self.fx_value_label.setText("X: " + f"{particle.force_dynamic[0]:.2f}")
        self.fy_value_label.setText("Y: " + f"{particle.force_dynamic[1]:.2f}")
        self.fz_value_label.setText("Z: " + f"{particle.force_dynamic[2]:.2f}")
        self.f_value_label.setText("|F|: " + f"{particle.force_magnitude:.2f}")

        self.ke_value_label.setText("KE: " + f"{particle.kinetic_energy_dynamic:.2f}")
        self.pe_value_label.setText("PE: " + f"{particle.potential_energy_dynamic:.2f}")
        self.te_value_label.setText("TE: " + f"{particle.total_energy_dynamic:.2f}")

    def reset_particle_variables(self):
        """Resets all radio buttons' values back to unchecked"""

        self.position_x = {"x": 0, "y": 0, "z": 0}
        self.position_y = {"x": 0, "y": 0, "z": 0}
        self.position_z = {"x": 0, "y": 0, "z": 0}

        self.velocity_x = {"x": 0, "y": 0, "z": 0}
        self.velocity_y = {"x": 0, "y": 0, "z": 0}
        self.velocity_z = {"x": 0, "y": 0, "z": 0}
        self.velocity_mag = {"x": 0, "y": 0, "z": 0}

        self.acceleration_x = {"x": 0, "y": 0, "z": 0}
        self.acceleration_y = {"x": 0, "y": 0, "z": 0}
        self.acceleration_z = {"x": 0, "y": 0, "z": 0}
        self.acceleration_mag = {"x": 0, "y": 0, "z": 0}

        self.momentum_x = {"x": 0, "y": 0, "z": 0}
        self.momentum_y = {"x": 0, "y": 0, "z": 0}
        self.momentum_z = {"x": 0, "y": 0, "z": 0}
        self.momentum_mag = {"x": 0, "y": 0, "z": 0}
        
        self.force_x = {"x": 0, "y": 0, "z": 0}
        self.force_y = {"x": 0, "y": 0, "z": 0}
        self.force_z = {"x": 0, "y": 0, "z": 0}
        self.force_mag = {"x": 0, "y": 0, "z": 0}

        self.energy_ke = {"x": 0, "y": 0, "z": 0}
        self.energy_pe = {"x": 0, "y": 0, "z": 0}
        self.energy_te = {"x": 0, "y": 0, "z": 0}

        self.selected_variables = {}
        self.delete_labels()
        self.particle_variable_group.hide()

    def setup_particle_variable(self, control_information_frame, particle):
        """Configure Partice Properties and Variables"""
        
        self.particle_variable_group = create.create_group_box(
            parent = control_information_frame,
            objname = "particle_variable_group",
            font_size = 18,
            title = "default",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            geometry = QtCore.QRect(10, 80, 930, 270)
        )
        
        self.particle_tab_scroll = create.create_scroll(
            parent = self.particle_variable_group,
            objname = "particle_tab_scroll",
            geometry = QtCore.QRect(0, 30, 931, 241),
            resizable = True
        )
        self.particle_tab_scroll_contents = create.create_widget(
            geometry = QtCore.QRect(0, 0, 912, 408),
            objname = "particle_tab_scroll_contents"
        )
        self.particle_tab_grid = create.create_grid_layout(
            parent = self.particle_tab_scroll_contents,
            objname = "particle_tab_grid"
        )

        # Position

        self.position_tab_group = create.create_group_box(
            parent = self.particle_tab_scroll_contents,
            font_size = 18,
            objname = "position_tab_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Position:"
        )
        self.position_grid = create.create_grid_layout(
            parent = self.position_tab_group,
            objname = "position_grid"
        )
        
        self.pos_axis_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "Axis:",
            objname = "pos_axis_label"
        )
        self.posx_graph_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "X",
            objname = "posx_graph_label"
        )
        self.posy_graph_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "Y",
            objname = "posy_graph_label"
        )
        self.posz_graph_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "Z",
            objname = "posz_axis_label"
        )
        self.posx_value_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "X: 0.0",
            objname = "posx_value_label"
        )
        self.posy_value_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "Y: 0.0",
            objname = "posy_value_label"
        )
        self.posz_value_label = create.create_name_label(
            parent = self.position_tab_group,
            font_size = 16,
            text = "Z: 0.0",
            objname = "posz_value_label"
        )
        
        self.posx_value_buttongroup = QtWidgets.QButtonGroup()
        self.posx_x_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posx_y_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posx_z_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posx_value_buttongroup.addButton(self.posx_x_radio)
        self.posx_value_buttongroup.addButton(self.posx_y_radio)
        self.posx_value_buttongroup.addButton(self.posx_z_radio)

        self.posy_value_buttongroup = QtWidgets.QButtonGroup()
        self.posy_x_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posy_y_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posy_z_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posy_value_buttongroup.addButton(self.posy_x_radio)
        self.posy_value_buttongroup.addButton(self.posy_y_radio)
        self.posy_value_buttongroup.addButton(self.posy_z_radio)

        self.posz_value_buttongroup = QtWidgets.QButtonGroup()
        self.posz_x_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posz_y_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posz_z_radio = create.create_radio(
            parent = self.position_tab_group
        )
        self.posz_value_buttongroup.addButton(self.posz_x_radio)
        self.posz_value_buttongroup.addButton(self.posz_y_radio)
        self.posz_value_buttongroup.addButton(self.posz_z_radio)
        
        self.position_grid.addWidget(self.pos_axis_label, 0, 0, 1, 1)
        self.position_grid.addWidget(self.posx_graph_label, 0, 1, 1, 1)
        self.position_grid.addWidget(self.posy_graph_label, 0, 2, 1, 1)
        self.position_grid.addWidget(self.posz_graph_label, 0, 3, 1, 1)
        self.position_grid.addWidget(self.posx_value_label, 1, 0, 1, 1)
        self.position_grid.addWidget(self.posy_value_label, 2, 0, 1, 1)
        self.position_grid.addWidget(self.posz_value_label, 3, 0, 1, 1)
        self.position_grid.addWidget(self.posx_x_radio, 1, 1, 1, 1)
        self.position_grid.addWidget(self.posx_y_radio, 1, 2, 1, 1)
        self.position_grid.addWidget(self.posx_z_radio, 1, 3, 1, 1)
        self.position_grid.addWidget(self.posy_x_radio, 2, 1, 1, 1)
        self.position_grid.addWidget(self.posy_y_radio, 2, 2, 1, 1)
        self.position_grid.addWidget(self.posy_z_radio, 2, 3, 1, 1)
        self.position_grid.addWidget(self.posz_x_radio, 3, 1, 1, 1)
        self.position_grid.addWidget(self.posz_y_radio, 3, 2, 1, 1)
        self.position_grid.addWidget(self.posz_z_radio, 3, 3, 1, 1)

        self.posx_x_radio.clicked.connect(lambda checked: self.set_position('x', 1, 'x', particle) if checked else None)
        self.posx_y_radio.clicked.connect(lambda checked: self.set_position('y', 1, 'x', particle) if checked else None)
        self.posx_z_radio.clicked.connect(lambda checked: self.set_position('z', 1, 'x', particle) if checked else None)

        self.posy_x_radio.clicked.connect(lambda checked: self.set_position('x', 1, 'y', particle) if checked else None)
        self.posy_y_radio.clicked.connect(lambda checked: self.set_position('y', 1, 'y', particle) if checked else None)
        self.posy_z_radio.clicked.connect(lambda checked: self.set_position('z', 1, 'y', particle) if checked else None)

        self.posz_x_radio.clicked.connect(lambda checked: self.set_position('x', 1, 'z', particle) if checked else None)
        self.posz_y_radio.clicked.connect(lambda checked: self.set_position('y', 1, 'z', particle) if checked else None)
        self.posz_z_radio.clicked.connect(lambda checked: self.set_position('z', 1, 'z', particle) if checked else None)

        self.posx_x_radio.setChecked(bool(self.position_x['x']))
        self.posx_y_radio.setChecked(bool(self.position_x['y']))
        self.posx_z_radio.setChecked(bool(self.position_x['z']))

        self.posy_x_radio.setChecked(bool(self.position_y['x']))
        self.posy_y_radio.setChecked(bool(self.position_y['y']))
        self.posy_z_radio.setChecked(bool(self.position_y['z']))

        self.posz_x_radio.setChecked(bool(self.position_z['x']))
        self.posz_y_radio.setChecked(bool(self.position_z['y']))
        self.posz_z_radio.setChecked(bool(self.position_z['z']))


        #Velocity

        self.velocity_tab_group = create.create_group_box(
            parent = self.particle_tab_scroll_contents,
            font_size = 18,
            objname = "velocity_tab_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Velocity:"
        )
        self.velocity_grid = create.create_grid_layout(
            parent = self.velocity_tab_group,
            objname = "velocity_grid"
        )
        
        self.v_axis_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "Axis:",
            objname = "v_axis_label"
        )
        self.vx_graph_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "X",
            objname = "vx_graph_label"
        )
        self.vy_graph_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "Y",
            objname = "vy_graph_label"
        )
        self.vz_graph_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "Z",
            objname = "vz_axis_label"
        )
        self.vx_value_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "Vx: 0.0",
            objname = "vx_value_label"
        )
        self.vy_value_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "Vy: 0.0",
            objname = "vy_value_label"
        )
        self.vz_value_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "Vz: 0.0",
            objname = "vz_value_label"
        )
        self.v_value_label = create.create_name_label(
            parent = self.velocity_tab_group,
            font_size = 16,
            text = "|V|: 0.0",
            objname = "v_value_label"
        )

        self.vx_value_buttongroup = QtWidgets.QButtonGroup()
        self.vx_x_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vx_y_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vx_z_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vx_value_buttongroup.addButton(self.vx_x_radio)
        self.vx_value_buttongroup.addButton(self.vx_y_radio)
        self.vx_value_buttongroup.addButton(self.vx_z_radio)

        self.vy_value_buttongroup = QtWidgets.QButtonGroup()
        self.vy_x_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vy_y_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vy_z_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vy_value_buttongroup.addButton(self.vy_x_radio)
        self.vy_value_buttongroup.addButton(self.vy_y_radio)
        self.vy_value_buttongroup.addButton(self.vy_z_radio)

        self.vz_value_buttongroup = QtWidgets.QButtonGroup()
        self.vz_x_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vz_y_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vz_z_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.vz_value_buttongroup.addButton(self.vz_x_radio)
        self.vz_value_buttongroup.addButton(self.vz_y_radio)
        self.vz_value_buttongroup.addButton(self.vz_z_radio)

        self.v_value_buttongroup = QtWidgets.QButtonGroup()
        self.v_x_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.v_y_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.v_z_radio = create.create_radio(
            parent = self.velocity_tab_group
        )
        self.v_value_buttongroup.addButton(self.v_x_radio)
        self.v_value_buttongroup.addButton(self.v_y_radio)
        self.v_value_buttongroup.addButton(self.v_z_radio)
        
        self.velocity_grid.addWidget(self.v_axis_label, 0, 0, 1, 1)
        self.velocity_grid.addWidget(self.vx_graph_label, 0, 1, 1, 1)
        self.velocity_grid.addWidget(self.vy_graph_label, 0, 2, 1, 1)
        self.velocity_grid.addWidget(self.vz_graph_label, 0, 3, 1, 1)
        self.velocity_grid.addWidget(self.vx_value_label, 1, 0, 1, 1)
        self.velocity_grid.addWidget(self.vy_value_label, 2, 0, 1, 1)
        self.velocity_grid.addWidget(self.vz_value_label, 3, 0, 1, 1)
        self.velocity_grid.addWidget(self.v_value_label, 4, 0, 1, 1)
        self.velocity_grid.addWidget(self.vx_x_radio, 1, 1, 1, 1)
        self.velocity_grid.addWidget(self.vx_y_radio, 1, 2, 1, 1)
        self.velocity_grid.addWidget(self.vx_z_radio, 1, 3, 1, 1)
        self.velocity_grid.addWidget(self.vy_x_radio, 2, 1, 1, 1)
        self.velocity_grid.addWidget(self.vy_y_radio, 2, 2, 1, 1)
        self.velocity_grid.addWidget(self.vy_z_radio, 2, 3, 1, 1)
        self.velocity_grid.addWidget(self.vz_x_radio, 3, 1, 1, 1)
        self.velocity_grid.addWidget(self.vz_y_radio, 3, 2, 1, 1)
        self.velocity_grid.addWidget(self.vz_z_radio, 3, 3, 1, 1)
        self.velocity_grid.addWidget(self.v_x_radio, 4, 1, 1, 1)
        self.velocity_grid.addWidget(self.v_y_radio, 4, 2, 1, 1)
        self.velocity_grid.addWidget(self.v_z_radio, 4, 3, 1, 1)

        self.vx_x_radio.clicked.connect(lambda checked: self.set_velocity('x', 1, 'x', particle) if checked else None)
        self.vx_y_radio.clicked.connect(lambda checked: self.set_velocity('y', 1, 'x', particle) if checked else None)
        self.vx_z_radio.clicked.connect(lambda checked: self.set_velocity('z', 1, 'x', particle) if checked else None)

        self.vy_x_radio.clicked.connect(lambda checked: self.set_velocity('x', 1, 'y', particle) if checked else None)
        self.vy_y_radio.clicked.connect(lambda checked: self.set_velocity('y', 1, 'y', particle) if checked else None)
        self.vy_z_radio.clicked.connect(lambda checked: self.set_velocity('z', 1, 'y', particle) if checked else None)

        self.vz_x_radio.clicked.connect(lambda checked: self.set_velocity('x', 1, 'z', particle) if checked else None)
        self.vz_y_radio.clicked.connect(lambda checked: self.set_velocity('y', 1, 'z', particle) if checked else None)
        self.vz_z_radio.clicked.connect(lambda checked: self.set_velocity('z', 1, 'z', particle) if checked else None)

        self.v_x_radio.clicked.connect(lambda checked: self.set_velocity('x', 1, 'mag', particle) if checked else None)
        self.v_y_radio.clicked.connect(lambda checked: self.set_velocity('y', 1, 'mag', particle) if checked else None)
        self.v_z_radio.clicked.connect(lambda checked: self.set_velocity('z', 1, 'mag', particle) if checked else None)
        
        self.vx_x_radio.setChecked(bool(self.velocity_x['x']))
        self.vx_y_radio.setChecked(bool(self.velocity_x['y']))
        self.vx_z_radio.setChecked(bool(self.velocity_x['z']))

        self.vy_x_radio.setChecked(bool(self.velocity_y['x']))
        self.vy_y_radio.setChecked(bool(self.velocity_y['y']))
        self.vy_z_radio.setChecked(bool(self.velocity_y['z']))

        self.vz_x_radio.setChecked(bool(self.velocity_z['x']))
        self.vz_y_radio.setChecked(bool(self.velocity_z['y']))
        self.vz_z_radio.setChecked(bool(self.velocity_z['z']))

        self.v_x_radio.setChecked(bool(self.velocity_mag['x']))
        self.v_y_radio.setChecked(bool(self.velocity_mag['y']))
        self.v_z_radio.setChecked(bool(self.velocity_mag['z']))


        # Acceleration

        self.acceleration_tab_group = create.create_group_box(
            parent = self.particle_tab_scroll_contents,
            font_size = 18,
            objname = "acceleration_tab_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Acceleration:"
        )
        self.acceleration_grid = create.create_grid_layout(
            parent = self.acceleration_tab_group,
            objname = "acceleration_grid"
        )
        
        self.a_axis_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "Axis:",
            objname = "a_axis_label"
        )
        self.ax_graph_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "X",
            objname = "ax_graph_label"
        )
        self.ay_graph_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "Y",
            objname = "ay_graph_label"
        )
        self.az_graph_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "Z",
            objname = "az_axis_label"
        )
        self.ax_value_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "Ax: 0.0",
            objname = "ax_value_label"
        )
        self.ay_value_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "Ay: 0.0",
            objname = "ay_value_label"
        )
        self.az_value_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "Az: 0.0",
            objname = "az_value_label"
        )
        self.a_value_label = create.create_name_label(
            parent = self.acceleration_tab_group,
            font_size = 16,
            text = "|A|: 0.0",
            objname = "a_value_label"
        )

        self.ax_value_buttongroup = QtWidgets.QButtonGroup()
        self.ax_x_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.ax_y_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.ax_z_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.ax_value_buttongroup.addButton(self.ax_x_radio)
        self.ax_value_buttongroup.addButton(self.ax_y_radio)
        self.ax_value_buttongroup.addButton(self.ax_z_radio)

        self.ay_value_buttongroup = QtWidgets.QButtonGroup()
        self.ay_x_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.ay_y_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.ay_z_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.ay_value_buttongroup.addButton(self.ay_x_radio)
        self.ay_value_buttongroup.addButton(self.ay_y_radio)
        self.ay_value_buttongroup.addButton(self.ay_z_radio)

        self.az_value_buttongroup = QtWidgets.QButtonGroup()
        self.az_x_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.az_y_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.az_z_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.az_value_buttongroup.addButton(self.az_x_radio)
        self.az_value_buttongroup.addButton(self.az_y_radio)
        self.az_value_buttongroup.addButton(self.az_z_radio)

        self.a_value_buttongroup = QtWidgets.QButtonGroup()
        self.a_x_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.a_y_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.a_z_radio = create.create_radio(
            parent = self.acceleration_tab_group
        )
        self.a_value_buttongroup.addButton(self.a_x_radio)
        self.a_value_buttongroup.addButton(self.a_y_radio)
        self.a_value_buttongroup.addButton(self.a_z_radio)
        
        self.acceleration_grid.addWidget(self.a_axis_label, 0, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ax_graph_label, 0, 1, 1, 1)
        self.acceleration_grid.addWidget(self.ay_graph_label, 0, 2, 1, 1)
        self.acceleration_grid.addWidget(self.az_graph_label, 0, 3, 1, 1)
        self.acceleration_grid.addWidget(self.ax_value_label, 1, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ay_value_label, 2, 0, 1, 1)
        self.acceleration_grid.addWidget(self.az_value_label, 3, 0, 1, 1)
        self.acceleration_grid.addWidget(self.a_value_label, 4, 0, 1, 1)
        self.acceleration_grid.addWidget(self.ax_x_radio, 1, 1, 1, 1)
        self.acceleration_grid.addWidget(self.ax_y_radio, 1, 2, 1, 1)
        self.acceleration_grid.addWidget(self.ax_z_radio, 1, 3, 1, 1)
        self.acceleration_grid.addWidget(self.ay_x_radio, 2, 1, 1, 1)
        self.acceleration_grid.addWidget(self.ay_y_radio, 2, 2, 1, 1)
        self.acceleration_grid.addWidget(self.ay_z_radio, 2, 3, 1, 1)
        self.acceleration_grid.addWidget(self.az_x_radio, 3, 1, 1, 1)
        self.acceleration_grid.addWidget(self.az_y_radio, 3, 2, 1, 1)
        self.acceleration_grid.addWidget(self.az_z_radio, 3, 3, 1, 1)
        self.acceleration_grid.addWidget(self.a_x_radio, 4, 1, 1, 1)
        self.acceleration_grid.addWidget(self.a_y_radio, 4, 2, 1, 1)
        self.acceleration_grid.addWidget(self.a_z_radio, 4, 3, 1, 1)

        self.ax_x_radio.clicked.connect(lambda checked: self.set_acceleration('x', 1, 'x', particle) if checked else None)
        self.ax_y_radio.clicked.connect(lambda checked: self.set_acceleration('y', 1, 'x', particle) if checked else None)
        self.ax_z_radio.clicked.connect(lambda checked: self.set_acceleration('z', 1, 'x', particle) if checked else None)

        self.ay_x_radio.clicked.connect(lambda checked: self.set_acceleration('x', 1, 'y', particle) if checked else None)
        self.ay_y_radio.clicked.connect(lambda checked: self.set_acceleration('y', 1, 'y', particle) if checked else None)
        self.ay_z_radio.clicked.connect(lambda checked: self.set_acceleration('z', 1, 'y', particle) if checked else None)

        self.az_x_radio.clicked.connect(lambda checked: self.set_acceleration('x', 1, 'z', particle) if checked else None)
        self.az_y_radio.clicked.connect(lambda checked: self.set_acceleration('y', 1, 'z', particle) if checked else None)
        self.az_z_radio.clicked.connect(lambda checked: self.set_acceleration('z', 1, 'z', particle) if checked else None)

        self.a_x_radio.clicked.connect(lambda checked: self.set_acceleration('x', 1, 'mag', particle) if checked else None)
        self.a_y_radio.clicked.connect(lambda checked: self.set_acceleration('y', 1, 'mag', particle) if checked else None)
        self.a_z_radio.clicked.connect(lambda checked: self.set_acceleration('z', 1, 'mag', particle) if checked else None)

        self.ax_x_radio.setChecked(bool(self.acceleration_x['x']))
        self.ax_y_radio.setChecked(bool(self.acceleration_x['y']))
        self.ax_z_radio.setChecked(bool(self.acceleration_x['z']))

        self.ay_x_radio.setChecked(bool(self.acceleration_y['x']))
        self.ay_y_radio.setChecked(bool(self.acceleration_y['y']))
        self.ay_z_radio.setChecked(bool(self.acceleration_y['z']))

        self.az_x_radio.setChecked(bool(self.acceleration_z['x']))
        self.az_y_radio.setChecked(bool(self.acceleration_z['y']))
        self.az_z_radio.setChecked(bool(self.acceleration_z['z']))

        self.a_x_radio.setChecked(bool(self.acceleration_mag['x']))
        self.a_y_radio.setChecked(bool(self.acceleration_mag['y']))
        self.a_z_radio.setChecked(bool(self.acceleration_mag['z']))

        # Momentum

        self.momentum_tab_group = create.create_group_box(
            parent = self.particle_tab_scroll_contents,
            font_size = 18,
            objname = "momentum_tab_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Momentum:"
        )
        self.momentum_grid = create.create_grid_layout(
            parent = self.momentum_tab_group,
            objname = "momentum_grid"
        )
        
        self.p_axis_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "Axis:",
            objname = "p_axis_label"
        )
        self.px_graph_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "X",
            objname = "px_graph_label"
        )
        self.py_graph_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "Y",
            objname = "py_graph_label"
        )
        self.pz_graph_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "Z",
            objname = "pz_axis_label"
        )
        self.px_value_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "px: 0.0",
            objname = "px_value_label"
        )
        self.py_value_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "py: 0.0",
            objname = "py_value_label"
        )
        self.pz_value_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "pz: 0.0",
            objname = "pz_value_label"
        )
        self.p_value_label = create.create_name_label(
            parent = self.momentum_tab_group,
            font_size = 16,
            text = "|p|: 0.0",
            objname = "p_value_label"
        )

        self.px_value_buttongroup = QtWidgets.QButtonGroup()
        self.px_x_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.px_y_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.px_z_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.px_value_buttongroup.addButton(self.px_x_radio)
        self.px_value_buttongroup.addButton(self.px_y_radio)
        self.px_value_buttongroup.addButton(self.px_z_radio)

        self.py_value_buttongroup = QtWidgets.QButtonGroup()
        self.py_x_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.py_y_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.py_z_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.py_value_buttongroup.addButton(self.py_x_radio)
        self.py_value_buttongroup.addButton(self.py_y_radio)
        self.py_value_buttongroup.addButton(self.py_z_radio)

        self.pz_value_buttongroup = QtWidgets.QButtonGroup()
        self.pz_x_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.pz_y_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.pz_z_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.pz_value_buttongroup.addButton(self.pz_x_radio)
        self.pz_value_buttongroup.addButton(self.pz_y_radio)
        self.pz_value_buttongroup.addButton(self.pz_z_radio)

        self.p_value_buttongroup = QtWidgets.QButtonGroup()
        self.p_x_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.p_y_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.p_z_radio = create.create_radio(
            parent = self.momentum_tab_group
        )
        self.p_value_buttongroup.addButton(self.p_x_radio)
        self.p_value_buttongroup.addButton(self.p_y_radio)
        self.p_value_buttongroup.addButton(self.p_z_radio)
        
        self.momentum_grid.addWidget(self.p_axis_label, 0, 0, 1, 1)
        self.momentum_grid.addWidget(self.px_graph_label, 0, 1, 1, 1)
        self.momentum_grid.addWidget(self.py_graph_label, 0, 2, 1, 1)
        self.momentum_grid.addWidget(self.pz_graph_label, 0, 3, 1, 1)
        self.momentum_grid.addWidget(self.px_value_label, 1, 0, 1, 1)
        self.momentum_grid.addWidget(self.py_value_label, 2, 0, 1, 1)
        self.momentum_grid.addWidget(self.pz_value_label, 3, 0, 1, 1)
        self.momentum_grid.addWidget(self.p_value_label, 4, 0, 1, 1)
        self.momentum_grid.addWidget(self.px_x_radio, 1, 1, 1, 1)
        self.momentum_grid.addWidget(self.px_y_radio, 1, 2, 1, 1)
        self.momentum_grid.addWidget(self.px_z_radio, 1, 3, 1, 1)
        self.momentum_grid.addWidget(self.py_x_radio, 2, 1, 1, 1)
        self.momentum_grid.addWidget(self.py_y_radio, 2, 2, 1, 1)
        self.momentum_grid.addWidget(self.py_z_radio, 2, 3, 1, 1)
        self.momentum_grid.addWidget(self.pz_x_radio, 3, 1, 1, 1)
        self.momentum_grid.addWidget(self.pz_y_radio, 3, 2, 1, 1)
        self.momentum_grid.addWidget(self.pz_z_radio, 3, 3, 1, 1)
        self.momentum_grid.addWidget(self.p_x_radio, 4, 1, 1, 1)
        self.momentum_grid.addWidget(self.p_y_radio, 4, 2, 1, 1)
        self.momentum_grid.addWidget(self.p_z_radio, 4, 3, 1, 1)

        self.px_x_radio.clicked.connect(lambda checked: self.set_momentum('x', 1, 'x', particle) if checked else None)
        self.px_y_radio.clicked.connect(lambda checked: self.set_momentum('y', 1, 'x', particle) if checked else None)
        self.px_z_radio.clicked.connect(lambda checked: self.set_momentum('z', 1, 'x', particle) if checked else None)

        self.py_x_radio.clicked.connect(lambda checked: self.set_momentum('x', 1, 'y', particle) if checked else None)
        self.py_y_radio.clicked.connect(lambda checked: self.set_momentum('y', 1, 'y', particle) if checked else None)
        self.py_z_radio.clicked.connect(lambda checked: self.set_momentum('z', 1, 'y', particle) if checked else None)

        self.pz_x_radio.clicked.connect(lambda checked: self.set_momentum('x', 1, 'z', particle) if checked else None)
        self.pz_y_radio.clicked.connect(lambda checked: self.set_momentum('y', 1, 'z', particle) if checked else None)
        self.pz_z_radio.clicked.connect(lambda checked: self.set_momentum('z', 1, 'z', particle) if checked else None)

        self.p_x_radio.clicked.connect(lambda checked: self.set_momentum('x', 1, 'mag', particle) if checked else None)
        self.p_y_radio.clicked.connect(lambda checked: self.set_momentum('y', 1, 'mag', particle) if checked else None)
        self.p_z_radio.clicked.connect(lambda checked: self.set_momentum('z', 1, 'mag', particle) if checked else None)

        self.px_x_radio.setChecked(bool(self.momentum_x['x']))
        self.px_y_radio.setChecked(bool(self.momentum_x['y']))
        self.px_z_radio.setChecked(bool(self.momentum_x['z']))

        self.py_x_radio.setChecked(bool(self.momentum_y['x']))
        self.py_y_radio.setChecked(bool(self.momentum_y['y']))
        self.py_z_radio.setChecked(bool(self.momentum_y['z']))

        self.pz_x_radio.setChecked(bool(self.momentum_z['x']))
        self.pz_y_radio.setChecked(bool(self.momentum_z['y']))
        self.pz_z_radio.setChecked(bool(self.momentum_z['z']))

        self.p_x_radio.setChecked(bool(self.momentum_mag['x']))
        self.p_y_radio.setChecked(bool(self.momentum_mag['y']))
        self.p_z_radio.setChecked(bool(self.momentum_mag['z']))

        # Force

        self.force_tab_group = create.create_group_box(
            parent = self.particle_tab_scroll_contents,
            font_size = 18,
            objname = "force_tab_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Force:"
        )
        self.force_grid = create.create_grid_layout(
            parent = self.force_tab_group,
            objname = "force_grid"
        )
        
        self.f_axis_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "Axis:",
            objname = "f_axis_label"
        )
        self.fx_graph_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "X",
            objname = "fx_graph_label"
        )
        self.fy_graph_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "Y",
            objname = "fy_graph_label"
        )
        self.fz_graph_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "Z",
            objname = "fz_graph_label"
        )
        self.fx_value_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "Fx: 0.0",
            objname = "fx_value_label"
        )
        self.fy_value_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "Fy: 0.0",
            objname = "fy_value_label"
        )
        self.fz_value_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "Fz: 0.0",
            objname = "fz_value_label"
        )
        self.f_value_label = create.create_name_label(
            parent = self.force_tab_group,
            font_size = 16,
            text = "|F|: 0.0",
            objname = "f_value_label"
        )

        self.fx_value_buttongroup = QtWidgets.QButtonGroup()
        self.fx_x_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fx_y_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fx_z_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fx_value_buttongroup.addButton(self.fx_x_radio)
        self.fx_value_buttongroup.addButton(self.fx_y_radio)
        self.fx_value_buttongroup.addButton(self.fx_z_radio)

        self.fy_value_buttongroup = QtWidgets.QButtonGroup()
        self.fy_x_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fy_y_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fy_z_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fy_value_buttongroup.addButton(self.fy_x_radio)
        self.fy_value_buttongroup.addButton(self.fy_y_radio)
        self.fy_value_buttongroup.addButton(self.fy_z_radio)

        self.fz_value_buttongroup = QtWidgets.QButtonGroup()
        self.fz_x_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fz_y_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fz_z_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.fz_value_buttongroup.addButton(self.fz_x_radio)
        self.fz_value_buttongroup.addButton(self.fz_y_radio)
        self.fz_value_buttongroup.addButton(self.fz_z_radio)

        self.f_value_buttongroup = QtWidgets.QButtonGroup()
        self.f_x_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.f_y_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.f_z_radio = create.create_radio(
            parent = self.force_tab_group
        )
        self.f_value_buttongroup.addButton(self.f_x_radio)
        self.f_value_buttongroup.addButton(self.f_y_radio)
        self.f_value_buttongroup.addButton(self.f_z_radio)
        
        self.force_grid.addWidget(self.f_axis_label, 0, 0, 1, 1)
        self.force_grid.addWidget(self.fx_graph_label, 0, 1, 1, 1)
        self.force_grid.addWidget(self.fy_graph_label, 0, 2, 1, 1)
        self.force_grid.addWidget(self.fz_graph_label, 0, 3, 1, 1)
        self.force_grid.addWidget(self.fx_value_label, 1, 0, 1, 1)
        self.force_grid.addWidget(self.fy_value_label, 2, 0, 1, 1)
        self.force_grid.addWidget(self.fz_value_label, 3, 0, 1, 1)
        self.force_grid.addWidget(self.f_value_label, 4, 0, 1, 1)
        self.force_grid.addWidget(self.fx_x_radio, 1, 1, 1, 1)
        self.force_grid.addWidget(self.fx_y_radio, 1, 2, 1, 1)
        self.force_grid.addWidget(self.fx_z_radio, 1, 3, 1, 1)
        self.force_grid.addWidget(self.fy_x_radio, 2, 1, 1, 1)
        self.force_grid.addWidget(self.fy_y_radio, 2, 2, 1, 1)
        self.force_grid.addWidget(self.fy_z_radio, 2, 3, 1, 1)
        self.force_grid.addWidget(self.fz_x_radio, 3, 1, 1, 1)
        self.force_grid.addWidget(self.fz_y_radio, 3, 2, 1, 1)
        self.force_grid.addWidget(self.fz_z_radio, 3, 3, 1, 1)
        self.force_grid.addWidget(self.f_x_radio, 4, 1, 1, 1)
        self.force_grid.addWidget(self.f_y_radio, 4, 2, 1, 1)
        self.force_grid.addWidget(self.f_z_radio, 4, 3, 1, 1)

        self.fx_x_radio.clicked.connect(lambda checked: self.set_force('x', 1, 'x', particle) if checked else None)
        self.fx_y_radio.clicked.connect(lambda checked: self.set_force('y', 1, 'x', particle) if checked else None)
        self.fx_z_radio.clicked.connect(lambda checked: self.set_force('z', 1, 'x', particle) if checked else None)

        self.fy_x_radio.clicked.connect(lambda checked: self.set_force('x', 1, 'y', particle) if checked else None)
        self.fy_y_radio.clicked.connect(lambda checked: self.set_force('y', 1, 'y', particle) if checked else None)
        self.fy_z_radio.clicked.connect(lambda checked: self.set_force('z', 1, 'y', particle) if checked else None)

        self.fz_x_radio.clicked.connect(lambda checked: self.set_force('x', 1, 'z', particle) if checked else None)
        self.fz_y_radio.clicked.connect(lambda checked: self.set_force('y', 1, 'z', particle) if checked else None)
        self.fz_z_radio.clicked.connect(lambda checked: self.set_force('z', 1, 'z', particle) if checked else None)

        self.f_x_radio.clicked.connect(lambda checked: self.set_force('x', 1, 'mag', particle) if checked else None)
        self.f_y_radio.clicked.connect(lambda checked: self.set_force('y', 1, 'mag', particle) if checked else None)
        self.f_z_radio.clicked.connect(lambda checked: self.set_force('z', 1, 'mag', particle) if checked else None)

        self.fx_x_radio.setChecked(bool(self.force_x['x']))
        self.fx_y_radio.setChecked(bool(self.force_x['y']))
        self.fx_z_radio.setChecked(bool(self.force_x['z']))

        self.fy_x_radio.setChecked(bool(self.force_y['x']))
        self.fy_y_radio.setChecked(bool(self.force_y['y']))
        self.fy_z_radio.setChecked(bool(self.force_y['z']))

        self.fz_x_radio.setChecked(bool(self.force_z['x']))
        self.fz_y_radio.setChecked(bool(self.force_z['y']))
        self.fz_z_radio.setChecked(bool(self.force_z['z']))

        self.f_x_radio.setChecked(bool(self.force_mag['x']))
        self.f_y_radio.setChecked(bool(self.force_mag['y']))
        self.f_z_radio.setChecked(bool(self.force_mag['z']))

        # Energy

        self.energy_tab_group = create.create_group_box(
            parent = self.particle_tab_scroll_contents,
            font_size = 18,
            objname = "energy_tab_group",
            layout = QtCore.Qt.LeftToRight,
            alignment = QtCore.Qt.AlignCenter,
            title = "Energy:"
        )
        self.energy_grid = create.create_grid_layout(
            parent = self.energy_tab_group,
            objname = "energy_grid"
        )
        
        self.e_type_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "Type:",
            objname = "e_axis_label"
        )
        self.ex_graph_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "X",
            objname = "ex_graph_label"
        )
        self.ey_graph_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "Y",
            objname = "ey_graph_label"
        )
        self.ez_graph_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "Z",
            objname = "ez_axis_label"
        )
        self.ke_value_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "KE: 0.00",
            objname = "ke_value_label"
        )
        self.pe_value_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "PE: 0.00",
            objname = "pe_value_label"
        )
        self.te_value_label = create.create_name_label(
            parent = self.energy_tab_group,
            font_size = 16,
            text = "TE: 0.00",
            objname = "te_value_label"
        )
        
        self.ke_value_buttongroup = QtWidgets.QButtonGroup()
        self.ke_x_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.ke_y_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.ke_z_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.ke_value_buttongroup.addButton(self.ke_x_radio)
        self.ke_value_buttongroup.addButton(self.ke_y_radio)
        self.ke_value_buttongroup.addButton(self.ke_z_radio)

        self.pe_value_buttongroup = QtWidgets.QButtonGroup()
        self.pe_x_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.pe_y_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.pe_z_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.pe_value_buttongroup.addButton(self.pe_x_radio)
        self.pe_value_buttongroup.addButton(self.pe_y_radio)
        self.pe_value_buttongroup.addButton(self.pe_z_radio)

        self.te_value_buttongroup = QtWidgets.QButtonGroup()
        self.te_x_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.te_y_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.te_z_radio = create.create_radio(
            parent = self.energy_tab_group
        )
        self.te_value_buttongroup.addButton(self.te_x_radio)
        self.te_value_buttongroup.addButton(self.te_y_radio)
        self.te_value_buttongroup.addButton(self.te_z_radio)
        
        self.energy_grid.addWidget(self.e_type_label, 0, 0, 1, 1)
        self.energy_grid.addWidget(self.ex_graph_label, 0, 1, 1, 1)
        self.energy_grid.addWidget(self.ey_graph_label, 0, 2, 1, 1)
        self.energy_grid.addWidget(self.ez_graph_label, 0, 3, 1, 1)
        self.energy_grid.addWidget(self.ke_value_label, 1, 0, 1, 1)
        self.energy_grid.addWidget(self.pe_value_label, 2, 0, 1, 1)
        self.energy_grid.addWidget(self.te_value_label, 3, 0, 1, 1)
        self.energy_grid.addWidget(self.ke_x_radio, 1, 1, 1, 1)
        self.energy_grid.addWidget(self.ke_y_radio, 1, 2, 1, 1)
        self.energy_grid.addWidget(self.ke_z_radio, 1, 3, 1, 1)
        self.energy_grid.addWidget(self.pe_x_radio, 2, 1, 1, 1)
        self.energy_grid.addWidget(self.pe_y_radio, 2, 2, 1, 1)
        self.energy_grid.addWidget(self.pe_z_radio, 2, 3, 1, 1)
        self.energy_grid.addWidget(self.te_x_radio, 3, 1, 1, 1)
        self.energy_grid.addWidget(self.te_y_radio, 3, 2, 1, 1)
        self.energy_grid.addWidget(self.te_z_radio, 3, 3, 1, 1)

        self.ke_x_radio.clicked.connect(lambda checked: self.set_energy('x', 1, 'ke', particle) if checked else None)
        self.ke_y_radio.clicked.connect(lambda checked: self.set_energy('y', 1, 'ke', particle) if checked else None)
        self.ke_z_radio.clicked.connect(lambda checked: self.set_energy('z', 1, 'ke', particle) if checked else None)

        self.pe_x_radio.clicked.connect(lambda checked: self.set_energy('x', 1, 'pe', particle) if checked else None)
        self.pe_y_radio.clicked.connect(lambda checked: self.set_energy('y', 1, 'pe', particle) if checked else None)
        self.pe_z_radio.clicked.connect(lambda checked: self.set_energy('z', 1, 'pe', particle) if checked else None)

        self.te_x_radio.clicked.connect(lambda checked: self.set_energy('x', 1, 'te', particle) if checked else None)
        self.te_y_radio.clicked.connect(lambda checked: self.set_energy('y', 1, 'te', particle) if checked else None)
        self.te_z_radio.clicked.connect(lambda checked: self.set_energy('z', 1, 'te', particle) if checked else None)

        self.ke_x_radio.setChecked(bool(self.energy_ke['x']))
        self.ke_y_radio.setChecked(bool(self.energy_ke['y']))
        self.ke_z_radio.setChecked(bool(self.energy_ke['z']))

        self.pe_x_radio.setChecked(bool(self.energy_pe['x']))
        self.pe_y_radio.setChecked(bool(self.energy_pe['y']))
        self.pe_z_radio.setChecked(bool(self.energy_pe['z']))

        self.te_x_radio.setChecked(bool(self.energy_te['x']))
        self.te_y_radio.setChecked(bool(self.energy_te['y']))
        self.te_z_radio.setChecked(bool(self.energy_te['z']))


        self.particle_tab_grid.addWidget(self.position_tab_group, 0, 0, 1, 1)
        self.particle_tab_grid.addWidget(self.velocity_tab_group, 0, 1, 1, 1)
        self.particle_tab_grid.addWidget(self.acceleration_tab_group, 0, 2, 1, 1)
        self.particle_tab_grid.addWidget(self.momentum_tab_group, 1, 0, 1, 1)
        self.particle_tab_grid.addWidget(self.force_tab_group, 1, 1, 1, 1)
        self.particle_tab_grid.addWidget(self.energy_tab_group, 1, 2, 1, 1)

        self.particle_tab_scroll.setWidget(self.particle_tab_scroll_contents)
        self.particle_variable_group.hide()