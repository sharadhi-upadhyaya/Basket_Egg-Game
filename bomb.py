import pygame
from pygame.constants import K_DOWN
from pygame.locals import *
import random
WIDTH = 800
HEIGHT = 600
SIZE=40
import time

class Start:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SR Game")
        self.play_background_music()
        self.surface = pygame.display.set_mode((WIDTH,HEIGHT))
        self.render_background()
        self.basket = Basket(self.surface)
        self.basket.draw()
        self.egg = Egg(self.surface)
        self.egg.draw()
        self.bomb = Bomb(self.surface)
        self.bomb.draw()
        # self.egg.move_down()
        pygame.display.flip()

    def render_background(self):
        bg = pygame.image.load("images/background.jpg")
        self.surface.blit(bg, (0,0))
        
    def play_background_music(self):
        pygame.mixer.music.load("music/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"music/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def is_collision(self, bx, ex, by, ey):
        # print(bx, ex)
        # print(by, ey)
        if bx == ex and by == ey:
            return True
        return False

    def play(self):
        self.render_background()
        self.egg.draw()
        self.basket.draw()
        self.bomb.draw()
        self.self_score()
        pygame.display.flip()
        # basket_y = 560
        # egg_x = 250
        # print("Y", self.egg.egg_y, self.basket.basket_y)
        # print("X", self.egg.egg_x, self.basket.basket_x)
        if self.is_collision(self.basket.basket_x, self.egg.egg_x, self.basket.basket_y, self.egg.egg_y):
            self.egg.length += 1
            self.egg.egg_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
            self.egg.egg_y = 40

        if self.egg.egg_y == HEIGHT:
            # self.pause = True
            # self.show_game_over()
            self.play_sound("crash")
            raise "Game Over"        
            
        
    def show_game_over(self):
        font = pygame.font.SysFont('Arial',30)
        line = font.render(f"Game is Over!! Your Score is: {self.egg.length}", True, (255,255,255))
        self.surface.blit(line,(50,100))
        line1 = font.render(f"To play again press ENTER. To exit press ESCAPE", True, (255,255,255))
        self.surface.blit(line1,(50,200))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def self_score(self):
        font = pygame.font.SysFont('Arial',30)
        score = font.render(f"Score: {self.egg.length}",True,(255,255,255))
        self.surface.blit(score,(450,10))
        
    
    def reset(self):
        self.basket = Basket(self.surface)
        self.egg = Egg(self.surface)
        self.bomb = Bomb(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            # print(pause)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.basket.move_left()
                            
                        if event.key == K_RIGHT:
                            self.basket.move_right()
                        
                if event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play() 
            except Exception as e:            
                self.show_game_over()
                pause = True
                self.reset()
               
            # self.play()
            # pygame.display.flip()
            if(self.egg.length > 5):
                time.sleep(0.3)
            elif(self.egg.length > 10):
                time.sleep(0.1)
            else:
                time.sleep(0.5)

class Basket:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.basket_image = pygame.image.load("images/basket.png").convert()
        # self.parent_screen.blit(self.basket_image,(250,560))
        # pygame.display.flip()
        self.direction = 'right'
        self.basket_x = (WIDTH/2)  #280
        self.basket_y = (HEIGHT - SIZE) #560

    def draw(self):
        self.parent_screen.blit(self.basket_image, (self.basket_x, self.basket_y))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'
        self.walk()

    def move_right(self):
        self.direction = 'right'
        self.walk()

    def walk(self):
        if self.direction == 'right':
            if self.basket_x != (WIDTH - SIZE):  #560
                self.basket_x += SIZE
            else:
                self.direction = 'left'
     
        else:
            if self.basket_x != 0:
                self.basket_x -= SIZE
            else:
                self.direction = 'right'
            
class Egg:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.dir = "down"
        self.egg_y = 40
        self.egg_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
        self.egg_image = pygame.image.load("images/egg.png").convert()
        self.length = 0
        # self.x = 250
        
        
    def draw(self):
        self.move_down()
        self.parent_screen.blit(self.egg_image, (self.egg_x, self.egg_y))
        pygame.display.flip()
        # time.sleep(1)

    def move_down(self):
        self.egg_y += SIZE

class Bomb:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.dir = "down"
        self.bomb_y = 40
        self.bomb_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
        self.bomb_image = pygame.image.load("images/bomb.jpg").convert()
        self.length = 0

    def draw(self):
        self.move_down()
        self.parent_screen.blit(self.bomb_image, (self.bomb_x, self.bomb_y))
        pygame.display.flip()

    def move_down(self):
        self.bomb_y += SIZE



if __name__ == "__main__":
    start = Start()
    start.run()