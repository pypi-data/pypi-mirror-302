import tkinter as tk
from tkinter import filedialog
# file_writer.py

def writenewline(filename, texttowrite):
    """
    Schreibt den angegebenen Text als neue Zeile in die Datei.

    :param filename: Name der Datei, in die geschrieben werden soll.
    :param texttowrite: Der Text, der als neue Zeile geschrieben werden soll.
    """
    with open(filename, 'a') as file:  # 'a' steht für 'append', um an die Datei anzuhängen
        file.write(texttowrite + '\n')

def choose_file():
    root = tk.Tk()
    root.withdraw()  # Versteckt das Hauptfenster
    file_path = filedialog.askopenfilename()  # Öffnet das Dateiauswahlfenster
    return file_path
