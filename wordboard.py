import pygame

def draw_text(win, text, size, color, pos_x, pos_y, text_center=True):
    options_text = pygame.font.SysFont("Tahoma", size)
    TextSurf = options_text.render(text, True, color)
    TextRect = TextSurf.get_rect()
    if text_center:
        TextRect.center = (int(pos_x), int(pos_y))
    else:
        TextRect = (int(pos_x), int(pos_y))
    win.blit(TextSurf, TextRect)

class WordBoard:
    def __init__(self, word):
        self.word = word
        self.length = len(self.word)
        self.wrong_guessed = []
        self.guessed = []
        for x in range(self.length):
            self.guessed.append(False)
        self.size = 0
        self.score = 0
        self.meaning = ""

    def new_word(self, word):
        self.word = word
        self.length = len(self.word)
        self.wrong_guessed = []
        self.guessed = []
        for x in range(self.length):
            self.guessed.append(False)
        self.size = 0

    def new_meaning(self, meaning):
        self.meaning = meaning

    def draw_man(self, win):
        pygame.draw.rect(win, (255, 255, 255), ([210, 30, 10, 50])) # noose
        pygame.draw.rect(win, (255, 255, 255), ([60, 10, 170, 20])) # top
        pygame.draw.rect(win, (255, 255, 255), ([60, 10, 20, 400])) # tall bit
        pygame.draw.rect(win, (255, 255, 255), ([10, 400, 200, 20])) # base
        if self.size >= 1:
            pygame.draw.circle(win, (255, 255, 255), ([220, 90]), 30) # head
            if self.size >= 2:
                pygame.draw.rect(win, (255, 255, 255), ([210, 110, 20, 140])) # body
                if self.size >= 3:
                    pygame.draw.rect(win, (255, 255, 255), ([150, 140, 60, 20])) # left arm
                    if self.size >= 4:
                        pygame.draw.rect(win, (255, 255, 255), ([230, 140, 60, 20])) # right arm
                        if self.size >= 5:
                            pygame.draw.polygon(win, (255, 255, 255), ([220, 250], [220, 245], [190, 370]), 20) # left leg
                            if self.size >= 6:
                                pygame.draw.polygon(win, (255, 255, 255), ([220, 250], [220, 245], [250, 370]), 20) # right leg

    def draw_wrong(self, win):
        distance = 45
        pos_x = 270
        for wrong in self.wrong_guessed:
            draw_text(win, wrong.upper(), 35, (225, 130, 130), pos_x, 300)
            pos_x += distance

    def draw_guessed(self, win):
        distance = 45
        pos_x = 263
        for x in range(self.length):
            if self.guessed[x]:
                draw_text(win, self.word[x].upper(), 35, (255, 255, 255), pos_x, 235)
            pos_x += distance

    def draw_blanks(self, win):
        distance = 45
        pos_x = 250
        for x in range(self.length):
            pygame.draw.rect(win, (255, 255, 255), ([pos_x, 255, 30, 5]))
            pos_x += distance

    def check_input(self, letter):
        if (letter.isalpha() or letter == '-') and len(letter) == 1:
            already_guessed = False
            for x in range(len(self.guessed)):
                if letter.upper() == self.word[x].upper() and self.guessed[x]:
                    already_guessed = True
                    return "You already guessed that letter."
            in_word = False
            for x in range(self.length):
                if letter.upper() == self.word[x].upper():
                    self.guessed[x] = True
                    in_word = True

            if not in_word:
                already_guessed = False
                for char in self.wrong_guessed:
                    if char.upper() == letter.upper():
                        already_guessed = True

                if already_guessed:
                    return "You already tried that letter!"
                else:
                    self.wrong_guessed.append(letter)
                    self.size += 1
                    return ""
            else:
                if already_guessed:
                    return "You already guessed that letter."
                else:
                    return ""
        else:
            return "Input is not a valid letter."
