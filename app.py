import random
import os
import sys

words = [
    "python", "apple", "mango", "grapes", "house", "galaxy", "rocket",
    "jungle", "puzzle", "wizard", "banana", "orange", "sunshine",
    "holiday", "diamond", "teacher", "library", "computer", "science",
    "forest", "mountain", "rainbow", "turtle", "butterfly", "adventure",
    "dolphin", "chocolate", "festival", "planet", "texture", "freedom",
    "harmony", "journey", "kitchen", "monster", "ocean", "pirate",
    "quartz", "stadium", "unicorn", "village", "whistle"
]
hangman_stages = [
    "\n  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "\n  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    "\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========="
]

DIFFICULTY_SETTINGS = {
    "easy": {"max_attempts": 6, "base_score": 10, "bonus_per_attempt": 2},
    "medium": {"max_attempts": 5, "base_score": 20, "bonus_per_attempt": 3},
    "hard": {"max_attempts": 4, "base_score": 30, "bonus_per_attempt": 5}
}

COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_CYAN = "\033[36m"
COLOR_MAGENTA = "\033[35m"


def color(text, code):
    if not sys.stdout.isatty():
        return text
    return f"{code}{text}{COLOR_RESET}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_title():
    print(color("╔════════════════════════════════╗", COLOR_CYAN))
    print(color("║        H A N G M A N  G A M E   ║", COLOR_CYAN))
    print(color("╚════════════════════════════════╝", COLOR_CYAN))
    print(color("A simple, colorful word guessing game.", COLOR_YELLOW))
    print(color("Guess one letter at a time and watch the hangman art build up.\n", COLOR_YELLOW))


def get_random_word(difficulty):
    easy_words = [w for w in words if len(w) <= 5]
    medium_words = [w for w in words if 6 <= len(w) <= 7]
    hard_words = [w for w in words if len(w) >= 8]

    difficulty_map = {
        "easy": easy_words,
        "medium": medium_words,
        "hard": hard_words
    }

    selected_words = difficulty_map.get(difficulty, words)
    return random.choice(selected_words) if selected_words else random.choice(words)


def format_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        print(color("\nInput closed. Exiting the game.", COLOR_RED))
        exit()


def is_valid_guess(guess, guessed_letters):
    return len(guess) == 1 and guess.isalpha() and guess not in guessed_letters


def get_difficulty_choice():
    while True:
        clear_screen()
        display_title()
        print(color("Select a difficulty level:", COLOR_YELLOW))
        print(color("  easy   - shorter words, more attempts", COLOR_GREEN))
        print(color("  medium - moderate word length and attempts", COLOR_MAGENTA))
        print(color("  hard   - longer words, fewer attempts", COLOR_RED))
        choice = ask(color("\nEnter difficulty (easy/medium/hard): ", COLOR_CYAN)).lower().strip()
        if choice in DIFFICULTY_SETTINGS:
            return choice
        print(color("Please choose easy, medium, or hard.", COLOR_RED))
        ask(color("Press Enter to continue...", COLOR_YELLOW))


def calculate_score(difficulty, wrong_guesses):
    settings = DIFFICULTY_SETTINGS[difficulty]
    remaining = max(settings["max_attempts"] - wrong_guesses, 0)
    return settings["base_score"] + remaining * settings["bonus_per_attempt"]


def play_game(difficulty):
    word = get_random_word(difficulty)
    guessed_letters = []
    wrong_guesses = 0
    settings = DIFFICULTY_SETTINGS[difficulty]

    while True:
        clear_screen()
        display_title()

        current_display = format_word(word, guessed_letters)
        stage = min(wrong_guesses, len(hangman_stages) - 1)
        print(color(hangman_stages[stage], COLOR_YELLOW))
        print(color(f"\nDifficulty: {difficulty.title()}", COLOR_MAGENTA))
        print(color(f"Word: {current_display}", COLOR_BOLD))
        print(color(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}", COLOR_MAGENTA))
        print(color(f"Remaining attempts: {settings['max_attempts'] - wrong_guesses}\n", COLOR_CYAN))

        if "_" not in current_display:
            score = calculate_score(difficulty, wrong_guesses)
            print(color("🎉 Congratulations! You guessed the word!", COLOR_GREEN))
            print(color(f"The word was: {word}", COLOR_GREEN))
            print(color(f"You earned {score} points for this win!\n", COLOR_GREEN))
            return True, score

        if wrong_guesses >= settings["max_attempts"]:
            print(color("💀 Game Over. The hangman is complete.", COLOR_RED))
            print(color(f"The word was: {word}\n", COLOR_RED))
            return False, 0

        guess = ask(color("Enter a letter: ", COLOR_CYAN)).lower().strip()

        if not guess:
            print(color("Please enter a letter.", COLOR_RED))
            ask(color("Press Enter to continue...", COLOR_YELLOW))
            continue

        if not guess.isalpha() or len(guess) != 1:
            print(color("Please enter a single alphabet letter.", COLOR_RED))
            ask(color("Press Enter to continue...", COLOR_YELLOW))
            continue

        if guess in guessed_letters:
            print(color("You already guessed this letter. Try another one.", COLOR_YELLOW))
            ask(color("Press Enter to continue...", COLOR_YELLOW))
            continue

        guessed_letters.append(guess)

        if guess in word:
            print(color("✅ Great! That letter is in the word.", COLOR_GREEN))
        else:
            wrong_guesses += 1
            print(color("❌ Sorry, that letter is not in the word.", COLOR_RED))

        ask(color("Press Enter to continue...", COLOR_YELLOW))


def display_stats(games_played, games_won, total_score):
    print(color("\nGame Summary", COLOR_CYAN))
    print(color(f"  Games played: {games_played}", COLOR_YELLOW))
    print(color(f"  Games won: {games_won}", COLOR_GREEN))
    print(color(f"  Total score: {total_score}", COLOR_MAGENTA))


def main():
    games_played = 0
    games_won = 0
    total_score = 0

    while True:
        difficulty = get_difficulty_choice()
        won, score = play_game(difficulty)
        games_played += 1
        total_score += score
        if won:
            games_won += 1

        display_stats(games_played, games_won, total_score)
        answer = ask(color("\nWould you like to play again? (y/n): ", COLOR_CYAN)).lower().strip()
        if answer != "y":
            print(color("\nThanks for playing Hangman! Goodbye.", COLOR_YELLOW))
            break


if __name__ == "__main__":
    main()