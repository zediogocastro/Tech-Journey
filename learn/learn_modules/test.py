from text_analyzer import sum_counters
from collections import Counter

words_counter = [Counter("abca"), Counter("aaa")]
summed_counters = sum_counters(words_counter)
print(summed_counters)
