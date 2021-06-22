""" This game is all about catching the eggs with the help of Basket. Bomb will appear to confuse the gamer. Game will end if the basket catches the bomb """
import pygame
from pygame.constants import K_DOWN
from pygame.locals import *
import random
WIDTH = 800
HEIGHT = 600
SIZE=40
import time

class Start:
    """ This is the class where main objects are initialised and holds info how the game has been developed """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SR Game")
        self.play_background_music()
        self.surface = pygame.display.set_mode((WIDTH,HEIGHT))
        self.render_background()
        self.basket = Basket(self.surface)
        self.egg = Egg(self.surface)
        self.bomb = Bomb(self.surface)
        self.random_no = 1
        pygame.display.flip()

    """ Function where background image is set"""
    def render_background(self):
        bg = pygame.image.load("images/backgnd.jpg")
        self.surface.blit(bg, (0,0))

    """ Background music loaded"""   
    def play_background_music(self):
        pygame.mixer.music.load("music/bg_music_1.mp3")
        pygame.mixer.music.play()

    """ General function for sounds to be loaded at specific operations"""
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"music/{sound}.mp3")
        pygame.mixer.Sound.play(sound)


    """ This function is to check collision between Basket and egg W.R.T X and Y axis"""
    def is_collision(self, bx, ex, by, ey):
        if bx == ex and by == ey:
            return True
        return False

    """ Function where specific operations are called. Scores are displayed and checks collision of objects with each other"""
    def play(self):
        self.render_background()
        if self.random_no % 2 == 0 or self.random_no % 5 == 0:
            self.draw("bomb")
        else:
            self.draw("egg")
        
        self.draw("basket")
        self.self_score()
        pygame.display.flip()


        """ Checks collision between basket and egg with X and Y axis."""
        if self.is_collision(self.basket.basket_x, self.egg.egg_x, self.basket.basket_y, self.egg.egg_y):
            self.egg.length += 1
            self.egg.egg_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
            self.egg.egg_y = SIZE
            self.random_no = random.randint(1,10000)

        """ Checks collision between basket and bomb with X and Y axis."""
        if self.is_collision(self.basket.basket_x, self.bomb.bomb_x, self.basket.basket_y, self.bomb.bomb_y):
            self.bomb.bomb_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
            self.random_no += 1
            self.play_sound("crash")
            raise "Game Over" 

        """Condition if egg collides with ground"""
        if self.egg.egg_y == HEIGHT:
            self.play_sound("crash")
            raise "Game Over"

        """Condition if bomb collides with ground"""
        if self.bomb.bomb_y >= HEIGHT:
            self.random_no += 1
            self.bomb.bomb_y = SIZE
            
    """Function which displayes info regarding the scores and options whether to start new game oe exit"""
    def show_game_over(self):
        font = pygame.font.SysFont('Arial',30)
        line = font.render(f"Game is Over!! Your Score is: {self.egg.length}", True, (255,255,255))
        self.surface.blit(line,(50,100))
        line1 = font.render(f"To play again press ENTER. To exit press ESCAPE", True, (255,255,255))
        self.surface.blit(line1,(50,200))
        pygame.mixer.music.pause()
        pygame.display.flip()

    """Score Displaying function"""
    def self_score(self):
        font = pygame.font.SysFont('Arial',30)
        score = font.render(f"Score: {self.egg.length}",True,(255,255,255))
        self.surface.blit(score,(450,10))
        
    """Function for the apperance and movement of objects w.r.t X and Y axis"""
    def draw(self, element):
        if element == "bomb":
            self.bomb.move_down()
            el_image = self.bomb.bomb_image
            el_x = self.bomb.bomb_x
            el_y = self.bomb.bomb_y
        elif element == "egg":
            self.egg.move_down()
            el_image = self.egg.egg_image
            el_x = self.egg.egg_x
            el_y = self.egg.egg_y
        elif element == "basket":
            el_image = self.basket.basket_image
            el_x = self.basket.basket_x
            el_y = self.basket.basket_y
        else:
            pass

        self.surface.blit(el_image,(el_x,el_y))
        pygame.display.flip()

    """New game with reset of the objects takes place"""
    def reset(self):
        self.basket = Basket(self.surface)
        self.egg = Egg(self.surface)
        self.bomb = Bomb(self.surface)

    """ Function where the function of keys on which the respective takes place, """
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
               
            if(self.egg.length > 5):
                time.sleep(0.3)
            elif(self.egg.length > 10):
                time.sleep(0.1)
            else:
                time.sleep(0.5)

class Basket:
    """ This class is initialisation of basket with respective position and also for movement of Baskets"""
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.basket_image = pygame.image.load("images/basket.png").convert()
        self.direction = 'right'
        self.basket_x = (WIDTH/2)  #280
        self.basket_y = (HEIGHT - SIZE) #560

    def move_left(self):
        self.direction = 'left'
        self.move()

    def move_right(self):
        self.direction = 'right'
        self.move()

    """Function for movement of basket in right and left directions based on the conditions of hitting the edges"""
    def move(self):
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
    """ This class is initialisation of egg and also for movement of eggs in up and down directions"""
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.dir = "down"
        self.egg_y = 40
        self.egg_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
        self.egg_image = pygame.image.load("images/egg.png").convert()
        self.length = 0

    def move_down(self):
        self.egg_y += SIZE

class Bomb:
    """ This class is initialisation of bomb and also for movement of bombs in up and down directions"""
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.dir = "down"
        self.bomb_y = 40
        self.bomb_x = random.randint(1,int(WIDTH/SIZE - 1)) * SIZE
        self.bomb_image = pygame.image.load("images/bomb.jpg").convert()
        self.length = 0

    def move_down(self):
        self.bomb_y += SIZE


"""Main Control of the program"""
if __name__ == "__main__":
    start = Start()
    start.run()