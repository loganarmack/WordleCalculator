from solver import wordle_solver
from gen_best_openers import gen_best_openers

guess_file = open("word_lists/guesses.txt", "r")
guesses = guess_file.read().splitlines()
guess_file.close()

solution_file = open("word_lists/solutions.txt", "r")
solutions = solution_file.read().splitlines()
solution_file.close()

wordle_solver(guesses, solutions)

#gen_best_openers(guesses, solutions, "MEAN")
#gen_best_openers(guesses, solutions, "MEDIAN")
#gen_best_openers(guesses, solutions, "MODE")
