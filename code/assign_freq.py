from sys import argv
import itertools
import collections

script, old_data, new_data = argv

old_data_file = open(old_data, 'r')
all_text = old_data_file.read()
old_data_file.close()

lines = all_text.split('\n')

#ctr = collections.Counter(lines)

ctr_dict = {}

for word in lines:
    if word in ctr_dict.keys():
        ctr_dict[word] += 1
    else:
        ctr_dict[word] = 1

freq_file = open(new_data, 'w')

sorted_words = sorted(ctr_dict.items(), key=lambda x:x[1], reverse=True)
words_lst = [item[0] + "\t" + str(item[1]) for item in sorted_words]
freq_file.write("\n".join(words_lst))
        
