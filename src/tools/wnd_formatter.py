import argparse
import os
import sys

# Add the project root to Python's path dynamically
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
src_folder = os.path.join(project_root, 'src')
sys.path.insert(0, src_folder)

# Import the parser and the error handler from the project
try:
    from src.window.wnd_parser import WndParser
    from src.error_handler import ErrorHandler
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure you are running this script from the project root.")
    sys.exit(1)


# =====================================================================
# CLI ERROR HANDLER PATCH (Monkey Patching)
# =====================================================================
def cli_raise_error(file_path, line_number, line_content, error_message, error_level=2):
    """
    Replaces the original graphical error handler for CLI usage.
    Instead of popping up a Qt dialog, it prints the error to the terminal
    and automatically simulates choosing "Ignore" for non-critical warnings.
    """
    error_details = (f"Error in file '{os.path.basename(str(file_path))}'\n"
                     f"  -> At line {line_number + 1}: {error_message}\n"
                     f"  -> Line content: `{line_content}`")

    if error_level == 1:
        # Critical Error (Level 1) - Print in red and abort execution
        print(f"\n\033[91m[CRITICAL ERROR]\033[0m {error_details}")
        return

    elif error_level == 2:
        # Warning (Level 2) - Print in yellow and continue (simulates "Ignore")
        print(f"\n\033[93m[WARNING - SKIPPED]\033[0m {error_details}")
        return  # Returning here allows the parser to continue its execution

    else:
        # Standard logs (Level 3+) - Print in blue
        print(f"\n\033[94m[INFO]\033[0m {error_details}")
        return


# Apply the patch by replacing the original method reference
ErrorHandler.raise_error = cli_raise_error


# =====================================================================

def format_wnd_file(input_path: str, output_path: str = None) -> None:
    """
    Parses a WND file into an AST and writes it back formatted.
    """
    if not os.path.exists(input_path):
        print(f"[!] Error: Could not find file '{input_path}'")
        return

    if output_path is None:
        output_path = input_path

    # print(f"[*] Parsing and formatting '{os.path.basename(input_path)}'...")

    parser = WndParser()

    try:
        parser.parse_file(input_path)
        formatted_text = repr(parser)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
            f.write("\n")

        # print(f"[+] Success! Formatted file saved.")

    except Exception as e:
        print(f"\n[!] Failed to format '{os.path.basename(input_path)}'.")
        print(f"Reason: {e}")


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description="Standalone WND formatter tool")
    cli_parser.add_argument("input_file", help="Path to the input .wnd file")
    cli_parser.add_argument("-o", "--output", help="Path to output file", default=None)

    args = cli_parser.parse_args()
    format_wnd_file(args.input_file, args.output)