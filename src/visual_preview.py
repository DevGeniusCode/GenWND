# --- START OF FILE visual_preview.py ---
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPainter
from PyQt6.QtCore import Qt


class VisualPreview(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the Scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Enable anti-aliasing for smoother lines
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Allow panning the view with the mouse
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        # Set a default background color for the view area
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))

    def clear(self):
        """Clears the visual preview canvas."""
        self.scene.clear()

    def load_hierarchy(self, windows):
        """Reads WND coordinates and draws them on the scene."""
        self.clear()
        if not windows:
            return

        # Determine Canvas Size (CREATIONRESOLUTION)
        # We fall back to 800x600 if not found in the root window
        res_w, res_h = 800, 600
        if 'SCREENRECT' in windows[0].properties:
            res = windows[0].properties['SCREENRECT'].get('CREATIONRESOLUTION', [800, 600])
            res_w, res_h = res[0], res[1]

        # Draw the "Screen" Background (Represents the monitor/game resolution)
        bg_rect = QGraphicsRectItem(0, 0, res_w, res_h)
        bg_rect.setBrush(QBrush(QColor(50, 50, 50)))  # Dark gray screen
        bg_rect.setPen(QPen(QColor(255, 255, 255), 2))  # White border
        bg_rect.setZValue(-1)  # Ensure background is always at the back
        self.scene.addItem(bg_rect)

        # Set the scene rect with some padding so panning feels natural
        self.scene.setSceneRect(-100, -100, res_w + 200, res_h + 200)

        # Render all items
        self._render_windows(windows, depth=1)

    def _render_windows(self, windows, depth):
        """Recursively renders windows and their children."""
        for window in windows:
            props = window.properties
            screenrect = props.get('SCREENRECT')

            if screenrect:
                ul = screenrect.get('UPPERLEFT', [0, 0])
                br = screenrect.get('BOTTOMRIGHT', [0, 0])

                # Calculate width and height
                w = br[0] - ul[0]
                h = br[1] - ul[1]

                # Only draw if it has valid dimensions
                if w > 0 and h > 0:
                    # 1. Create the Rectangle
                    # Position it locally at 0,0, then move it to the absolute coordinates
                    rect_item = QGraphicsRectItem(0, 0, w, h)
                    rect_item.setPos(ul[0], ul[1])

                    # Apply Styling (Semi-transparent blue fill, solid blue border)
                    rect_item.setBrush(QBrush(QColor(100, 150, 255, 40)))
                    rect_item.setPen(QPen(QColor(100, 150, 255, 200), 1))

                    # Higher depth = higher Z-value (Children render on top of parents)
                    rect_item.setZValue(depth)

                    # 2. Create the Text Label
                    name = props.get('NAME', 'Unnamed')
                    wtype = props.get('WINDOWTYPE', 'UNKNOWN')
                    label = QGraphicsTextItem(f"{wtype}: {name}")

                    # Attach label to the rectangle so they share coordinate space
                    label.setParentItem(rect_item)
                    label.setPos(2, 2)  # Slight padding inside the box
                    label.setDefaultTextColor(QColor(255, 255, 255))
                    label.setFont(QFont("Arial", 8, QFont.Weight.Bold))

                    self.scene.addItem(rect_item)

            # Process children recursively
            if hasattr(window, 'children') and window.children:
                self._render_windows(window.children, depth + 1)