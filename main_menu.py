import pygame
from pygame.locals import *
import os.path
import crossy_road


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
            scr.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

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


def menu():
    '''
    Display the menu screen
    '''
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

    def redraw_screen():
        '''
        Refresh the screen
        '''
        Button1.draw(screen, dark_green)
        Button2.draw(screen, dark_green)
        Button3.draw(screen, dark_green)
        Button4.draw(screen, dark_green)
        Button5.draw(screen, dark_green)
        Button6.draw(screen, dark_green)


    def text_display():
        '''
        Display the text on the screen
        '''
        font = pygame.font.SysFont("Consolas", 20)
        text = font.render('Set difficulty level: ', False, (0, 0, 0))
        screen.blit(text, (320, 350))


    pygame.init()
    SCREEN_WIDTH = 590
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
    Button1 = Button(yellow_green, 50, 350, 150, 40, "Start")
    Button2 = Button(yellow_green, 50, 400, 150, 40, "Instruction")
    Button3 = Button(yellow_green, 50, 450, 150, 40, "About me")
    Button4 = Button(yellow_green, 50, 500, 150, 40, "Exit")
    Button5 = Button(yellow_green, 330, 400, 90, 30, "Easy")
    Button6 = Button(yellow_green, 450, 400, 90, 30, "Hard")

    screenSprite.draw(screen)

    running = True
    while running:
        redraw_screen()
        pygame.display.update()
        text_display()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button4.check(mouse):
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button3.check(mouse):
                    about_me()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button2.check(mouse):
                    instruction()
            if event.type == pygame.MOUSEMOTION:
                if Button1.check(mouse):
                    Button1.color = pale_green
                else:
                    Button1.color = yellow_green
                if Button2.check(mouse):
                    Button2.color = pale_green
                else:
                    Button2.color = yellow_green
                if Button3.check(mouse):
                    Button3.color = pale_green
                else:
                    Button3.color = yellow_green
                if Button4.check(mouse):
                    Button4.color = pale_green
                else:
                    Button4.color = yellow_green
                if Button5.check(mouse):
                    Button5.color = pale_green
                else:
                    Button5.color = yellow_green
                if Button6.check(mouse):
                    Button6.color = pale_green
                else:
                    Button6.color = yellow_green

    pygame.quit()

def about_me():
    '''
    Display the about me screen
    '''
    def text_display():
        '''
        Display a text on the screen
        '''
        font1 = pygame.font.SysFont("Consolas", 40)
        font2 = pygame.font.SysFont("Consolas", 20)
        text1 = font1.render('Hello! ', True, (0, 0, 0))
        text2 = font2.render('Here is a game - Crossy Road, a turtle version.', False, (0, 0, 0))
        text3 = font2.render('I chose this game to create because I have always', False, (0, 0, 0))
        text4 = font2.render('associated it with my childhood. Working on it', False, (0, 0, 0))
        text5 = font2.render('allowed me to remember this carefree time and gave', False, (0, 0, 0))
        text6 = font2.render('me a lot of fun. Enjoy!', False, (0, 0, 0))
        text7 = font2.render('Author: Małgorzata Kowalczyk', True, (0,0,0))
        screen2.blit(text1, (220, 50))
        screen2.blit(text2, (10, 200))
        screen2.blit(text3, (10, 250))
        screen2.blit(text4, (10, 300))
        screen2.blit(text5, (10, 350))
        screen2.blit(text6, (10, 400))
        screen2.blit(text7, (10, 600))
    def redraw_screen_me():
        '''
        Refresh the screen
        '''
        Button1.draw(screen2, dark_green)

    pygame.init()
    SCREEN_WIDTH = 590
    SCREEN_HEIGHT = 700
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen2 = pygame.display.set_mode(SCREEN_SIZE)
    pale_green = (152, 251, 152)
    yellow_green = (154, 205, 50)
    dark_green = (0, 100, 0)
    clock = pygame.time.Clock()
    screen2.fill(pale_green)
    pygame.display.flip()
    Button1 = Button(yellow_green, 400, 620, 150, 40, "Exit")

    running = True
    while running:
        redraw_screen_me()
        text_display()
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
                    menu()
            if event.type == pygame.MOUSEMOTION:
                if Button1.check(mouse):
                    Button1.color = pale_green
                else:
                    Button1.color = yellow_green
    pygame.quit()


def instruction():
    '''
    Display an instruction
    '''
    def load_image(name, use_color_key=False):
        '''
        Upload an image and convert it to a surface.
        :param name: (str) name of image
        :param use_color_key: (bool) if the useColorKey flag is set to True, the color contained in the pixel (0,0)
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

    def redraw_screen_instruction():
        '''
        Refresh the screen
        '''
        Button1.draw(screen3, dark_green)

    def text_display():
        '''
        Display a text on the screen
        '''
        font1 = pygame.font.SysFont("Consolas", 40)
        font2 = pygame.font.SysFont("Consolas", 20)
        text1 = font1.render('Instruction ', True, (0, 0, 0))
        text2 = font2.render('The game is about running a turtle through a busy', False, (0, 0, 0))
        text3 = font2.render('street who cares about money. Thanks to them, he', False, (0, 0, 0))
        text4 = font2.render('scores points. He has to watch out for speeding cars,', False, (0, 0, 0))
        text5 = font2.render('avoid them to collect as many of money as possible.', False, (0, 0, 0))
        text6 = font2.render('Moving: ', False, (0, 0, 0))
        screen3.blit(text1, (180, 50))
        screen3.blit(text2, (10, 200))
        screen3.blit(text3, (10, 250))
        screen3.blit(text4, (10, 300))
        screen3.blit(text5, (10, 350))
        screen3.blit(text6, (10, 500))

    pygame.init()
    SCREEN_WIDTH = 590
    SCREEN_HEIGHT = 700
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen3 = pygame.display.set_mode(SCREEN_SIZE)
    pale_green = (152, 251, 152)
    yellow_green = (154, 205, 50)
    dark_green = (0, 100, 0)
    clock = pygame.time.Clock()
    screen3.fill(pale_green)
    pygame.display.flip()
    Button1 = Button(yellow_green, 400, 620, 150, 40, "Exit")
    keys = load_image('keycap.jpg', True)
    running = True
    while running:
        redraw_screen_instruction()
        text_display()
        screen3.blit(keys, (120, 430))
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
                    menu()
            if event.type == pygame.MOUSEMOTION:
                if Button1.check(mouse):
                    Button1.color = pale_green
                else:
                    Button1.color = yellow_green
    pygame.quit()

menu()

