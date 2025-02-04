from PyQt5 import QtCore, QtWidgets

class ResolutionScaler:
    """Handles UI scaling across different screen resolutions relative to 1920x1080 base"""
    
    def __init__(self, base_width=1920, base_height=1080):
        self.base_width = base_width
        self.base_height = base_height
        
    def get_scaling_factors(self):
        """Calculate scaling factors based on the current screen resolution relative to base dimensions"""
        screen = QtWidgets.QApplication.primaryScreen()
        size = screen.size()
        width_scale = size.width() / self.base_width
        height_scale = size.height() / self.base_height
        return width_scale, height_scale
    
    def scale_rect(self, rect):
        """Scale a QRect based on current screen resolution"""

        width_scale, height_scale = self.get_scaling_factors()
        
        return QtCore.QRect(
            int(rect.x() * width_scale),
            int(rect.y() * height_scale),
            int(rect.width() * width_scale),
            int(rect.height() * height_scale)
        )
    
    def scale_font_size(self, size):
        """Scale font size based on current screen resolution"""

        width_scale, height_scale = self.get_scaling_factors()
        # Use the smaller scaling factor to ensure text remains readable
        scale = min(width_scale, height_scale)
        return int(size * scale)

    def scale_size(self, width, height):
        """Scale width and height size based on current screen resolution"""

        width_scale, height_scale = self.get_scaling_factors()
        return int(width * width_scale), int(height * height_scale)