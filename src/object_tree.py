from PyQt6.QtWidgets import QTreeView, QLabel, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QDrag, QCursor
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QByteArray, QDataStream, QIODevice

class ObjectTree(QWidget):
    # Signal to notify when an object is selected
    object_selected_signal = pyqtSignal(object)

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Object Tree"])

        # Create the tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        # Enable drag and drop
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.setDragDropMode(QTreeView.DragDropMode.InternalMove)

        # Set up signal for item selection
        self.tree_view.selectionModel().selectionChanged.connect(self.on_item_selected)
        self.tree_view.setVisible(False)

        # Create a label to display when there's no content or error
        self.empty_label = QLabel("Select a file to display its Windows.", self)
        self.empty_label.setObjectName("emptyLabel")
        self.empty_label.setWordWrap(True)
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create buttons for saving and resetting
        self.save_button = QPushButton("Save to file")
        self.reset_button = QPushButton("Reset from file")
        self.save_button.setVisible(False)  # Disable until a file is selected
        self.reset_button.setVisible(False)

        # Create the button layout at the bottom
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)

        # Create the tree layout
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree_view)
        self.tree_layout.addLayout(self.button_layout)

        # Create the main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.empty_label)
        self.layout.addLayout(self.tree_layout)
        self.layout.setStretch(0, 1)

        # Connect buttons to their functions
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.update_buttons_state()
        self.parser_windows = []  # Store the original windows data

        # **NEW:** Replace the default event handlers:
        self.tree_view.startDrag = self.startDrag
        self.tree_view.dragEnterEvent = self.dragEnterEvent
        self.tree_view.dragMoveEvent = self.dragMoveEvent
        self.tree_view.dropEvent = self.dropEvent
        self.tree_view.dragLeaveEvent = self.dragLeaveEvent # new

    def load_objects(self, windows):
        """Load the windows into the tree view."""
        if not windows:
            raise ValueError("Empty or invalid file")

        # Hide the empty label and show the buttons if there are file windows
        self.empty_label.setVisible(False)
        self.save_button.setVisible(True)
        self.reset_button.setVisible(True)
        self.tree_view.setVisible(True)
        self.parser_windows = windows
        self.model.clear()
        self._populate_tree(windows, self.model)

    def _populate_tree(self, windows, parent_item):
        """
        Recursively populate the tree with windows and their children.
        :param windows: List of Window objects
        :param parent_item: Parent item in the tree to append items
        """
        for window in windows:
            item = QStandardItem(f"{window.properties.get('WINDOWTYPE')} - {window.properties.get('NAME', 'Unnamed')}")
            item.setData(window)
            parent_item.appendRow(item)
            if hasattr(window, 'children'):
                self._populate_tree(window.children, item)
        self.tree_view.expandAll()

    def on_item_selected(self, selected, deselected):
        """
        Handle item selection changes in the object tree.
        """
        selected_indexes = self.tree_view.selectedIndexes()
        if selected_indexes:
            # Get the selected item
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            selected_object = selected_item.data()
            self.object_selected_signal.emit(selected_object)

    def display_error(self, error_message):
        """
        Display an error message in the object tree.
        :param error_message: The error message to display.
        """
        # Clear the model to ensure no old data is left
        self.model.clear()
        self.empty_label.setVisible(False)
        self.tree_view.setVisible(True)

        # Create an error item to show in the tree
        error_item = QStandardItem("Error")
        error_item.setForeground(QColor("red"))
        error_item.setEditable(False)

        # Add the error message as a child item
        error_message_item = QStandardItem(error_message)
        error_message_item.setEditable(False)
        error_item.appendRow(error_message_item)

        # Add the error item as the root item of the model
        self.model.appendRow(error_item)

        # Optionally expand the error item so it's visible
        self.tree_view.expandAll()

    def clear(self):
        self.model.clear()
        self.empty_label.setVisible(True)
        self.save_button.setVisible(False)
        self.reset_button.setVisible(False)
        self.tree_view.setVisible(False)

    def on_save_button_clicked(self):
        """
        Handle save button click event. Calls the save_file function from the main window.
        """
        self.main_window.save_file()

    def on_reset_button_clicked(self):
        """
        Handle reset button click event. Calls the load_wnd_file function from the main window.
        """
        selected_file = self.main_window.selected_file
        self.main_window.load_wnd_file(selected_file)

    def update_buttons_state(self):
        """
        Update the state of the save and reset buttons based on the is_modified flag.
        """
        is_modified = getattr(self.main_window, "is_modified", False)
        if is_modified:
            self.save_button.setEnabled(True)
            self.reset_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)
            self.reset_button.setEnabled(False)

    def startDrag(self, supportedActions: Qt.DropAction) -> None:
        # Get the selected item
        selected_indexes = self.tree_view.selectedIndexes()
        if not selected_indexes:
            return

        selected_item = self.model.itemFromIndex(selected_indexes[0])
        selected_window = selected_item.data()
        #log
        message = f"startDrag - selected item: {selected_window.properties.get('NAME')}"
        self.main_window.log_manager.log(message)

        # Convert window data to byte array for drag and drop
        mime_data = QMimeData()
        data = QByteArray()
        stream = QDataStream(data, QDataStream.OpenModeFlag.WriteOnly)
        encoded_uuid = selected_window.window_uuid.encode('utf-8')
        stream.writeBytes(encoded_uuid)

        mime_data.setData('application/x-window-object', data)
        drag = QDrag(self.tree_view)
        drag.setMimeData(mime_data)
        drag.exec(supportedActions)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-window-object'):
            event.acceptProposedAction()
            drop_index = self.tree_view.indexAt(event.position().toPoint())
            drop_item = self.model.itemFromIndex(drop_index)
            if drop_item:
                drop_window = drop_item.data()
                if drop_window:
                   data = event.mimeData().data('application/x-window-object')
                   stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)

                   source_window_uuid_bytes = stream.readBytes()
                   source_window_uuid = source_window_uuid_bytes.decode('utf-8')

                   source_window = self._find_window_by_uuid(self.parser_windows, source_window_uuid)
                   if source_window and source_window.properties.get('WINDOWTYPE') == 'USER':
                       if self.is_ancestor(source_window, drop_window) or self.is_ancestor(drop_window, source_window) :
                           event.ignore()
                           self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
                           return
        else:
            event.ignore()
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-window-object'):
            drop_index = self.tree_view.indexAt(event.position().toPoint())
            drop_item = self.model.itemFromIndex(drop_index)

            if drop_item:
                 drop_window = drop_item.data()
                 if drop_window:
                    data = event.mimeData().data('application/x-window-object')
                    stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)

                    source_window_uuid_bytes = stream.readBytes()
                    source_window_uuid = source_window_uuid_bytes.decode('utf-8')

                    source_window = self._find_window_by_uuid(self.parser_windows, source_window_uuid)
                    if source_window and source_window.properties.get('WINDOWTYPE') == 'USER':
                        if self.is_ancestor(source_window, drop_window) or self.is_ancestor(drop_window, source_window):
                            event.ignore()
                            self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
                            return
        else:
            event.ignore()
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        event.acceptProposedAction()

    def dropEvent(self, event):
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor)) # Reset the cursor on drop
        if event.mimeData().hasFormat('application/x-window-object'):
            data = event.mimeData().data('application/x-window-object')
            stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)

            source_window_uuid_bytes = stream.readBytes()
            source_window_uuid = source_window_uuid_bytes.decode('utf-8')

            # Get drop target
            drop_index = self.tree_view.indexAt(event.position().toPoint())
            drop_item = self.model.itemFromIndex(drop_index)

            if drop_item:
                drop_window = drop_item.data()
                if not drop_window:
                    self.main_window.log_manager.log(f"dropEvent - no drop window, cannot reorder", level="WARNING")
                    drop_window = None # to be root
                    self.main_window.log_manager.log(f"dropEvent - adding to root as fallback")

                # Check if the drop window are parent (USER)
                if drop_window and drop_window.properties.get('WINDOWTYPE') != 'USER':
                    self.main_window.log_manager.log(f"dropEvent - drop window not user, adding as sibling", level="INFO")
                    source_parent = self._find_window_parent(self.parser_windows, drop_window.window_uuid)
                    if source_parent:
                        drop_window = source_parent
                    else:
                         drop_window = None # to be root
            else:  # dropped on the root
                drop_window = None  # root

            if drop_window:
                 self.main_window.log_manager.log(f"dropEvent - source window: {drop_window.properties.get('NAME')}")
            else:
                 self.main_window.log_manager.log(f"dropEvent - adding to root")

            self.reorder_windows(source_window_uuid, drop_window)

            event.acceptProposedAction()
            self.main_window.update_modified_state(True)
            self.update_buttons_state()
            self.model.clear()
            self._populate_tree(self.parser_windows, self.model)

    def reorder_windows(self, source_window_uuid, drop_window):

        """Reorder the windows data based on drag and drop"""
        source_window = self._find_window_by_uuid(self.parser_windows, source_window_uuid)
        if not source_window:
            self.main_window.log_manager.log(f"reorder_windows - no source window of uuid {source_window_uuid}",
                                             level="WARNING")
            return

        # Remove the window from its parent
        source_parent_children = self._find_window_parent_children(self.parser_windows, source_window_uuid)
        if source_parent_children:
            source_parent_children.remove(source_window)
            self.main_window.log_manager.log(f"reorder_windows - removed from parent")
            # Reset the list if its empty
            if not source_parent_children:
                source_parent = self._find_window_parent(self.parser_windows, source_window_uuid)
                if source_parent:
                    source_parent.pop('children', None)
        # Add to the new parent
        if drop_window:
            if not hasattr(drop_window, 'children'):
                drop_window.children = []
            drop_window.children.append(source_window)
            self.main_window.log_manager.log(f"reorder_windows - added to new parent: {drop_window.properties.get('NAME')}")

        else:  # Adding to the root
            self.parser_windows.append(source_window)
            self.main_window.log_manager.log(f"reorder_windows - added to root")

        self.main_window.log_manager.log(f"reorder_windows - reordered")

    def _find_window_by_uuid(self, windows, window_uuid):
        """Recursive function to find a window by uuid"""
        for window in windows:
            if window.window_uuid == window_uuid:
                return window
        for window in windows:
            if hasattr(window, 'children'):
                found_window = self._find_window_by_uuid(window.children, window_uuid)
                if found_window:
                    return found_window
        return None

    def _find_window_parent_children(self, windows, window_uuid):
        for window in windows:
            if hasattr(window, 'children'):
                for child in window.children:
                    if child.window_uuid == window_uuid:
                        self.main_window.log_manager.log(f"parent found: {window.properties.get('NAME')}, uuid: {window.window_uuid}")
                        return window.children
        for window in windows:
            if hasattr(window, 'children'):
                found_children = self._find_window_parent_children(window.children, window_uuid)
                if found_children:
                    return found_children
        return None

    def _find_window_parent(self, windows, window_uuid):
        for window in windows:
            if hasattr(window, 'children'):
                for child in window.children:
                    if child.window_uuid == window_uuid:
                        self.main_window.log_manager.log(f"parent found: {window.properties.get('NAME')},"
                                                         f" uuid: {window.window_uuid}")
                        return window
        for window in windows:
            if hasattr(window, 'children'):
                found_parent = self._find_window_parent(window.children, window_uuid)
                if found_parent:
                    return found_parent
        return None

    def is_ancestor(self, potential_ancestor, potential_descendant):
        """
        Check if potential_descendant is a descendant of potential_ancestor
        or they are the same object
        """
        if potential_ancestor == potential_descendant:
            return True

        def _recursive_check(parent, descendant):
            if hasattr(parent, 'children'):
                 for child in parent.children:
                    if child == descendant:
                       return True
                    if _recursive_check(child, descendant):
                        return True
            return False

        return _recursive_check(potential_ancestor, potential_descendant)

    def dragLeaveEvent(self, event):
      self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))