# Quelle: [Ymoslem, o. D.b]
# Quelle: [Jitsi, o. D.]

# Korpusbewertung mit Word Error Rate (WER)

# WER Score für den gesamten Textkorpus
# Befehl: python3 corpus-wer.py test_file_name.txt mt_file_name.txt
# Beispielbefehl: python3 corpus-wer.py Data/Europarl.de-en.de-filtered.de.subword.test.desubword Output/pred.txt.desubword

import sys
from jiwer import wer


target_test = sys.argv[1]	#  Testdatei-Argument
target_pred = sys.argv[2]	#  MÜ-Datei-Argument


# Öffnen der Datei mit der Referenzübersetzung des Testdatensatzes
with open(target_test) as test:
    refs = test.readlines()

#print("Referenz des 1. Satzes:", refs[0])

# Die Datei mit der maschinellen Übersetzung öffnen
with open(target_pred) as pred:
    preds = pred.readlines()

wer_file = "wer-" + target_pred + ".txt"

# Den WER Score über den gesamten Korpus berechnen
wer_score = wer(refs, preds, standardize=True)    # "standardize" erweitert Abkürzungen
print("WER Score:", wer_score)