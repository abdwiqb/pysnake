from tkinter import *
import random
import pygame

pygame.mixer.init()
 
eat_sound = pygame.mixer.Sound('sounds\\eat.wav')
death_sound = pygame.mixer.Sound('sounds\\death.wav')

CELL_SIZE = 20
WIN_WIDTH = 24
WIN_HEIGHT = 24
SCORE_LABEL_SIZE = 24
FONT_NAME = 'consolas'

SNAKE_SPAWN = [1, 12]
START_SNAKE = 3
MAX_SNAKE = 300

FRAME_DELAY = 100

SNAKE_C = '#0F0'
FOOD_C = '#F00'
BG_C = '#000'
N_TXT_C = '#000'

dead = False
score = 0
snake_dir = 'r'

snakes = []
foods = []

win = Tk()
win.geometry(f'{CELL_SIZE*WIN_WIDTH}x{(CELL_SIZE*WIN_HEIGHT)+SCORE_LABEL_SIZE}')
win.resizable(False, False)
win.config()
win.title('Snake')

score_label = Label(text=f'Score: {score}', font=(FONT_NAME, SCORE_LABEL_SIZE))
score_label.pack(side='top')

canvas = Canvas(width=WIN_WIDTH*CELL_SIZE, height=WIN_HEIGHT*CELL_SIZE, bg=BG_C)
canvas.pack(side='top')


class Snake:
    def __init__(self):
        
        self.size = START_SNAKE
        self.cords = []
        self.parts = []

        for i in range(0, self.size):
            self.cords.append([SNAKE_SPAWN[0], SNAKE_SPAWN[1]])

        for x, y in self.cords:
            part = canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, x*CELL_SIZE+CELL_SIZE, y*CELL_SIZE+CELL_SIZE, fill=SNAKE_C, tag='snake')
            self.parts.append(part)



class Food:

    def __init__(self):

        x = random.randint(0, WIN_WIDTH-1)
        y = random.randint(0, WIN_HEIGHT-2)
        
        self.cords = [x, y]

        canvas.create_rectangle(x*CELL_SIZE+(CELL_SIZE/4), y*CELL_SIZE+(CELL_SIZE/4), x*CELL_SIZE+(CELL_SIZE/4*3), y*CELL_SIZE+(CELL_SIZE/4*3), fill=FOOD_C, tag='food')


    def eat(self):
        
        global score

        eat_sound.play()

        score += 1
        score_label.config(text=f'Score: {score}')
        canvas.delete('food')
        foods.append(Food())
        del foods[0]


def game_death():

    global dead

    death_sound.play()
    
    score_label.config(text=f'You ate {score} apples')

    dead = True


def snake_coll(snake):
    
    x, y = snake.cords[0]
    
    if x >= WIN_WIDTH or x < 0 or y >= WIN_HEIGHT-1 or y < 0:
        game_death()
        return 'dead'

    for part in snake.cords[1:]:
        if part[0] == x and part[1] == y:
            game_death()
            return 'dead'

    for food in foods:
        if x == food.cords[0] and y == food.cords[1]:
            food.eat()
            return True
    return False


def game_frame():

    if dead:
        return None
    
    for snake in snakes:

        x, y = snake.cords[0]

        if snake_dir == 'u':
            y -= 1
        elif snake_dir == 'l':
            x -= 1
        elif snake_dir == 'd':
            y += 1
        elif snake_dir == 'r':
            x += 1
        
        snake.cords.insert(0, (x, y))
        part = canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill=SNAKE_C, tag='snake')
        snake.parts.insert(0, part)
        
        coll = snake_coll(snake)

        if coll == 'dead':
            return None
        elif not coll or len(snake.parts) >= MAX_SNAKE+1:

            del snake.cords[-1]

            canvas.delete(snake.parts[-1])

            del snake.parts[-1]

        win.after(FRAME_DELAY, game_frame)


def take_key(k):
    
    global snake_dir, dead

    if dead:
        return None

    if (k=='w' and snake_dir=='d') or (k=='a' and snake_dir=='r') or (k=='s' and snake_dir=='u') or (k=='d' and snake_dir=='l'):
        return None
    if k == 'w':
        snake_dir = 'u'
    elif k == 'a':
        snake_dir = 'l'
    elif k == 's':
        snake_dir = 'd'
    elif k == 'd':
        snake_dir = 'r'


def main():

    for i in ['w', 'a', 's', 'd']:
        win.bind(f'<{i}>', lambda k=i:take_key(k.char))
    
    food = Food()
    snake = Snake()

    foods.append(food)
    snakes.append(snake)

    game_frame()
    
    win.mainloop()


if __name__ == '__main__':
    main()
