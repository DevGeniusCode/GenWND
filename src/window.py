import re

class Window:
    def __init__(self, window_key, config=None, children=None):
        """
        Initializes a new window object.
        :param window_key: A unique identifier for the window (UUID).
        :param config: Configuration options for the window.
        :param children: A list of child windows, defaults to an empty list if no children are provided.
        """
        self.window_key = window_key
        self.options = config or {}
        self.children = children if children is not None else []

class Config:
    def __init__(self, window_type, screen_rect, name, status, style,
                 system_callback, input_callback, tooltip_callback, draw_callback,
                 font, header_template, tooltip_delay, text, text_color, enabled_draw_data,
                 disabled_draw_data, hilited_draw_data, config_fields):
        self.window_type = window_type
        self.screen_rect = screen_rect
        self.name = name
        self.status = status
        self.style = style
        self.system_callback = system_callback
        self.input_callback = input_callback
        self.tooltip_callback = tooltip_callback
        self.draw_callback = draw_callback
        self.font = font
        self.header_template = header_template
        self.tooltip_delay = tooltip_delay
        self.text = text
        self.text_color = text_color
        self._enabled_draw_data = enabled_draw_data
        self._disabled_draw_data = disabled_draw_data
        self._hilited_draw_data = hilited_draw_data
        self.config_fields = config_fields

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        # Font name must be one of the valid options
        valid_fonts = ["Times New Roman", "Arial", "Courier New", "Placard MT Condensed"]
        if value["name"] not in valid_fonts:
            raise ValueError(f"Invalid font name: {value['name']}. Valid options: {valid_fonts}")

        # Font size must be between 8 and 72
        if not (8 <= value["size"] <= 72):
            raise ValueError("Font size must be between 8 and 72.")

        # Bold value must be either 0 or 1
        if value["bold"] not in [0, 1]:
            raise ValueError("Font bold must be either 0 or 1.")

        self._font = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_status = ["ENABLED", "DISABLED", "IMAGE", "HIDDEN"]
        # Status must be one of the predefined options
        if not any(status in value for status in valid_status):
            raise ValueError(f"Invalid status: {value}. Valid options: {valid_status}")
        self._status = value

    @property
    def screen_rect(self):
        return self._screen_rect

    @screen_rect.setter
    def screen_rect(self, value):
        upper_left, bottom_right = value["upper_left"], value["bottom_right"]
        creation_resolution = value["creation_resolution"]  # New addition to handle the resolution

        # Check that upper_left coordinates are within the bounds of creation_resolution
        if not (0 <= upper_left[0] <= creation_resolution[0] and 0 <= upper_left[1] <= creation_resolution[1]):
            raise ValueError(f"Upper left coordinates must be within screen bounds defined by creation_resolution.")

        # Check that bottom_right coordinates are within the bounds of creation_resolution
        if not (0 <= bottom_right[0] <= creation_resolution[0] and 0 <= bottom_right[1] <= creation_resolution[1]):
            raise ValueError(f"Bottom right coordinates must be within screen bounds defined by creation_resolution.")

        # Ensure the rectangle size is at least 1x1 pixel
        if not (bottom_right[0] > upper_left[0] and bottom_right[1] > upper_left[1]):
            raise ValueError("Rectangle size must be at least 1x1 pixel.")

        # If all validations pass, store the value
        self._screen_rect = value

    @property
    def text_color(self):
        return self._text_color

    def _is_valid_color(self, color):
        # Check if the color is a tuple of 4 integers (RGBA format)
        if isinstance(color, tuple) and len(color) == 4:
            # Ensure each component is in the range 0-255
            return all(0 <= component <= 255 for component in color)
        return False

    @text_color.setter
    def text_color(self, value):
        # Every color must be in RGBA format with values between 0 and 255
        for color_name, color in value.items():
            if not self._is_valid_color(color):
                raise ValueError(
                    f"Invalid color for {color_name}: {color}. Colors must be in RGBA format with values between 0 and 255.")

        self._text_color = value

    # Utility function to validate RGBA color format
    def _validate_rgba(self, color):
        if len(color) != 4:
            raise ValueError("Color must have exactly 4 values (R, G, B, A).")
        for value in color:
            if not (0 <= value <= 255):
                raise ValueError("Color values must be between 0 and 255.")

    # Utility function to validate IMAGE field
    def _validate_image(self, image):
        if image != "NoImage" and not isinstance(image, str):
            raise ValueError("Image must be a string or 'NoImage'.")

    # General draw data validation
    def _validate_draw_data(self, draw_data):
        # Validate the format for each entry
        if not isinstance(draw_data, list) or len(draw_data) != 9:
            raise ValueError("Draw data must be a list with exactly 9 items.")

        for entry in draw_data:
            if "image" not in entry or "color" not in entry or "border_color" not in entry:
                raise ValueError("Each draw data entry must contain IMAGE, COLOR, and BORDERCOLOR.")
            self._validate_image(entry["image"])
            self._validate_rgba(entry["color"])
            self._validate_rgba(entry["border_color"])

    # Use internal variables for drawing data


    # Setter for ENABLEDDRAWDATA
    @property
    def enabled_draw_data(self):
        return self._enabled_draw_data

    @enabled_draw_data.setter
    def enabled_draw_data(self, value):
        self._validate_draw_data(value)
        self._enabled_draw_data  = value

    # Setter for DISABLEDDRAWDATA
    @property
    def disabled_draw_data(self):
        return self._disabled_draw_data

    @disabled_draw_data.setter
    def disabled_draw_data(self, value):
        self._validate_draw_data(value)
        self._disabled_draw_data = value

    # Setter for HILITEDRAWDATA
    @property
    def hilite_draw_data(self):
        return self._hilited_draw_data

    @hilite_draw_data.setter
    def hilite_draw_data(self, value):
        self._validate_draw_data(value)
        self._hilited_draw_data = value


