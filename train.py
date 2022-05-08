# Quelle: [Ymoslem, o. D.a]
# Quelle: [Google Github, o. D.]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Training von SentencePiece-Modellen (N-Gram Modell) für die Quellsprache und Zielsprache
# Befehl: python3 train_unigram.py <train_source_file_tok> <train_target_file_tok>
# Beispielbefehl: python3 train.py Data/Europarl.de-en.en-filtered.en Data/Europarl.de-en.de-filtered.de


import sys
import sentencepiece as spm


path = ""    # Pfad bei Bedarf wechseln

train_source_file_tok = path + sys.argv[1]
train_target_file_tok = path + sys.argv[2]
    

# Trainiere das SentencePiece-Modell aus den Quell- und Zieldateien und erstelle `source/target.model` und `source/target.vocab`.
# `source/target.vocab` ist nur ein Verweis, der nicht für die Segmentierung verwendet wird.

# Wenn die Trainingsdaten zu klein sind und die maximale Anzahl der reservierten Segmente weniger als 4000 beträgt,
# dann --vocab size oder --hard_vocab_limit=false verringern, wodurch die Vokabelgröße automatisch verkleinert wird.

# Der Standardwert für --vocab_size beträgt 8.000 Sätze. 
# Es kann ein höherer Wert zwischen 30.000 und 50.000 gewählt werden. Bis zu 100.000 für einen sehr großen Korpus. 
# Es gilt zu beachten, dass kleinere Werte das Modell dazu ermutigen, mehr Worttrennungen vorzunehmen, was im Falle eines mehrsprachigen Modells besser sein könnte, wenn die Sprachen das gleiche Alphabet verwenden.

# Quellsprache - Teilwortmodell (Subword Model)

source_train_value = '--input='+train_source_file_tok+' --model_prefix=source --vocab_size=50000 --hard_vocab_limit=false --split_digits=true'
spm.SentencePieceTrainer.train(source_train_value)
print("Das Training eines SentencepPiece Modells für die Quellsprache wurde erfolgreich abgeschlossen!")


# Zielsprache - Teilwortmodell (Subword Modell)

target_train_value = '--input='+train_target_file_tok+' --model_prefix=target --vocab_size=50000 --hard_vocab_limit=false --split_digits=true'
spm.SentencePieceTrainer.train(target_train_value)
print("Das Training eines SentencepPiece Modells für die Zielsprache wurde erfolgreich abgeschlossen!")