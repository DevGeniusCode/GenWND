import uuid
from window import *

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

        lines_iter = iter(lines)  # Create an iterator for the lines
        # Parse metadata
        lines_iter = self._parse_metadata(lines_iter)

        # Parse windows
        self._parse_windows(lines_iter)

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

    def _parse_metadata(self, lines_iter):
        """
        Extracts metadata from the beginning of the file.
        :param lines_iter: iter of lines from the file.
        :return: Index of the line where metadata ends.
        """
        file_version_found = False
        start_layout_block_found = False
        end_layout_block_found = False

        while True:
            try:
                line = next(lines_iter).strip()
            except StopIteration:
                break
            line = line.strip()
            if line.startswith(";"):
                continue

            # If a WINDOW tag is found, end of metadata is reached
            if line.startswith("WINDOW"):
                lines_iter = iter([line] + list(lines_iter))
                break

            # If STARTLAYOUTBLOCK is found, save block content
            if line.startswith("STARTLAYOUTBLOCK"):
                start_layout_block_found = True
                layout_block = {}
                while True:
                    try:
                        layout_line = next(lines_iter)
                    except StopIteration:
                        break
                    layout_line = layout_line.strip()

                    if layout_line.startswith(self.block_tags["STARTLAYOUTBLOCK"]):
                        end_layout_block_found = True
                        break

                    # Match key-value pairs inside the layout block
                    match = self.tag_pattern.match(layout_line)
                    if self._valid_match(match, 0 - 1, layout_line):
                        key, value = match.groups()
                        if key in layout_block:
                            self._raise_error(0 - 1, layout_line, f"Duplicate key '{key}' in layout block")
                        layout_block[key] = value.strip()

                if not end_layout_block_found:
                    self._raise_error(0 - 1, line, "ENDLAYOUTBLOCK is missing")
                # Store the parsed layout block as a dictionary
                self.file_metadata["LAYOUTBLOCK"] = layout_block
                continue

            # General tag matching for the metadata
            match = self.tag_pattern.match(line)

            if self._valid_match(match, 0, line):
                key, value = match.groups()
                if key in self.file_metadata:
                    self._raise_error(0 - 1, line, f"Duplicate key '{key}' in metadata")
                self.file_metadata[key] = value

            # If FILE_VERSION tag is found
            if line.startswith("FILE_VERSION"):
                file_version_found = True

        # Check for missing or improperly formatted LAYOUTBLOCK or FILE_VERSION
        if not start_layout_block_found or not end_layout_block_found:
            self._raise_error(0 - 1, 0, "LAYOUTBLOCK is missing or improperly formatted")
        if not file_version_found:
            self._raise_error(0 - 1, 0, "Missing FILE_VERSION")
        return lines_iter


    def _parse_windows(self, lines_iter):
        """
        Parses the configuration lines that define a hierarchy of windows and their relationships (parents and children).

        This function processes a series of configuration lines starting with the first "WINDOW" line, extracting
        the configuration of each window, and building a hierarchical structure of windows and their respective children.

        The hierarchy follows these rules:
        - A "WINDOW" defines a new window, which may have a parent window (the last window in the stack).
        - "CHILD" lines indicate a window is a child of the current parent window (the last window in the stack).
        - "END" indicates the end of the current window, and the function will pop the current window from the stack,
          effectively making the previous window the new parent for subsequent windows.
        - "ENDALLCHILDREN" marks the end of a block of child windows, and the parent window remains the same.

        As the windows are processed:
        - Each window is assigned a unique identifier (UUID).
        - Configuration settings for each window (such as options and parameters) are parsed and stored in a dictionary.
        - The windows are stored in a hierarchical tree structure, with each window having a `children` list to hold its child windows.

        :param lines_iter: An iterator over the configuration lines, starting with the first "WINDOW" line.
        :return: None. The parsed windows are stored in the instance attribute `self.windows`.
        :raises ValueError: If any unexpected line structure or inconsistency is encountered (e.g., "CHILD" without a parent window,
                             "END" without an opening "WINDOW", or missing `ENDLAYOUTBLOCK`).
        """
        stack = []  # Stack to manage parent-child relationships
        current_window = None
        parent_window = None  # Track the current parent window

        while True:
            try:
                line = next(lines_iter)
            except StopIteration:
                break
            line = line.strip()


            if line.startswith("WINDOW"):
                # Create a unique UUID for the window
                window_key = str(uuid.uuid4())

                # Gather all lines for this window (until END or CHILD)
                window_lines = []
                while True:
                    try:
                        next_line = next(lines_iter)
                    except StopIteration:
                        break
                    next_line = next_line.strip()

                    # Check for END or CHILD tags to stop collecting lines for the window
                    if next_line.startswith("END") or next_line.startswith("CHILD"):
                        lines_iter = iter([next_line] + list(lines_iter))  # Push back the line for later processing
                        break

                    window_lines.append(next_line)

                # Parse the window's configuration using the parse_window_config function
                window_config = parse_window_config(iter(window_lines))

                # Create a new Window object
                new_window = Window(window_key, config=window_config, children=[])

                # If there is a parent window, add the new window as a child of the correct parent
                if parent_window:
                    parent_window.children.append(new_window)
                else:
                    self.windows.append(new_window)  # Add to the root list of windows

                # Push the new window onto the stack for child processing
                stack.append(new_window)
                parent_window = new_window  # The new window becomes the current parent
                current_window = new_window

            elif line.startswith("END"):
                # Close the current window and return to the parent
                if not stack:
                    raise ValueError(f"Unexpected END without a corresponding WINDOW at line {0}.")
                stack.pop()
                parent_window = stack[-1] if stack else None  # Update the parent window after popping

            elif line.startswith("CHILD"):
                # Handle the CHILD tag (children are implicitly added by the window processing)
                if not parent_window:
                    raise ValueError(f"Unexpected CHILD without a parent window at line {0}.")
                # Skip over the CHILD line, it's just a marker for window nesting
                continue

            elif line.startswith("ENDALLCHILDREN"):
                # Handle the ENDALLCHILDREN tag (ends child block for the current window)
                if not parent_window or not parent_window.children:
                    raise ValueError(f"ENDALLCHILDREN found without children at line {0}.")
                # Skip over the ENDALLCHILDREN line, it's just a marker
                continue

            else:
                # Handle invalid lines (optional for your case)
                pass

        # Check if there are any unclosed windows left
        if stack:
            self._raise_error(0 - 1, "EOF", "Unclosed windows found.")




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
