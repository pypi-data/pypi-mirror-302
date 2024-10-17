import tkinter as tk
from tkinter import filedialog
import ast
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

def getcoms(filename):
    # Liste zum Speichern der gefundenen Funktionen
    functions = []
    
    # Datei einlesen
    with open(filename, "r") as file:
        # Inhalt der Datei in den abstrakten Syntaxbaum (AST) umwandeln
        tree = ast.parse(file.read(), filename=filename)
    
    # Alle Knoten im AST durchlaufen und nur die FunctionDef-Knoten extrahieren
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    
    return functions
    
def writetofile(filename, texttowrite):
    
    with open(filename, 'a') as file:  # 'a' steht für 'append', um an die Datei anzuhängen
        file.write(texttowrite)