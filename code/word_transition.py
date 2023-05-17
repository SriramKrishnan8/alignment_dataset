import sys
import re

from tqdm import tqdm

script, pd, word_wb, word_wb_coded, word_wt, word_wt_coded = sys.argv


def update_dict(item, dict_):
    if item in dict_.keys():
        dict_[item] += 1
    else:
        dict_[item] = 1
    
    return dict_
    

def process_result(t_list, t_f):
    t_dict = {}
    for item in t_list:
        item_str = "\t".join(item)
        t_dict = update_dict(item_str, t_dict)
    
    sorted_trans = sorted(t_dict.items(), key=lambda x:x[1], reverse=True)
    trans_lst = [item[0] + "\t" + str(item[1]) for item in sorted_trans]
    
    t_file = open(t_f, 'w')
    t_file.write("\n".join(trans_lst))
    t_file.close()


alphabet_dict = {
    "a":1,
    "A":2,
    "i":3,
    "I":4,
    "u":5,
    "U":6,
    "q":7,
    "Q":8,
    "L":9,
    "e":10,
    "E":11,
    "o":12,
    "O":13,
    "M":14,
    "z":15,
    "H":16,
    "k":17,
    "K":18, 
    "g":19,
    "G":20,
    "f":21,
    "c":22,
    "C":23,
    "j":24,
    "J":25,
    "F":26,
    "t":27,
    "T":28,
    "d":29,
    "D":30,
    "N":31,
    "w":32,
    "W":33,
    "x":34,
    "X":35,
    "n":36,
    "p":37,
    "P":38,
    "b":39,
    "B":40,
    "m":41,
    "y":42,
    "r":43,
    "l":44,
    "v":45,
    "S":46,
    "R":47,
    "s":48,
    "h":49,
    "Z":-1,
}


def get_code_for_letters(element):
    element_list = list(element)
    code = "["
    for item in element_list:
        code = code + str(alphabet_dict[item])
        if item != element_list[-1]:
            code = code + ";"
    code = code + "]"
    return code


def get_word_transitions(bigram):
    word_1 = bigram[0]
    word_2 = bigram[1]
    is_compound = bigram[2]
    
    t1 = word_1[-2:] if word_1.endswith("H") else word_1[-1]
    t2 = word_2[0]
    
#    print(word_1, word_2)
    
    coded_t1 = get_code_for_letters(t1)
    coded_t2 = get_code_for_letters(t2)
    
    word_bigram = (word_1, word_2, t1, t2, is_compound)
    word_bigram_coded = (word_1, word_2, coded_t1, coded_t2, is_compound)
    word_transition = (word_1, t1, t2, is_compound)
    word_transition_coded = (word_1, coded_t1, coded_t2, is_compound)
    
    return word_bigram, word_bigram_coded, word_transition, word_transition_coded
    

def get_word_bigrams(words_list):
    word_bigrams = []
    word_bigrams_coded = []
    word_transitions = []
    word_transitions_coded = []
    
    cur = ""
    for i in range(len(words_list)):
        word = words_list[i]
        if "-" in word:
            comps = word.split("-")
            if not (cur == ""):
#                word_bigrams += [(cur, comps[0], "2")]
                wb, wb_coded, wt, wt_coded = get_word_transitions((cur, comps[0], "2"))
                word_bigrams += [ wb ]
                word_bigrams_coded += [ wb_coded ]
                word_transitions += [ wt ]
                word_transitions_coded += [ wt_coded ]
#            comp_bigram = [(x, comps[j + 1], "1") 
#                           for j, x in enumerate(comps) if j < (len(comps) - 1)]
            comp_bigram = [get_word_transitions((x, comps[j + 1], "1")) 
                           for j, x in enumerate(comps) if j < (len(comps) - 1)]
            word_bigrams += [x[0] for x in comp_bigram]
            word_bigrams_coded += [x[1] for x in comp_bigram]
            word_transitions += [x[2] for x in comp_bigram]
            word_transitions_coded += [x[3] for x in comp_bigram]
            cur = comps[-1]
        else:
            if i < len(words_list):
                if not (cur == ""):
#                    word_bigrams += [(cur, word, "2")]
                    wb, wb_coded, wt, wt_coded = get_word_transitions((cur, word, "2"))
                    word_bigrams += [ wb ]
                    word_bigrams_coded += [ wb_coded ]
                    word_transitions += [ wt ]
                    word_transitions_coded += [ wt_coded ]
                    cur = word
                else:
                    cur = word
    
    return word_bigrams, word_bigrams_coded, word_transitions, word_transitions_coded


pd_file = open(pd, 'r')
all_text = pd_file.read()
pd_file.close()

lines = list(filter(None, all_text.split("\n")))

bigrams = []
bigrams_coded = []
transitions = []
transitions_coded = []
#for i in range(len(lines)):
for i in tqdm(range(len(lines))):
    line = lines[i]
    split_line = line.split("\t")
    id_ = split_line[0]
    unsegmented = split_line[1]
    segmented = split_line[2].strip()
    
    result = get_word_bigrams(segmented.split(" "))
    
    bigrams += result[0]
    bigrams_coded += result[1]
    transitions += result[2]
    transitions_coded += result[3]
    

process_result(bigrams, word_wb)
process_result(bigrams_coded, word_wb_coded)
process_result(transitions, word_wt)
process_result(transitions_coded, word_wt_coded)

#write_bigrams = ["\t".join(item) for item in bigrams]
#write_bigrams_coded = ["\t".join(item) for item in bigrams_coded]
#write_transitions = ["\t".join(item) for item in transitions]
#write_transitions_coded = ["\t".join(item) for item in transitions_coded]
#
#bigrams_dict = {}
#for item in write_bigrams:
#    bigrams_dict = update_dict(item, bigrams_dict)
#
#bigrams_coded_dict = {}
#for item in write_bigrams_coded:
#    bigrams_coded_dict = update_dict(item, bigrams_coded_dict)
#
#process_t_dict(bigrams_dict, word_wt)
#process_t_dict(bigrams_coded_dict, word_wt_coded)
#
#word_file = open(word_wt, 'w')
#word_file.write("\n".join(write_bigrams))
#word_file.close()
#
#word_file = open(word_wt_coded, 'w')
#word_file.write("\n".join(write_bigrams_coded))
#word_file.close()
