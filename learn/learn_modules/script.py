import text_analyzer 
from collections import Counter


words_counter = [Counter("abca"), Counter("aaa")]
summed_counters = text_analyzer.sum_counters(words_counter)
print(summed_counters)

my_istance = text_analyzer.n("test #ai is correct ! test #data #ai")
print(my_istance.word_counts.most_common(2))

print(my_istance.hashtag_counts)