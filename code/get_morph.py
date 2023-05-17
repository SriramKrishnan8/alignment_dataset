from sys import argv
import itertools
import collections

from tqdm import tqdm

script, old_data, pada_i, comp_i, pada_m, comp_m, pada_f, comp_f, pada_m_f, comp_m_f = argv


def write_to_file(list_, file_name):
    file_ = open(file_name, 'w')
    file_.write("\n".join(list_))
    file_.close()


def generate_freq(list_, freq_file_name):
    ctr_dict = {}
    
    for word in list_:
        if word in ctr_dict.keys():
            ctr_dict[word] += 1
        else:
            ctr_dict[word] = 1
    
    sorted_words = sorted(ctr_dict.items(), key=lambda x:x[1], reverse=True)
    words_lst = [item[0] + "\t" + str(item[1]) for item in sorted_words]
    
    write_to_file(words_lst, freq_file_name)
        

old_data_file = open(old_data, 'r')
all_text = old_data_file.read()
old_data_file.close()

lines = list(filter(None, all_text.split('\n')))

pada = []
pada_morph = []
comp = []
comp_morph = []

iic = False

#for i in tqdm(range(len(lines))):
for i in range(len(lines)):
    line = lines[i]
    
    split_line = line.split("\t")
    word = split_line[0]
    stem = split_line[1]
    inf = split_line[2]
    base = split_line[3]
    der = split_line[4]
    
    if iic or inf == "iic.":
        comp.append(line)
        comp_morph.append("\t".join((stem, inf, base, der)))
    else:
        pada.append(line)
        pada_morph.append("\t".join((stem, inf, base, der)))
    
    iic = True if inf == "iic." else False


write_to_file(pada, pada_i)
write_to_file(comp, comp_i)
write_to_file(pada_morph, pada_m)
write_to_file(comp_morph, comp_m)

generate_freq(pada, pada_f)
generate_freq(comp, comp_f)
generate_freq(pada_morph, pada_m_f)
generate_freq(comp_morph, comp_m_f)
