#!/bin/bash

# Evaluate combinations of libraries and stemming
python3 -m klexikon.baselines.baselines lead-3 GeRouge val > lead-3_GeRouge_val_no_stem.txt
python3 -m klexikon.baselines.baselines lead-3 Rouge val > lead-3_Rouge_val_no_stem.txt
python3 -m klexikon.baselines.baselines lead-3 GeRouge val --use-rouge-stemming > lead-3_GeRouge_val_stem.txt
python3 -m klexikon.baselines.baselines lead-3 Rouge val --use-rouge-stemming > lead-3_Rouge_val_stem.txt
python3 -m klexikon.baselines.baselines lead-3 GeRouge-Cistem val --use-rouge-stemming > lead-3_GeRouge-Cistem_val_stem.txt
python3 -m klexikon.baselines.baselines lead-3 Rouge-Cistem val --use-rouge-stemming > lead-3_Rouge-Cistem_val_stem.txt

# Same for test set
python3 -m klexikon.baselines.baselines lead-3 GeRouge val > lead-3_GeRouge_test_no_stem.txt
python3 -m klexikon.baselines.baselines lead-3 Rouge val > lead-3_Rouge_test_no_stem.txt
python3 -m klexikon.baselines.baselines lead-3 GeRouge val --use-rouge-stemming > lead-3_GeRouge_test_stem.txt
python3 -m klexikon.baselines.baselines lead-3 Rouge val --use-rouge-stemming > lead-3_Rouge_test_stem.txt
python3 -m klexikon.baselines.baselines lead-3 GeRouge-Cistem val --use-rouge-stemming > lead-3_GeRouge-Cistem_test_stem.txt
python3 -m klexikon.baselines.baselines lead-3 Rouge-Cistem val --use-rouge-stemming > lead-3_Rouge-Cistem_test_stem.txt

