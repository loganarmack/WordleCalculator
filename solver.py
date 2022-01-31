from eliminate_words import find_eliminated_words, colour_word


# Uses the elimination and average algorithm to solve the wordle
# and provide the user with the next best guess
def wordle_solver(guesses, solutions):
    remaining = solutions.copy()
    while True:
        last_word = input("What's the last word you entered? ").lower()
        last_colours = input("What colours did you get? ").lower()
        if last_colours == "ggggg":
            break

        eliminated = find_eliminated_words(
            last_colours, last_word, remaining)
        remaining = [w for w in remaining if w not in eliminated]
        print(f"Remaining words: {remaining}")
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
                best_word = guess
                best_eliminated = avg_eliminated
            elif avg_eliminated == best_eliminated and guess in remaining:
                best_word = guess
                best_eliminated = avg_eliminated

        print(f"Best continuation guess: {best_word}")


# Uses the elimination algorithm to display which words are still possible given the user's guesses
# Does not provide any suggestions, so better if you want to still feel like you're solving the wordle
# yourself.
def show_remaining_words(solutions):
    remaining = solutions.copy()
    while True:
        last_word = input("What's the last word you entered? ").lower()
        last_colours = input("What colours did you get? ").lower()
        if last_colours == "ggggg":
            break

        eliminated = find_eliminated_words(
            last_colours, last_word, remaining)
        remaining = [w for w in remaining if w not in eliminated]
        print(f"Remaining words: {remaining}")
