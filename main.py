# FIRST GUESS:
#
# GOAL: eliminate as many words as possible consistently

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


def get_duplicates(word):
    letter_counts = {}
    for letter in word:
        letter_count = word.count(letter)
        if letter_count > 1:
            letter_counts[letter] = [
                i for i, l in enumerate(word) if l == letter]

    return letter_counts


def find_eliminated_words(colours, word, all_words):
    # Check for duplicate letters
    duplicates = get_duplicates(word)

    eliminated_words = set()
    for potential_word in all_words:
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


def gen_best_words(guesses, solutions):
    NUM_WORDS = len(solutions)
    output = {}
    for word in guesses:
        guess_values = {}
        for target_word in solutions:
            colours = colour_word(word, target_word)
            if guess_values.get(colours):
                guess_values[colours]["freq"] += 1
            else:
                guess_values[colours] = {
                    "freq": 1,
                    "score": len(find_eliminated_words(colours, word, solutions))
                }

        avg_eliminated = 0
        for key in guess_values:
            avg_eliminated += (guess_values[key]["freq"] /
                               NUM_WORDS) * guess_values[key]["score"]

        output[word] = avg_eliminated

    print(output)

    with open("best_words.txt", "w") as f:
        for key in {k: v for k, v in sorted(output.items(), key=lambda x: x[1], reverse=True)}:
            f.write(f"{key}: {output[key]}\n")


def play_for_me(guesses, solutions):
    while True:
        last_word = input("What's the last word you entered? ").lower()
        last_colours = input("What colours did you get? ").lower()
        remaining = solutions.copy()
        if last_colours == "ggggg":
            break
        else:
            eliminated = find_eliminated_words(
                last_colours, last_word, remaining)
            remaining = [w for w in solutions if w not in eliminated]
            print(f"Remaining words: {remaining}")
            num_words = len(remaining)
            best_word = ""
            best_eliminated = 0
            for word in guesses:
                guess_values = {}
                for target_word in remaining:
                    colours = colour_word(word, target_word)
                    if guess_values.get(colours):
                        guess_values[colours]["freq"] += 1
                    else:
                        guess_values[colours] = {
                            "freq": 1,
                            "score": len(find_eliminated_words(colours, word, solutions))
                        }

                avg_eliminated = 0
                for key in guess_values:
                    avg_eliminated += (guess_values[key]["freq"] /
                                       num_words) * guess_values[key]["score"]

                if avg_eliminated > best_eliminated:
                    best_word = word
                    best_eliminated = avg_eliminated

            print(f"Best continuation guess: {best_word}")


guess_file = open("guesses.txt", "r")
guesses = guess_file.read().splitlines()
guess_file.close()

solution_file = open("solutions.txt", "r")
solutions = solution_file.read().splitlines()
solution_file.close()

play_for_me(guesses, solutions)
