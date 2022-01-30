with open("solutions.txt", "r") as f:
    all_words = f.read().splitlines()

    freq = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
    for word in all_words:
        for pos, letter in enumerate(word):
            if freq[pos].get(letter):
                freq[pos][letter] += 1
            else:
                freq[pos][letter] = 1

    for pos in freq:
        s = {k: v for k, v in sorted(
            freq[pos].items(), key=lambda x: x[1], reverse=True)}
        print(f"{pos}: {s}")
