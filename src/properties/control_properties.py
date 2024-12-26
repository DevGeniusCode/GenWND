from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QTabWidget, QWidget, \
    QGridLayout, QCheckBox, QScrollArea, QFrame, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QColor

from src.properties.collapsible_section import CollapsibleSection, SectionManager
from src.properties.text_color import ColorPickerApp


class ControlForm(QWidget):
    def __init__(self, parent=None, control_attributes=None):
        super().__init__(parent)
        self.control_attributes = control_attributes

        # Layout for the control-specific attributes
        self.layout = QVBoxLayout(self)

        # Determine control type
        self.type = self.control_attributes.get('WINDOWTYPE', 'No Type')
        self.type_label = QLabel(f"{self.type} Control", self)
        self.type_label.setStyleSheet("font-size: 16pt;")
        self.layout.addWidget(self.type_label)
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Dynamically create fields based on control type
        self.create_attributes_for_control_type(self.type)

    def create_attributes_for_control_type(self, control_type):
        """Dynamically create attributes based on control type. USER is default"""
        control_creation_map = {
            "USER": self.create_user_attributes,
            # "PUSHBUTTON": self.create_pushbutton_attributes,
            # "RADIOBUTTON": self.create_radiobutton_attributes,
            # "ENTRYFIELD": self.create_entryfield_attributes,
            # "STATICTEXT": self.create_statictxt_attributes,
            # "PROGRESSBAR": self.create_progressbar_attributes,
            # "SCROLLLISTBOX": self.create_scrolllistbox_attributes,
            "COMBOBOX": self.create_combobox_attributes,
            # "CHECKBOX": self.create_checkbox_attributes,
            # "HORZSLIDER": self.create_horzslider_attributes,
            # "VERTSLIDER": self.create_vertslider_attributes
        }

        if control_type in control_creation_map:
            control_creation_map[control_type](self.control_attributes)
        # else:
        #     raise ValueError(f"Unknown type: {control_type}")

    def create_user_attributes(self, n):
        """Creates a simple label with 'Hello'."""
        pass

    def create_attributes_for_control(self, attributes):
        """Creates controls for each property of the window depending on the control type
        Example of control_attributes:
        {'ASCIIONLY': False, 'ISEDITABLE': False, 'LETTERSANDNUMBERS': False, 'MAXCHARS': 16, 'MAXDISPLAY': 5}
        """
        group_box = QGroupBox("Attributes", self)
        attributes_grid = QGridLayout()
        # Iterate through attributes and create corresponding widgets
        row = 0
        for prop, value in attributes.items():
            prop_label = QLabel(prop, self)
            if isinstance(value, list):
                # If the property is a list, create a QComboBox
                prop_combobox = QComboBox(self)
                for item in value:
                    prop_combobox.addItem(str(item))
                prop_combobox.currentTextChanged.connect(
                    lambda text, p=prop: self.update_sub_property(f'{self.type}DATA', p, text)
                )
                attributes_grid.addWidget(prop_combobox, row, 1)
            elif isinstance(value, bool):
                # If the property is a boolean, create a QCheckBox
                prop_checkbox = QCheckBox(self)
                prop_checkbox.setChecked(value)
                prop_checkbox.toggled.connect(
                    lambda checked, p=prop: self.update_sub_property(f'{self.type}DATA', p, int(checked))
                )
                attributes_grid.addWidget(prop_checkbox, row, 1)
            elif isinstance(value, int):
                # If the property is an integer, create a QSpinBox
                prop_spinbox = QSpinBox(self)
                prop_spinbox.setValue(value)
                prop_spinbox.valueChanged.connect(
                    lambda val, p=prop: self.update_sub_property(f'{self.type}DATA', p, val)
                )
                attributes_grid.addWidget(prop_spinbox, row, 1)
            attributes_grid.addWidget(prop_label, row, 0)
            row += 1
        group_box.setLayout(attributes_grid)
        self.layout.addWidget(group_box)

    def create_textures_for_control(self, textures_attributes):
        outer_section_manager = SectionManager()
        inner_section_manager = SectionManager()
        self.layout.addWidget(create_header_with_separator("Textures"))

        def update_texture_color(texture_type, image, color_picker_app):
            color = color_picker_app.color_data['texture_layout']['color']
            border = color_picker_app.color_data['texture_layout']['shadow']

            self.update_texture_property(texture_type, 'color', image, (
                color.red(), color.green(), color.blue(), color.alpha()))
            self.update_texture_property(texture_type, 'BORDERCOLOR', image, (
                border.red(), border.green(), border.blue(), border.alpha()))

        for texture_type, texture_data in textures_attributes.items():
            if texture_type.endswith("DRAWDATA"):
                texture_type_name = texture_type[:-8]  # Remove 'DRAWDATA' suffix
                section = CollapsibleSection(title=texture_type_name, parent=self,
                                             section_manager=outer_section_manager)
                for texture in texture_data:
                    inner_section_title = texture.get('image', 'No Image')
                    inner_section = create_inner_section(inner_section_title, section, inner_section_manager,
                                                         "InnerSection")

                    color_picker_app = ColorPickerApp(
                        color_data={'texture_layout': {
                            "color": QColor(texture.get('color')[0], texture.get('color')[1], texture.get('color')[2],
                                            texture.get('color')[3]),
                            "shadow": QColor(texture.get('BORDERCOLOR')[0], texture.get('BORDERCOLOR')[1],
                                             texture.get('BORDERCOLOR')[2], texture.get('BORDERCOLOR')[3])
                        }}
                    )

                    color_label = color_picker_app.findChild(QLabel, "colorLabel")
                    color_label.setText("Color:")
                    shadow_label = color_picker_app.findChild(QLabel, "shadowLabel")
                    shadow_label.setText("Border Color:")

                    color_picker_app.color_data['texture_layout']['color_button'].clicked.connect(
                        lambda _, t=texture_type, i=inner_section_title, c=color_picker_app: update_texture_color(t, i, c))
                    color_picker_app.color_data['texture_layout']['shadow_button'].clicked.connect(
                        lambda _, t=texture_type, i=inner_section_title, c=color_picker_app: update_texture_color(t, i, c))

                    inner_section.addWidget(color_picker_app)
                    section.addWidget(inner_section)

                self.layout.addWidget(section)

    def update_sub_property(self, main_key, sub_key, value=None):
        list_dict = self.control_attributes.textures \
            if main_key in self.control_attributes.textures \
            else self.control_attributes.attributes

        for d in list_dict[main_key]:
            if sub_key in d and d[sub_key] != value:
                d[sub_key] = value
                # self.main_window.update_modified_state(True)

    def update_texture_property(self, main_key, sub_key, image, value=None):
        list_dict = self.control_attributes.textures

        for d in list_dict[main_key]:
            if 'image' in d and d['image'] == image and sub_key in d and d[sub_key] != value:
                d[sub_key] = value
                # self.main_window.update_modified_state(True)

    def create_combobox_attributes(self, properties):
        def filter_empty_properties(properties_list):
            return [
                prop for prop in properties_list if not (
                        'image' in prop and prop['image'] == 'NoImage'
                        and 'color' in prop and prop['color'] == (255, 255, 255, 0)
                        and 'BORDERCOLOR' in prop and prop['BORDERCOLOR'] == (255, 255, 255, 0)
                )
            ]

        def convert_combobox_data(combobox_data):
            """
            Converts specific values (0 -> False, 1 -> True) for boolean-like fields in combobox attributes.
            COMBOBOXDATA = ISEDITABLE: 0, # boolean-like field
            MAXCHARS: 16, # integer field
            MAXDISPLAY: 5, # integer field
            ASCIIONLY: 0, # boolean-like field
            LETTERSANDNUMBERS: 0; # boolean-like field
            """
            converted_data = {}
            for item in combobox_data:
                for key, value in item.items():
                    if key in ['ISEDITABLE', 'ASCIIONLY', 'LETTERSANDNUMBERS']:
                        if value == 0:
                            converted_data[key] = False
                        elif value == 1:
                            converted_data[key] = True
                        else:
                            converted_data[key] = value
                    else:
                        converted_data[key] = value
            return converted_data

        combobox_data = convert_combobox_data(properties.attributes['COMBOBOXDATA'])
        self.create_attributes_for_control(combobox_data)

        enabled_data = filter_empty_properties(properties.textures['ENABLEDDRAWDATA'])
        disabled_data = filter_empty_properties(properties.textures['DISABLEDDRAWDATA'])
        hilite_data = filter_empty_properties(properties.textures['HILITEDRAWDATA'])
        dropdown_button_enabled_data = filter_empty_properties(properties.textures['COMBOBOXDROPDOWNBUTTONENABLEDDRAWDATA'])
        dropdown_button_disabled_data = filter_empty_properties(properties.textures['COMBOBOXDROPDOWNBUTTONDISABLEDDRAWDATA'])
        dropdown_button_hilite_data = filter_empty_properties(properties.textures['COMBOBOXDROPDOWNBUTTONHILITEDRAWDATA'])
        editbox_enabled_data = filter_empty_properties(properties.textures['COMBOBOXEDITBOXENABLEDDRAWDATA'])
        editbox_disabled_data = filter_empty_properties(properties.textures['COMBOBOXEDITBOXDISABLEDDRAWDATA'])
        editbox_hilite_data = filter_empty_properties(properties.textures['COMBOBOXEDITBOXHILITEDRAWDATA'])


        self.create_textures_for_control({
            'ENABLEDDRAWDATA': enabled_data,
            'DISABLEDDRAWDATA': disabled_data,
            'HILITEDRAWDATA': hilite_data,
            'COMBOBOXDROPDOWNBUTTONENABLEDDRAWDATA': dropdown_button_enabled_data,
            'COMBOBOXDROPDOWNBUTTONDISABLEDDRAWDATA': dropdown_button_disabled_data,
            'COMBOBOXDROPDOWNBUTTONHILITEDRAWDATA': dropdown_button_hilite_data,
            'COMBOBOXEDITBOXENABLEDDRAWDATA': editbox_enabled_data,
            'COMBOBOXEDITBOXDISABLEDDRAWDATA': editbox_disabled_data,
            'COMBOBOXEDITBOXHILITEDRAWDATA': editbox_hilite_data
        })

    def clear(self):
        """Clear all widgets from the layout."""
        layout = self.layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout = item.layout()
                if layout is not None:
                    self.clear_layout(layout)

        self.type_label = QLabel(self.type, self)
        layout.addWidget(self.type_label)


    def clear_layout(self, layout):
        """Recursively clears a layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                inner_layout = item.layout()
                if inner_layout is not None:
                    self.clear_layout(inner_layout)

def create_header_with_separator(title):
    # Create the separator line
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)

    # Create the header label
    header_label = QLabel(f"  {title}  ")

    # Create the layout and add the label and separator
    line_layout = QHBoxLayout()
    line_layout.addWidget(header_label)
    line_layout.addWidget(separator)
    line_layout.setStretch(1, 1)  # Add stretch to the separator
    line_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

    # Create a container widget to hold the layout
    container_widget = QWidget()
    container_widget.setLayout(line_layout)
    container_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    return container_widget

def create_inner_section(title, parent, section_manager, object_name):
    section = CollapsibleSection(title, parent, section_manager=section_manager)
    section.setObjectName(object_name)  # Set the object name for QSS styling
    section.setStyleSheet("QFrame { border: none; }")  # Minimal styling
    return section