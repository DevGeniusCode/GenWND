from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QGroupBox, QLabel, QLineEdit, QSpinBox,
    QTabWidget, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout
)
from PyQt6.QtGui import QColor

from src.properties.text_color import ColorPickerApp
from src.commands import CommandChangeGeometry, CommandChangeProperty


class GeneralForm(QWidget):
    """The main Property Editor form for editing common Window attributes."""

    def __init__(self, parent=None, main_window=None, general_data=None):
        super().__init__(parent)
        self.general_data = general_data or {}
        self.main_window = main_window

        self.creation_resolution_width = 100
        self.creation_resolution_height = 100

        self.layout = QVBoxLayout(self)

        # Build Form Sections
        self._setup_identification_group()
        self._setup_position_group()
        self._setup_status_group()
        self._setup_text_group()
        self._setup_font_group()
        self._setup_text_color_group()

    def _setup_identification_group(self):
        """Builds the internal NAME input."""
        self.name_label = QLabel("Internal reference identification", self)
        self.name_entry = QLineEdit(self)
        self.name_entry.setObjectName("name_entry")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_entry)

        self.name_entry.editingFinished.connect(
            lambda: self.commit_text_change('NAME', self.name_entry)
        )

    def _setup_position_group(self):
        """Builds the Geometry/ScreenRect X,Y coordinate spinboxes."""
        self.position_group = QGroupBox("Position", self)
        pos_layout = QGridLayout(self.position_group)

        self.upper_left_x_spinbox = QSpinBox(self.position_group)
        self.upper_left_y_spinbox = QSpinBox(self.position_group)
        self.bottom_right_x_spinbox = QSpinBox(self.position_group)
        self.bottom_right_y_spinbox = QSpinBox(self.position_group)

        for spinbox in [self.upper_left_x_spinbox, self.bottom_right_x_spinbox]:
            spinbox.setMaximum(self.creation_resolution_width)
            spinbox.editingFinished.connect(self.commit_geometry_change)

        for spinbox in [self.upper_left_y_spinbox, self.bottom_right_y_spinbox]:
            spinbox.setMaximum(self.creation_resolution_height)
            spinbox.editingFinished.connect(self.commit_geometry_change)

        pos_layout.addWidget(QLabel("Upper Left"), 0, 0)
        pos_layout.addWidget(QLabel("X"), 0, 1)
        pos_layout.addWidget(self.upper_left_x_spinbox, 0, 2)
        pos_layout.addWidget(QLabel("Y"), 0, 3)
        pos_layout.addWidget(self.upper_left_y_spinbox, 0, 4)

        pos_layout.addWidget(QLabel("Bottom Right"), 1, 0)
        pos_layout.addWidget(QLabel("X"), 1, 1)
        pos_layout.addWidget(self.bottom_right_x_spinbox, 1, 2)
        pos_layout.addWidget(QLabel("Y"), 1, 3)
        pos_layout.addWidget(self.bottom_right_y_spinbox, 1, 4)

        self.layout.addWidget(self.position_group)

    def _setup_status_group(self):
        """Builds the Status properties checkable tabs."""
        self.status_group = QGroupBox("Status", self)
        status_layout = QVBoxLayout(self.status_group)
        self.tab_widget = QTabWidget(self)

        # Helper to create checkboxes cleanly
        self.checkboxes = {}

        def add_checkbox(tab_layout, label, status_flag, attr_name, row, col):
            cb = QCheckBox(label)
            cb.toggled.connect(self.update_statuses)
            tab_layout.addWidget(cb, row, col)
            self.checkboxes[status_flag] = cb
            setattr(self, attr_name, cb)  # Dynamically bind to self for property_editor.py

        # Tab 1
        tab1 = QWidget()
        l1 = QGridLayout(tab1)
        add_checkbox(l1, "Enabled", "ENABLED", "status_enable", 0, 0)
        add_checkbox(l1, "Hidden", "HIDDEN", "status_hidden", 0, 1)
        add_checkbox(l1, "See Thru", "SEE_THRU", "status_see_thru", 1, 0)
        add_checkbox(l1, "Image", "IMAGE", "status_image", 1, 1)
        add_checkbox(l1, "Border", "BORDER", "status_border", 2, 0)
        add_checkbox(l1, "No Input", "NOINPUT", "status_no_input", 2, 1)

        # Tab 2
        tab2 = QWidget()
        l2 = QGridLayout(tab2)
        add_checkbox(l2, "No Focus", "NOFOCUS", "status_no_focus", 0, 0)
        add_checkbox(l2, "Draggable", "DRAGABLE", "status_draggable", 0, 1)
        add_checkbox(l2, "Wrap Centered", "WRAP_CENTERED", "status_wrap_centered", 1, 0)
        add_checkbox(l2, "On Mouse Down", "ON_MOUSE_DOWN", "status_on_mouse_down", 1, 1)
        add_checkbox(l2, "Hotkey Text", "HOTKEY_TEXT", "status_hotkey_text", 2, 0)
        add_checkbox(l2, "Right Click", "RIGHT_CLICK", "status_right_click", 2, 1)

        # Tab 3
        tab3 = QWidget()
        l3 = QGridLayout(tab3)
        add_checkbox(l3, "Check Like", "CHECK_LIKE", "status_check_like", 0, 0)
        add_checkbox(l3, "Tab Stop", "TABSTOP", "status_tabstop", 1, 0)
        l3.setRowStretch(0, 1)
        l3.setRowStretch(1, 1)
        l3.setRowStretch(2, 1)

        self.tab_widget.addTab(tab1, "Basic")
        self.tab_widget.addTab(tab2, "Interaction")
        self.tab_widget.addTab(tab3, "Misc")

        status_layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.status_group)

    def _setup_text_group(self):
        """Builds the UI Text and Tooltip entry blocks."""
        self.text_group = QGroupBox("Text Data", self)
        grid_layout = QGridLayout(self.text_group)

        self.text_entry = QLineEdit()
        self.tooltip_entry = QLineEdit()

        grid_layout.addWidget(QLabel("Text"), 0, 0)
        grid_layout.addWidget(self.text_entry, 0, 1)
        grid_layout.addWidget(QLabel("Tooltip"), 1, 0)
        grid_layout.addWidget(self.tooltip_entry, 1, 1)

        self.text_entry.editingFinished.connect(
            lambda: self.commit_text_change('TEXT', self.text_entry)
        )
        self.tooltip_entry.editingFinished.connect(
            lambda: self.commit_text_change('TOOLTIPTEXT', self.tooltip_entry)
        )

        self.layout.addWidget(self.text_group)

    def _setup_font_group(self):
        """Builds the Font definition blocks."""
        self.font_group = QGroupBox("Font Style", self)
        font_layout = QVBoxLayout(self.font_group)

        # Font Row
        font_h = QHBoxLayout()
        self.bold_checkbox = QCheckBox("Bold")
        self.font_list = QComboBox()
        self.font_list.addItems(["Arial", "Times New Roman", "Courier New", "Verdana"])

        font_h.addWidget(self.bold_checkbox)
        font_h.addWidget(self.font_list)

        # Template Row
        template_h = QHBoxLayout()
        self.template_list = QComboBox()
        self.template_list.addItems(["Template 1", "Template 2", "Template 3"])

        template_h.addWidget(QLabel("Template"))
        template_h.addWidget(self.template_list)

        font_layout.addLayout(font_h)
        font_layout.addLayout(template_h)

        # Connections via Undo Stack mapping
        self.bold_checkbox.toggled.connect(
            lambda checked: self.commit_sub_property_change('FONT', 'bold', int(checked))
        )
        self.font_list.currentTextChanged.connect(
            lambda text: self.commit_sub_property_change('FONT', 'name', text)
        )
        self.template_list.currentTextChanged.connect(
            lambda text: self.commit_property_change('HEADERTEMPLATE', text)
        )

        self.layout.addWidget(self.font_group)

    def _setup_text_color_group(self):
        """Builds the external component for defining Text and Border colors."""
        self.text_color_group = QGroupBox("Text Color", self)
        color_layout = QVBoxLayout(self.text_color_group)
        color_layout.setContentsMargins(0, 0, 0, 0)

        default_color_data = {
            "enable": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)},
            "disable": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)},
            "highlight": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)}
        }

        self.text_color_tabs = ColorPickerApp(color_data=default_color_data)
        color_layout.addWidget(self.text_color_tabs)

        def update_text_color():
            data = self.text_color_tabs.color_data

            # Helper mapper
            def to_tuple(col):
                return col.red(), col.green(), col.blue(), col.alpha()

            self.commit_sub_property_change('TEXTCOLOR', 'ENABLED', to_tuple(data['enable']['color']))
            self.commit_sub_property_change('TEXTCOLOR', 'ENABLEDBORDER', to_tuple(data['enable']['shadow']))

            self.commit_sub_property_change('TEXTCOLOR', 'DISABLED', to_tuple(data['disable']['color']))
            self.commit_sub_property_change('TEXTCOLOR', 'DISABLEDBORDER', to_tuple(data['disable']['shadow']))

            self.commit_sub_property_change('TEXTCOLOR', 'HILITE', to_tuple(data['highlight']['color']))
            self.commit_sub_property_change('TEXTCOLOR', 'HILITEBORDER', to_tuple(data['highlight']['shadow']))

        # Connect picker buttons to update function
        for state in ['enable', 'disable', 'highlight']:
            self.text_color_tabs.color_data[state]['color_button'].clicked.connect(update_text_color)
            self.text_color_tabs.color_data[state]['shadow_button'].clicked.connect(update_text_color)

        self.layout.addWidget(self.text_color_group)

    # --- GEOMETRY AND RESOLUTION UPDATES ---
    def update_resolution(self, width, height):
        self.creation_resolution_width = width
        self.creation_resolution_height = height
        self.upper_left_x_spinbox.setMaximum(width)
        self.upper_left_y_spinbox.setMaximum(height)
        self.bottom_right_x_spinbox.setMaximum(width)
        self.bottom_right_y_spinbox.setMaximum(height)

    def commit_geometry_change(self):
        """Fires a geometry command specifically for the Canvas syncing."""
        if getattr(self.main_window, '_is_undoing', False):
            return

        if not hasattr(self.main_window, 'selected_object') or not self.main_window.selected_object:
            return

        new_ul = (self.upper_left_x_spinbox.value(), self.upper_left_y_spinbox.value())
        new_br = (self.bottom_right_x_spinbox.value(), self.bottom_right_y_spinbox.value())

        screen_rect = self.general_data.get('SCREENRECT', {})
        old_ul = tuple(screen_rect.get('UPPERLEFT', [0, 0]))
        old_br = tuple(screen_rect.get('BOTTOMRIGHT', [0, 0]))

        if new_ul != old_ul or new_br != old_br:
            cmd = CommandChangeGeometry(
                self.main_window,
                self.main_window.selected_object.window_uuid,
                old_ul, old_br, new_ul, new_br
            )
            self.main_window.undo_stack.push(cmd)

    # --- UNDO STACK COMMAND WRAPPERS ---
    def commit_text_change(self, prop_key, line_edit):
        """Pushes string edits to the Undo Stack."""
        self.commit_property_change(prop_key, line_edit.text())

    def commit_property_change(self, prop_key, new_value):
        """Generic property committer for the Undo Stack."""
        if getattr(self.main_window, '_is_undoing', False) or getattr(self.main_window, '_is_syncing', False):
            return

        if not hasattr(self.main_window, 'selected_object') or not self.main_window.selected_object:
            return

        old_value = self.general_data.get(prop_key)
        if new_value != old_value:
            cmd = CommandChangeProperty(
                self.main_window,
                self.main_window.selected_object.window_uuid,
                prop_key, old_value, new_value
            )
            self.main_window.undo_stack.push(cmd)

    def commit_sub_property_change(self, dict_key, sub_key, new_value):
        """Commits changes for nested dictionaries like FONT['bold'] or TEXTCOLOR['ENABLED']."""
        if getattr(self.main_window, '_is_undoing', False) or getattr(self.main_window, '_is_syncing', False):
            return

        if not hasattr(self.main_window, 'selected_object') or not self.main_window.selected_object:
            return

        parent_dict = self.general_data.get(dict_key, {})

        # Make a deep copy to ensure the undo stack holds distinct object states
        old_dict = parent_dict.copy()
        new_dict = parent_dict.copy()

        new_dict[sub_key] = new_value

        if new_dict != old_dict:
            cmd = CommandChangeProperty(
                self.main_window,
                self.main_window.selected_object.window_uuid,
                dict_key, old_dict, new_dict
            )
            self.main_window.undo_stack.push(cmd)

            # Sync font/color updates immediately back to canvas if applicable
            if hasattr(self.main_window, 'visual_preview'):
                self.main_window.visual_preview.update_item_geometry_from_data(self.main_window.selected_object)

    def update_statuses(self):
        """Compiles checked boxes into an array and fires a property update command."""
        active_flags = []
        for flag, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                active_flags.append(flag)

        self.commit_property_change("STATUS", active_flags)