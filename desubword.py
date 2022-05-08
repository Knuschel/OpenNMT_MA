# Quelle: [Ymoslem, o. D.a]
# Quelle: [Google Github, o. D.]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Detokenisierung der Übersetzung
# Befehl: python3 desubword.py <Zielmodell-Datei> <Zielprognose-Datei>
# Beispielbefehl: python3 desubword.py target.model Output/pred.txt


import sys
import sentencepiece as spm


target_model = sys.argv[1]
target_pred = sys.argv[2]
target_decodeded = target_pred + ".desubword"


sp = spm.SentencePieceProcessor()
sp.load(target_model)


with open(target_pred) as pred, open(target_decodeded, "w+") as pred_decoded:
    for line in pred:
        line = line.strip().split(" ")
        line = sp.decode_pieces(line)
        pred_decoded.write(line + "\n")
        
print("Detokenisierung beendet! Ausgabe:", target_decodeded)