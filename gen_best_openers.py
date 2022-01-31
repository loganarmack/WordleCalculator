from eliminate_words import find_eliminated_words, colour_word


# Outputs the best opening guesses to a text file based on how many words
# they eliminate on average
def gen_best_openers(guesses, solutions, centre_type="MEAN"):
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

        # Calculate average number of eliminated words using different methods
        avg_eliminated = 0
        if centre_type == "MEAN":
            for key in guess_values:
                avg_eliminated += (guess_values[key]["freq"] /
                                   NUM_WORDS) * guess_values[key]["score"]

        elif centre_type == "MEDIAN":
            distance_from_centre = NUM_WORDS // 2 + 1
            sorted_guess_values = {k: v for k, v in sorted(
                guess_values.items(), key=lambda x: x[1]["score"])}
            for key in sorted_guess_values:
                distance_from_centre -= guess_values[key]["freq"]
                if distance_from_centre <= 0:
                    avg_eliminated = guess_values[key]["score"]
                    break

        elif centre_type == "MODE":
            sorted_guess_values = {k: v for k, v in sorted(
                guess_values.items(), key=lambda x: x[1]["freq"], reverse=True)}

            first = next(iter(sorted_guess_values))
            avg_eliminated = sorted_guess_values[first]["score"]

        else:
            print("Invalid centre type")

        print(f"{centre_type}: {word} -> {avg_eliminated}")
        output[word] = avg_eliminated

    print(output)

    with open(f"best_openers/best_openers_{centre_type}.txt", "w") as f:
        for key in {k: v for k, v in sorted(output.items(), key=lambda x: x[1], reverse=True)}:
            f.write(f"{key}: {output[key]}\n")

# Computes the average number of guesses to find the word for a given opener
# A little bit too slow to use, but could maybe be optimized to verify that
# considering openers as standalone is reasonable


def avg_num_guesses(opener, guesses, solutions):
    for word in solutions:
        num_guesses = 1
        remaining = solutions.copy()
        last_guess = opener
        while True:
            last_colours = colour_word(last_guess, word)

            # Got the word
            if last_colours == "ggggg":
                break

            eliminated = find_eliminated_words(
                last_colours, last_guess, remaining)
            remaining = [w for w in remaining if w not in eliminated]
            num_words = len(remaining)
            best_word = ""
            best_eliminated = 0
            for guess in guesses:
                guess_values = {}
                for target_word in remaining:
                    colours = colour_word(guess, target_word)
                    if guess_values.get(colours):
                        guess_values[colours]["freq"] += 1
                    else:
                        guess_values[colours] = {
                            "freq": 1,
                            "score": len(find_eliminated_words(colours, guess, remaining))
                        }

                avg_eliminated = 0
                for key in guess_values:
                    avg_eliminated += (guess_values[key]["freq"] /
                                       num_words) * guess_values[key]["score"]

                if avg_eliminated > best_eliminated:
                    best_word = word
                    best_eliminated = avg_eliminated
                elif avg_eliminated == best_eliminated and guess in remaining:
                    best_word = word
                    best_eliminated = avg_eliminated

            last_guess = best_word
            num_guesses += 1

        print(num_guesses)

    return num_guesses / len(solutions)
