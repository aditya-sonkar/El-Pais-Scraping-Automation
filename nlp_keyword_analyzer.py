import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

stop_words = set(stopwords.words('english'))

def analyze_titles(titles):

    words=[]

    for t in titles:
        tokens = nltk.word_tokenize(t.lower())

        for w in tokens:
            if w.isalpha() and w not in stop_words:
                words.append(w)

    freq = Counter(words)

    print(f"\n-> Analyzing {len(titles)} translated headers...")
    print(f"-> Tokens extracted: {len(words)} meaningful words after filtering")
    for w in words:
        print(f"   -> {w}")
    print(f"-> Running frequency analysis...")

    print("\n-> Repeated Words (More than twice):")
    found_any = False
    for word, count in freq.most_common():
        if count > 2:
            print(f"-> {word} : {count}")
            found_any = True
            
    if not found_any:
        print("-> No words repeated more than 2 occurrences.")

    return {word: count for word, count in freq.most_common() if count > 2}