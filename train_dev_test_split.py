# Quelle: [Ymoslem, o. D.a]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Aufteilung des parallelen Datensatzes in Trainings-, Validierungs- und Testdatensätze für die maschinelle Übersetzung
# Befehl: python3 train_dev_test_split.py <Anzahl Validierungssegmente> <Anzahl Testsegmente> <Quelldatei_pfad> <Zieldateipfad>
# Beispielbefehl: python3 train_dev_test_split.py 10000 10000 Data/Europarl.de-en.en-filtered.en.subword Data/Europarl.de-en.de-filtered.de.subword


import pandas as pd
import numpy as np
import re
import csv
import sys

# display(df) funktioniert nur, wenn Sie IPython/Jupyter Notebooks verwenden oder aktivieren:
# from IPython.display import display


segment_no_dev = sys.argv[1]    # Anzahl der Segmente im Dev-Set (Validierungsdatensatz)
segment_no_test = sys.argv[2]    # Anzahl der Segmente im Test-Set
source_file = sys.argv[3]   # Pfad zur Quelldatei
target_file = sys.argv[4]   # Pfad zur Zieldatei


def extract_dev(segment_no_dev, segment_no_test, source_file, target_file):

    df_source = pd.read_csv(source_file, names=['Source'], sep="\n", quoting=csv.QUOTE_NONE, error_bad_lines=False)
    df_target = pd.read_csv(target_file, names=['Target'], sep="\n", quoting=csv.QUOTE_NONE, error_bad_lines=False)
    df = pd.concat([df_source, df_target], axis=1)  # Die beiden Datenbereiche entlang der Spalten verbinden
    print("Datenstruktur:", df.shape)


    # Zeilen mit leeren Zellen löschen (Quelle oder Ziel)
    df = df.dropna()

    print("--- Leere Zellen entfernt", "--> Zeilen:", df.shape[0])


    # Dev-Set aus dem Hauptdatensatz extrahieren
    df_dev = df.sample(n = int(segment_no_dev))
    df_train = df.drop(df_dev.index)

    # Test-Set aus dem Hauptdatensatz extrahieren
    df_test = df_train.sample(n = int(segment_no_test))
    df_train = df_train.drop(df_test.index)

    # Den Datenbereich in zwei Quell- und Zieldateien schreiben
    source_file_train = source_file+'.train'
    target_file_train = target_file+'.train'

    source_file_dev = source_file+'.dev'
    target_file_dev = target_file+'.dev'

    source_file_test = source_file+'.test'
    target_file_test = target_file+'.test'

    df_dic_train = df_train.to_dict(orient='list')


    with open(source_file_train, "w") as sf:
        sf.write("\n".join(line for line in df_dic_train['Source']))
        sf.write("\n") # Ende der Datei, Zeilenumbruch

    with open(target_file_train, "w") as tf:
        tf.write("\n".join(line for line in df_dic_train['Target']))
        tf.write("\n") # Ende der Datei, Zeilenumbruch


    df_dic_dev = df_dev.to_dict(orient='list')

    with open(source_file_dev, "w") as sf:
        sf.write("\n".join(line for line in df_dic_dev['Source']))
        sf.write("\n") # Ende der Datei, Zeilenumbruch
        
    with open(target_file_dev, "w") as tf:
        tf.write("\n".join(line for line in df_dic_dev['Target']))
        tf.write("\n") # Ende der Datei, Zeilenumbruch
        

    df_dic_test = df_test.to_dict(orient='list')

    with open(source_file_test, "w") as sf:
        sf.write("\n".join(line for line in df_dic_test['Source']))
        sf.write("\n") # Ende der Datei, Zeilenumbruch
        
    with open(target_file_test, "w") as tf:
        tf.write("\n".join(line for line in df_dic_test['Target']))
        tf.write("\n") # Ende der Datei, Zeilenumbruch
        

    print("--- Dateien geschrieben")
    print("Beendet!")
    print("Ausgabedateien", *[source_file_train, target_file_train, source_file_dev, target_file_dev, source_file_test, target_file_test], sep="\n")



extract_dev(segment_no_dev, segment_no_test, source_file, target_file)