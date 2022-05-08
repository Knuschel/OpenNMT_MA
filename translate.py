# Quelle: [OpenNMT, o. D.b]

# Beispielbefehl: python translate.py -model NMT_Modelle/model_baseline_step_40000.pt -src Data/Europarl.de-en.en-filtered.en.subword.test -output Output/pred.txt -replace_unk -verbose

#!/usr/bin/env python
from onmt.bin.translate import main


if __name__ == "__main__":
    main()