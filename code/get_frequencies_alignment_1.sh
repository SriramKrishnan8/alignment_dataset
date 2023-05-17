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
mkdir -p $(BASE)/working
awk -F"\t" '{ print $1}' $(BASE)/wclm_final > $(BASE)/working/word_iast.tsv
awk -F"\t" '{ print $3}' $(BASE)/wclm_final > $(BASE)/working/stem_iast.tsv
awk -F"\t" '{ print $5}' $(BASE)/wclm_final > $(BASE)/working/i_morph.tsv
awk -F"\t" '{ print $7}' $(BASE)/wclm_final > $(BASE)/working/base_iast.tsv
awk -F"\t" '{ print $9}' $(BASE)/wclm_final > $(BASE)/working/d_morph.tsv
transliterate -d iast -e wx -i $(BASE)/working/word_iast.tsv -o $(BASE)/working/word.tsv
transliterate -d iast -e wx -i $(BASE)/working/stem_iast.tsv -o $(BASE)/working/stem.tsv
transliterate -d iast -e wx -i $(BASE)/working/base_iast.tsv -o $(BASE)/working/base.tsv
paste $(BASE)/working/word.tsv $(BASE)/working/stem.tsv $(BASE)/working/i_morph.tsv $(BASE)/working/base.tsv $(BASE)/working/d_morph.tsv > $(BASE)/wclm_all_entries.tsv
cp $(BASE)/wclm_all_entries.tsv $(GENERATED)/wm/word_morph.tsv
awk -F"\t" '{ print $2 "\t" $3 "\t" $4 "\t" $5}' $(GENERATED)/wm/word_morph.tsv > $(GENERATED)/morph/morph.tsv
rm -rf $(BASE)/working/
python3 get_morph.py $(GENERATED)/wm/word_morph.tsv $(GENERATED)/wm/pada_word_morph.tsv $(GENERATED)/wm/comp_word_morph.tsv $(GENERATED)/morph/pada_morph.tsv $(GENERATED)/morph/comp_morph.tsv $(GENERATED)/wm/pada_word_morph_freq.tsv $(GENERATED)/wm/comp_word_morph_freq.tsv $(GENERATED)/morph/pada_morph_freq.tsv $(GENERATED)/morph/comp_morph_freq.tsv 
python3 assign_freq.py $(GENERATED)/wm/word_morph.tsv $(GENERATED)/wm/word_morph_freq.tsv
python3 assign_freq.py $(GENERATED)/morph/morph.tsv $(GENERATED)/morph/morph_freq.tsv
echo "Finalising..."
cp $(GENERATED)/morph/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/transition/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/wm/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/word/*_freq.tsv $(GENERATED)/frequencies/
cp $(GENERATED)/wt/*_freq.tsv $(GENERATED)/frequencies/
echo "Done."
