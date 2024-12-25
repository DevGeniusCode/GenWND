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
            control_creation_map[control_type](self.control_attributes.extra_properties)
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
                attributes_grid.addWidget(prop_combobox, row, 1)
            elif isinstance(value, bool):
                # If the property is a boolean, create a QCheckBox
                prop_checkbox = QCheckBox(self)
                prop_checkbox.setChecked(value)
                attributes_grid.addWidget(prop_checkbox, row, 1)
            elif isinstance(value, int):
                # If the property is an integer, create a QSpinBox
                prop_spinbox = QSpinBox(self)
                prop_spinbox.setValue(value)
                attributes_grid.addWidget(prop_spinbox, row, 1)
            attributes_grid.addWidget(prop_label, row, 0)
            row += 1
        group_box.setLayout(attributes_grid)
        self.layout.addWidget(group_box)

    def create_textures_for_control(self, textures_attributes):
        """Creates texture attributes controls dynamically based on texture data.
        The textures_attributes appear as Collapsible Section in the control properties tab.
        """
        section_manager = SectionManager()  # Create a section manager
        # header with line separator
        self.layout.addWidget(create_header_with_separator("Textures"))

        for texture_type, texture_data in textures_attributes.items():
            if texture_type.endswith("DRAWDATA"):
                texture_type_name = texture_type[:-8]  # Remove 'DRAWDATA' suffix
                section = CollapsibleSection(title=texture_type_name, parent=self, section_manager=section_manager)
                for texture in texture_data:
                    image_combobox = QComboBox(self)
                    image_combobox.addItem(str(texture.get('image', 'No Image')))

                    color_picker_app = ColorPickerApp(
                        color_data= {'texture_layout' : {
                            "color": QColor(texture.get('color')[0], texture.get('color')[1], texture.get('color')[2],
                                            texture.get('color')[3]),
                            "shadow": QColor(texture.get('border_color')[0], texture.get('border_color')[1],
                                             texture.get('border_color')[2], texture.get('border_color')[3])
                        }}
                    )
                    image_layout = QHBoxLayout()
                    image_layout.addWidget(QLabel("Image", self))
                    image_layout.addWidget(image_combobox)
                    image_widget = QWidget()
                    image_widget.setLayout(image_layout)
                    # Disable margins only on top and bottom, keep side margins as they were
                    image_layout.layout().setContentsMargins(image_layout.layout().contentsMargins().left(), 0,
                                                             image_layout.layout().contentsMargins().right(), 0)
                    image_widget.layout().setContentsMargins(image_widget.layout().contentsMargins().left(), 0,
                                                             image_widget.layout().contentsMargins().right(), 0)

                    section.addWidget(image_widget)

                    # colorLabel widget
                    color_label = color_picker_app.findChild(QLabel, "colorLabel")
                    color_label.setText("Color:")
                    shadow_label = color_picker_app.findChild(QLabel, "shadowLabel")
                    shadow_label.setText("Border Color:")
                    section.addWidget(color_picker_app)

                    # Add a separator line after the texture
                    # only if there are more textures to display
                    if texture != texture_data[-1]:
                        separator = QFrame(self)
                        separator.setFrameShape(QFrame.Shape.HLine)
                        separator.setFrameShadow(QFrame.Shadow.Sunken)
                        section.addWidget(separator)

                self.layout.addWidget(section)


    def create_combobox_attributes(self, extra_properties):
        def filter_empty_properties(properties_list):
            return [
                prop for prop in properties_list if not (
                        'image' in prop and prop['image'] == 'NoImage'
                        # or 'color' in prop and prop['color'] == (255, 255, 255, 0)
                        # or 'border_color' in prop and prop['border_color'] == (255, 255, 255, 0)
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

        enabled_data = filter_empty_properties(extra_properties.get('ENABLEDDRAWDATA', []))
        disabled_data = filter_empty_properties(extra_properties.get('DISABLEDDRAWDATA', []))
        hilite_data = filter_empty_properties(extra_properties.get('HILITEDRAWDATA', []))
        combobox_data = convert_combobox_data(extra_properties.get('COMBOBOXDATA', []))
        dropdown_button_enabled_data = filter_empty_properties(
            extra_properties.get('COMBOBOXDROPDOWNBUTTONENABLEDDRAWDATA', []))
        dropdown_button_disabled_data = filter_empty_properties(
            extra_properties.get('COMBOBOXDROPDOWNBUTTONDISABLEDDRAWDATA', []))
        dropdown_button_hilite_data = filter_empty_properties(
            extra_properties.get('COMBOBOXDROPDOWNBUTTONHILITEDRAWDATA', []))
        editbox_enabled_data = filter_empty_properties(extra_properties.get('COMBOBOXEDITBOXENABLEDDRAWDATA', []))
        editbox_disabled_data = filter_empty_properties(extra_properties.get('COMBOBOXEDITBOXDISABLEDDRAWDATA', []))
        editbox_hilite_data = filter_empty_properties(extra_properties.get('COMBOBOXEDITBOXHILITEDRAWDATA', []))

        self.create_attributes_for_control(combobox_data)

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