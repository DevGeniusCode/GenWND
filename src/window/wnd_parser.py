import uuid
from src.window.window_properties import *
from src.error_handler import ErrorHandler
from src.window.line_iterator import LineIterator


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

    def __repr__(self):
        """
        Returns a string representation of the WndParser instance in the format of the original WND file.
        """
        lines = []

        # Metadata section
        if 'FILE_VERSION' in self.file_metadata:
            lines.append(f"FILE_VERSION = {self.file_metadata['FILE_VERSION']};")

        # Layout block (if exists)
        if "LAYOUTBLOCK" in self.file_metadata:
            lines.append("STARTLAYOUTBLOCK")
            layout_block = self.file_metadata["LAYOUTBLOCK"]
            for key, value in layout_block.items():
                lines.append(f"  {key} = {value};")
            lines.append("ENDLAYOUTBLOCK")

        # Windows section
        for window in self.windows:
            self._repr_window(window, lines, indent_level=0)

        return "\n".join(lines)

    def _repr_window(self, window, lines, indent_level):
        """
        Recursively generates the string representation for a window and its children.
        """
        indent = "  " * indent_level
        lines.append(f"{indent}WINDOW")

        # Add window properties (e.g., name, type, etc.)
        options_repr = repr(window)
        for line in options_repr.splitlines():
            lines.append(f"{indent}  {line}")  # Add 2 more spaces for indentation inside the window

        # Process children windows
        if window.children:
            for child in window.children:
                lines.append(f"{indent}  CHILD")
                self._repr_window(child, lines, indent_level + 1)
            lines.append(f"{indent}  ENDALLCHILDREN")

        # Close the current window
        lines.append(f"{indent}END")

    def parse_file(self, file_path):
        """
        Parse a WND file and extract metadata and windows hierarchy.
        :param file_path: Path to the WND file.
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Create a LineIterator for better line management
        lines_iter = LineIterator(lines)
        lines_iter.file_path = file_path

        # Parse metadata
        self._parse_metadata(lines_iter, file_path)

        # Parse windows
        self._parse_windows(lines_iter, file_path)

    def _valid_match(self, match, i, line, file_path) -> bool:
        """
        Validates the format of a key-value pair match.
        :param match: The match object for the key-value pair.
        :param i: The line number where the match was found.
        :param line: The actual line of tag being validated.
        :param file_path: The path of the file being parsed.
        :return: True if match is valid, raises error if invalid.
        """
        if match:
            key, value = match.groups()
            if not value or not key:
                ErrorHandler.raise_error(file_path, i, line, "Missing value or key")

            # Ensure there are spaces around '='
            if '=' not in line or ' ' not in line.split('=')[0] or ' ' not in line.split('=')[1]:
                ErrorHandler.raise_error(file_path, i, line, "Missing spaces around '='", error_level=2)
        else:
            if line in self.block_tags or line in self.block_tags.values():
                return False
            if line == '':
                return False
            if not line.endswith(';'):
                ErrorHandler.raise_error(file_path, i, line, "Missing ';' at the end of the line")
            elif line and not any(line.startswith(tag) for tag in self.block_tags):
                ErrorHandler.raise_error(file_path, i, line, "Invalid format", error_level=2)

        return True

    def _parse_metadata(self, lines_iter, file_path):
        """
        Extracts metadata from the beginning of the file.
        :param lines_iter: iter of lines from the file.
        :param file_path: The path of the file being parsed.
        :return: None.
        """
        file_version_found = False
        start_layout_block_found = False
        end_layout_block_found = False

        while True:
            try:
                line = lines_iter.peek().strip()
            except StopIteration:
                break

            # Skip the comment line
            if line.startswith(";"):
                next(lines_iter)
                continue

            # If a WINDOW tag is found, end of metadata is reached
            if line.startswith("WINDOW"):
                # next(lines_iter)  # Move to the next line after the WINDOW tag
                break

            # If STARTLAYOUTBLOCK is found, save block content
            if line.startswith("STARTLAYOUTBLOCK"):
                start_layout_block_found = True
                layout_block = {}
                next(lines_iter)
                while True:
                    layout_line = lines_iter.peek().strip()

                    if layout_line.startswith(self.block_tags["STARTLAYOUTBLOCK"]):
                        end_layout_block_found = True
                        # next(lines_iter)  # Move past the ENDLAYOUTBLOCK tag
                        break

                    # Match key-value pairs inside the layout block
                    match = self.tag_pattern.match(layout_line)
                    if self._valid_match(match, lines_iter.line_number, layout_line, file_path):
                        key, value = match.groups()
                        if key in layout_block:
                            ErrorHandler.raise_error(file_path, lines_iter.line_number, layout_line, f"Duplicate key '{key}' in layout block", error_level=2)
                        layout_block[key] = value.strip()
                    else:
                        break

                    next(lines_iter)

                if not end_layout_block_found:
                    ErrorHandler.raise_error(file_path, lines_iter.line_number, lines_iter.peek().strip(), "ENDLAYOUTBLOCK is missing")
                # Store the parsed layout block as a dictionary
                self.file_metadata["LAYOUTBLOCK"] = layout_block
                next(lines_iter)
                continue

            # General tag matching for the metadata
            match = self.tag_pattern.match(line)

            if self._valid_match(match, lines_iter.line_number, line, file_path):
                key, value = match.groups()
                if key in self.file_metadata:
                    ErrorHandler.raise_error(file_path, lines_iter.line_number, line, f"Duplicate key '{key}' in metadata", error_level=2)
                self.file_metadata[key] = value

            # If FILE_VERSION tag is found
            if line.startswith("FILE_VERSION"):
                file_version_found = True

            next(lines_iter)

        # Check for missing or improperly formatted LAYOUTBLOCK or FILE_VERSION
        if not start_layout_block_found or not end_layout_block_found:
            ErrorHandler.raise_error(file_path, lines_iter.line_number, 0, "LAYOUTBLOCK is missing or improperly formatted")
        if not file_version_found:
            ErrorHandler.raise_error(file_path, lines_iter.line_number, 0, "Missing FILE_VERSION", error_level=2)

    def _parse_windows(self, lines_iter, file_path):
        """
        Parses a hierarchical configuration of windows and their relationships, including parent-child structures.

        This method processes configuration lines starting from the first "WINDOW" line and extracts window definitions,
        storing them in a hierarchical structure. Each window may have children, and the function properly handles nesting
        of child windows under their respective parent windows.

        Rules of parsing:
        - A "WINDOW" line starts the definition of a new window. The window may have a parent (the last window in the stack).
        - A "CHILD" line indicates the current window is a child of the last window on the stack.
        - "END" signifies the end of the current window's definition, and the function pops the window from the stack,
          making the previous window the new parent.
        - "ENDALLCHILDREN" marks the end of a block of child windows for the current parent, without altering the parent-child
          relationship.

        Each window is assigned a unique identifier (UUID), and its properties are parsed and stored in a dictionary.
        Child windows are added to their parent window’s `children` list, creating a tree-like structure.

        :param lines_iter: An iterator over the configuration lines. Starts with the first "WINDOW" line.
        :param file_path: The path to the configuration file being parsed.
        :return: None. The parsed windows are stored in the instance attribute `self.windows`.
        :raises ValueError: If an unexpected line structure is encountered, such as "CHILD" without a parent window,
                             "END" without a corresponding "WINDOW", or missing "ENDALLCHILDREN" when required.
        """
        stack = []  # Stack to manage parent-child relationships
        parent_window = None  # Track the current parent window

        while True:
            try:
                line = lines_iter.peek().strip()
            except StopIteration:
                break


            if line == "WINDOW":
                next(lines_iter)
                # Create a unique UUID for the window
                window_uuid = str(uuid.uuid4())

                # Parse the window's properties using the parse_window_properties function
                new_window = parse_window_properties(lines_iter, file_name=lines_iter.file_path, window_uuid=window_uuid)

                # Create a new Window object with its properties
                next_line = lines_iter.peek().strip()
                if next_line.startswith("END") or next_line.startswith("CHILD"):
                    line = next_line
                # If there is a parent window, add the new window as a child of the correct parent
                if parent_window:
                    parent_window.children.append(new_window)
                else:
                    self.windows.append(new_window)  # Add to the root list of windows

                # Push the new window onto the stack for child processing
                stack.append(new_window)
                parent_window = new_window  # The new window becomes the current parent

            if line == "END":
                # Close the current window and return to the parent
                if not stack:
                    ErrorHandler.raise_error(file_path, lines_iter.line_number, line, "Unexpected END without a corresponding WINDOW")
                stack.pop()
                parent_window = stack[-1] if stack else None  # Update the parent window after popping

            if line == "CHILD":
                # Handle the CHILD tag (children are implicitly added by the window processing)
                if not parent_window:
                    ErrorHandler.raise_error(file_path, lines_iter.line_number, line, "Unexpected CHILD without a parent window")
                # Skip over the CHILD line, it's just a marker for window nesting

            if line == "ENDALLCHILDREN":
                # Handle the ENDALLCHILDREN tag (ends child block for the current window)
                if not parent_window or not parent_window.children:
                    ErrorHandler.raise_error(file_path, lines_iter.line_number, line, "ENDALLCHILDREN found without children")
                # Skip over the ENDALLCHILDREN line, it's just a marker

            if line.startswith(';') :
                pass

            if not (line == "WINDOW" or line == "END" or line == "CHILD" or line == "ENDALLCHILDREN" or line.startswith(
                    ';')):
                # Throw an error if an invalid line is encountered
                ErrorHandler.raise_error(file_path, lines_iter.line_number, line, "Unexpected line encountered.", error_level=2)

            next(lines_iter)  # Continue processing the next line

        # Check if there are any unclosed windows left

        if stack:
            ErrorHandler.raise_error(file_path, lines_iter.line_number, "EOF", "Unclosed windows found.")

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


def print_window_hierarchy(windows, indent_level=0):
    """
    Prints the window hierarchy with names and indentation.

    :param windows: A list of Window objects.
    :param indent_level: The current indentation level (for recursive calls).
    """
    for window in windows:
        # Extract window name, default to "UNKNOWN" if not found
        window_name = window.properties.get('name', 'Unnamed')
        if window_name:
            complete_name = f"{ window.properties.WINDOWTYPE}:{window_name}"
        else:
            complete_name = f"{ window.properties.WINDOWTYPE}"

        # Print the window name with proper indentation
        indent = "   " * indent_level  # Use spaces for indent
        print(f"{indent}{complete_name}")
        if window.children:
            print(f"{indent} |")
            # Recursively print children with increased indent
            print_window_hierarchy(window.children, indent_level + 1)


# Example usage
if __name__ == "__main__":
    parser = WndParser()
    parser.parse_file(r"resources/example.wnd")
    print(parser)
    # print("Metadata:")
    # print(parser.get_metadata())
    #
    # print("Windows:")
    # print_window_hierarchy(parser.windows)
