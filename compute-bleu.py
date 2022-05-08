# Quelle: [Ymoslem, o. D.b]
# Quelle: [Mjpost, o. D.]

# Corpus BLEU - Dateien müssen untokenized/unsubworded sein.
# Befehl: python3 compute-bleu.py test_datei_name.txt mt_datei_name.txt
# Beispielbefehl: python3 compute-bleu.py Data/Europarl.de-en.de-filtered.de.subword.test.desubword Output/pred.txt.desubword


import sys
import sacrebleu

target_test = sys.argv[1]  # Testdatei-Argument
target_pred = sys.argv[2]  # MÜ-Datei-Argument

# Den Testdatensatz der Referenzübersetzung öffnen und die Referenzen enttoken
refs = []

with open(target_test) as test:
    for line in test: 
        line = line.strip()
        refs.append(line)

print("Beispiel, Referenz 1. Satz:", refs[0]) # Beispiel Referenzsatz

refs = [refs]  # Es handelt sich um eine Liste von Listen und wird so von sacreBLEU gefordert.


# Die Datei mit der maschinellen Übersetzung öffnen und die Vorhersagen enttoken
preds = []

with open(target_pred) as pred:  
    for line in pred: 
        line = line.strip()
        preds.append(line)

print("Beispiel, MÜ 1. Satz:", preds[0]) # Beispiel MÜ Satz


# Berechnung und Ausgabe des BLEU-Scores
bleu = sacrebleu.corpus_bleu(preds, refs)
print("BLEU: ", bleu.score)