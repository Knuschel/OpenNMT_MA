# Quelle: [Ymoslem, o. D.a]
# Quelle: [Google Github, o. D.]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Tokenisierung der Quell- und Zieldateien
# Befehl: python3 subword.py <sp_quell_modell_pfad> <sp_ziel_modell_pfad> <quell_datei_pfad> <ziel_datei_pfad>
# Beispielbefehl: python3 subword.py source.model target.model Data/Europarl.de-en.en-filtered.en Data/Europarl.de-en.de-filtered.de


import sys
import sentencepiece as spm


source_model = sys.argv[1]
target_model = sys.argv[2]
source_raw = sys.argv[3]
target_raw = sys.argv[4]
source_subworded = source_raw + ".subword"
target_subworded = target_raw + ".subword"

print("Source Model:", source_model)
print("Target Model:", target_model)
print("Source Dataset:", source_raw)
print("Target Dataset:", target_raw)


sp = spm.SentencePieceProcessor()


# Tokenisierung der Quellsprache/Quelldatei

sp.load(source_model)

with open(source_raw) as source, open(source_subworded, "w+") as source_subword:
    for line in source:
        line = line.strip()
        line = sp.encode_as_pieces(line)
        # line = ['<s>'] + line + ['</s>']    # Start- und End-Token hinzufügen; nicht erforderlich für OpenNMT
        line = " ".join([token for token in line])
        source_subword.write(line + "\n")

print("Tokenisierung der Quelldatei beendet! Ausgabe:", source_subworded)


# Tokenisierung Zielsprache/Zieldatei

sp.load(target_model)

with open(target_raw) as target, open(target_subworded, "w+") as target_subword:
    for line in target:
        line = line.strip()
        line = sp.encode_as_pieces(line)
        # line = ['<s>'] + line + ['</s>']    # Start- und End-Token hinzufügen; nicht erforderlich für OpenNMT
        line = " ".join([token for token in line])
        target_subword.write(line + "\n")

print("Tokenisierung der Zieldatei beendet! Ausgabe:", target_subworded)