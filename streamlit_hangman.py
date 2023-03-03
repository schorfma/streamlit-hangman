import string
from typing import Text, Dict, List, Optional, Set

import streamlit

streamlit.set_page_config(
    page_title="Streamlit Hangman",
    page_icon="game",
)

LANGUAGES = {"en": "English", "de": "Deutsch"}

LANGUAGE = streamlit.sidebar.selectbox(
    "🌍 Language",
    list(LANGUAGES.keys()),
    format_func=lambda lang: LANGUAGES[lang],
)

SHOW_SOURCE_LINK_TEXT = {
    "en": "Show link to Source Code Repository",
    "de": "Link zu Quelltext-Verzeichnis einblenden",
}

SOURCE_CODE_REPO_URL = "https://gitlab.com/schorfma/streamlit-hangman"

SELF_HOSTING_INFO_TEXT = {
    "en": f"Host your own Hangman interface using <{SOURCE_CODE_REPO_URL}>",
    "de": f"Hoste deine eigene Galgenraten-Oberfläche mit <{SOURCE_CODE_REPO_URL}>",
}

if streamlit.sidebar.checkbox(SHOW_SOURCE_LINK_TEXT[LANGUAGE]):
    streamlit.info(SELF_HOSTING_INFO_TEXT[LANGUAGE])

TITLE_TEXT = {"en": "Streamlit Hangman", "de": "Streamlit Galgenraten"}

streamlit.title(TITLE_TEXT[LANGUAGE])

INSTRUCTIONS_TEXT = {
    "en": (
        "1. Write your secret word into the input within the sidebar on the left.\n"
        "2. Don't forget to hide the sidebar before sharing this page in the browser.\n"
        "3. Happy Hangman playing!"
    ),
    "de": (
        "1. Schreibe dein geheimes Wort in das Eingabefeld in der Seitenleiste links.\n"
        "2. Vergiss nicht die Seitenleiste wieder vor dem Teilen dieser Seite zu schließen\n"
        "3. Viel Spaß beim Galgenraten!"
    ),
}

streamlit.markdown(INSTRUCTIONS_TEXT[LANGUAGE])

ALPHABET: List[Text] = [letter for letter in string.ascii_uppercase]

LETTER_PLACEHOLDER = "☐"
SPACE_CHARACTER = " "

SECRET_TEXT_INPUT_TEXT = {
    "en": "Input the Secret word or words",
    "de": "Gib das geheime Wort oder mehrere geheime Wörter ein",
}

SECRET_TEXT = streamlit.sidebar.text_input(SECRET_TEXT_INPUT_TEXT[LANGUAGE]).upper()

SECRET_TEXT = "".join(
    [character if character in ALPHABET else " " for character in SECRET_TEXT]
)

MAX_WRONG_GUESSES_TEXT = {
    "en": "Maximum number of wrong guesses",
    "de": "Maximale Anzahl an falsch geratenen Buchstaben",
}

MAX_WRONG_GUESSES_DEFAULT = 6

MAX_WRONG_GUESSES = streamlit.sidebar.slider(
    MAX_WRONG_GUESSES_TEXT[LANGUAGE],
    value=MAX_WRONG_GUESSES_DEFAULT,
    min_value=4,
    max_value=10,
)

SHOW_HANGMAN_IMAGES_TEXT = {
    "en": "Show Hangman Images",
    "de": "Galgenraten-Bilder anzeigen",
}

if MAX_WRONG_GUESSES == MAX_WRONG_GUESSES_DEFAULT:
    SHOW_HANGMAN_IMAGES = streamlit.sidebar.checkbox(
        SHOW_HANGMAN_IMAGES_TEXT[LANGUAGE], value=True
    )
else:
    SHOW_HANGMAN_IMAGES = False
    streamlit.sidebar.markdown(f"~~{SHOW_HANGMAN_IMAGES_TEXT[LANGUAGE]}~~")

