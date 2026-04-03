# --- START OF FILE commands.py ---
from PyQt6.QtGui import QUndoCommand


class CommandChangeGeometry(QUndoCommand):
    """Command to handle moving and resizing window objects."""

    def __init__(self, main_window, window_uuid, old_ul, old_br, new_ul, new_br, description="Change Geometry"):
        super().__init__(description)
        self.main_window = main_window
        self.window_uuid = window_uuid
        self.old_ul = old_ul
        self.old_br = old_br
        self.new_ul = new_ul
        self.new_br = new_br

    def redo(self):
        self._apply_geometry(self.new_ul, self.new_br)

    def undo(self):
        self._apply_geometry(self.old_ul, self.old_br)

    def _apply_geometry(self, ul, br):
        # Find the window object recursively from the model
        window = self.main_window.object_tree.model._find_window_by_uuid(self.main_window.parser.get_windows(),
                                                                         self.window_uuid)
        if not window:
            return

        # 1. Update the underlying data dictionary
        if 'SCREENRECT' not in window.properties:
            window.properties['SCREENRECT'] = {}
        window.properties['SCREENRECT']['UPPERLEFT'] = list(ul)
        window.properties['SCREENRECT']['BOTTOMRIGHT'] = list(br)

        self.main_window.update_modified_state(True)

        # 2. Update Canvas visual representation
        if hasattr(self.main_window, 'visual_preview'):
            self.main_window.visual_preview.update_item_geometry_from_data(window)

        # 3. Update Property Editor spinboxes (only if this object is currently selected)
        if getattr(self.main_window, 'selected_object',
                   None) and self.main_window.selected_object.window_uuid == self.window_uuid:
            if hasattr(self.main_window.property_editor, 'general_properties'):
                gp = self.main_window.property_editor.general_properties

                # Block signals temporarily to prevent infinite feedback loops
                gp.upper_left_x_spinbox.blockSignals(True)
                gp.upper_left_y_spinbox.blockSignals(True)
                gp.bottom_right_x_spinbox.blockSignals(True)
                gp.bottom_right_y_spinbox.blockSignals(True)

                gp.upper_left_x_spinbox.setValue(ul[0])
                gp.upper_left_y_spinbox.setValue(ul[1])
                gp.bottom_right_x_spinbox.setValue(br[0])
                gp.bottom_right_y_spinbox.setValue(br[1])

                gp.upper_left_x_spinbox.blockSignals(False)
                gp.upper_left_y_spinbox.blockSignals(False)
                gp.bottom_right_x_spinbox.blockSignals(False)
                gp.bottom_right_y_spinbox.blockSignals(False)


class CommandChangeProperty(QUndoCommand):
    """Command to handle changing standard text/value properties."""

    def __init__(self, main_window, window_uuid, prop_key, old_value, new_value, description="Change Property"):
        super().__init__(description)
        self.main_window = main_window
        self.window_uuid = window_uuid
        self.prop_key = prop_key
        self.old_value = old_value
        self.new_value = new_value

    def redo(self):
        self._apply_property(self.new_value)

    def undo(self):
        self._apply_property(self.old_value)

    def _apply_property(self, val):
        window = self.main_window.object_tree.model._find_window_by_uuid(self.main_window.parser.get_windows(),
                                                                         self.window_uuid)
        if not window:
            return

        window.properties[self.prop_key] = val
        self.main_window.update_modified_state(True)

        # Reload the property editor UI if this object is selected
        if getattr(self.main_window, 'selected_object',
                   None) and self.main_window.selected_object.window_uuid == self.window_uuid:
            self.main_window.load_object_property()