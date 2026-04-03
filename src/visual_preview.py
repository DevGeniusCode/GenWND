# --- START OF FILE visual_preview.py ---
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QToolBar, QGraphicsView,
                             QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
                             QGraphicsItem)
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPainter, QAction
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF


class WndGraphicsItem(QGraphicsRectItem):
    HANDLE_SIZE = 8

    def __init__(self, window, preview_widget, w, h):
        super().__init__(0, 0, w, h)
        self.window = window
        self.window_uuid = window.window_uuid
        self.preview_widget = preview_widget  # The parent VisualPreview widget containing logic
        self.original_z = 0

        # Enable Interactivity
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)  # Required for changing cursors on handles

        # Default Styling
        self.default_brush = QBrush(QColor(100, 150, 255, 40))
        self.default_pen = QPen(QColor(100, 150, 255, 200), 1)
        self.selected_pen = QPen(QColor(255, 50, 50, 255), 2)

        self.setBrush(self.default_brush)
        self.setPen(self.default_pen)

        # Resize State
        self.active_handle = None
        self.is_resizing = False

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

            self.setPos(ul)
            self.setRect(0, 0, br.x() - ul.x(), br.y() - ul.y())

            new_ul = (int(ul.x()), int(ul.y()))
            new_br = (int(br.x()), int(br.y()))
            self.preview_widget.handle_item_moved(self.window, new_ul, new_br)

            self.preview_widget._is_syncing = False
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
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
                QRectF(0 - half, 0 - half, hs, hs),  # TL
                QRectF(rect.width() / 2 - half, 0 - half, hs, hs),  # T
                QRectF(rect.width() - half, 0 - half, hs, hs),  # TR
                QRectF(rect.width() - half, rect.height() / 2 - half, hs, hs),  # R
                QRectF(rect.width() - half, rect.height() - half, hs, hs),  # BR
                QRectF(rect.width() / 2 - half, rect.height() - half, hs, hs),  # B
                QRectF(0 - half, rect.height() - half, hs, hs),  # BL
                QRectF(0 - half, rect.height() / 2 - half, hs, hs)  # L
            ]
            for h in handles:
                painter.drawRect(h)

    def _get_handle_at(self, pos):
        hs = self.HANDLE_SIZE
        rect = self.rect()
        t, b, l, r = -hs, rect.height() + hs, -hs, rect.width() + hs

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


class VisualPreview(QWidget):
    item_selected_signal = pyqtSignal(str)
    item_moved_signal = pyqtSignal(object, tuple, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 2. Fixed Top Toolbar
        self.toolbar = QToolBar("Alignment Toolbar", self)
        self.layout.addWidget(self.toolbar)
        self._setup_toolbar()

        # 3. Graphics View & Scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.view.setBackgroundBrush(QBrush(QColor(30, 30, 30)))

        self.layout.addWidget(self.view)

        # State Variables
        self.items_map = {}
        self._is_syncing = False

        self.scene.selectionChanged.connect(self.handle_selection_changed)

    def _setup_toolbar(self):
        """Initializes the toolbar actions and sets them to disabled by default."""
        self.align_actions = []

        # Helper to create and bind actions
        def add_align_action(text, command):
            action = QAction(text, self)
            action.triggered.connect(lambda checked, cmd=command: self.align_items(cmd))
            action.setEnabled(False)
            self.toolbar.addAction(action)
            self.align_actions.append(action)

        add_align_action("Align Left", 'left')
        add_align_action("Align H-Center", 'hcenter')
        add_align_action("Align Right", 'right')

        self.toolbar.addSeparator()

        add_align_action("Align Top", 'top')
        add_align_action("Align V-Center", 'vcenter')
        add_align_action("Align Bottom", 'bottom')

        self.toolbar.addSeparator()

        add_align_action("Distribute H", 'dist_h')
        add_align_action("Distribute V", 'dist_v')

    def clear(self):
        self.scene.clear()
        self.items_map.clear()
        self.update_toolbar_state(0)

    def handle_selection_changed(self):
        selected = self.scene.selectedItems()
        wnd_items = [i for i in selected if isinstance(i, WndGraphicsItem)]

        # 1. Update Toolbar State (Enable if 2+ items selected)
        self.update_toolbar_state(len(wnd_items))

        # 2. Sync to Object Tree (if a single item is selected)
        if not self._is_syncing and len(wnd_items) == 1:
            self.item_selected_signal.emit(wnd_items[0].window_uuid)

    def update_toolbar_state(self, selected_count):
        """Enables or disables alignment buttons based on selection count."""
        is_enabled = selected_count >= 2
        for action in self.align_actions:
            action.setEnabled(is_enabled)

    def align_items(self, alignment):
        """Aligns or distributes multiple selected items."""
        items = [i for i in self.scene.selectedItems() if isinstance(i, WndGraphicsItem)]
        if len(items) < 2:
            return

        self._is_syncing = True

        min_x = min(i.scenePos().x() for i in items)
        max_r = max(i.scenePos().x() + i.rect().width() for i in items)
        min_y = min(i.scenePos().y() for i in items)
        max_b = max(i.scenePos().y() + i.rect().height() for i in items)

        center_x = (min_x + max_r) / 2
        center_y = (min_y + max_b) / 2

        if alignment == 'dist_h':
            items.sort(key=lambda i: i.scenePos().x())
            total_w = sum(i.rect().width() for i in items)
            space = (max_r - min_x - total_w) / (len(items) - 1) if len(items) > 1 else 0
            curr_x = min_x
            for i in items:
                i.setPos(curr_x, i.scenePos().y())
                curr_x += i.rect().width() + space

        elif alignment == 'dist_v':
            items.sort(key=lambda i: i.scenePos().y())
            total_h = sum(i.rect().height() for i in items)
            space = (max_b - min_y - total_h) / (len(items) - 1) if len(items) > 1 else 0
            curr_y = min_y
            for i in items:
                i.setPos(i.scenePos().x(), curr_y)
                curr_y += i.rect().height() + space

        else:
            for i in items:
                rect = i.rect()
                new_x, new_y = i.scenePos().x(), i.scenePos().y()

                if alignment == 'left':
                    new_x = min_x
                elif alignment == 'right':
                    new_x = max_r - rect.width()
                elif alignment == 'hcenter':
                    new_x = center_x - (rect.width() / 2)
                elif alignment == 'top':
                    new_y = min_y
                elif alignment == 'bottom':
                    new_y = max_b - rect.height()
                elif alignment == 'vcenter':
                    new_y = center_y - (rect.height() / 2)

                i.setPos(new_x, new_y)

        # Emit sync signals for ALL modified items
        for i in items:
            ul = i.scenePos()
            br = QPointF(ul.x() + i.rect().width(), ul.y() + i.rect().height())
            new_ul = (int(ul.x()), int(ul.y()))
            new_br = (int(br.x()), int(br.y()))
            self.handle_item_moved(i.window, new_ul, new_br)

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
        w = br[0] - ul[0];
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

    def _render_windows(self, windows, depth):
        for window in windows:
            props = window.properties
            screenrect = props.get('SCREENRECT')
            if screenrect:
                ul = screenrect.get('UPPERLEFT', [0, 0])
                br = screenrect.get('BOTTOMRIGHT', [0, 0])
                w = br[0] - ul[0];
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