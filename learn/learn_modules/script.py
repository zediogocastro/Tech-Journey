import text_analyzer as ta
from collections import Counter

words_counter = [Counter("abca"), Counter("aaa")]
summed_counters = ta.sum_counters(words_counter)
print(summed_counters)
