#!/bin/bash
BASE=$1
GENERATED=$2

mkdir -p $(GENERATED)/morph $(GENERATED)/transition $(GENERATED)/wm $(GENERATED)/word $(GENERATED)/wt $(GENERATED)/frequencies
echo "Extracting Word Frequencies..."
python3 get_word_freq.py $(BASE)/parallel.tsv $(GENERATED)/word/pada_freq.tsv $(GENERATED)/word/comp_freq.tsv $(GENERATED)/word/word_freq.tsv $(GENERATED)/word/word_cpd_freq.tsv
echo "Extracting Transition Frequencies..."
python3 get_trans_freq.py $(BASE)/parallel.tsv $(GENERATED)/transition/pada_trans_freq.tsv $(GENERATED)/transition/comp_trans_freq.tsv $(GENERATED)/transition/trans_freq.tsv $(GENERATED)/transition/trans_cpd_freq.tsv $(GENERATED)/transition/pada_trans_coded_freq.tsv $(GENERATED)/transition/comp_trans_coded_freq.tsv $(GENERATED)/transition/trans_coded_freq.tsv $(GENERATED)/transition/trans_cpd_coded_freq.tsv
echo "Extracting Word-Transition Frequencies..."
python3 word_transition.py $(BASE)/parallel.tsv $(GENERATED)/wt/word_bigram_transition_freq.tsv $(GENERATED)/wt/word_bigram_transition_coded_freq.tsv $(GENERATED)/wt/word_transition_freq.tsv $(GENERATED)/wt/word_transition_coded_freq.tsv
echo "Extracting Morph Frequencies..."
awk -F"\t" '{ print $8 "\t" $10 "\t" $14 "\t" $12 "\t" $15 }' $(BASE)/comp_entries.tsv > $(GENERATED)/wm/comp_word_morph.tsv
awk -F"\t" '{ print $8 "\t" $10 "\t" $14 "\t" $12 "\t" $15 }' $(BASE)/pada_entries.tsv > $(GENERATED)/wm/pada_word_morph.tsv
awk -F"\t" '{ print $8 "\t" $10 "\t" $14 "\t" $12 "\t" $15 }' $(BASE)/all_entries.tsv > $(GENERATED)/wm/word_morph.tsv
awk -F"\t" '{ print $10 "\t" $14 "\t" $12 "\t" $15 }' $(BASE)/comp_entries.tsv > $(GENERATED)/morph/comp_morph.tsv
awk -F"\t" '{ print $10 "\t" $14 "\t" $12 "\t" $15 }' $(BASE)/pada_entries.tsv > $(GENERATED)/morph/pada_morph.tsv
awk -F"\t" '{ print $10 "\t" $14 "\t" $12 "\t" $15 }' $(BASE)/all_entries.tsv > $(GENERATED)/morph/morph.tsv
python3 assign_freq.py $(GENERATED)/wm/comp_word_morph.tsv $(GENERATED)/wm/comp_word_morph_freq.tsv
python3 assign_freq.py $(GENERATED)/wm/pada_word_morph.tsv $(GENERATED)/wm/pada_word_morph_freq.tsv
python3 assign_freq.py $(GENERATED)/wm/word_morph.tsv $(GENERATED)/wm/word_morph_freq.tsv
python3 assign_freq.py $(GENERATED)/morph/comp_morph.tsv $(GENERATED)/morph/comp_morph_freq.tsv
python3 assign_freq.py $(GENERATED)/morph/pada_morph.tsv $(GENERATED)/morph/pada_morph_freq.tsv
python3 assign_freq.py $(GENERATED)/morph/morph.tsv $(GENERATED)/morph/morph_freq.tsv
echo "Finalising..."
cp $(GENERATED)/morph/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/transition/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/wm/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/word/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/wt/*_freq.tsv $(GENERATED)/frequencies/
echo "Done."
