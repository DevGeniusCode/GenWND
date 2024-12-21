# WNDEdit - Tool for Analyzing and Editing WND Files

**WNDEdit** is a software tool designed to analyze and edit **WND** files, which contain UI settings for the game **Generals**. The tool allows for loading, analyzing, and displaying window (Windows) objects from a WND file in a graphical and organized manner. It was built using **PyQt6** and provides an intuitive user interface for managing and understanding WND files.

The project is inspired by an existing proprietary software with the same name, developed by deezer. The goal of WNDEdit is to enhance the functionality and features of the original tool, while maintaining the original purpose and design.


## Folder Structure

The project is structured as follows:

```
WNDEdit/
├── logs/
│   ├── log_current.log
│   └── log_current_old.log
├── resources/
│   ├── config.py
│   ├── example.wnd
│   └── styles.qss
├── src/
│   ├── error_handler.py
│   ├── file_tree.py
│   ├── log_manager.py
│   ├── main.py
│   ├── object_tree.py
│   ├── property_editor.py
│   ├── window/
│   │   ├── line_iterator.py
│   │   ├── window.py
│   │   └── wnd_parser.py
```

### File Descriptions

1. **main.py**: The main UI file. Displays the graphical interface, which is divided into three parts:
   - The left section for folder management.
   - The next section for navigating objects in the WND file.
   - The section to display the properties of the selected object.
   
2. **error_handler.py**: Error handling. At error level 2, it allows skipping errors without stopping the process (for example, when loading a WND file, if errors are not skipped, they will stop the loading process).

3. **file_tree.py**: File tree management. Allows navigation between files in the folder.

4. **log_manager.py**: Log management. Creates a new log file and replaces the old one with `log_current_old.log`.

5. **object_tree.py**: Creates an object tree from the WND file and displays the windows and their hierarchy.

6. **property_editor.py**: Window property editor. Displays and allows changes to the selected window's properties.

7. **window/line_iterator.py**: Allows line-by-line iteration through the WND file, including a line counter and filename.

8. **window/window.py**: Processes a single window structure from the WND file, creating objects with window properties (Config).

9. **window/wnd_parser.py**: A processing file that parses a WND file and returns an object representing the window hierarchy.

## WND File Example

A WND file is a simple text file containing UI settings for the game. Here's an example of a WND file:

```txt
WINDOW
  WINDOWTYPE = USER
  NAME = "dummy"
  ... rest of window options
  CHILD
  WINDOW ; child
    WINDOWTYPE = CHECKBOX
    ... rest of window child options
  END
  ENDALLCHILDREN
END
```

After parsing the file, a Python object like this would be generated:

```python
parser = {
    'file_metadata': {
        'FILE_VERSION': 'num',
        'LAYOUTBLOCK': {
            'LAYOUTINIT': 'value',
            'LAYOUTSHUTDOWN': 'value',
            'LAYOUTUPDATE': 'value'
        }
    },
    'windows': [
        Window(
            key=uuid1,  # Random UUID for each window
            options={'OPTION1': 'value1', 'OPTION2': 'value2'},
            children=[
                Window(
                    key=uuid2,
                    options={'OPTION1': 'value1', 'OPTION2': 'value2'},
                    children=[]
                ),
                Window(
                    key=uuid3,
                    options={'OPTION3': 'value3'},
                    children=[]
                ),
                Window(
                    key=uuid4,
                    options={'OPTION4': 'value4'},
                    children=[
                        Window(
                            key=uuid5,
                            options={'OPTION5': 'value5'},
                            children=[]
                        )
                    ]
                )
            ]
        )
    ]
}
```

## How to Use

### System Requirements

- Python 3.10
- PyQt6

### Installation

1. Download the code:
   ```bash
   git clone https://github.com/DevGeniusCode/WNDEdit.git
   cd WNDEdit
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Software

To run the software, simply execute the `main.py` file:
```bash
python src/main.py
```

### Analyzing a WND File

1. Open the WND file via the interface.
2. The software will analyze the file and display the object tree.
3. You can navigate between windows and view the properties of each window.

### Error Handling

In case of errors during the WND file parsing, **WNDEdit** uses an error-handling mechanism:
- Errors at level 2 allow the user to skip the error.
- If the error is critical, the loading process will stop.

## Contributions

If you would like to contribute, feel free to submit a Pull Request or open an Issue with suggestions or problems.

## Licensing

The project is licensed under the **Mozilla Public License 2.0** (MPL-2.0) and requires contributions in a collaborative manner while adhering to the **Contributor Covenant** code of conduct. 

