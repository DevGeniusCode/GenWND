import re
from src.error_handler import ErrorHandler, InvalidValuesError
from src.window.controls.checkbox import CheckBoxControl
from src.window.controls.combobox import ComboBoxControl
from src.window.controls.entryfiled import EntryFieldControl
from src.window.controls.horzslider import HorzSliderControl
from src.window.controls.progressbar import ProgressBarControl
from src.window.controls.pushbutton import PushButtonControl
from src.window.controls.radiobutton import RadioButtonControl
from src.window.controls.scrollistbox import ScrollListBoxControl
from src.window.controls.statictext import StaticTextControl
from src.window.controls.user import UserControl
from src.window.controls.vertslider import VertSliderControl
from src.window.line_iterator import LineIterator


class ObjectFactory:
    def __init__(self):
        # Mapping from object types to control classes
        self.control_classes = {
            "USER": UserControl,
            "PUSHBUTTON": PushButtonControl,
            "STATICTEXT": StaticTextControl,
            "ENTRYFIELD": EntryFieldControl,
            "CHECKBOX": CheckBoxControl,
            "RADIOBUTTON": RadioButtonControl,
            "PROGRESSBAR": ProgressBarControl,
            "HORZSLIDER": HorzSliderControl,
            "VERTSLIDER": VertSliderControl,
            "SCROLLLISTBOX": ScrollListBoxControl,
            "COMBOBOX": ComboBoxControl
        }

    def create_object(self, object_type, window_uuid, properties=None, children=None, file_name=None):
        control_class = self.control_classes.get(object_type)
        if not control_class:
            raise ValueError(f"Invalid window type: {object_type}")
        return control_class(window_uuid, properties, children, file_name)


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
                        "UPPERLEFT": (upper_left_x, upper_left_y),
                        "BOTTOMRIGHT": (bottom_right_x, bottom_right_y),
                        "CREATIONRESOLUTION": (creation_res_x, creation_res_y),
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
                    for image, color, BORDERCOLOR in draw_matches:
                        draw_data.append({
                            "IMAGE": image,
                            "COLOR": tuple(map(int, color.split())),
                            "BORDERCOLOR": tuple(map(int, BORDERCOLOR.split()))
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


def parse_textures_properties(lines_iter):
    # Dictionary to store parsed values
    textures_properties = {}
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
                    textures_properties[tag] = parse_draw_data(LineIterator(combined_line.splitlines()))
                else:
                    raise ValueError("Invalid window_properties field format")
                combined_line = ""
            next(lines_iter)
        except StopIteration:
            break
    return textures_properties


def parse_attributes_properties(lines_iter):
    # Dictionary to store parsed values
    combined_line = ""
    tag_value_pattern = re.compile(r'(\w+)\s*=\s*([^;]+)(?:,|;)?')
    subfields = []
    columns_value = None
    columns_widths = 0

    while True:
        try:
            line = lines_iter.peek().strip()
            match = tag_value_pattern.match(line)
            if line in ["END", "CHILD"] or (match and match.group(1).endswith("DRAWDATA")):
                break
            combined_line += line
            if combined_line.endswith(';'):
                match = tag_value_pattern.match(combined_line)
                if match:
                    tag, value = match.groups()
                    value = value.strip()
                    sub_lines_iter = LineIterator(value.split(','))  # create iterator for subfields

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
                            if columns_value is not None and columns_value > 1:
                                if columns_widths != columns_value:
                                    ErrorHandler.raise_error(lines_iter.file_path, lines_iter.line_number,
                                                             combined_line,
                                                             f"Number of COLUMNSWIDTH ({columns_widths}) does not match COLUMNS number({columns_value})",
                                                             error_level=2)
                            break
                    if not subfields:
                        raise ValueError("Invalid data")
                else:
                    raise ValueError("Invalid window_properties field format")
                break
            next(lines_iter)
        except StopIteration:
            break

    return subfields


# Function to parse the window properties and return a Window object
def parse_window_properties(lines_iter, window_uuid, file_name):
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
    textures = {}
    attributes = {}

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

            if "=" not in line and not line.startswith(";"):
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
                    file_name = line.split("=")[1].strip().strip('"').split(":")[0]
                    if file_name == "":
                        ErrorHandler.raise_error(lines_iter.file_path, lines_iter.line_number, line,
                                                 f"file name is missing in name", error_level=2)
                    name = line.split("=")[1].strip().strip('"').split(":")[-1]

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

                # Handle other fields or additional custom parsing
                case _:
                    if tag.endswith("DRAWDATA"):
                        textures[tag] = parse_draw_data(lines_iter)
                    elif tag.endswith("DATA"):
                        attributes[tag] = parse_attributes_properties(lines_iter)
                    else:
                        raise ErrorHandler.raise_error(lines_iter.file_path, lines_iter.line_number, line,
                                                       f"Unknown tag: {tag}", error_level=2)

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

    # Return the  object with the parsed data, according to window_type
    try:
        factory = ObjectFactory()

        new_object = factory.create_object(window_type, window_uuid,
                                           properties={
                                               'WINDOWTYPE': window_type,
                                               'NAME': name,
                                               # 'SCREENRECT': screen_rect,
                                               # 'STATUS': status,
                                               'STYLE': style,
                                               'SYSTEMCALLBACK': system_callback,
                                               'INPUTCALLBACK': input_callback,
                                               'TOOLTIPCALLBACK': tooltip_callback,
                                               'DRAWCALLBACK': draw_callback,
                                               # 'FONT': font,
                                               'HEADERTEMPLATE': header_template,
                                               'TOOLTIPTEXT': tooltip_text,
                                               'TOOLTIPDELAY': tooltip_delay,
                                               'TEXT': text,
                                               # 'TEXTCOLOR': text_color,
                                               'attributes': attributes,
                                               # 'textures': textures
                                           }, file_name=file_name)
        new_object._set_SCREENRECT(screen_rect)
        new_object._set_STATUS(status)
        new_object._set_FONT(font)
        new_object._set_TEXTCOLOR(text_color)
        new_object._set_textures(textures)

        return new_object
    except ValueError as e:
        ErrorHandler.raise_error(lines_iter.file_path, -1, f"Window block that start in {line_start}", e, error_level=1)
    except InvalidValuesError as e:
        ErrorHandler.raise_error(lines_iter.file_path, -1, f"Window block that start in {line_start}", e, error_level=1)
