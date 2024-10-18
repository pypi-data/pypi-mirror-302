# Python File Browser

`filebrowse` is a simple library to browse and select files without creating GUIs using either PyQt5 or Tkinter. `filebrowse` uses PyQT but defaults to Tkinter if not installed.

## Features
- Provides a function `browse()` that opens a file dialog for selecting a file.
- Uses PyQt5 if available, otherwise falls back to Tkinter.

## Requirements
- PyQt5 or Tkinter must be installed.

## Installation
Clone the repository or download the `pyfilebrowser.py` file and include it in your project.

## Usage
To use this library, import it and call the `browse()` function:

```python
import filebrowse as fb

file_path_pyqt = browse()
print(f"Selected file using PyQt5: {file_path_pyqt}")

file_path_tk = browse('Tkinter')
print(f"Selected file using Tkinter: {file_path_tk}")

```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Jatin Gera
