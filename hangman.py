import math
from unicodedata import decimal
from wordboard import *
from getword import *
import pygame

pygame.init()

win_width = 1200
win_height = 440
win = pygame.display.set_mode((win_width, win_height))
pygame.display.update()

pygame.display.set_caption("Hangman")

source_array = ["urban-dictionary", "vocabulary.com", "animals", "random"]
source = "urban-dictionary"
min_size = 4
max_size = 10

def get_word():
    global source, min_size, max_size
    if source == "urban-dictionary": return get_word_from_urban_dictionary(min_size, max_size)
    elif source == "vocabulary.com": return get_word_from_vocabulary(min_size, max_size)
    elif source == "animals": return get_word_from_animals(min_size, max_size)
    else: return get_word_from_random_words(min_size, max_size)

def restart_game():
    draw_text(win, "PRESS ESC TO GO TO MAIN MENU OR ENTER TO START A NEW GAME", 20, (180, 180, 180), (win_width / 2) + 50, win_height - 20)

def game_over(word):
    draw_text(win, "GAME OVER", 50, (255, 0, 0), (win_width / 2) - 100, 50)
    draw_text(win, "THE WORD WAS ", 35, (180, 180, 180), (win_width / 2) - 100, 100)
    draw_text(win, word.upper(), 45, (220, 220, 220), (win_width / 2) - 100, 140)
    restart_game()

def game_won():
    draw_text(win, "YOU GUESSED IT", 50, (0, 255, 50), (win_width / 2) - 100, 50)
    restart_game()

def draw_meaning(meaning):
    length = 40
    if len(meaning) > length:
        rows = len(meaning)/length
        m_array = []
        start = 0
        end = length
        for i in range(round(rows) + 1):
            if end > len(meaning):
                end = len(meaning)
            m_array.append(meaning[start:end])
            start += length
            end += length
        pos_y = 10
        for row in m_array:
            draw_text(win, row, 20, (255, 255, 255), 750, pos_y, False)
            pos_y += 25
    else:
        draw_text(win, meaning, 25, (255, 255, 255), 700, 60, False)

def main():
    error_message = ""
    if source == "urban-dictionary" or source == "vocabulary.com":
        word, meaning = get_word()
        board = WordBoard(word)
        board.meaning = meaning
    else:
        word = get_word()
        board = WordBoard(word)
    show_meaning = False
    while True:
        # draw stuff
        win.fill((0, 0, 0))
        board.draw_man(win)
        board.draw_blanks(win)
        board.draw_guessed(win)
        board.draw_wrong(win)
        if show_meaning:
            draw_meaning(board.meaning)

        # end game if more than 5 wrong guesses
        if board.size >= 6:
            game_over(word)
            draw_meaning(board.meaning)

        # check if game is won
        is_guessed = True
        for guess in board.guessed:
            if not guess:
                is_guessed = False
        if is_guessed:
            game_won()
            draw_meaning(board.meaning)

        # draw error message
        if error_message is not None:
            draw_text(win, error_message, 20, (255, 255, 255), 350, 20, False)

        # draw score
        draw_text(win, "SCORE: " + str(board.score), 20, (255, 255, 255), 260, win_height - 30)

        # update window
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_F1:
                    show_meaning = True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    show_meaning = False
                    if is_guessed:
                        board.score += 1
                    if source == "urban-dictionary" or source == "vocabulary.com":
                        word, meaning = get_word()
                        board.new_word(word)
                        board.meaning = meaning
                    else:
                        word = get_word()
                        board = WordBoard(word)
                elif board.size < 6 and not is_guessed:
                    error_message = board.check_input(pygame.key.name(event.key))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    show_meaning = False

def manage_options(pos):
    global source, min_size, max_size
    min_colour = (255, 255, 255)
    max_colour = (255, 255, 255)
    source_colour = (255, 255, 255)
    exit_colour = (255, 255, 255)
    if pos == 0: min_colour = (0, 255, 255)
    elif pos == 1: max_colour = (0, 255, 255)
    elif pos == 2: source_colour = (0, 255, 255)
    elif pos == 3: exit_colour = (0, 255, 255)
    draw_text(win, "OPTIONS", 50, (255, 255, 255), win_width / 2, 75)
    draw_text(win, "MIN LETTERS: ", 30, (255, 255, 255), (win_width / 2) - 25, 200)
    draw_text(win, str(min_size), 30, min_colour, (win_width / 2) + 100, 200)
    draw_text(win, "MAX LETTERS: ", 30, (255, 255, 255), (win_width / 2) - 25, 250)
    draw_text(win, str(max_size), 30, max_colour, (win_width / 2) + 100, 250)
    draw_text(win, "SUBJECT: ", 30, (255, 255, 255), (win_width / 2) - 120, 300)
    draw_text(win, source.upper(), 30, source_colour, (win_width / 2) + 100, 300)
    draw_text(win, "BACK TO MAIN MENU", 28, exit_colour, win_width / 2, 400)

def options_menu():
    global source, min_size, max_size, source_array
    pos = 0
    subject = 0
    options = 4
    while True:
        win.fill((0, 0, 0))

        source = source_array[subject]

        manage_options(pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP:
                    if pos > 0:
                        pos -= 1
                    else: pos = options - 1
                if event.key == pygame.K_DOWN:
                    if pos < options - 1:
                        pos += 1
                    else: pos = 0
                if pos == 0:
                    if event.key == pygame.K_LEFT:
                        if min_size > 3:
                            min_size -= 1
                    if event.key == pygame.K_RIGHT:
                        if min_size < 18 and min_size < max_size:
                            min_size += 1
                        elif min_size < 18:
                            min_size += 1
                            max_size += 1
                if pos == 1:
                    if event.key == pygame.K_LEFT:
                        if max_size > 3 and max_size > min_size:
                            max_size -= 1
                        elif max_size > 3:
                            max_size -= 1
                            min_size -= 1
                    if event.key == pygame.K_RIGHT:
                        if max_size < 18:
                            max_size += 1
                if pos == 2:
                    if event.key == pygame.K_LEFT:
                        if subject > 0:
                            subject -= 1
                        else:
                            subject = len(source_array) - 1
                    if event.key == pygame.K_RIGHT:
                        if subject < len(source_array) - 1:
                            subject += 1
                        else: subject = 0
                if pos == 3:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        return

def manage_menu(pos):
    new_game = (255, 255, 255)
    options = (255, 255, 255)
    exit_game = (255, 255, 255)
    if pos == 0: new_game = (0, 255, 255)
    if pos == 1: options = (0, 255, 255)
    if pos == 2: exit_game = (0, 255, 255)

    draw_text(win, "HANGMAN", 60, (255, 255, 255), win_width / 2, 50)
    draw_text(win, "NEW GAME", 45, new_game, win_width / 2, (win_height / 2) - 45)
    draw_text(win, "OPTIONS", 45, options, win_width / 2, (win_height / 2) + 25)
    draw_text(win, "EXIT", 45, exit_game, win_width / 2, (win_height / 2) + 90)

def main_menu():
    pos = 0
    options = 3
    while True:
        win.fill((0, 0, 0))
        manage_menu(pos)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if pos > 0:
                    if event.key == pygame.K_UP:
                        pos -= 1
                if pos < options - 1:
                    if event.key == pygame.K_DOWN:
                        pos += 1
                if event.key == pygame.K_RETURN:
                    if pos == 0:
                        main()
                    if pos == 1:
                        options_menu()
                    if pos == options - 1:
                        quit()


main_menu()