def parse_screenrect(lines_iter):
    combined_line = ""
    while True:
        try:
            line = next(lines_iter)
            combined_line += line.strip()
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
        except StopIteration:
            break
    raise ValueError("SCREENRECT not found or formatted incorrectly")


def parse_text_colors(lines_iter):
    combined_line = ""
    text_colors = {}
    while True:
        try:
            line = next(lines_iter)
            combined_line += line.strip()
            if combined_line.endswith(';'):
                match = re.findall(r'(\w+):\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+);?', combined_line)
                if match:
                    for key, r, g, b, a in match:
                        text_colors[key] = (int(r), int(g), int(b), int(a))
                    return text_colors
                else:
                    raise ValueError("Invalid text color format")
        except StopIteration:
            break
    raise ValueError("TEXTCOLOR not found or formatted incorrectly")


def parse_draw_data(lines_iter):
    # Function to parse draw data with IMAGE, COLOR, BORDERCOLOR
    draw_data = []
    combined_line = ""
    while True:
        try:
            line = next(lines_iter)
            combined_line += line.strip()
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
                    raise ValueError(f"Invalid draw data format")
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


def parse_config_fields(lines_iter):
    # Dictionary to store parsed values
    config_fields = {}
    combined_line = ""
    tag_value_pattern = re.compile(r'(\w+)\s*=\s*([^;]+);')
    while True:
        try:
            line = next(lines_iter)
            combined_line += line.strip()
            if combined_line.endswith(';'):
                match = tag_value_pattern.match(combined_line)
                if match:
                    tag, value = match.groups()
                    value = value.strip()
                    # Handling draw data (like IMAGE, COLOR, BORDERCOLOR)
                    if tag.endswith("DRAWDATA"):
                        config_fields[tag] = parse_draw_data(iter(combined_line.splitlines()))
                    elif tag.endswith("DATA"):
                        subfields = {}
                        sub_lines_iter = iter(value.split(',')) # create iterator for subfields
                        while True:
                             try:
                                  sub_line = next(sub_lines_iter).strip()
                                  sub_match = re.match(r'(\w+):\s*([^,;]+)(?:,|$)', sub_line)
                                  if sub_match:
                                       sub_name, sub_value = sub_match.groups()
                                       subfields[sub_name] = int(sub_value.strip())
                                  elif sub_line: # Skip empty subfields
                                        raise ValueError(f"Invalid subfield format: '{sub_line}'")
                             except StopIteration:
                                  break
                        config_fields[tag] = subfields
                    else:
                        raise ValueError("Invalid data")
                else:
                    raise ValueError("Invalid config field format")
                combined_line = ""
        except StopIteration:
            break
    return config_fields

# Function to parse the window configuration and return a Config object
def parse_window_config(lines_iter):
    # Initialize variables to store parsed data
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
    tooltip_delay = None
    text = ""
    text_color = {}
    enabled_draw_data = []
    disabled_draw_data = []
    hilited_draw_data = {}
    config_fields = {}

    # A list to track tags we've seen so far, in the order they were encountered
    encountered_tags = []

    # Define the correct order of tags
    correct_tag_order = [
        "WINDOWTYPE", "SCREENRECT", "NAME", "STATUS", "STYLE",
        "SYSTEMCALLBACK", "INPUTCALLBACK", "TOOLTIPCALLBACK", "DRAWCALLBACK",
        "FONT", "HEADERTEMPLATE", "TOOLTIPDELAY", "TEXT", "TEXTCOLOR",
        "ENABLEDDRAWDATA", "DISABLEDDRAWDATA", "HILITEDRAWDATA"
    ]
    while True:
        try:
            line = next(lines_iter)
            line = line.strip().rstrip(";")  # Clean up the line

            if "=" not in line:
                continue  # Skip invalid lines without '='

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
                    lines_iter = iter([line] + list(lines_iter))
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
                        case "SYSTEMCALLBACK": system_callback = callback_value
                        case "INPUTCALLBACK": input_callback = callback_value
                        case "TOOLTIPCALLBACK": tooltip_callback = callback_value
                        case "DRAWCALLBACK": draw_callback = callback_value

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

                case "TOOLTIPDELAY":
                    tooltip_delay = int(line.split("=")[1].strip())

                case "TEXT":
                    text = line.split("=")[1].strip()

                case "TEXTCOLOR":
                    lines_iter = iter([line] + list(lines_iter))
                    text_color = parse_text_colors(lines_iter)

                # Handle DRAWDATA lines
                case "ENABLEDDRAWDATA":
                    lines_iter = iter([line] + list(lines_iter))
                    enabled_draw_data = parse_draw_data(lines_iter)

                case "DISABLEDDRAWDATA":
                    lines_iter = iter([line] + list(lines_iter))
                    disabled_draw_data = parse_draw_data(lines_iter)

                case "HILITEDRAWDATA":
                    lines_iter = iter([line] + list(lines_iter))
                    hilited_draw_data = parse_draw_data(lines_iter)

                # Handle other fields or additional custom parsing
                case _:
                    lines_iter = iter([line] + list(lines_iter))
                    config_fields = parse_config_fields(lines_iter)

            # After processing, add the tag to the list of encountered tags
            encountered_tags.append(tag)
        except StopIteration:
            break
        # Create and return a Config object with the parsed data
    return Config(
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
        tooltip_delay=tooltip_delay,
        text=text,
        text_color=text_color,
        enabled_draw_data=enabled_draw_data,
        disabled_draw_data=disabled_draw_data,
        hilited_draw_data=hilited_draw_data,
        config_fields=config_fields
    )
