# --- START OF FILE commands.py ---
from PyQt6.QtGui import QUndoCommand

class CommandAddObject(QUndoCommand):
    def __init__(self, main_window, new_object, parent_uuid, insert_index, description="Add Object"):
        super().__init__(description)
        self.main_window = main_window
        self.new_object = new_object
        self.parent_uuid = parent_uuid
        self.insert_index = insert_index

    def redo(self):
        windows = self.main_window.parser.get_windows()
        parent = self.main_window.object_tree.model._find_window_by_uuid(windows,
                                                                         self.parent_uuid) if self.parent_uuid else None

        if parent:
            if not hasattr(parent, "children"):
                parent.children = []
            parent.children.insert(self.insert_index, self.new_object)
        else:
            windows.insert(self.insert_index, self.new_object)

        self.main_window.update_modified_state(True)
        self.main_window.handle_object_added(self.new_object)

    def undo(self):
        windows = self.main_window.parser.get_windows()
        parent = self.main_window.object_tree.model._find_window_by_uuid(windows,
                                                                         self.parent_uuid) if self.parent_uuid else None

        if parent and hasattr(parent, "children"):
            parent.children.remove(self.new_object)
        elif self.new_object in windows:
            windows.remove(self.new_object)

        self.main_window.update_modified_state(True)
        self.main_window.handle_object_deleted(self.new_object.window_uuid)


class CommandDeleteObject(QUndoCommand):
    def __init__(self, main_window, target_object, parent_uuid, insert_index, description="Delete Object"):
        super().__init__(description)
        self.main_window = main_window
        self.target_object = target_object
        self.parent_uuid = parent_uuid
        self.insert_index = insert_index

    def redo(self):
        windows = self.main_window.parser.get_windows()
        parent = self.main_window.object_tree.model._find_window_by_uuid(windows,
                                                                         self.parent_uuid) if self.parent_uuid else None

        if parent and hasattr(parent, "children"):
            parent.children.remove(self.target_object)
        elif self.target_object in windows:
            windows.remove(self.target_object)

        self.main_window.update_modified_state(True)
        self.main_window.handle_object_deleted(self.target_object.window_uuid)

    def undo(self):
        windows = self.main_window.parser.get_windows()
        parent = self.main_window.object_tree.model._find_window_by_uuid(windows,
                                                                         self.parent_uuid) if self.parent_uuid else None

        if parent:
            if not hasattr(parent, "children"):
                parent.children = []
            parent.children.insert(self.insert_index, self.target_object)
        else:
            windows.insert(self.insert_index, self.target_object)

        self.main_window.update_modified_state(True)
        self.main_window.handle_object_added(self.target_object)


class CommandMoveObject(QUndoCommand):
    def __init__(self, main_window, window_uuid, target_parent_uuid, target_row, description="Move Object"):
        super().__init__(description)
        self.main_window = main_window
        self.window_uuid = window_uuid
        self.target_parent_uuid = target_parent_uuid
        self.target_row = target_row

        self.old_parent_uuid = None
        self.old_row = -1
        self.first_run = True

    def redo(self):
        windows = self.main_window.parser.get_windows()
        tree_model = self.main_window.object_tree.model
        window = tree_model._find_window_by_uuid(windows, self.window_uuid)
        if not window: return

        if self.first_run:
            old_parent = tree_model._find_window_parent(windows, self.window_uuid)
            self.old_parent_uuid = old_parent.window_uuid if old_parent else None
            old_list = getattr(old_parent, 'children', windows) if old_parent else windows
            self.old_row = old_list.index(window)
            self.first_run = False

        # Remove from old location
        old_parent = tree_model._find_window_by_uuid(windows, self.old_parent_uuid) if self.old_parent_uuid else None
        old_list = getattr(old_parent, 'children', windows) if old_parent else windows
        old_list.remove(window)

        # Insert into new location
        new_parent = tree_model._find_window_by_uuid(windows, self.target_parent_uuid) if self.target_parent_uuid else None
        if new_parent and not hasattr(new_parent, 'children'): new_parent.children = []
        new_list = getattr(new_parent, 'children', windows) if new_parent else windows
        new_list.insert(min(self.target_row, len(new_list)), window)

        self.main_window.object_tree._refresh_tree_state()

    def undo(self):
        windows = self.main_window.parser.get_windows()
        tree_model = self.main_window.object_tree.model
        window = tree_model._find_window_by_uuid(windows, self.window_uuid)
        if not window: return

        # Reverse operations exactly
        new_parent = tree_model._find_window_by_uuid(windows, self.target_parent_uuid) if self.target_parent_uuid else None
        getattr(new_parent, 'children', windows).remove(window) if new_parent else windows.remove(window)
        old_parent = tree_model._find_window_by_uuid(windows, self.old_parent_uuid) if self.old_parent_uuid else None
        if old_parent and not hasattr(old_parent, 'children'): old_parent.children = []
        old_list = getattr(old_parent, 'children', windows) if old_parent else windows
        old_list.insert(self.old_row, window)

        self.main_window.object_tree._refresh_tree_state()


