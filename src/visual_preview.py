from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QToolBar, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem, QSlider,
    QLabel, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPainter, QAction
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF, QLineF


class WndGraphicsItem(QGraphicsRectItem):
    """Represents a selectable, draggable, and resizable WND object on the canvas."""
    HANDLE_SIZE = 8

    def __init__(self, window, preview_widget, width, height):
        super().__init__(0, 0, width, height)
        self.window = window
        self.window_uuid = window.window_uuid
        self.preview_widget = preview_widget
        self.original_z = 0

        # Enable Interactivity
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        # Default Styling
        self.default_brush = QBrush(QColor(100, 150, 255, 40))
        self.default_pen = QPen(QColor(100, 150, 255, 200), 1)
        self.selected_pen = QPen(QColor(255, 50, 50, 255), 2)

        self.setBrush(self.default_brush)
        self.setPen(self.default_pen)

        # Resize State
        self.active_handle = None
        self.is_resizing = False

    def boundingRect(self):
        """Expand the bounding rectangle to encompass the resize handles to prevent graphical ghosting."""
        margin = (self.HANDLE_SIZE / 2) + self.pen().widthF()
        return self.rect().adjusted(-margin, -margin, margin, margin)

    def hoverMoveEvent(self, event):
        """Change the cursor when hovering over resize handles."""
        if self.isSelected():
            handle = self._get_handle_at(event.pos())
            if handle in ('TL', 'BR'):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif handle in ('TR', 'BL'):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            elif handle in ('T', 'B'):
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            elif handle in ('L', 'R'):
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        """Detect if the user clicked a resize handle or is just dragging the item."""
        if self.isSelected():
            # Capture starting geometry for Undo tracking
            self._undo_start_ul = (int(self.scenePos().x()), int(self.scenePos().y()))
            self._undo_start_br = (
                int(self.scenePos().x() + self.rect().width()),
                int(self.scenePos().y() + self.rect().height())
            )

            self.active_handle = self._get_handle_at(event.pos())
            if self.active_handle:
                self.is_resizing = True
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle resizing logic if a handle was clicked."""
        if self.is_resizing and self.active_handle:
            rect = self.rect()
            ul = self.scenePos()
            br = QPointF(ul.x() + rect.width(), ul.y() + rect.height())

            scene_pos = event.scenePos()

            if 'L' in self.active_handle:
                ul.setX(min(scene_pos.x(), br.x() - 1))
            if 'R' in self.active_handle:
                br.setX(max(scene_pos.x(), ul.x() + 1))
            if 'T' in self.active_handle:
                ul.setY(min(scene_pos.y(), br.y() - 1))
            if 'B' in self.active_handle:
                br.setY(max(scene_pos.y(), ul.y() + 1))

            self.preview_widget._is_syncing = True

            # Notify Qt of the geometry change BEFORE updating pos/rect
            self.prepareGeometryChange()
            self.setPos(ul)
            self.setRect(0, 0, br.x() - ul.x(), br.y() - ul.y())

            new_ul = (int(ul.x()), int(ul.y()))
            new_br = (int(br.x()), int(br.y()))
            self.preview_widget.handle_item_moved(self.window, new_ul, new_br)

            self.preview_widget._is_syncing = False
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Capture ending geometry and emit signals for bulk tracking."""
        current_ul = (int(self.scenePos().x()), int(self.scenePos().y()))
        current_br = (
            int(self.scenePos().x() + self.rect().width()),
            int(self.scenePos().y() + self.rect().height())
        )

        # Check if geometry actually changed during the drag/resize
        if hasattr(self, '_undo_start_ul'):
            if current_ul != self._undo_start_ul or current_br != self._undo_start_br:
                self.preview_widget.item_drag_finished_signal.emit(
                    self.window_uuid,
                    self._undo_start_ul,
                    self._undo_start_br,
                    current_ul,
                    current_br
                )
            # Cleanup
            delattr(self, '_undo_start_ul')
            delattr(self, '_undo_start_br')

        self.is_resizing = False
        self.active_handle = None
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            if self.isSelected():
                self.setPen(self.selected_pen)
                self.setZValue(self.original_z + 1000)
            else:
                self.setPen(self.default_pen)
                self.setZValue(self.original_z)

        elif change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.scene() and not self.preview_widget._is_syncing and not self.is_resizing:
                new_pos = self.pos()
                rect = self.rect()
                new_ul = (int(new_pos.x()), int(new_pos.y()))
                new_br = (int(new_pos.x() + rect.width()), int(new_pos.y() + rect.height()))
                self.preview_widget.handle_item_moved(self.window, new_ul, new_br)

        return super().itemChange(change, value)

    def paint(self, painter, option, widget=None):
        """Draw the item, and if selected, draw the 8 resize handles on top."""
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.setPen(QPen(QColor(0, 0, 0), 1))

            rect = self.rect()
            hs = self.HANDLE_SIZE
            half = hs / 2

            handles = [
                QRectF(0 - half, 0 - half, hs, hs),                                 # TL
                QRectF(rect.width() / 2 - half, 0 - half, hs, hs),                  # T
                QRectF(rect.width() - half, 0 - half, hs, hs),                      # TR
                QRectF(rect.width() - half, rect.height() / 2 - half, hs, hs),      # R
                QRectF(rect.width() - half, rect.height() - half, hs, hs),          # BR
                QRectF(rect.width() / 2 - half, rect.height() - half, hs, hs),      # B
                QRectF(0 - half, rect.height() - half, hs, hs),                     # BL
                QRectF(0 - half, rect.height() / 2 - half, hs, hs)                  # L
            ]
            for h in handles:
                painter.drawRect(h)

    def _get_handle_at(self, pos):
        """Determine if a coordinate position hits a resize handle."""
        hs = self.HANDLE_SIZE
        rect = self.rect()

        if pos.y() < hs:
            if pos.x() < hs: return 'TL'
            if pos.x() > rect.width() - hs: return 'TR'
            return 'T'
        elif pos.y() > rect.height() - hs:
            if pos.x() < hs: return 'BL'
            if pos.x() > rect.width() - hs: return 'BR'
            return 'B'
        else:
            if pos.x() < hs: return 'L'
            if pos.x() > rect.width() - hs: return 'R'
        return None


