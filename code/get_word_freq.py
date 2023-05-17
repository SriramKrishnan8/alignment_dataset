import sys
import os

from tqdm import tqdm

script, inp, pada, comp, wrd, wcd = sys.argv

inp_f = open(inp, 'r')
all_text = inp_f.read()
inp_f.close()
all_lines = list(filter(None, all_text.split("\n")))

pada_dict = {}
comp_dict = {}
word_dict = {}
word_cpd_dict = {}

#for i in range(len(all_lines)):
for i in tqdm(range(len(all_lines))):
    item = all_lines[i].split("\t")
    sent_id = item[0]
    sentence = item[1]
    segmented = item[2]
    
    segmented_lst = segmented.split(" ")
    for word in segmented_lst:
        if "-" in word:
            comps = word.split("-")
            i = 1
            for component in comps:
                if component in comp_dict.keys():
                    comp_dict[component] += 1
                else:
                    comp_dict[component] = 1
                
                if component in word_dict.keys():
                    word_dict[component] += 1
                else:
                    word_dict[component] = 1
                
                is_cpd = "2" if (i == len(comps)) else "1"
                word_cpd = ("\t".join((component, is_cpd)))
                if word_cpd in word_cpd_dict.keys():
                    word_cpd_dict[word_cpd] += 1
                else:
                    word_cpd_dict[word_cpd] = 1
                
                i += 1
        else:
            if word in pada_dict.keys():
                pada_dict[word] += 1
            else:
                pada_dict[word] = 1
            
            if word in word_dict.keys():
                word_dict[word] += 1
            else:
                word_dict[word] = 1
            
            word_cpd = "\t".join((word, "2"))
            if word_cpd in word_cpd_dict.keys():
                word_cpd_dict[word_cpd] += 1
            else:
                word_cpd_dict[word_cpd] = 1
        
    
sorted_padas = sorted(pada_dict.items(), key=lambda x:x[1], reverse=True)
sorted_comps = sorted(comp_dict.items(), key=lambda x:x[1], reverse=True)
sorted_words = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
sorted_word_cpds = sorted(word_cpd_dict.items(), key=lambda x:x[1], reverse=True)

padas_lst = [item[0] + "\t" + str(item[1]) for item in sorted_padas]
comps_lst = [item[0] + "\t" + str(item[1]) for item in sorted_comps]
words_lst = [item[0] + "\t" + str(item[1]) for item in sorted_words]
word_cpds_lst = [item[0] + "\t" + str(item[1]) for item in sorted_word_cpds]

pada_file = open(pada, 'w')
pada_file.write("\n".join(padas_lst))
pada_file.close()

comp_file = open(comp, 'w')
comp_file.write("\n".join(comps_lst))
comp_file.close()

word_file = open(wrd, 'w')
word_file.write("\n".join(words_lst))
word_file.close()

word_cpd_file = open(wcd, 'w')
word_cpd_file.write("\n".join(word_cpds_lst))
word_cpd_file.close()

