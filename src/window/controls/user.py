from src.error_handler import ErrorHandler, InvalidValuesError

class Window:
    def __init__(self, window_uuid, window_properties=None, children=None, file_name=None):
        """
        Initializes a new window object.
        :param window_uuid: A unique identifier for the window (UUID).
        :param window_properties: Configuration properties for the window.
        :param children: A list of child windows, defaults to an empty list if no children are provided.
        """
        self.window_uuid = window_uuid
        self.properties = window_properties or {}
        self.children = children if children is not None else []
        self.file_name = file_name


class UserControl(Window):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for UserControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'USER'
            self.properties['NAME'] = 'user'
            self.properties['SCREENRECT'] = {
                'UPPERLEFT': [10, 10],
                'BOTTOMRIGHT': [200, 100],
                'CREATIONRESOLUTION': [800, 600]
            }
            self.properties['STATUS'] = 'ENABLED'
            self.properties['STYLE'] = 'USER'
            self.properties['SYSTEMCALLBACK'] = '[None]'
            self.properties['INPUTCALLBACK'] = '[None]'
            self.properties['TOOLTIPCALLBACK'] = '[None]'
            self.properties['DRAWCALLBACK'] = '[None]'
            self.properties['FONT'] = {
                'name': "Times New Roman",
                'size': 14,
                'bold': 0
            }
            self.properties['HEADERTEMPLATE'] = '[NONE]'
            self.properties['TOOLTIPTEXT'] = ''
            self.properties['TOOLTIPDELAY'] = -1
            self.properties['TEXT'] = ''
            self.properties['TEXTCOLOR'] = {
                'ENABLED': (255, 255, 255, 255), 'ENABLEDBORDER': (255, 255, 255, 255),
                'DISABLED': (255, 255, 255, 255), 'DISABLEDBORDER': (255, 255, 255, 255),
                'HILITE': (255, 255, 255, 255), 'HILITEBORDER': (255, 255, 255, 255)
            }
            self.properties['attributes'] = {}
            self.properties['textures'] = {
                'ENABLEDDRAWDATA':  [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}],
            }

    def _set_FONT(self, value):
         # Font name must be one of the valid properties
        valid_fonts = ["Times New Roman", "Arial", "Courier New", "Placard MT Condensed", "Generals", "Courier"]
        if value["name"] not in valid_fonts:
            raise InvalidValuesError(f"Invalid font name: {value['name']}. Valid properties: {valid_fonts}")
        # Font size must be between 8 and 72
        if not (8 <= value["size"] <= 72):
            raise InvalidValuesError("Font size must be between 8 and 72.")
        # Bold value must be either 0 or 1
        if value["bold"] not in [0, 1]:
            raise InvalidValuesError("Font bold must be either 0 or 1.")

        self.properties['FONT'] = value

    def _set_STATUS(self, value):
        valid_status = ["ENABLED", "DISABLED", "IMAGE", "HIDDEN"]
        # Status must be one of the predefined properties
        if not any(status in value for status in valid_status):
            raise InvalidValuesError(f"Invalid status: {value}. Valid properties: {valid_status}")
        self.properties['STATUS'] = value

    def _set_SCREENRECT(self, value):
        upper_left, bottom_right = value["UPPERLEFT"], value["BOTTOMRIGHT"]
        creation_resolution = value["CREATIONRESOLUTION"]

        # Check that upper_left coordinates are within the bounds of creation_resolution
        if not (0 <= upper_left[0] <= creation_resolution[0] and 0 <= upper_left[1] <= creation_resolution[1]):
            ErrorHandler.raise_error( self.file_name, 0, '',
                f"Window name: {self.properties['NAME']}:\n"
                f"Upper left {upper_left} coordinates must be within screen bounds\n"
                f"defined by creation_resolution {creation_resolution}.", error_level=2)
        # Check that bottom_right coordinates are within the bounds of creation_resolution
        if not (0 <= bottom_right[0] <= creation_resolution[0] and 0 <= bottom_right[1] <= creation_resolution[1]):
            ErrorHandler.raise_error( self.file_name, 0, '',
                f"Window name: {self.properties['NAME']}:\n"
                f"Bottom right {bottom_right} coordinates must be within screen bounds\n"
                f"defined by creation_resolution {creation_resolution}.", error_level=2)

        # Ensure the rectangle size is at least 1x1 pixel
        if not (bottom_right[0] > upper_left[0] and bottom_right[1] > upper_left[1]):
            raise InvalidValuesError("Rectangle size must be at least 1x1 pixel.")

        # If all validations pass, store the value
        self.properties['SCREENRECT'] = value

    def _is_valid_color(self, color):
        # Check if the color is a tuple of 4 integers (RGBA format)
        if isinstance(color, tuple) and len(color) == 4:
            # Ensure each component is in the range 0-255
            return all(0 <= component <= 255 for component in color)
        return False

    def _set_TEXTCOLOR(self, value):
        # Every color must be in RGBA format with values between 0 and 255
        for color_name, color in value.items():
            if not self._is_valid_color(color):
                raise InvalidValuesError(
                    f"Invalid color for {color_name}: {color}. Colors must be in RGBA format with values between 0 and 255.")

        self.properties['TEXTCOLOR'] = value

    # Utility function to validate RGBA color format
    def _validate_rgba(self, color):
        if len(color) != 4:
            raise InvalidValuesError("Color must have exactly 4 values (R, G, B, A).")
        for value in color:
            if not (0 <= value <= 255):
                raise InvalidValuesError("Color values must be between 0 and 255.")

    # Utility function to validate IMAGE field
    def _validate_image(self, image):
        if image != "NoImage" and not isinstance(image, str):
            raise InvalidValuesError("Image must be a string or 'NoImage'.")

    # General draw data validation
    def _validate_draw_data(self, draw_data):
        # Validate the format for each entry
        if not isinstance(draw_data, list) or len(draw_data) != 9:
            raise InvalidValuesError(f"Draw data must be a list with exactly 9 items, len: {len(draw_data)}")

        for entry in draw_data:
            if 'IMAGE' not in entry or 'COLOR' not in entry or "BORDERCOLOR" not in entry:
                raise InvalidValuesError("Each draw data entry must contain IMAGE, COLOR, and BORDERCOLOR.")
            self._validate_image(entry['IMAGE'])
            self._validate_rgba(entry['COLOR'])
            self._validate_rgba(entry["BORDERCOLOR"])

    # Use internal variables for drawing data
    def _set_textures(self, value):
        for key, draw_data in value.items():
            self._validate_draw_data(draw_data)
        self.properties['textures'] = value

    def _format_screenrect(self):
        """
        Formats the screen rectangle (upper left, bottom right, and creation resolution)
        into a human-readable string.
        """
        screen_rect = self.properties['SCREENRECT']
        return (
            f"SCREENRECT = UPPERLEFT: {screen_rect['UPPERLEFT'][0]} {screen_rect['UPPERLEFT'][1]},\n"
            f"             BOTTOMRIGHT: {screen_rect['BOTTOMRIGHT'][0]} {screen_rect['BOTTOMRIGHT'][1]},\n"
            f"             CREATIONRESOLUTION: {screen_rect['CREATIONRESOLUTION'][0]} {screen_rect['CREATIONRESOLUTION'][1]};"
        )

    def _format_font(self):
        """Formats the font data (name, size, bold status) into a human-readable string."""
        font = self.properties['FONT']
        return f'FONT = NAME: "{font["name"]}", SIZE: {font["size"]}, BOLD: {font["bold"]};'

    def _format_text_color(self):
        """
      Formats the text color settings into a human-readable string, with explicit formatting
      and precise spacing as required using f-strings.
      """
        text_color_str = "TEXTCOLOR = "
        text_colors = self.properties['TEXTCOLOR']
        indent = " " * len(text_color_str)

        formatted_str = (
            f"{text_color_str}"
            f"ENABLED:  {text_colors['ENABLED'][0]} {text_colors['ENABLED'][1]} {text_colors['ENABLED'][2]} {text_colors['ENABLED'][3]}, "
            f"ENABLEDBORDER:  {text_colors['ENABLEDBORDER'][0]} {text_colors['ENABLEDBORDER'][1]} {text_colors['ENABLEDBORDER'][2]} {text_colors['ENABLEDBORDER'][3]},\n"
            f"{indent}DISABLED: {text_colors['DISABLED'][0]} {text_colors['DISABLED'][1]} {text_colors['DISABLED'][2]} {text_colors['DISABLED'][3]}, "
            f"DISABLEDBORDER: {text_colors['DISABLEDBORDER'][0]} {text_colors['DISABLEDBORDER'][1]} {text_colors['DISABLEDBORDER'][2]} {text_colors['DISABLEDBORDER'][3]},\n"
            f"{indent}HILITE:   {text_colors['HILITE'][0]} {text_colors['HILITE'][1]} {text_colors['HILITE'][2]} {text_colors['HILITE'][3]}, "
            f"HILITEBORDER:   {text_colors['HILITEBORDER'][0]} {text_colors['HILITEBORDER'][1]} {text_colors['HILITEBORDER'][2]} {text_colors['HILITEBORDER'][3]};"
        )
        return formatted_str

    def _format_draw_data(self, draw_data, tag):
        """
        Formats the draw data into a human-readable string. Each entry in the draw data is formatted as
        'IMAGE: <image>, COLOR: <color>, BORDERCOLOR: <BORDERCOLOR>'.

        Args:
            draw_data (list): A list of dictionaries containing the draw data (image, color, and border color).
            tag (str): The name of the tag for the draw data (e.g., ENABLEDDRAWDATA).
        """
        # Calculate the indentation width based on the tag
        width = len(tag + ' = ')
        indent = " " * width

        # If there is no draw data, return an empty string
        if not draw_data:
            return ""

        formatted_lines = []  # Start without the tag
        # Iterate through each entry in the draw data
        for i, entry in enumerate(draw_data):
            image = entry['IMAGE']
            color = " ".join(map(str, entry['COLOR']))
            BORDERCOLOR = " ".join(map(str, entry["BORDERCOLOR"]))

            # Format the draw data entry as a string
            formatted_line = f"IMAGE: {image}, COLOR: {color}, BORDERCOLOR: {BORDERCOLOR}"

            # If it's the last item, end with ';'
            if i == len(draw_data) - 1:
                formatted_lines.append(indent + formatted_line + ";")
            elif i == 0:
                formatted_lines.append(formatted_line + ",")
            else:
                formatted_lines.append(indent + formatted_line + ",")

        # Join the formatted lines into a final string
        return "\n".join(formatted_lines)

    def _format_extra_properties(self, properties):
        """Formats the properties fields into a human-readable string."""
        output = []
        if properties:
            for key, value in properties.items():
                if isinstance(value, list):
                    if key.endswith("DRAWDATA"):
                        draw_data_str = self._format_draw_data(value, key)
                        if draw_data_str:
                            output.append(f"{key} = " + draw_data_str)
                    else:
                        formatted_lines = [f"{key} ="]
                        indent = " " * (len(key + ' = '))
                        first = True
                        for item in value:
                            # Process each dictionary in the list
                            for k, v in item.items():
                                if first:
                                    formatted_lines[0] += f" {k}: {v},"  # Add to the key line
                                    first = False
                                else:
                                    formatted_lines.append(f"{indent}{k}: {v},")  # Subsequent values indented

                        # Remove the last comma and add semicolon
                        formatted_lines[-1] = formatted_lines[-1].rstrip(",") + ";"
                        output.extend(formatted_lines)

        return "\n".join(output)

    def __repr__(self):
        """Formats the entire object into a string representation."""
        output = []

        output.append(f"WINDOWTYPE = {self.properties['WINDOWTYPE']};")
        output.append(self._format_screenrect())
        output.append(f'NAME = "{self.file_name}:{self.properties["NAME"]}";')
        output.append(f"STATUS = {'+'.join(self.properties['STATUS'])};")
        output.append(f"STYLE = {'+'.join(self.properties['STYLE'])};")
        output.append(f'SYSTEMCALLBACK = "{self.properties["SYSTEMCALLBACK"]}";')
        output.append(f'INPUTCALLBACK = "{self.properties["INPUTCALLBACK"]}";')
        output.append(f'TOOLTIPCALLBACK = "{self.properties["TOOLTIPCALLBACK"]}";')
        output.append(f'DRAWCALLBACK = "{self.properties["DRAWCALLBACK"]}";')
        output.append(self._format_font())
        output.append(f'HEADERTEMPLATE = "{self.properties["HEADERTEMPLATE"]}";')

        if self.properties['TOOLTIPTEXT']:
            output.append(f'TOOLTIPTEXT = "{self.properties["TOOLTIPTEXT"]}";')
        if self.properties['TOOLTIPDELAY']:
            output.append(f'TOOLTIPDELAY = {self.properties["TOOLTIPDELAY"]};')
        if self.properties['TEXT']:
            output.append(f'TEXT = "{self.properties["TEXT"]}";')
        output.append(self._format_text_color())

        # Add default draw data
        default_draw_data = ['ENABLEDDRAWDATA', 'DISABLEDDRAWDATA', 'HILITEDRAWDATA']
        for texture_key in default_draw_data:
            output.append(
                f"{texture_key} = {self._format_draw_data(self.properties['textures'][texture_key], texture_key)}")

        attributes = self._format_extra_properties(self.properties['attributes'])
        output.append(attributes)

        for texture_key in self.properties['textures']:
            if texture_key not in default_draw_data:
                output.append(
                    f"{texture_key} = {self._format_draw_data(self.properties['textures'][texture_key], texture_key)}")

        return '\n'.join(output)