class PreviewGraphicsView(QGraphicsView):
    """Custom QGraphicsView to handle Zooming and Background Grids."""
    zoom_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.show_grid = False
        self.grid_size = 20
        self._zoom_level = 100

    def set_show_grid(self, show):
        self.show_grid = show
        self.scene().invalidate(self.sceneRect(), QGraphicsScene.SceneLayer.ForegroundLayer)
        self.viewport().update()

    def drawForeground(self, painter, rect):
        """Draws the grid on top of all items when enabled."""
        super().drawForeground(painter, rect)

        if not self.show_grid:
            return

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        lines = []
        x = left
        while x < rect.right():
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))
            x += self.grid_size

        y = top
        while y < rect.bottom():
            lines.append(QLineF(rect.left(), y, rect.right(), y))
            y += self.grid_size

        pen = QPen(QColor(100, 100, 100, 80), 1)
        pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        painter.drawLines(lines)

    def set_zoom(self, level):
        """Safely apply scale transformations based on a percentage zoom level."""
        self._zoom_level = max(10, min(500, level))
        factor = self._zoom_level / 100.0

        self.setTransform(self.transform().fromScale(factor, factor))
        self.zoom_changed.emit(self._zoom_level)

    def wheelEvent(self, event):
        """Allows mouse-wheel zooming ONLY when Ctrl is pressed. Otherwise, pan."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            angle = event.angleDelta().y()
            if angle > 0:
                self.set_zoom(self._zoom_level + 10)
            elif angle < 0:
                self.set_zoom(self._zoom_level - 10)
            event.accept()
        else:
            super().wheelEvent(event)


class VisualPreview(QWidget):
    """Main Canvas container combining the Toolbar, the View, and the Control Bar."""
    item_selected_signal = pyqtSignal(str)
    item_moved_signal = pyqtSignal(object, tuple, tuple)
    item_drag_finished_signal = pyqtSignal(str, tuple, tuple, tuple, tuple)
    bulk_geometry_change_signal = pyqtSignal(str, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # State Variables
        self.items_map = {}
        self._is_syncing = False
        self.align_actions = []

        self._setup_toolbar()
        self._setup_view()
        self._setup_bottom_bar()

    def _setup_toolbar(self):
        self.toolbar = QToolBar("Alignment Toolbar", self)
        self.layout.addWidget(self.toolbar)

        def add_action(text, command, is_extend=False):
            action = QAction(text, self)
            if is_extend:
                action.triggered.connect(lambda checked, cmd=command: self.extend_items(cmd))
            else:
                action.triggered.connect(lambda checked, cmd=command: self.align_items(cmd))
            action.setEnabled(False)
            self.toolbar.addAction(action)
            self.align_actions.append(action)

        add_action("Align Left", 'left')
        add_action("Align H-Center", 'hcenter')
        add_action("Align Right", 'right')
        self.toolbar.addSeparator()
        add_action("Align Top", 'top')
        add_action("Align V-Center", 'vcenter')
        add_action("Align Bottom", 'bottom')
        self.toolbar.addSeparator()
        add_action("Distribute H", 'dist_h')
        add_action("Distribute V", 'dist_v')
        self.toolbar.addSeparator()
        add_action("Extend Left", 'ext_left', True)
        add_action("Extend Right", 'ext_right', True)
        add_action("Extend Top", 'ext_top', True)
        add_action("Extend Bottom", 'ext_bottom', True)

    def _setup_view(self):
        self.scene = QGraphicsScene(self)
        self.scene.selectionChanged.connect(self.handle_selection_changed)

        self.view = PreviewGraphicsView(self)
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view, stretch=1)

    def _setup_bottom_bar(self):
        self.bottom_bar = QWidget(self)
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(10, 5, 10, 5)

        self.btn_grid = QPushButton("Toggle Grid")
        self.btn_grid.setCheckable(True)
        self.btn_grid.clicked.connect(self.view.set_show_grid)

        self.btn_zoom_out = QPushButton("-")
        self.btn_zoom_out.setFixedWidth(30)
        self.btn_zoom_out.clicked.connect(lambda: self.view.set_zoom(self.view._zoom_level - 10))

        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(10, 500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(150)
        self.zoom_slider.valueChanged.connect(self.view.set_zoom)

        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_in.setFixedWidth(30)
        self.btn_zoom_in.clicked.connect(lambda: self.view.set_zoom(self.view._zoom_level + 10))

        self.zoom_label = QLabel("100%")
        self.zoom_label.setFixedWidth(40)
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.view.zoom_changed.connect(self._update_zoom_ui)

        self.bottom_layout.addWidget(self.btn_grid)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.btn_zoom_out)
        self.bottom_layout.addWidget(self.zoom_slider)
        self.bottom_layout.addWidget(self.btn_zoom_in)
        self.bottom_layout.addWidget(self.zoom_label)

        self.layout.addWidget(self.bottom_bar)

    def _update_zoom_ui(self, level):
        self.zoom_slider.blockSignals(True)
        self.zoom_slider.setValue(level)
        self.zoom_slider.blockSignals(False)
        self.zoom_label.setText(f"{level}%")

    def clear(self):
        self.scene.clear()
        self.items_map.clear()
        self.update_toolbar_state(0)

    def handle_selection_changed(self):
        selected = self.scene.selectedItems()
        wnd_items = [i for i in selected if isinstance(i, WndGraphicsItem)]

        self.update_toolbar_state(len(wnd_items))

        if not self._is_syncing and len(wnd_items) == 1:
            self.item_selected_signal.emit(wnd_items[0].window_uuid)

    def update_toolbar_state(self, selected_count):
        is_enabled = selected_count >= 2
        for action in self.align_actions:
            action.setEnabled(is_enabled)

    def extend_items(self, direction):
        items = [i for i in self.scene.selectedItems() if isinstance(i, WndGraphicsItem)]
        if len(items) < 2: return

        self._is_syncing = True

        min_x = min(i.scenePos().x() for i in items)
        max_r = max(i.scenePos().x() + i.rect().width() for i in items)
        min_y = min(i.scenePos().y() for i in items)
        max_b = max(i.scenePos().y() + i.rect().height() for i in items)

        changes = []
        for i in items:
            rect = i.rect()
            old_ul = (int(i.scenePos().x()), int(i.scenePos().y()))
            old_br = (int(i.scenePos().x() + rect.width()), int(i.scenePos().y() + rect.height()))

            new_ul_x, new_ul_y = old_ul[0], old_ul[1]
            new_br_x, new_br_y = old_br[0], old_br[1]

            if direction == 'ext_left': new_ul_x = min_x
            elif direction == 'ext_right': new_br_x = max_r
            elif direction == 'ext_top': new_ul_y = min_y
            elif direction == 'ext_bottom': new_br_y = max_b

            new_ul = (int(new_ul_x), int(new_ul_y))
            new_br = (int(new_br_x), int(new_br_y))

            if old_ul != new_ul or old_br != new_br:
                i.setPos(new_ul[0], new_ul[1])
                i.setRect(0, 0, new_br[0] - new_ul[0], new_br[1] - new_ul[1])
                changes.append((i.window_uuid, old_ul, old_br, new_ul, new_br))
                self.handle_item_moved(i.window, new_ul, new_br)

        if changes:
            macro_name = f"Extend {direction.split('_')[1].capitalize()}"
            self.bulk_geometry_change_signal.emit(macro_name, changes)

        self._is_syncing = False

    def align_items(self, alignment):
        items = [i for i in self.scene.selectedItems() if isinstance(i, WndGraphicsItem)]
        if len(items) < 2: return
        self._is_syncing = True

        min_x = min(i.scenePos().x() for i in items)
        max_r = max(i.scenePos().x() + i.rect().width() for i in items)
        min_y = min(i.scenePos().y() for i in items)
        max_b = max(i.scenePos().y() + i.rect().height() for i in items)

        center_x = (min_x + max_r) / 2
        center_y = (min_y + max_b) / 2

        changes = []

        if alignment == 'dist_h':
            items.sort(key=lambda i: i.scenePos().x())
            total_w = sum(i.rect().width() for i in items)
            space = (max_r - min_x - total_w) / (len(items) - 1) if len(items) > 1 else 0
            curr_x = min_x
            for i in items:
                new_x = curr_x
                curr_x += i.rect().width() + space
                old_ul = (int(i.scenePos().x()), int(i.scenePos().y()))
                old_br = (int(i.scenePos().x() + i.rect().width()), int(i.scenePos().y() + i.rect().height()))
                new_ul = (int(new_x), old_ul[1])
                new_br = (int(new_x + i.rect().width()), old_br[1])
                changes.append((i.window_uuid, old_ul, old_br, new_ul, new_br))

        elif alignment == 'dist_v':
            items.sort(key=lambda i: i.scenePos().y())
            total_h = sum(i.rect().height() for i in items)
            space = (max_b - min_y - total_h) / (len(items) - 1) if len(items) > 1 else 0
            curr_y = min_y
            for i in items:
                new_y = curr_y
                curr_y += i.rect().height() + space
                old_ul = (int(i.scenePos().x()), int(i.scenePos().y()))
                old_br = (int(i.scenePos().x() + i.rect().width()), int(i.scenePos().y() + i.rect().height()))
                new_ul = (old_ul[0], int(new_y))
                new_br = (old_br[0], int(new_y + i.rect().height()))
                changes.append((i.window_uuid, old_ul, old_br, new_ul, new_br))
        else:
            for i in items:
                rect = i.rect()
                old_ul = (int(i.scenePos().x()), int(i.scenePos().y()))
                old_br = (int(i.scenePos().x() + rect.width()), int(i.scenePos().y() + rect.height()))
                new_x, new_y = old_ul[0], old_ul[1]

                if alignment == 'left': new_x = min_x
                elif alignment == 'right': new_x = max_r - rect.width()
                elif alignment == 'hcenter': new_x = center_x - (rect.width() / 2)
                elif alignment == 'top': new_y = min_y
                elif alignment == 'bottom': new_y = max_b - rect.height()
                elif alignment == 'vcenter': new_y = center_y - (rect.height() / 2)

                new_ul = (int(new_x), int(new_y))
                new_br = (int(new_x + rect.width()), int(new_y + rect.height()))

                if old_ul != new_ul or old_br != new_br:
                    changes.append((i.window_uuid, old_ul, old_br, new_ul, new_br))

        if changes:
            self.bulk_geometry_change_signal.emit("Align Items", changes)

        self._is_syncing = False

    def handle_item_moved(self, window, new_ul, new_br):
        self.item_moved_signal.emit(window, new_ul, new_br)

    def select_item(self, uuid):
        self._is_syncing = True
        self.scene.clearSelection()
        if uuid in self.items_map:
            item = self.items_map[uuid]
            item.setSelected(True)
            self.view.ensureVisible(item)
        self._is_syncing = False

    def update_item_geometry_from_data(self, window):
        if not window or window.window_uuid not in self.items_map:
            return
        self._is_syncing = True
        item = self.items_map[window.window_uuid]
        ul = window.properties['SCREENRECT'].get('UPPERLEFT', [0, 0])
        br = window.properties['SCREENRECT'].get('BOTTOMRIGHT', [0, 0])
        w = br[0] - ul[0]
        h = br[1] - ul[1]
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

    def set_item_visibility(self, uuid, is_visible):
        """Toggles the visibility of a graphics item based on the Object Tree toggle."""
        if uuid in self.items_map:
            self.items_map[uuid].setVisible(is_visible)

            if not is_visible:
                self.items_map[uuid].setSelected(False)

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