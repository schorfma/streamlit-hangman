import string
from typing import Text, Dict, List, Optional, Set

import streamlit

streamlit.title("Streamlit Hangman")

streamlit.markdown(
    "1. Write your secret word into the input within the sidebar on the left.\n"
    "2. Don't forget to hide the sidebar before sharing this page in the browser.\n"
    "3. Happy Hangman playing!"
)

ALPHABET: List[Text] = [
    letter
    for letter in string.ascii_uppercase
]

SECRET_TEXT = streamlit.sidebar.text_input("Input the Secret word or words").upper()

SECRET_TEXT = "".join(
    [character if ord(character) < 128 else " " for character in SECRET_TEXT]
)

if SECRET_TEXT:
    GUESSED_LETTERS: Set[Text] = set(streamlit.text_input("Type letters to guess"))

    GUESS_ALPHABET: Dict[Text, Optional[bool]] = {
        letter: None
        for letter in ALPHABET
    }

    for guessed_letter in [
            guessed_letter.upper() for guessed_letter in list(GUESSED_LETTERS)
    ]:
        GUESS_ALPHABET[guessed_letter] = bool(guessed_letter in SECRET_TEXT)

    streamlit.subheader("Status for the letters of the Alphabet")
    streamlit.write(GUESS_ALPHABET)

    UNCOVERED_SECRET_TEXT: List[Text] = [
        character if GUESS_ALPHABET.get(character) or character == " " else "☐"
        for character in SECRET_TEXT
    ]

    streamlit.markdown(
        f"# `{''.join(UNCOVERED_SECRET_TEXT)}`"
    )

    WRONG_GUESSES = len(
        [
            value
            for value in GUESS_ALPHABET.values()
            if value == False
        ]
    )

    MAX_WRONG_GUESSES = 6

    streamlit.subheader(f"Wrongly guessed letters: `{WRONG_GUESSES}`/ `{MAX_WRONG_GUESSES}`")

    if WRONG_GUESSES >= MAX_WRONG_GUESSES:
        streamlit.error("Game Over!")
    elif "☐" not in UNCOVERED_SECRET_TEXT:
        streamlit.success("Game Won!")
