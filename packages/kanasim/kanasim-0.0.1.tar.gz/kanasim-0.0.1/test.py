from kanasim import create_kana_distance_calculator

# The vowel_ratio parameter determines the weight of vowels when calculating the distance between kana.
# By default, it is set to 0.5, meaning vowels and consonants are weighted equally (1:1).
calculator = create_kana_distance_calculator(vowel_ratio=0.2)

word = "カナダ"
wordlist = ["サラタ", "ケナダ"]

topn = calculator.get_topn(word, wordlist, n=10)
print("vowel_ratio=0.0")
for i, (w, d) in enumerate(topn, 1):
    print(f"{i}: {w} ({d})")
