import pygame
from pygame.locals import *
import os.path
import crossy_road


def load_image(name, use_color_key=False):
    '''
    Upload an image and convert it to a surface.
    :param name: (str) name of image
    :param use_color_key: (bool) If the useColorKey flag is set to True, the color contained in the pixel (0,0)
    the image will be treated as transparent
    :return: image
    '''
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if use_color_key is True:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(name):
    '''
    Load audio files
    :param name: (str) name of file
    :return: sound
    '''
    fullname = os.path.join("sound", name)
    sound = pygame.mixer.Sound(fullname)
    return sound


class Screen(pygame.sprite.Sprite):
    '''
    A class to add a background
    '''
    def __init__(self):
        '''
        Initialize the screen class base
        '''
        pygame.sprite.Sprite.__init__(self)
        self.img1 = load_image("bg2.png")
        self.img1 = pygame.transform.scale(self.img1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image = self.img1
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect()


class Button:
    '''
    A class to add a button
    '''
    def __init__(self, color, x, y, width, height, text=""):
        '''
        Initialize the button class base
        :param color: (tuple) a tuple of numbers, which gives code RGB
        :param x: (int) a button location - width
        :param y: (int) a button location - height
        :param width: (int) a button width
        :param height: (int) a button height
        :param text: (str) the text to be printed
        '''
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, scr, outline=None):
        '''
        Draw a button on the screen
        :param scr: (str) the screen on which to print
        :param outline: (list) outline color in rgb
        '''
        if outline:
            pygame.draw.rect(scr, outline, (self.x - 4, self.y - 4, self.width + 8, self.height + 8), 0)
        pygame.draw.rect(scr, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont("Consolas", 20)
            text = font.render(self.text, True, (0, 0, 0))
            scr.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def check(self, pos):
        '''
        Check where the mouse cursor is
        :param pos: list of 3 values, where the mouse cursor is
        :return: (bool) True if the cursor is in good place, false in other case
        '''
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def redraw_screen():
    '''
    Refresh the screen
    '''
    Button1.draw(screen, dark_green)


pygame.init()
SCREEN_WIDTH = 580
SCREEN_HEIGHT = 700
pale_green = (152, 251, 152)
yellow_green = (154, 205, 50)
dark_green = (0, 100, 0)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Crossy Road")
clock = pygame.time.Clock()

startFX = load_sound("start.wav")

background = Screen()
screenSprite = pygame.sprite.Group()
screenSprite.add(background)
Button1 = Button(yellow_green, 50, 350, 120, 40, "Start")
screenSprite.draw(screen)

running = True
while running:
    redraw_screen()
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if Button1.check(mouse):
                startFX.play()
                crossy_road.mygame()
        if event.type == pygame.MOUSEMOTION:
            if Button1.check(mouse):
                Button1.color = pale_green
            else:
                Button1.color = yellow_green

pygame.quit()
