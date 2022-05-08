# Quelle: [Ymoslem, o. D.a]

# Ein Skript, zur Bereinigung des Datensatzes für die maschinelle Übersetzung. 
# Voraussetzung sind zwei Dateien: Eine Quelldatei (Quellsprache) und eine Zieldatei (Zielsprache).
# Das Filterskript führt die folgenden Schritte aus:
# Löschen von leeren Zeilen;
# Löschen von Duplikaten;
# Löschen von in der Quelle kopierten Zeilen;
# Löschen von zu langen Quell-/Zieltexten (Verhältnis 200% und > 200 Wörter);
# Entfernen von HTML;
# Segmente bleiben verbleiben in ihrer korrekten Groß- und Kleinschreibung, es sei denn, lower wird auf true gesetzt;
# Mischen von Zeilen;
# Schreiben der Ausgabedateien.


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Befehl: python3 filter.py <Quelldatei_pfad> <Zieldateipfad> <Quellsprache> <Zielsprache>
# Beispielbefehl: python3 filter.py Data/Europarl.de-en.en Data/Europarl.de-en.de en de


import pandas as pd
import numpy as np
import re
import csv
import sys

# display(df) funktioniert nur, wenn Sie sich in IPython/Jupyter Notebooks befinden oder es aktivieren:
# from IPython.display import display


def prepare(source_file, target_file, source_lang, target_lang, lower=False):
    
    df_source = pd.read_csv(source_file, names=['Source'], sep="\n", quoting=csv.QUOTE_NONE)
    df_target = pd.read_csv(target_file, names=['Target'], sep="\n", quoting=csv.QUOTE_NONE)
    df = pd.concat([df_source, df_target], axis=1)  # Die beiden Datenbereiche entlang der Spalten verbinden
    print("Datenstruktur (Zeilen, Spalten):", df.shape)

    
    # NaN löschen
    df = df.dropna()

    print("--- Zeile mit leeren Zellen gelöscht\t--> Zeilen:", df.shape[0])


    # Duplikate entfernen
    df = df.drop_duplicates()
    # df = df.drop_duplicates(subset=['Target'])

    print("--- Duplikate entfernt\t\t\t--> Zeilen:", df.shape[0])


    # Kopierte Zeilen löschen
    df["Source-Copied"] = df['Source'] == df['Target']
    #display(df.loc[df['Source-Copied'] == True]) # nur kopierte Zeilen anzeigen
    df = df.set_index(['Source-Copied'])

    try: # (KeyError: '[True] not found in axis') vermeiden, wenn es keine Zellen gibt, die aus der Quelle kopiert wurden
        df = df.drop([True]) # Boolean, kein String, keine Anführungszeichen hinzufügen
    except:
        pass
    
    df = df.reset_index()
    df = df.drop(['Source-Copied'], axis = 1)
    
    print("--- Quellkopierte Zeilen entfernt\t\t--> Zeilen:", df.shape[0])


    # Zu lange Zeilen verwerfen (Quelle oder Ziel)
    # Je nach Sprache die Werte "2" und "200" ändern.
    df["Too-Long"] = ((df['Source'].str.count(' ')+1) > (df['Target'].str.count(' ')+1) * 2) |  \
                     ((df['Target'].str.count(' ')+1) > (df['Source'].str.count(' ')+1) * 2) |  \
                     ((df['Source'].str.count(' ')+1) > 200) |  \
                     ((df['Target'].str.count(' ')+1) > 200)
                
    # display(df.loc[df['Too-Long'] == True]) # nur zu lange Zeilen anzeigen
    df = df.set_index(['Too-Long'])

    try: # (KeyError: '[True] not found in axis') vermeiden, wenn es keine Zellen gibt, die aus der Quelle kopiert wurden
        df = df.drop([True]) # Boolean, kein String, keine Anführungszeichen hinzufügen
    except:
        pass

    df = df.reset_index()
    df = df.drop(['Too-Long'], axis = 1)

    print("--- Zu lange Quell-/Zielzeilen entfernt\t--> Zeilen:", df.shape[0])


    # HTML entfernen und normalisieren
    # str() verwenden, um (TypeError: expected string or bytes-like object) zu vermeiden.
    # Hinweis: Das Entfernen von Tags sollte vor dem Entfernen von leeren Zellen erfolgen, da einige Zellen nur Tags enthalten und leer werden könnten.

    df = df.replace(r'<.*?>|&lt;.*?&gt;|&?(amp|nbsp|quot);|{}', ' ', regex=True)
    df = df.replace(r'  ', ' ', regex=True)  # doppelte Leerzeichen durch ein Leerzeichen ersetzen

    print("--- HTML entfernt\t\t\t--> Zeilen:", df.shape[0])


    # Kleinschreibung wenn lower=True
    if lower == True:
        df['Source'] = df['Source'].str.lower()
        df['Target'] = df['Target'].str.lower()

        print("--- Diese Zeilen werden kleingeschrieben\t--> Zeilen:", df.shape[0])
    else:
        print("--- Diese Zeilen verbleiben in Großbuchstaben\t--> Zeilen:", df.shape[0])


    # Ersetze leere Zellen durch NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)

    # NaN löschen (bereits vorhanden oder aus den vorangegangenen Schritten erzeugt)
    df = df.dropna()

    print("--- Zeilen mit leeren Zellen entfernt\t--> Zeilen:", df.shape[0])


    # Mischen der Daten
    df = df.sample(frac=1).reset_index(drop=True)
    print("--- Zeilen gemischt\t\t\t--> Zeilen:", df.shape[0])


    # Den Datenbereich in zwei Quell- und Zieldateien schreiben
    source_file = source_file+'-filtered.'+source_lang
    target_file = target_file+'-filtered.'+target_lang


    # Quelle und Ziel in zwei Textdateien speichern
    df_source = df["Source"]
    df_target = df["Target"]

    df_source.to_csv(source_file, header=False, index=False, quoting=csv.QUOTE_NONE, sep="\n")
    print("--- Source Saved:", source_file)
    df_target.to_csv(target_file, header=False, index=False, quoting=csv.QUOTE_NONE, sep="\n")
    print("--- Target Saved:", target_file)


# Korpora Details
source_file = sys.argv[1]    # Pfad zur Quelldatei
target_file = sys.argv[2]    # Pfad zur Zieldatei
source_lang = sys.argv[3]    # Quellsprache
target_lang = sys.argv[4]    # Zielsprache

# Die Funktion prepare() ausführen
# Daten werden in Großbuchstaben geschrieben; für Kleinbuchstaben auf True ändern
prepare(source_file, target_file, source_lang, target_lang, lower=False)