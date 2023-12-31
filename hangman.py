'''
HANGMAN

'''
import pygame
import random

pygame.init()
Height = 480
Width = 700
win=pygame.display.set_mode((Width,Height))


#colors
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
BLUE = (0,0,255)
GRAY = (240,255,255)
#fonts
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
word = ''
buttons = []
guessed = []
#couldn't figure out a better way to do this, had to paste each path
hangmanPics = [pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman0.png'), 
               pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman1.png'), 
               pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman2.png'), 
               pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman3.png'), 
               pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman4.png'), 
               pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman5.png'), 
               pygame.image.load('C:/Users/drea1/CSE 120 HW/Hangman/Hangman6.png')]

limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(WHITE)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(Width/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (Width/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()



def loadWords(difficulty):
    file_path = f ("C:/Users/drea1/CSE 120 HW/Hangman/words_{difficulty}.txt")
    with open(file_path) as file: 
        words = file.readlines()
    return [word.strip() for word in words]

def difficultyMenu():
    pygame.font.init()
    menu_font = pygame.font.SysFont("Arial", 30)
    options = ["Easy", "Medium", "Hard"]
    selected_option = 0

    while True:
        win.fill(WHITE)
        pygame.draw.rect(win, GRAY, (50, 50, 600, 300))

        for i, option in enumerate(options):
            text = menu_font.render(option, True, BLACK if i == selected_option else WHITE)
            win.blit(text, (300 - text.get_width() // 2, 100 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]
    


def randomWord():
    file = open("C:/Users/drea1/CSE 120 HW/Hangman/words.txt")
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(WHITE)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (Width/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (Width/2 - wordWas.get_width()/2, 245))
    win.blit(label, (Width / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    
    difficulty = difficultyMenu()
    word = random.choice(loadWords(difficulty))
    
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

#MAINLINE


# Setup buttons
increase = round(Width / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([GRAY, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

difficulty = difficultyMenu()
word = randomWord(difficulty)

inPlay = True 

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()

# always quit pygame when done!
