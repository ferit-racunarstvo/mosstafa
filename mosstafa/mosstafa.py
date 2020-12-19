import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import mosspy
import os
import webbrowser
from mosstafa.validation import validation


def add_directory(directory, type):
    file_directory = browse_button()
    directory[type].insert(tk.END, file_directory)


def remove_selected_directory(directory, type):
    selected = directory[type].curselection()

    for index in selected[::-1]:
        directory[type].delete(index)


def browse_button():
    filename = filedialog.askdirectory()
    return filename


def generate_report(dir, entries):
    base_files, test_files, config = [], [], []

    base_files, test_files = _populate_files_from_directory(dir, base_files, test_files)
    config = _set_config_from_entries(entries)

    if validation.required_entries_missing(config) or not test_files:
        messagebox.showinfo("Notice", "Missing UserID, language or test directory ! Check your fields and try again")
        return

    _send_request(config, base_files, test_files)


def _populate_files_from_directory(dir, base_files, test_files):
    for key, value in dir.items():
        directories = value.get(0, tk.END)

        for directory in directories:
            for path, subdirs, files in os.walk(directory):
                for name in files:
                    if key == "Base":
                        base_files.append(os.path.join(path, name))
                    else:
                        test_files.append(os.path.join(path, name))

    return base_files, test_files


def _set_config_from_entries(entries):
    config = []

    for key, value in entries.items():
        config.append(value.get())

    return config


def _send_request(config, base, test):
    m = _init_moss(config)

    for file in base:
        m.addBaseFile(file)

    for file in test:
        m.addFile(file)

    try:
        url = m.send()
        messagebox.showinfo("Info", "Report successfully generated !")
        webbrowser.open(url, new=2)

    except Exception as e:
        messagebox.showinfo("Error", "Error: %s" % str(e))


def _init_moss(config):
    m = mosspy.Moss(config[0], config[5])

    if config[3] != "":
        m.setIgnoreLimit(int(config[3]))

    if config[6] != "":
        m.setCommentString(config[6])

    if config[4] != "":
        m.setNumberOfMatchingFiles(int(config[4]))

    if config[1] != "":
        m.setDirectoryMode(int(config[1]))

    if config[2] != "":
        m.setExperimentalServer(int(config[2]))

    return m