class CommandChangeGeometry(QUndoCommand):
    """Command to change the position/size of an object with rapid-input merging."""

    def __init__(self, main_window, window_uuid, old_ul, old_br, new_ul, new_br):
        super().__init__("Change Geometry")
        self.main_window = main_window
        self.window_uuid = window_uuid

        self.old_ul = list(old_ul)
        self.old_br = list(old_br)
        self.new_ul = list(new_ul)
        self.new_br = list(new_br)

    def id(self):
        """Returns a unique ID so Qt knows which commands can be merged."""
        # Constrain hash to 32-bit signed integer range
        hash_val = hash(self.window_uuid) & 0x7FFFFFFF  # Keep only positive values
        return 1100 + (hash_val % 1000000)

    def mergeWith(self, command):
        """Compresses rapid spinbox inputs into a single Undo action."""
        if command.id() != self.id():
            return False

        # Update our 'new' state to the incoming command's state, preserving the original 'old' state
        self.new_ul = command.new_ul
        self.new_br = command.new_br
        return True

    def _sync_system_state(self, is_undo):
        """Helper to apply data and synchronize the Canvas and UI without duplicating code."""
        self.main_window._is_undoing = True

        ul = self.old_ul if is_undo else self.new_ul
        br = self.old_br if is_undo else self.new_br

        # 1. Update the underlying data model
        window = self.main_window.object_tree.model._find_window_by_uuid(
            self.main_window.object_tree.model.parser_windows, self.window_uuid
        )
        if window:
            if 'SCREENRECT' not in window.properties:
                window.properties['SCREENRECT'] = {}
            window.properties['SCREENRECT']['UPPERLEFT'] = ul
            window.properties['SCREENRECT']['BOTTOMRIGHT'] = br

            # 2. Instantly update Canvas graphics
            if hasattr(self.main_window, 'visual_preview'):
                self.main_window.visual_preview.update_item_geometry_from_data(window)

            # 3. Synchronize Property Editor UI if the item is currently selected
            if self.main_window.selected_object and self.main_window.selected_object.window_uuid == self.window_uuid:
                self.main_window._is_syncing = True
                gp = self.main_window.property_editor.general_properties
                gp.upper_left_x_spinbox.setValue(ul[0])
                gp.upper_left_y_spinbox.setValue(ul[1])
                gp.bottom_right_x_spinbox.setValue(br[0])
                gp.bottom_right_y_spinbox.setValue(br[1])
                gp.width_spinbox.setValue(max(0, br[0] - ul[0]))
                gp.height_spinbox.setValue(max(0, br[1] - ul[1]))
                self.main_window._is_syncing = False

        self.main_window.update_modified_state(True)
        self.main_window._is_undoing = False

    def redo(self):
        self._sync_system_state(is_undo=False)

    def undo(self):
        self._sync_system_state(is_undo=True)

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

        # Set a flag to prevent UI property syncs from creating feedback loops in the Undo Stack
        self.main_window._is_undoing = True
        try:
            # Reload the property editor UI if this object is selected
            if getattr(self.main_window, 'selected_object',
                       None) and self.main_window.selected_object.window_uuid == self.window_uuid:
                self.main_window.load_object_property()
        finally:
            self.main_window._is_undoing = False
