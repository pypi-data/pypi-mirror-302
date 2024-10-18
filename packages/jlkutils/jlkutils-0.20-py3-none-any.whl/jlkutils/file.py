import tkinter as tk
from tkinter import filedialog

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

def getcoms(filename):
    # Liste zum Speichern der gefundenen Funktionen
    functions = []
    
    # Datei einlesen
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # Durch alle Zeilen iterieren
    for line in lines:
        line = line.strip()  # Entfernt führende und nachfolgende Leerzeichen
        
        # Prüfen, ob die Zeile mit "def " beginnt
        if line.startswith("def "):
            # Funktionsnamen extrahieren (zwischen "def " und "(")
            func_name = line[4:line.index("(")].strip()
            functions.append(func_name)
    
    return functions

    
def writetofile(filename, texttowrite):
    
    with open(filename, 'a') as file:  # 'a' steht für 'append', um an die Datei anzuhängen
        file.write(texttowrite)