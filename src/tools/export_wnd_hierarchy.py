import os
# Import your real parser (ensure the path matches your project structure)
from src.window.wnd_parser import WndParser


# ==========================================
# Markdown/tree generation logic
# ==========================================
def generate_visual_tree(windows, prefix=""):
    """
    Walk through windows and build a CMD/Linux-style visual tree.
    """
    lines = []

    for i, window in enumerate(windows):
        # Check whether this is the last window in the current level
        is_last = (i == len(windows) - 1)
        connector = "└── " if is_last else "├── "

        # Safely extract properties
        props = getattr(window, 'properties', {})
        name = 'Unnamed'
        wtype = 'UnknownType'

        if isinstance(props, dict):
            name = props.get('Name', props.get('NAME', props.get('name', 'Unnamed')))
            wtype = props.get('WINDOWTYPE', props.get('WindowType', props.get('Type', 'UnknownType')))
        else:
            name = getattr(props, 'Name', getattr(props, 'NAME', getattr(props, 'name', 'Unnamed')))
            wtype = getattr(props, 'WINDOWTYPE', getattr(props, 'WindowType', getattr(props, 'Type', 'UnknownType')))

        name = name.replace('"', '')

        # Build current line
        lines.append(f"{prefix}{connector}[{wtype}] {name}")

        # Handle children (if any)
        if hasattr(window, 'children') and window.children:
            # If parent is last, continue with spaces; otherwise keep vertical branch
            extension = "    " if is_last else "│   "
            lines.extend(generate_visual_tree(window.children, prefix + extension))

    return lines


def export_wnd_to_txt(windows, output_filepath):
    """
    Generate tree text and save it to a file (TXT or Markdown code block).
    """
    lines = generate_visual_tree(windows)

    # Wrap in a code block so spacing is preserved in Markdown viewers
    file_content = "WND Hierarchy Tree\n==================\n\n```text\n" + "\n".join(lines) + "\n```\n"

    # Preview (first 20 lines only)
    print("--- Preview ---")
    print("\n".join(lines[:20]))
    print("...\n--------------------\n")

    # Save to file
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)

    print(f"Hierarchy tree saved successfully to: {os.path.abspath(output_filepath)}")


# ==========================================
# Script entry point
# ==========================================
def main():
    # 1) Path to your WND file
    wnd_file_path = r"C:\Users\User\Documents\GitHub\GeneralsIsraelMod\Patch104pZH\GameFilesEdited\Window\Menus\MainMenu.wnd"  # Update path if needed

    if not os.path.exists(wnd_file_path):
        print(f"Error: file not found: {wnd_file_path}")
        return

    # 2) Run parser (correct method is parse_file, not parse)
    my_parser = WndParser()
    my_parser.parse_file(wnd_file_path)

    # 3) Get windows (via attribute or get_windows())
    real_root_windows = my_parser.get_windows()

    if not real_root_windows:
        print("No windows found in file, or parsing failed.")
        return

    # 4) Export hierarchy to Markdown/TXT
    output_md_path = "real_hierarchy.md"
    export_wnd_to_txt(real_root_windows, output_md_path)


if __name__ == "__main__":
    main()
