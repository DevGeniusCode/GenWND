import uuid
from window import *
from resources.config import config
def increment_line_number():
    """
    Increments the global line_number by 1 each time it is called.
    """
    config.line_number += 1

class WndParser:
    block_tags = {
        "STARTLAYOUTBLOCK": "ENDLAYOUTBLOCK",
        "WINDOW": "END",
        "CHILD": "ENDALLCHILDREN"
    }
    tag_pattern = re.compile(r'^(\w+)\s*=\s*(.*);$')

    def __init__(self):
        self.file_metadata = {}
        self.windows = []

    def parse_file(self, file_path):
        """
        Parse a WND file and extract metadata and windows hierarchy.
        :param file_path: Path to the WND file.
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Parse metadata
        self._parse_metadata(lines)

        # Parse windows
        self._parse_windows(lines[config.line_number:])

    def _raise_error(self, line_error, line, error_message) -> None:
        """
        Raises a ValueError with the error message, line content, and line number.
        :param line_error: The line number where the error occurred.
        :param line: The content of the line that caused the error.
        :param error_message: The message describing the error.
        """
        raise ValueError(f"Error: {error_message} at line {line_error + 1}: {line}")

    def _valid_match(self, match, i, line) -> bool:
        """
        Validates the format of a key-value pair match.
        :param match: The match object for the key-value pair.
        :param i: The line number where the match was found.
        :param line: The actual line of text being validated.
        :return: True if match is valid, raises error if invalid.
        """
        if match:
            key, value = match.groups()
            if not value or not key:
                self._raise_error(i, line, "Missing value or key")

            # Ensure there are spaces around '='
            if '=' not in line or ' ' not in line.split('=')[0] or ' ' not in line.split('=')[1]:
                self._raise_error(i, line, "Missing spaces around '='")
        else:
            if line in self.block_tags or line in self.block_tags.values():
                return False
            if line == '':
                return False
            if not line.endswith(';'):
                self._raise_error(i, line, "Missing ';' at the end of the line")
            elif line and not any(line.startswith(tag) for tag in self.block_tags):
                self._raise_error(i, line, "Invalid format")

        return True


    def _parse_metadata(self, lines):
        """
        Extracts metadata from the beginning of the file.
        :param lines: List of lines from the file.
        :return: Index of the line where metadata ends.
        """
        global global_line_number
        metadata_end_index = 0
        file_version_found = False
        start_layout_block_found = False
        end_layout_block_found = False
        i = config.line_number


        while i < len(lines):
            line = lines[i].strip()

            if line.startswith(";"):
                i += 1
                continue

            # If a WINDOW tag is found, end of metadata is reached
            if line.startswith("WINDOW"):
                metadata_end_index = i
                break

            # If STARTLAYOUTBLOCK is found, save block content
            if line.startswith("STARTLAYOUTBLOCK"):
                start_layout_block_found = True
                layout_block = {}
                i += 1
                while i < len(lines):
                    layout_line = lines[i].strip()
                    if layout_line.startswith(self.block_tags["STARTLAYOUTBLOCK"]):
                        end_layout_block_found = True
                        break

                    # Match key-value pairs inside the layout block
                    match = self.tag_pattern.match(layout_line)
                    if self._valid_match(match, i, layout_line):
                        key, value = match.groups()
                        if key in layout_block:
                            self._raise_error(i, line, f"Duplicate key '{key}' in layout block")
                        layout_block[key] = value.strip()
                    i += 1

                if not end_layout_block_found:
                    self._raise_error(i, line, "ENDLAYOUTBLOCK is missing")
                # Store the parsed layout block as a dictionary
                self.file_metadata["LAYOUTBLOCK"] = layout_block
                continue

            match = self.tag_pattern.match(line)
            if self._valid_match(match, i, line):
                key, value = match.groups()
                if key in self.file_metadata:
                    self._raise_error(i, line, f"Duplicate key '{key}' in metadata")
                self.file_metadata[key] = value

            if line.startswith("FILE_VERSION"):
                file_version_found = True

            i += 1
        if not start_layout_block_found or not end_layout_block_found:
            self._raise_error(i, line, "LAYOUTBLOCK is missing or improperly formatted")
        if not file_version_found:
            self._raise_error(i, line, "Missing FILE_VERSION")

        config.line_number = metadata_end_index

    def _parse_windows(self, lines):
        """
        Parses the window configuration lines and builds the hierarchy of windows and their children.
        :param lines: List of lines from the configuration starting from the first "WINDOW" line.
        :return: None (windows are stored in the instance).
        """
        stack = []  # Stack to manage parent-child relationships
        current_window = None
        line_number = 0

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            line_number += 1
            increment_line_number()

            if line.startswith("WINDOW"):
                # Create a unique UUID for the window
                window_key = str(uuid.uuid4())

                # Gather all lines for this window (until END or CHILD)
                window_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("END") and not lines[i].strip().startswith("CHILD"):
                    window_lines.append(lines[i])
                    i += 1


                # Parse the window's configuration using the parse_window_config function
                window_config = parse_window_config(window_lines)
                # Create a new Window object
                new_window = Window(window_key, config=window_config, children=[])

                # If there is a parent window, add the new window as a child
                if stack:
                    stack[-1].children.append(new_window)
                else:
                    self.windows.append(new_window)  # Add to the root list of windows

                # Push the new window onto the stack for child processing
                stack.append(new_window)
                current_window = new_window

            elif line.startswith("END"):
                # Close the current window and return to the parent
                if not stack:
                    raise ValueError(f"Unexpected END without a corresponding WINDOW at line {line_number}.")
                stack.pop()
                current_window = stack[-1] if stack else None

            elif line.startswith("CHILD"):
                # Handle the CHILD tag (children are implicitly added by the window processing)
                if not current_window:
                    raise ValueError(f"Unexpected CHILD without a parent window at line {line_number}.")
                continue  # Skip over the CHILD line, it's just a marker for window nesting

            elif line.startswith("ENDALLCHILDREN"):
                # Handle the ENDALLCHILDREN tag (ends child block for the current window)
                if not current_window or not current_window.children:
                    raise ValueError(f"ENDALLCHILDREN found without children at line {line_number}.")
                continue  # Skip over the ENDALLCHILDREN line, it's just a marker

            else:
                # Handle invalid lines (optional for your case)
                pass

            i += 1

        if stack:
            self._raise_error(line_number, "EOF", "Unclosed windows found.")

    def get_metadata(self):
        """
        Get the parsed metadata from the file.
        :return: Metadata dictionary.
        """
        return self.file_metadata

    def get_windows(self):
        """
        Get the parsed windows' hierarchy.
        :return: List of windows.
        """
        return self.windows

# Example usage
if __name__ == "__main__":
    parser = WndParser()
    parser.parse_file("example.wnd")

    print("Metadata:")
    print(parser.get_metadata())

    print("Windows:")
    print(parser.get_windows())
