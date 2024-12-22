import re
from src.error_handler import ErrorHandler
from src.window.line_iterator import LineIterator


class InvalidValuesError(Exception):
    """Exception raised when the values are invalid."""

    def __init__(self, message="Invalid values provided"):
        self.message = message
        super().__init__(self.message)


class Window:
    def __init__(self, window_uuid, window_properties=None, children=None):
        """
        Initializes a new window object.
        :param window_uuid: A unique identifier for the window (UUID).
        :param window_properties: Configuration properties for the window.
        :param children: A list of child windows, defaults to an empty list if no children are provided.
        """
        self.window_uuid = window_uuid
        self.properties = window_properties or {}
        self.children = children if children is not None else []


class WindowProperties:
    def __init__(self, window_type, screen_rect, name, status, style,
                 system_callback, input_callback, tooltip_callback, draw_callback,
                 font, header_template, tooltip_text, tooltip_delay, text, text_color, enabled_draw_data,
                 disabled_draw_data, hilited_draw_data, extra_properties):
        self.WINDOWTYPE = window_type
        self.SCREENRECT = screen_rect
        self.NAME = name
        self.STATUS = status
        self.STYLE = style
        self.SYSTEMCALLBACK = system_callback
        self.INPUTCALLBACK = input_callback
        self.TOOLTIPCALLBACK = tooltip_callback
        self.DRAWCALLBACK = draw_callback
        self.FONT = font
        self.HEADERTEMPLATE = header_template
        self.TOOLTIPTEXT = tooltip_text
        self.TOOLTIPDELAY = tooltip_delay
        self.TEXT = text
        self.TEXTCOLOR = text_color
        self._ENABLEDDRAWDATA = enabled_draw_data
        self._DISABLEDDRAWDATA = disabled_draw_data
        self._HILITEDRAWDATA = hilited_draw_data
        self.extra_properties = extra_properties

    def get(self, key, default=None):
        """
        Retrieve a value by key, returning default if the key does not exist.
        If the key is 'name' and the value contains a colon (":"), return the part after the colon.
        """
        value = getattr(self, key, default)
        if key == 'name' and isinstance(value, str) and ":" in value:
            return value.split(":")[-1]
        return value

    @property
    def FONT(self):
        return self._font

    @FONT.setter
    def FONT(self, value):
        # Font name must be one of the valid properties
        valid_fonts = ["Times New Roman", "Arial", "Courier New", "Placard MT Condensed", "Generals"]
        if value["name"] not in valid_fonts:
            raise InvalidValuesError(f"Invalid font name: {value['name']}. Valid properties: {valid_fonts}")

        # Font size must be between 8 and 72
        if not (8 <= value["size"] <= 72):
            raise InvalidValuesError("Font size must be between 8 and 72.")

        # Bold value must be either 0 or 1
        if value["bold"] not in [0, 1]:
            raise InvalidValuesError("Font bold must be either 0 or 1.")

        self._font = value

    @property
    def STATUS(self):
        return self._status

    @STATUS.setter
    def STATUS(self, value):
        valid_status = ["ENABLED", "DISABLED", "IMAGE", "HIDDEN"]
        # Status must be one of the predefined properties
        if not any(status in value for status in valid_status):
            raise InvalidValuesError(f"Invalid status: {value}. Valid properties: {valid_status}")
        self._status = value

    @property
    def SCREENRECT(self):
        return self._screen_rect

    @SCREENRECT.setter
    def SCREENRECT(self, value):
        upper_left, bottom_right = value["upper_left"], value["bottom_right"]
        creation_resolution = value["creation_resolution"]  # New addition to handle the resolution

        # Check that upper_left coordinates are within the bounds of creation_resolution
        if not (0 <= upper_left[0] <= creation_resolution[0] and 0 <= upper_left[1] <= creation_resolution[1]):
            raise InvalidValuesError(
                f"Upper left coordinates must be within screen bounds defined by creation_resolution.")
        #
        # # # Check that bottom_right coordinates are within the bounds of creation_resolution
        # if not (0 <= bottom_right[0] <= creation_resolution[0] and 0 <= bottom_right[1] <= creation_resolution[1]):
        #     raise InvalidValuesError(
        #         f"Bottom right coordinates must be within screen bounds defined by creation_resolution.")

        # Ensure the rectangle size is at least 1x1 pixel
        if not (bottom_right[0] > upper_left[0] and bottom_right[1] > upper_left[1]):
            raise InvalidValuesError("Rectangle size must be at least 1x1 pixel.")

        # If all validations pass, store the value
        self._screen_rect = value

    @property
    def TEXTCOLOR(self):
        return self._text_color

    def _is_valid_color(self, color):
        # Check if the color is a tuple of 4 integers (RGBA format)
        if isinstance(color, tuple) and len(color) == 4:
            # Ensure each component is in the range 0-255
            return all(0 <= component <= 255 for component in color)
        return False

    @TEXTCOLOR.setter
    def TEXTCOLOR(self, value):
        # Every color must be in RGBA format with values between 0 and 255
        for color_name, color in value.items():
            if not self._is_valid_color(color):
                raise InvalidValuesError(
                    f"Invalid color for {color_name}: {color}. Colors must be in RGBA format with values between 0 and 255.")

        self._text_color = value

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
            if "image" not in entry or "color" not in entry or "border_color" not in entry:
                raise InvalidValuesError("Each draw data entry must contain IMAGE, COLOR, and BORDERCOLOR.")
            self._validate_image(entry["image"])
            self._validate_rgba(entry["color"])
            self._validate_rgba(entry["border_color"])

    # Use internal variables for drawing data

    # Setter for ENABLEDDRAWDATA
    @property
    def enabled_draw_data(self):
        return self._ENABLEDDRAWDATA

    @enabled_draw_data.setter
    def enabled_draw_data(self, value):
        self._validate_draw_data(value)
        self._ENABLEDDRAWDATA = value

    # Setter for DISABLEDDRAWDATA
    @property
    def disabled_draw_data(self):
        return self._DISABLEDDRAWDATA

    @disabled_draw_data.setter
    def disabled_draw_data(self, value):
        self._validate_draw_data(value)
        self._DISABLEDDRAWDATA = value

    # Setter for HILITEDRAWDATA
    @property
    def hilite_draw_data(self):
        return self._HILITEDRAWDATA

    @hilite_draw_data.setter
    def hilite_draw_data(self, value):
        self._validate_draw_data(value)
        self._HILITEDRAWDATA = value

    def _format_screenrect(self):
        """
        Formats the screen rectangle (upper left, bottom right, and creation resolution)
        into a human-readable string.

        Returns:
            str: The formatted screen rectangle string.
        """
        screen_rect = self.SCREENRECT
        return (
            f"SCREENRECT = UPPERLEFT: {screen_rect['upper_left'][0]} {screen_rect['upper_left'][1]},\n"
            f"             BOTTOMRIGHT: {screen_rect['bottom_right'][0]} {screen_rect['bottom_right'][1]},\n"
            f"             CREATIONRESOLUTION: {screen_rect['creation_resolution'][0]} {screen_rect['creation_resolution'][1]};"
        )

    def _format_font(self):
        """
        Formats the font data (name, size, bold status) into a human-readable string.

        Returns:
            str: The formatted font string.
        """
        font = self.FONT
        return f'FONT = NAME: "{font["name"]}", SIZE: {font["size"]}, BOLD: {font["bold"]};'

    def _format_text_color(self):
        """
        Formats the text color settings into a human-readable string, splitting across multiple lines
        with indentation.

        Returns:
            str: The formatted text color string.
        """
        text_color_str = "TEXTCOLOR ="
        color_strings = []
        indent = " " * len(text_color_str) + " "  # Create an indent with the width of "TEXTCOLOR = "

        # Iterate through the text color dictionary and create formatted color strings
        for key, color in self.TEXTCOLOR.items():
            r, g, b, a = color
            color_strings.append(f"{key}: {r} {g} {b} {a}")

        formatted_lines = [text_color_str]
        current_line = text_color_str  # Start with the initial "TEXTCOLOR =" line
        for i, color_str in enumerate(color_strings):
            if i % 2 == 0 and i != 0:  # If this is the first color on a new line
                formatted_lines.append(indent + color_str + ",")  # Add a new line with the indent
            else:  # If it's on the same line, just add it to the current_line string
                if i == 0:
                    formatted_lines[0] += " " + color_str + ","
                else:
                    formatted_lines[-1] += " " + color_str + ","

        # Ensure the last line ends with a semicolon
        formatted_lines[-1] = formatted_lines[-1].rstrip(",") + ";"

        return '\n'.join(formatted_lines)

    def _format_draw_data(self, draw_data, tag):
        """
        Formats the draw data into a human-readable string. Each entry in the draw data is formatted as
        'IMAGE: <image>, COLOR: <color>, BORDERCOLOR: <border_color>'.

        Args:
            draw_data (list): A list of dictionaries containing the draw data (image, color, and border color).
            tag (str): The name of the tag for the draw data (e.g., ENABLEDDRAWDATA).

        Returns:
            str: The formatted draw data string.
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
            image = entry["image"]
            color = " ".join(map(str, entry["color"]))
            border_color = " ".join(map(str, entry["border_color"]))

            # Format the draw data entry as a string
            formatted_line = f"IMAGE: {image}, COLOR: {color}, BORDERCOLOR: {border_color}"

            # If it's the last item, end with ';'
            if i == len(draw_data) - 1:
                formatted_lines.append(indent + formatted_line + ";")
            elif i == 0:
                formatted_lines.append(formatted_line + ",")
            else:
                formatted_lines.append(indent + formatted_line + ",")

        # Join the formatted lines into a final string
        return "\n".join(formatted_lines)

    def _format_extra_properties(self):
        """
        Formats the properties fields into a human-readable string.

        Returns:
            str: The formatted properties fields string.
        """
        output = []
        if self.extra_properties:
            for key, value in self.extra_properties.items():
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
        """
        Formats the entire object into a string representation.

        Returns:
            str: The formatted string representation of the object.
        """
        output = []

        output.append(f"WINDOWTYPE = {self.WINDOWTYPE};")
        output.append(self._format_screenrect())
        output.append(f'NAME = "{self.NAME}";')
        output.append(f"STATUS = {'+'.join(self.STATUS)};")
        output.append(f"STYLE = {'+'.join(self.STYLE)};")
        output.append(f'SYSTEMCALLBACK = "{self.SYSTEMCALLBACK}";')
        output.append(f'INPUTCALLBACK = "{self.INPUTCALLBACK}";')
        output.append(f'TOOLTIPCALLBACK = "{self.TOOLTIPCALLBACK}";')
        output.append(f'DRAWCALLBACK = "{self.DRAWCALLBACK}";')
        output.append(self._format_font())
        output.append(f'HEADERTEMPLATE = "{self.HEADERTEMPLATE}";')

        if self.TOOLTIPTEXT:
            output.append(f'TOOLTIPTEXT = "{self.TOOLTIPTEXT}";')
        if self.TOOLTIPDELAY:
            output.append(f'TOOLTIPDELAY = {self.TOOLTIPDELAY};')
        if self.TEXT:
            output.append(f'TEXT = "{self.TEXT}";')
        output.append(self._format_text_color())

        # Add formatted draw data
        output.append(f"ENABLEDDRAWDATA = {self._format_draw_data(self.enabled_draw_data, 'ENABLEDDRAWDATA')}")
        output.append(f"DISABLEDDRAWDATA = {self._format_draw_data(self.disabled_draw_data, 'DISABLEDDRAWDATA')}")
        output.append(f"HILITEDRAWDATA = {self._format_draw_data(self.hilite_draw_data, 'HILITEDRAWDATA')}")

        # Add properties fields if they exist
        output.append(self._format_extra_properties())

        return '\n'.join(output)


def parse_screenrect(lines_iter):
    combined_line = ""
    while True:
        try:
            line = lines_iter.peek().strip()
            combined_line += line
            if combined_line.endswith(';'):
                match = re.match(
                    r"SCREENRECT = UPPERLEFT: (\d+) (\d+),\s*BOTTOMRIGHT: (\d+) (\d+),\s*CREATIONRESOLUTION: (\d+) (\d+);",
                    combined_line
                )
                if match:
                    upper_left_x = int(match.group(1))
                    upper_left_y = int(match.group(2))
                    bottom_right_x = int(match.group(3))
                    bottom_right_y = int(match.group(4))
                    creation_res_x = int(match.group(5))
                    creation_res_y = int(match.group(6))

                    return {
                        "upper_left": (upper_left_x, upper_left_y),
                        "bottom_right": (bottom_right_x, bottom_right_y),
                        "creation_resolution": (creation_res_x, creation_res_y),
                    }
                else:
                    raise ValueError("Invalid SCREENRECT format")
            next(lines_iter)
        except StopIteration:
            break
    raise ValueError("SCREENRECT not found or formatted incorrectly")


def parse_text_colors(lines_iter):
    combined_line = ""
    text_colors = {}
    while True:
        try:
            line = lines_iter.peek().strip()
            combined_line += line
            if combined_line.endswith(';'):
                match = re.findall(r'(\w+):\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+);?', combined_line)
                if match:
                    for key, r, g, b, a in match:
                        text_colors[key] = (int(r), int(g), int(b), int(a))
                    return text_colors
                else:
                    raise ValueError("Invalid text color format")
            next(lines_iter)
        except StopIteration:
            break
    raise ValueError("TEXTCOLOR not found or formatted incorrectly")


def parse_draw_data(lines_iter):
    # Function to parse draw data with IMAGE, COLOR, BORDERCOLOR
    draw_data = []
    combined_line = ""
    while True:
        try:
            line = lines_iter.peek().strip()
            combined_line += line
            if combined_line.endswith(';'):
                draw_matches = re.findall(r'IMAGE: (\S+), COLOR: (\d+ \d+ \d+ \d+), BORDERCOLOR: (\d+ \d+ \d+ \d+)',
                                          combined_line)
                if draw_matches:
                    for image, color, border_color in draw_matches:
                        draw_data.append({
                            "image": image,
                            "color": tuple(map(int, color.split())),
                            "border_color": tuple(map(int, border_color.split()))
                        })
                    return draw_data  # Return if valid data found
                else:
                    raise ValueError("Invalid draw data format")

            next(lines_iter)
        except StopIteration:
            break
    raise ValueError("Draw data not found or formatted incorrectly")


def parse_color_field(value):
    # Function to parse color-related properties (like TEXTCOLOR)
    color_data = {}
    color_matches = re.findall(r'(\w+):\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)', value)
    for name, r, g, b, a in color_matches:
        # Store the color as a tuple (r, g, b, a)
        color_data[name] = (int(r), int(g), int(b), int(a))
    return color_data


def parse_extra_properties(lines_iter):
    # Dictionary to store parsed values
    extra_properties = {}
    combined_line = ""
    tag_value_pattern = re.compile(r'(\w+)\s*=\s*([^;]+);')

    while True:
        try:
            line = lines_iter.peek().strip()
            if line in ["END", "CHILD"]:
                break
            combined_line += line
            if combined_line.endswith(';'):
                match = tag_value_pattern.match(combined_line)
                if match:
                    tag, value = match.groups()
                    value = value.strip()
                    # Handling draw data (like IMAGE, COLOR, BORDERCOLOR)
                    if tag.endswith("DRAWDATA"):
                        extra_properties[tag] = parse_draw_data(LineIterator(combined_line.splitlines()))
                    elif tag.endswith("DATA"):
                        subfields = []
                        sub_lines_iter = LineIterator(value.split(','))  # create iterator for subfields
                        columns_value = None
                        columns_widths = 0

                        while True:
                            try:
                                sub_line = next(sub_lines_iter).strip()
                                sub_match = re.match(r'(\w+):\s*([^,;]+)(?:,|$)', sub_line)
                                if sub_match:
                                    sub_name, sub_value = sub_match.groups()
                                    sub_value = int(sub_value.strip())

                                    if sub_name == "COLUMNS":
                                        # Save the COLUMNS value to check COLUMNSWIDTH later
                                        columns_value = sub_value
                                    elif sub_name == "COLUMNSWIDTH":
                                        # Collect COLUMNSWIDTH appears
                                        columns_widths += 1
                                    subfields.append({sub_name: sub_value})
                                elif sub_line:  # Skip empty subfields
                                    raise ValueError(f"Invalid subfield format: '{sub_line}'")

                            except StopIteration:
                                # After processing, check if the number of COLUMNSWIDTH matches COLUMNS
                                if columns_value is not None:
                                    if columns_widths != columns_value:
                                        ErrorHandler.raise_error(lines_iter.file_path, lines_iter.line_number, combined_line,
                                            f"Number of COLUMNSWIDTH ({columns_widths}) does not match COLUMNS number({columns_value})", error_level=2)
                                break
                        extra_properties[tag] = subfields
                    else:
                        raise ValueError("Invalid data")
                else:
                    raise ValueError("Invalid window_properties field format")
                combined_line = ""
            next(lines_iter)
        except StopIteration:
            break
    return extra_properties


# Function to parse the window properties and return a WindowProperties object
def parse_window_properties(lines_iter):
    # Initialize variables to store parsed data
    line_start = lines_iter.line_number
    window_type = ""
    screen_rect = {}
    name = ""
    status = []
    style = []
    system_callback = ""
    input_callback = ""
    tooltip_callback = ""
    draw_callback = ""
    font = {}
    header_template = ""
    tooltip_text = ""
    tooltip_delay = None
    text = ""
    text_color = {}
    enabled_draw_data = []
    disabled_draw_data = []
    hilited_draw_data = {}
    extra_properties = {}

    # A list to track tags we've seen so far, in the order they were encountered
    encountered_tags = []

    # Define the correct order of tags
    correct_tag_order = [
        "WINDOWTYPE", "SCREENRECT", "NAME", "STATUS", "STYLE",
        "SYSTEMCALLBACK", "INPUTCALLBACK", "TOOLTIPCALLBACK", "DRAWCALLBACK",
        "FONT", "HEADERTEMPLATE", "TOOLTIPTEXT", "TOOLTIPDELAY", "TEXT", "TEXTCOLOR",
        "ENABLEDDRAWDATA", "DISABLEDDRAWDATA", "HILITEDRAWDATA"
    ]
    while True:
        try:
            line = lines_iter.peek().strip().rstrip(";")  # Clean up the line

            # If we encounter END or CHILD, break the loop
            if line in ["END", "CHILD", "ENDALLCHILDREN"]:
                break

            if "=" not in line and not line.startwith(";"):
                ErrorHandler.raise_error(lines_iter.file_path, lines_iter.line_number, line,
                "Unexpeced line", error_level=2)

            tag = line.split('=')[0].strip()

            # Check if the tag appears in the correct order
            if tag in correct_tag_order:
                expected_index = correct_tag_order.index(tag)
                if encountered_tags:
                    last_encountered_tag = encountered_tags[-1]
                    last_encountered_index = correct_tag_order.index(last_encountered_tag)
                    if expected_index < last_encountered_index:
                        # If the tag appears out of order, raise an error using _raise_error
                        raise ValueError(f"Tag '{tag}' appeared out of order. Expected after '{last_encountered_tag}'.")
            # Parse each line based on its tag
            match tag:
                case "WINDOWTYPE":
                    window_type = line.split("=")[1].strip()

                case "SCREENRECT":
                    screen_rect = parse_screenrect(lines_iter)

                case "NAME":
                    name = line.split("=")[1].strip().strip('"')

                # Handle multiple STATUS values (e.g., ENABLED+IMAGE)
                case "STATUS":
                    status = [s.strip() for s in line.strip().split("=")[1].split("+")]

                # Handle multiple STYLE values (e.g., MOUSETRACK+COMBOBOX)
                case "STYLE":
                    style = [s.strip() for s in line.strip().split("=")[1].strip().split("+")]

                # Handle CALLBACK lines
                case "SYSTEMCALLBACK" | "INPUTCALLBACK" | "TOOLTIPCALLBACK" | "DRAWCALLBACK":
                    callback_value = line.split("=")[1].strip().strip('"')
                    match tag:
                        case "SYSTEMCALLBACK":
                            system_callback = callback_value
                        case "INPUTCALLBACK":
                            input_callback = callback_value
                        case "TOOLTIPCALLBACK":
                            tooltip_callback = callback_value
                        case "DRAWCALLBACK":
                            draw_callback = callback_value

                case "FONT":
                    match = re.match(r'FONT = NAME: "(.+)", SIZE: (\d+), BOLD: (\d+)?', line)
                    if match:
                        font = {
                            "name": match.group(1),
                            "size": int(match.group(2)),
                            "bold": int(match.group(3))
                        }

                case "HEADERTEMPLATE":
                    header_template = line.split("=")[1].strip().strip('"')

                case "TOOLTIPTEXT":
                    tooltip_text = line.split("=")[1].strip().strip('"')

                case "TOOLTIPDELAY":
                    tooltip_delay = int(line.split("=")[1].strip())

                case "TEXT":
                    text = line.split("=")[1].strip().strip('"')

                case "TEXTCOLOR":
                    text_color = parse_text_colors(lines_iter)

                # Handle DRAWDATA lines
                case "ENABLEDDRAWDATA":
                    enabled_draw_data = parse_draw_data(lines_iter)

                case "DISABLEDDRAWDATA":
                    disabled_draw_data = parse_draw_data(lines_iter)

                case "HILITEDRAWDATA":
                    hilited_draw_data = parse_draw_data(lines_iter)

                # Handle other fields or additional custom parsing
                case _:
                    extra_properties = parse_extra_properties(lines_iter)

            # After processing, add the tag to the list of encountered tags
            line = lines_iter.peek().strip().rstrip(";")
            encountered_tags.append(tag)
            if line in ["END", "CHILD", "ENDALLCHILDREN"]:
                break

            next(lines_iter)

        except StopIteration:
            break
        except ValueError as e:
            ErrorHandler.raise_error(lines_iter.file_path, lines_iter.line_number, line, e, error_level=2)

    # Return the WindowProperties object with the parsed data
    try:
        return WindowProperties(
            window_type=window_type,
            screen_rect=screen_rect,
            name=name,
            status=status,
            style=style,
            system_callback=system_callback,
            input_callback=input_callback,
            tooltip_callback=tooltip_callback,
            draw_callback=draw_callback,
            font=font,
            header_template=header_template,
            tooltip_text=tooltip_text,
            tooltip_delay=tooltip_delay,
            text=text,
            text_color=text_color,
            enabled_draw_data=enabled_draw_data,
            disabled_draw_data=disabled_draw_data,
            hilited_draw_data=hilited_draw_data,
            extra_properties=extra_properties
        )
    except ValueError as e:
        ErrorHandler.raise_error(lines_iter.file_path, -1, f"Window block that start in {line_start}", e, error_level=1)
    except InvalidValuesError as e:
        ErrorHandler.raise_error(lines_iter.file_path, -1, f"Window block that start in {line_start}", e, error_level=1)
