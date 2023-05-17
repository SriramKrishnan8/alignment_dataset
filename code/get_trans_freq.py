import sys
import os

from tqdm import tqdm

script, inp, pada_t, comp_t, trans, trans_cpd, pada_t_c, comp_t_c, trans_c, trans_cpd_c = sys.argv


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
    
    transition = "\t".join((t1, t2))
    transition_cpd = "\t".join((t1, t2, is_compound))
    transition_coded = "\t".join((coded_t1, coded_t2))
    transition_coded_cpd = "\t".join((coded_t1, coded_t2, is_compound))
    
    return transition, transition_coded, transition_cpd, transition_coded_cpd
    

def update_dict(item, dict_):
    if item in dict_.keys():
        dict_[item] += 1
    else:
        dict_[item] = 1
    
    return dict_
    

def process_t_dict(t_dict, t_f):
    sorted_trans = sorted(t_dict.items(), key=lambda x:x[1], reverse=True)
    trans_lst = [item[0] + "\t" + str(item[1]) for item in sorted_trans]
    
    t_file = open(t_f, 'w')
    t_file.write("\n".join(trans_lst))
    t_file.close()
    

inp_f = open(inp, 'r')
all_text = inp_f.read()
inp_f.close()
all_lines = list(filter(None, all_text.split("\n")))

pada_t_dict = {}
comp_t_dict = {}
trans_dict = {}
trans_cpd_dict = {}

pada_t_dict_coded = {}
comp_t_dict_coded = {}
trans_dict_coded = {}
trans_cpd_dict_coded = {}

#for i in range(len(all_lines)):
for i in tqdm(range(len(all_lines))):
    item = all_lines[i].split("\t")
    sent_id = item[0]
    sentence = item[1]
    segmented = item[2]
    
    segmented_lst = segmented.split(" ")
    cur = ""
    for word in segmented_lst:
        if "-" in word:
            comp_trans = word.split("-")
            i = 1
            for component in comp_trans:
                if cur == "":
                    cur = component
                    i += 1
                    continue
                
                if i == 1:
                    t, t_c, t_cpd, t_cpd_c = get_word_transitions((cur, component, "2"))
                    pada_t_dict = update_dict(t, pada_t_dict)
                    pada_t_dict_coded = update_dict(t_c, pada_t_dict_coded)
                    trans_dict = update_dict(t, trans_dict)
                    trans_dict_coded = update_dict(t_c, trans_dict_coded)
                    trans_cpd_dict = update_dict(t_cpd, trans_cpd_dict)
                    trans_cpd_dict_coded = update_dict(t_cpd_c, trans_cpd_dict_coded)
                else:
                    t, t_c, t_cpd, t_cpd_c = get_word_transitions((cur, component, "1"))
                    comp_t_dict = update_dict(t, comp_t_dict)
                    comp_t_dict_coded = update_dict(t_c, comp_t_dict_coded)
                    trans_dict = update_dict(t, trans_dict)
                    trans_dict_coded = update_dict(t_c, trans_dict_coded)
                    trans_cpd_dict = update_dict(t_cpd, trans_cpd_dict)
                    trans_cpd_dict_coded = update_dict(t_cpd_c, trans_cpd_dict_coded)
                
                cur = component
                
#                is_cpd = "2" if (i == len(comp_trans)) else "1"
#                trans_cpd = ("\t".join((component, is_cpd)))
#                if trans_cpd in trans_cpd_dict.keys():
#                    trans_cpd_dict[trans_cpd] += 1
#                else:
#                    trans_cpd_dict[trans_cpd] = 1
                
                i += 1
        else:
            if cur == "":
                cur = word
                continue
            
            t, t_c, t_cpd, t_cpd_c = get_word_transitions((cur, word, "2"))
            
            pada_t_dict = update_dict(t, pada_t_dict)
            pada_t_dict_coded = update_dict(t_c, pada_t_dict_coded)
            trans_dict = update_dict(t, trans_dict)
            trans_dict_coded = update_dict(t_c, trans_dict_coded)
            trans_cpd_dict = update_dict(t_cpd, trans_cpd_dict)
            trans_cpd_dict_coded = update_dict(t_cpd_c, trans_cpd_dict_coded)
            
            cur = word
        

process_t_dict(pada_t_dict, pada_t)
process_t_dict(comp_t_dict, comp_t)
process_t_dict(trans_dict, trans)
process_t_dict(trans_cpd_dict, trans_cpd)
process_t_dict(pada_t_dict_coded, pada_t_c)
process_t_dict(comp_t_dict_coded, comp_t_c)
process_t_dict(trans_dict_coded, trans_c)
process_t_dict(trans_cpd_dict_coded, trans_cpd_c)



#sorted_pada_trans = sorted(pada_t_dict.items(), key=lambda x:x[1], reverse=True)
#sorted_comp_trans = sorted(comp_t_dict.items(), key=lambda x:x[1], reverse=True)
#sorted_trans = sorted(trans_dict.items(), key=lambda x:x[1], reverse=True)
#sorted_trans_cpds = sorted(trans_cpd_dict.items(), key=lambda x:x[1], reverse=True)

#pada_trans_lst = [item[0] + "\t" + str(item[1]) for item in sorted_pada_trans]
#comp_trans_lst = [item[0] + "\t" + str(item[1]) for item in sorted_comp_trans]
#trans_lst = [item[0] + "\t" + str(item[1]) for item in sorted_trans]
#trans_cpds_lst = [item[0] + "\t" + str(item[1]) for item in sorted_trans_cpds]

#pada_t_file = open(pada_t, 'w')
#pada_t_file.write("\n".join(pada_trans_lst))
#pada_t_file.close()

#comp_t_file = open(comp_t, 'w')
#comp_t_file.write("\n".join(comp_trans_lst))
#comp_t_file.close()

#trans_file = open(trans, 'w')
#trans_file.write("\n".join(trans_lst))
#trans_file.close()

#trans_cpd_file = open(trans_c, 'w')
#trans_cpd_file.write("\n".join(trans_cpds_lst))
#trans_cpd_file.close()

