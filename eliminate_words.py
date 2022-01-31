# Returns the number of times each letter appears in a word
# for all duplicate letters in a word
def get_duplicates(word):
    letter_counts = {}
    for letter in word:
        letter_count = word.count(letter)
        if letter_count > 1:
            letter_counts[letter] = [
                i for i, l in enumerate(word) if l == letter]

    return letter_counts

# Colours a word as it would be in the wordle game given
# a target word (i.e. the solution)


def colour_word(word, target):
    colours = {}
    claimed = [False, False, False, False, False]

    # First pass: mark all green or black letters
    for index, letter in enumerate(word):
        if letter == target[index]:
            colours[index] = "g"
            # Claim this index so we don't count it for yellow later
            claimed[index] = True
        elif letter not in target:
            colours[index] = "b"

    for i in range(len(word)):
        # Second pass: mark all remaining letters
        if i not in colours:
            for index, letter in enumerate(target):
                # Yellow mark requires index not to already be claimed
                if letter == word[i] and not claimed[index]:
                    claimed[index] = True
                    colours[i] = "y"
                    break

                # No yellow mark, so mark as black
                if index == len(target) - 1:
                    colours[i] = "b"

    output = ""
    for i in range(len(word)):
        output += colours[i]
    return output

# Returns a list of words in the possible words list that
# would be eliminated by the given guess


def find_eliminated_words(colours, word, possible_words):
    # Check for duplicate letters
    duplicates = get_duplicates(word)

    eliminated_words = set()
    for potential_word in possible_words:
        for index, letter in enumerate(word):
            # First check if letter appears multiple times
            if letter in duplicates:
                duplicate_indexes = duplicates[letter]
                c = ""
                for i in duplicate_indexes:
                    c += colours[i]

                # General duplicate check
                if 'b' in c:
                    if potential_word.count(letter) != word.count(letter) - c.count('b'):
                        eliminated_words.add(potential_word)
                        break
                else:
                    if potential_word.count(letter) < word.count(letter):
                        eliminated_words.add(potential_word)
                        break

                # Position-specific check
                if colours[index] == 'g':
                    if potential_word[index] != letter:
                        eliminated_words.add(potential_word)
                        break
                else:
                    if potential_word[index] == letter:
                        eliminated_words.add(potential_word)
                        break

            # Green letter: must match index or eliminates word
            elif colours[index] == 'g':
                if potential_word[index] != letter:
                    eliminated_words.add(potential_word)
                    break
            # Yellow letter:
            elif colours[index] == 'y':
                # No duplicates, so must contain exactly one
                if potential_word.count(letter) < 1:
                    eliminated_words.add(potential_word)
                    break
                elif potential_word[index] == letter:
                    eliminated_words.add(potential_word)
                    break
        # Black letter
            else:
                # No duplicates, so can't contain any
                if letter in potential_word:
                    eliminated_words.add(potential_word)
                    break

    return eliminated_words
