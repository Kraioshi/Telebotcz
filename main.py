import csv
import random

PATH = 'words.csv'

def read_csv(path: str) -> list:
    """Reads a CSV file and returns its content as a list of rows."""
    try:
        with open(path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            return [row for row in reader]

    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        return []

    except csv.Error as e:
        print(f"Error reading CSV file at line {reader.line_num}: {e}")
        return []


def ask_question(question: str, correct_answer: str) -> bool:
    """Prompts the user with a question and checks their answer."""
    user_answer = input(question + '\n').strip().lower()

    if user_answer == "stop":
        return False  # Indicates to stop the game
    elif user_answer == correct_answer.lower():
        print('Correct!' + '\n')
    else:
        print(f"Wrong! The correct answer is: {correct_answer}")
        print("____________")

    return True  # Continue the game


def play_game(bank: list) -> None:
    """Main game loop that selects questions randomly from the bank."""
    game_is_on = True

    while game_is_on and bank:
        random_pair = random.choice(bank)
        question = random_pair[1]
        correct_answer = random_pair[0]
        game_is_on = ask_question(question, correct_answer)


def main() -> None:
    """Main entry point of the script."""
    bank = read_csv(PATH)
    if bank:
        play_game(bank)


if __name__ == "__main__":
    main()