if SECRET_TEXT:
    GUESSED_LETTERS_TEXT = {
        "en": "Type letters to guess",
        "de": "Gib Buchstaben zum Erraten ein",
    }

    GUESSED_LETTERS: Set[Text] = set(
        streamlit.text_input(GUESSED_LETTERS_TEXT[LANGUAGE])
    )

    GUESS_ALPHABET: Dict[Text, Optional[bool]] = {letter: None for letter in ALPHABET}

    for guessed_letter in [
        guessed_letter.upper()
        for guessed_letter in list(GUESSED_LETTERS)
        if guessed_letter.upper() in ALPHABET
    ]:
        GUESS_ALPHABET[guessed_letter] = bool(guessed_letter in SECRET_TEXT)

    ALPHABET_LETTERS_STATUS_TEXT = {
        "en": "Show status for the letters of the Alphabet",
        "de": "Status der Buchstaben des Alphabets zeigen",
    }

    if streamlit.checkbox(ALPHABET_LETTERS_STATUS_TEXT[LANGUAGE]):
        streamlit.write(GUESS_ALPHABET)

    UNCOVERED_SECRET_TEXT: List[Text] = [
        character
        if GUESS_ALPHABET.get(character) or character == SPACE_CHARACTER
        else LETTER_PLACEHOLDER
        for character in SECRET_TEXT
    ]

    WRONG_GUESSES = len([value for value in GUESS_ALPHABET.values() if value == False])

    HANGMAN_IMAGES = [
        "images/Hangman-0.png",
        "images/Hangman-1.png",
        "images/Hangman-2.png",
        "images/Hangman-3.png",
        "images/Hangman-4.png",
        "images/Hangman-5.png",
        "images/Hangman-6.png",
    ]

    HANGMAN_IMAGES_SOURCE = [
        "https://commons.wikimedia.org/wiki/File:Hangman-0.png",
        "https://commons.wikimedia.org/wiki/File:Hangman-1.png",
        "https://commons.wikimedia.org/wiki/File:Hangman-2.png",
        "https://commons.wikimedia.org/wiki/File:Hangman-3.png",
        "https://commons.wikimedia.org/wiki/File:Hangman-4.png",
        "https://commons.wikimedia.org/wiki/File:Hangman-5.png",
        "https://commons.wikimedia.org/wiki/File:Hangman-6.png",
    ]

    if SHOW_HANGMAN_IMAGES:
        streamlit.image(HANGMAN_IMAGES[min(WRONG_GUESSES, MAX_WRONG_GUESSES_DEFAULT)])

        IMAGE_LICENSE_LINK = "[Creative Commons Attribution-Share Alike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en)"

        IMAGE_AUTHOR_LINK = "[Demi](https://en.wikipedia.org/wiki/User:Demi)"

        IMAGE_SOURCE_TEXT = {
            "en": (
                f"* Image License: {IMAGE_LICENSE_LINK}\n"
                f"* Image Author: User {IMAGE_AUTHOR_LINK} on English Wikipedia\n"
                f"* Image Source: <{HANGMAN_IMAGES_SOURCE[min(WRONG_GUESSES, MAX_WRONG_GUESSES_DEFAULT)]}>"
            ),
            "de": (
                f"* Bildlizenz: {IMAGE_LICENSE_LINK}\n"
                f"* Bildautor: Benutzer {IMAGE_AUTHOR_LINK} auf der englischen Wikipedia\n"
                f"* Bildquelle: <{HANGMAN_IMAGES_SOURCE[min(WRONG_GUESSES, MAX_WRONG_GUESSES_DEFAULT)]}>"
            ),
        }

        streamlit.info(IMAGE_SOURCE_TEXT[LANGUAGE])

    streamlit.markdown(f"# `{''.join(UNCOVERED_SECRET_TEXT)}`")

    WRONGLY_GUESSED_LETTERS_TEXT = {
        "en": "Wrongly guessed letters",
        "de": "Falsch geratene Buchstaben",
    }

    streamlit.subheader(
        f"{WRONGLY_GUESSED_LETTERS_TEXT[LANGUAGE]}: `{WRONG_GUESSES}`/ `{MAX_WRONG_GUESSES}`"
    )

    GAME_OVER_TEXT = {"en": "Game Over!", "de": "Spiel verloren!"}

    GAME_WON_TEXT = {"en": "Game Won!", "de": "Spiel gewonnen!"}

    GAME_UNDECIDED_TEXT = {
        "en": "Game is not decided, yet",
        "de": "Spiel ist noch nicht entschieden",
    }

    if WRONG_GUESSES >= MAX_WRONG_GUESSES:
        streamlit.error(f"### {GAME_OVER_TEXT[LANGUAGE]}")
    elif LETTER_PLACEHOLDER not in UNCOVERED_SECRET_TEXT:
        streamlit.success(f"### {GAME_WON_TEXT[LANGUAGE]}")
    else:
        streamlit.info(f"### {GAME_UNDECIDED_TEXT[LANGUAGE]}")
