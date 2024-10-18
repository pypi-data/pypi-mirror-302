"""
FileBrowse: A simple library to browse and select files using either PyQt5 or Tkinter.

This library provides a function `browse()` that opens a file dialog to allow the user to select a file.
The function will use PyQt5 if available, otherwise it will use Tkinter. If neither library is available,
an ImportError is raised.

Functions:
    browse(): Opens a file dialog using either PyQt5 or Tkinter and returns the selected file path.

Requirements:
    - PyQt5 or Tkinter must be installed.

Author:
    Jatin Gera

License:
    MIT License
    
    Copyright (c) 2024 Jatin Gera
    
"""

import importlib.util
import sys

def browse(lib='PyQt5'):
    """
    Opens a file dialog using either PyQt5 or Tkinter and returns the selected file path.

    Args:
    lib (str): The preferred library to use for the file dialog ('PyQt5' or 'Tkinter'). Default is 'PyQt5'.

    Returns:
        str: The full path of the selected file.

    Raises:
        ImportError: If neither PyQt5 nor Tkinter is installed.
    """
    # Use PyQt5 if preferred and available
    if lib == 'PyQt5' and importlib.util.find_spec("PyQt5") is not None:
        from PyQt5.QtWidgets import QApplication, QFileDialog
        app = QApplication(sys.argv)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            return file_dialog.selectedFiles()[0]
    # Use Tkinter if preferred or PyQt5 is not available
    elif lib == 'Tkinter' and importlib.util.find_spec("tkinter") is not None:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        return filedialog.askopenfilename()
    # Fallback to whichever library is available
    elif importlib.util.find_spec("PyQt5") is not None:
        from PyQt5.QtWidgets import QApplication, QFileDialog
        app = QApplication(sys.argv)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            return file_dialog.selectedFiles()[0]
    elif importlib.util.find_spec("tkinter") is not None:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        return filedialog.askopenfilename()
    else:
        # Neither PyQt5 nor Tkinter is installed
        raise ImportError("Either PyQt5 or Tkinter must be installed to use the browse function.")

if __name__ == "__main__":
    try:
        file_path_pyqt = browse('PyQt5')
        print(f"Selected file using PyQt5: {file_path_pyqt}")
        
        file_path_tk = browse('Tkinter')
        print(f"Selected file using Tkinter: {file_path_tk}")
    
    except ImportError as e:
        print(e)
