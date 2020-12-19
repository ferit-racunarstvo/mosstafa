import tkinter as tk
from types import SimpleNamespace
from queue import Queue
from enum import Enum
from threading import Thread
from mosstafa import mosstafa
from mosstafa.config import FIELDS, DIR


class Event(Enum):
    DIRECTORY_ADD = 0
    DIRECTORY_DELETE = 1
    GENERATE_REPORT = 2


def update_cycle(gui, queue):
    while True:
        msg = queue.get()

        if isinstance(msg, tuple):
            if msg[0] == Event.DIRECTORY_ADD:
                mosstafa.add_directory(gui.dir, msg[1])

            elif msg[0] == Event.DIRECTORY_DELETE:
                mosstafa.remove_selected_directory(gui.dir, msg[1])

        else:
            if msg == Event.GENERATE_REPORT:
                gui.generate_button.configure(text="Generating.. please wait")
                mosstafa.generate_report(gui.dir, gui.entries)
                gui.generate_button.configure(text="Generate report")


def init_gui(root, fields, directories, queue):
    entries, dir = {}, {}

    config_frame = tk.LabelFrame(root, text="Configuration")
    config_frame.pack(padx=5, pady=5)

    for key, value in fields.items():
        row = tk.Frame(config_frame)
        row.pack(side=tk.TOP,
                 fill=tk.X,
                 padx=5,
                 pady=5)

        lab = tk.Label(row, width=10, text=key + ": ", anchor='w')
        lab.pack(side=tk.LEFT)

        ent = tk.Entry(row)
        ent.insert(0, value)
        ent.pack(side=tk.RIGHT,
                 expand=tk.YES,
                 fill=tk.X,
                 padx=(15, 0))

        entries |= {key: ent}

    for frame in directories:
        base_frame = tk.LabelFrame(root, text=frame)
        base_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        base_frame.columnconfigure(0, weight=1)
        base_frame.rowconfigure(1, weight=1)

        listbox = tk.Listbox(base_frame, height=6)
        listbox.grid(row=0, columnspan=3, column=0, sticky='nsew')

        button = tk.Button(base_frame, text="Add directory",
                           command=lambda f=frame: queue.put((Event.DIRECTORY_ADD, f)))
        button.grid(row=1, column=1, padx=2, pady=2)

        button = tk.Button(base_frame, text="Delete", command=lambda f=frame: queue.put((Event.DIRECTORY_DELETE, f)))
        button.grid(row=1, column=2, padx=2, pady=2)

        dir |= {frame: listbox}

    generate_button = tk.Button(root, text="Generate report",
                                command=lambda: queue.put(Event.GENERATE_REPORT))
    generate_button.pack(side=tk.RIGHT, padx=5, pady=5, expand=True, fill=tk.BOTH)

    return SimpleNamespace(dir=dir, entries=entries, generate_button=generate_button)


if __name__ == '__main__':
    root = tk.Tk(className='Mosstafa v1-beta - Simple Moss Gui')
    queue = Queue()

    gui = init_gui(root, FIELDS, DIR, queue)

    t = Thread(target=update_cycle, args=(gui, queue,))
    t.daemon = True
    t.start()

    tk.mainloop()
