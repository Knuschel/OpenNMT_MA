# Quelle: [Ymoslem, o. D.b]

# Sentence METEOR

# METEOR arbeitet auf Satzebene und nicht auf Korpusebene.
# Befehl: python3 sentence-meteor.py test_datei_name.txt mt_datei_name.txt
# Beispielbefehl: python3 sentence-meteor.py Data/Europarl.de-en.de-filtered.de.subword.test.desubword Output/pred.txt.desubword

import sys
import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet
from nltk.translate.meteor_score import meteor_score


target_test = sys.argv[1]	# Testdatei-Argument
target_pred = sys.argv[2]	# MÜ-Datei-Argument


# Öffne die Datei mit der menschlichen Übersetzung des Testdatensatzes
with open(target_test) as test:
    refs = test.readlines()

#print("Referenz 1. Satz:", refs[0])

# Öffne die Datei mit der maschinellen Übersetzung
with open(target_pred) as pred:
    preds = pred.readlines()

meteor_file = "meteor-" + target_pred + ".txt"

# Berechne METEOR für jeden Satz und speichere das Ergebnis in einer Datei.
with open(meteor_file, "w+") as output:
    for line in zip(refs, preds):
        test = line[0]
        pred = line[1]
        #print(test, pred)

        meteor = round(meteor_score([test], pred), 2) # Liste der Referenzen
        #print(meteor, "\n")
        output.write(str(meteor) + "\n")

print("Beendet! Bitte die METEOR Datei '" + meteor_file + "' im gleichen Verzeichnis prüfen!")