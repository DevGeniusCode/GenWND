# --- START OF FILE visual_preview.py ---
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPainter
from PyQt6.QtCore import Qt, pyqtSignal


class WndGraphicsItem(QGraphicsRectItem):
    def __init__(self, window, view, w, h):
        super().__init__(0, 0, w, h)
        self.window = window
        self.window_uuid = window.window_uuid
        self.view = view
        self.original_z = 0

        # Enable Interactivity
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        # Default Styling
        self.default_brush = QBrush(QColor(100, 150, 255, 40))
        self.default_pen = QPen(QColor(100, 150, 255, 200), 1)

        # Selected Styling (Thick red border)
        self.selected_pen = QPen(QColor(255, 50, 50, 255), 2)

        self.setBrush(self.default_brush)
        self.setPen(self.default_pen)

    def itemChange(self, change, value):
        # Handle Selection Visuals
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            if self.isSelected():
                self.setPen(self.selected_pen)
                self.setZValue(self.original_z + 1000)  # Bring to front
            else:
                self.setPen(self.default_pen)
                self.setZValue(self.original_z)  # Restore Z order

        # Handle Dragging
        elif change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.scene() and not self.view._is_syncing:
                new_pos = self.pos()
                rect = self.rect()
                new_ul = (int(new_pos.x()), int(new_pos.y()))
                new_br = (int(new_pos.x() + rect.width()), int(new_pos.y() + rect.height()))
                self.view.handle_item_moved(self.window, new_ul, new_br)

        return super().itemChange(change, value)


class VisualPreview(QGraphicsView):
    item_selected_signal = pyqtSignal(str)
    item_moved_signal = pyqtSignal(object, tuple, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))

        self.items_map = {}
        self._is_syncing = False  # Guard to prevent infinite recursion

        # Connect Scene Selection
        self.scene.selectionChanged.connect(self.handle_selection_changed)

    def clear(self):
        self.scene.clear()
        self.items_map.clear()

    def handle_selection_changed(self):
        if self._is_syncing:
            return
        selected = self.scene.selectedItems()
        if selected and isinstance(selected[0], WndGraphicsItem):
            self.item_selected_signal.emit(selected[0].window_uuid)

    def handle_item_moved(self, window, new_ul, new_br):
        self.item_moved_signal.emit(window, new_ul, new_br)

    def select_item(self, uuid):
        """Called externally to highlight an item on the canvas."""
        self._is_syncing = True
        self.scene.clearSelection()
        if uuid in self.items_map:
            item = self.items_map[uuid]
            item.setSelected(True)
            self.ensureVisible(item)
        self._is_syncing = False

    def update_item_geometry_from_data(self, window):
        """Called externally when spinboxes change the size/pos."""
        if not window or window.window_uuid not in self.items_map:
            return

        self._is_syncing = True
        item = self.items_map[window.window_uuid]
        ul = window.properties['SCREENRECT'].get('UPPERLEFT', [0, 0])
        br = window.properties['SCREENRECT'].get('BOTTOMRIGHT', [0, 0])

        w = br[0] - ul[0]
        h = br[1] - ul[1]

        # Update Pos (X, Y) and Rect (Width, Height)
        if w > 0 and h > 0:
            item.setPos(ul[0], ul[1])
            item.setRect(0, 0, w, h)
        self._is_syncing = False

    def load_hierarchy(self, windows):
        self.clear()
        if not windows:
            return

        res_w, res_h = 800, 600
        if 'SCREENRECT' in windows[0].properties:
            res = windows[0].properties['SCREENRECT'].get('CREATIONRESOLUTION', [800, 600])
            res_w, res_h = res[0], res[1]

        bg_rect = QGraphicsRectItem(0, 0, res_w, res_h)
        bg_rect.setBrush(QBrush(QColor(50, 50, 50)))
        bg_rect.setPen(QPen(QColor(255, 255, 255), 2))
        bg_rect.setZValue(-1)
        self.scene.addItem(bg_rect)
        self.scene.setSceneRect(-100, -100, res_w + 200, res_h + 200)

        self._render_windows(windows, depth=1)

    def _render_windows(self, windows, depth):
        for window in windows:
            props = window.properties
            screenrect = props.get('SCREENRECT')

            if screenrect:
                ul = screenrect.get('UPPERLEFT', [0, 0])
                br = screenrect.get('BOTTOMRIGHT', [0, 0])
                w = br[0] - ul[0]
                h = br[1] - ul[1]

                if w > 0 and h > 0:
                    rect_item = WndGraphicsItem(window, self, w, h)
                    rect_item.setPos(ul[0], ul[1])
                    rect_item.original_z = depth
                    rect_item.setZValue(depth)

                    # Keep track for synchronization
                    self.items_map[window.window_uuid] = rect_item

                    name = props.get('NAME', 'Unnamed')
                    wtype = props.get('WINDOWTYPE', 'UNKNOWN')
                    label = QGraphicsTextItem(f"{wtype}: {name}")
                    label.setParentItem(rect_item)
                    label.setPos(2, 2)
                    label.setDefaultTextColor(QColor(255, 255, 255))
                    label.setFont(QFont("Arial", 8, QFont.Weight.Bold))

                    self.scene.addItem(rect_item)

            if hasattr(window, 'children') and window.children:
                self._render_windows(window.children, depth + 1)