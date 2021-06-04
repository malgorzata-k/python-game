import pygame
from pygame.locals import *
import os.path
import random
import time
import pickle

pale_green = (152, 251, 152)
yellow_green = (154, 205, 50)
dark_green = (0, 100, 0)
light_green = (128, 220, 116)
olive = (128,128,0)
black = (0, 0, 0)
white = (255, 255, 255)


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
            text = font.render(self.text, True, black)
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
            self.img1 = pygame.transform.scale(self.img1, (screen_width, screen_height))
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
        Button7.draw(screen, dark_green)

    def text_display():
        '''
        Display the text on the screen
        '''
        font = pygame.font.SysFont("Consolas", 20)
        text = font.render('Set difficulty level: ', False, black)
        screen.blit(text, (320, 350))

    def mode_display(n):
        '''
        Display the mode on the screen
        :param n: (int) a number which decide about a mode of game
        '''
        font = pygame.font.SysFont("Consolas", 15)
        if n == 1:
            text = font.render('You chose easier version.', False, black)
        else:
            text = font.render('You chose more difficult version.', False, black)
        screen.blit(text, (300, 450))

    pygame.init()
    screen_width = 590
    screen_height = 700
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    startFX = load_sound("start.wav")

    background = Screen()
    screenSprite = pygame.sprite.Group()
    screenSprite.add(background)
    Button1 = Button(yellow_green, 50, 350, 150, 40, "Start")
    Button2 = Button(yellow_green, 50, 400, 150, 40, "Instruction")
    Button3 = Button(yellow_green, 50, 450, 150, 40, "About me")
    Button4 = Button(yellow_green, 50, 550, 150, 40, "Exit")
    Button5 = Button(yellow_green, 330, 400, 90, 30, "Easy")
    Button6 = Button(yellow_green, 450, 400, 90, 30, "Hard")
    Button7 = Button(yellow_green, 50, 500, 150, 40, "Leaderboard")

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
                if Button5.check(mouse):
                    mode = 1
                    pygame.draw.rect(screen, light_green, pygame.Rect(290, 440, 300, 30))
                    pygame.display.flip()
                    mode_display(mode)
                if Button6.check(mouse):
                    mode = 2
                    pygame.draw.rect(screen, light_green, pygame.Rect(290, 440, 300, 30))
                    pygame.display.flip()
                    mode_display(mode)
                if Button1.check(mouse):
                    global points
                    points = 0
                    try:
                        mode
                    except NameError:
                        mode = None
                    if mode is None:
                        startFX.play()
                        my_game(1)
                    else:
                        startFX.play()
                        my_game(mode)
                if Button4.check(mouse):
                    pygame.quit()
                    quit()
                if Button3.check(mouse):
                    about_me()
                if Button2.check(mouse):
                    instruction()
                if Button7.check(mouse):
                    leaderboard()

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
                if Button7.check(mouse):
                    Button7.color = pale_green
                else:
                    Button7.color = yellow_green
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
        text1 = font1.render('Hello! ', True, black)
        text2 = font2.render('Here is a game - Crossy Road, a turtle version.', False, black)
        text3 = font2.render('I chose this game to create because I have always', False, black)
        text4 = font2.render('associated it with my childhood. Working on it', False, black)
        text5 = font2.render('allowed me to remember this carefree time and gave', False, black)
        text6 = font2.render('me a lot of fun. Enjoy!', False, black)
        text7 = font2.render('Author: Małgorzata Kowalczyk', True, black)
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
    screen_width = 590
    screen_height = 700
    screen_size = (screen_width, screen_height)
    screen2 = pygame.display.set_mode(screen_size)
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
        text1 = font1.render('Instruction ', True, black)
        text2 = font2.render('The game is about running a turtle through a busy', False, black)
        text3 = font2.render('street who cares about money. Thanks to them, he', False, black)
        text4 = font2.render('scores points. He has to watch out for speeding cars,', False, black)
        text5 = font2.render('avoid them to collect as many of money as possible.', False, black)
        text6 = font2.render('Moving: ', False, black)
        screen3.blit(text1, (180, 50))
        screen3.blit(text2, (10, 200))
        screen3.blit(text3, (10, 250))
        screen3.blit(text4, (10, 300))
        screen3.blit(text5, (10, 350))
        screen3.blit(text6, (10, 500))

    pygame.init()
    screen_width = 590
    screen_height = 700
    screen_size = (screen_width, screen_height)
    screen3 = pygame.display.set_mode(screen_size)
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

def leaderboard():
    '''
    Display the leaderboard screen
    '''
    def show_best_scores():
        '''
        Display the best scores
        '''
        font = pygame.font.SysFont("Consolas", 25)
        with open('high_score_e1.dat', 'rb') as file:
            last_high1 = pickle.load(file)
        with open('high_score_e2.dat', 'rb') as file:
            second_high1 = pickle.load(file)
        with open('high_score_e3.dat', 'rb') as file:
            third_high1 = pickle.load(file)
        with open('high_score_h1.dat', 'rb') as file:
            last_high2 = pickle.load(file)
        with open('high_score_h2.dat', 'rb') as file:
            second_high2 = pickle.load(file)
        with open('high_score_h3.dat', 'rb') as file:
            third_high2 = pickle.load(file)
        text1 = font.render('Best score in easier mode: {}'.format(last_high1), True, white)
        text2 = font.render('2-nd best score in easier mode: {}'.format(second_high1), True, white)
        text3 = font.render('3-rd best score in easier mode: {}'.format(third_high1), True, white)
        text4 = font.render('Best score in harder mode: {}'.format(last_high2), True, white)
        text5 = font.render('2-nd best score in harder mode: {}'.format(second_high2), True, white)
        text6 = font.render('3-rd best score in harder mode: {}'.format(third_high2), True, white)
        pygame.draw.rect(screen, black, pygame.Rect(40, 185, 510, 145))
        pygame.draw.rect(screen, black, pygame.Rect(40, 385, 510, 145))

        pygame.draw.rect(screen, olive, pygame.Rect(45, 190, 500, 135))
        pygame.draw.rect(screen, olive, pygame.Rect(45, 390, 500, 135))
        screen.blit(text1, (65, 200))
        screen.blit(text2, (65, 250))
        screen.blit(text3, (65, 300))
        screen.blit(text4, (65, 400))
        screen.blit(text5, (65, 450))
        screen.blit(text6, (65, 500))

    pygame.init()
    screen_width = 590
    screen_height = 700
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    screen.fill(pale_green)
    pygame.display.flip()
    Button1 = Button(yellow_green, 400, 620, 150, 40, "Exit")
    running = True
    while running:
        Button1.draw(screen, dark_green)
        show_best_scores()
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

def my_game(mode=1):
    '''
    Start a game
    :param mode: (int) a value that determines the difficulty of the game
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

    def load_sound(name):
        '''
        Load audio files
        :param name: (str) name of file
        :return: sound
        '''
        fullname = os.path.join("sound", name)
        sound = pygame.mixer.Sound(fullname)
        return sound

    def score():
        '''
        Count points and add speed
        :return: score
        '''
        global points
        if car1.velocity > 0:
            car1.velocity += 0.3
        else:
            car1.velocity -= 0.3
        if car2.velocity > 0:
            car2.velocity += 0.3
        else:
            car2.velocity -= 0.3
        if car3.velocity > 0:
            car3.velocity += 0.3
        else:
            car3.velocity -= 0.3

        points += 1

    def score_display():
        '''
        Display the number of points scored on the screen
        '''
        score_text = font_score.render(f'Score: {str(points)}', True, black)
        screen.blit(score_text, (20, 660))

    def high_score(high_score):
        '''
        Display the high score
        :param high_score: (tuple) name of file and opening mode
        '''
        result = font_score.render(f'High score: {int(high_score)}', True, black)
        screen.blit(result, (200, 660))

    def get_money():
        '''
        Get money by turtle
        '''
        for coin in money:
            if not coin.visible:
                coin.kill()
            else:
                if not coin.alive():
                    moneySprite.add(coin)

    def delete_turtle():
        '''
        Remove the turtle and other things from the screen when you lose
        '''
        if mode == 1:
            with open('high_score_e1.dat', 'rb') as file:
                last_high = pickle.load(file)
                if points > last_high:
                    with open('high_score_e1.dat', 'wb') as f:
                        pickle.dump(points, f)
                else:
                    with open('high_score_e2.dat', 'rb') as file:
                        last_high = pickle.load(file)
                        if points > last_high:
                            with open('high_score_e2.dat', 'wb') as f:
                                pickle.dump(points, f)
                        else:
                            with open('high_score_e3.dat', 'rb') as file:
                                last_high = pickle.load(file)
                                if points > last_high:
                                    with open('high_score_e3.dat', 'wb') as f:
                                        pickle.dump(points, f)
        else:
            with open('high_score_h1.dat', 'rb') as file:
                last_high = pickle.load(file)
                if points > last_high:
                    with open('high_score_h1.dat', 'wb') as f:
                        pickle.dump(points, f)
                else:
                    with open('high_score_h2.dat', 'rb') as file:
                        last_high = pickle.load(file)
                        if points > last_high:
                            with open('high_score_h2.dat', 'wb') as f:
                                pickle.dump(points, f)
                        else:
                            with open('high_score_h3.dat', 'rb') as file:
                                last_high = pickle.load(file)
                                if points > last_high:
                                    with open('high_score_h3.dat', 'wb') as f:
                                        pickle.dump(points, f)

        turtle.kill()
        screenSprite.draw(screen)
        turtleSprite.draw(screen)
        moneySprite.draw(screen)

        screenSprite.update()
        turtleSprite.update()
        moneySprite.update()
        pygame.display.update()

        carSprite.empty()
        moneySprite.empty()
        money.clear()

    class Turtle(pygame.sprite.Sprite):
        '''
        A class to represent a turtle
        '''
        def __init__(self):
            '''
            Initialize the turtle's class base
            '''
            pygame.sprite.Sprite.__init__(self)
            self.x = screen_width / 2
            self.y = 30
            self.velocity = 2
            self.width = 60
            self.height = 40
            self.turtle1 = load_image("turtle_r1.png", True)
            self.turtle2 = load_image("turtle_l1.png", True)
            self.turtle1 = pygame.transform.scale(self.turtle1, (self.width, self.height))
            self.turtle2 = pygame.transform.scale(self.turtle2, (self.width, self.height))
            self.image = self.turtle1
            self.rect = self.image.get_rect()

        def update(self):
            '''
            Perform the actions possible for the turtle
            '''
            self.move()
            self.correction()
            self.check_collision()
            self.rect.center = (self.x, self.y)

        def move(self):
            '''
            Move the turtle around the screen
            '''
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.x += self.velocity
                self.image = self.turtle1
            elif keys[pygame.K_LEFT]:
                self.x -= self.velocity
                self.image = self.turtle2
            if keys[pygame.K_DOWN]:
                self.y += self.velocity
            elif keys[pygame.K_UP]:
                self.y -= self.velocity

        def correction(self):
            '''
            Correct movement when the turtle goes off-screen
            '''
            if self.x - self.width / 2 < 0:
                self.x = self.width / 2
            elif self.x + self.width / 2 > screen_width:
                self.x = screen_width - self.width / 2
            if self.y - self.height / 2 < 0:
                self.y = self.height / 2
            elif self.y + self.height / 2 > screen_height:
                self.y = screen_height - self.width / 2

        def check_collision(self):
            '''
            Check the collision between the turtle and the car
            '''
            if pygame.sprite.groupcollide(carSprite, turtleSprite, True, True):
                explosion.explode(self.x, self.y)

    class Car(pygame.sprite.Sprite):
        '''
        A class to represent a car
        '''
        def __init__(self, number):
            '''
            Initialize the car's class base
            :param number: (int) a number that determines the position and speed of the car
            '''
            pygame.sprite.Sprite.__init__(self)
            if number == 1:
                self.y = 148
                self.image = load_image('car1.png', True)
                self.velocity = -1.2
            elif number == 2:
                self.y = 315
                self.image = load_image('car2.png', True)
                self.velocity = 1.5
            elif number==3:
                self.y = 484
                self.image = load_image("car3.png", True)
                self.velocity = -2
            elif number == 4:
                self.y = 235
                self.image = load_image("car5.png", True)
                self.velocity = 2.2
            else:
                self.y = 394
                self.image = load_image("car4.png", True)
                self.velocity = -1.7

            self.x = random.randint(100, 400)
            self.width = 95
            self.height = 55
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()

        def update(self):
            '''
            Perform the actions possible for the car
            '''
            self.move()
            self.rect.center = (self.x, self.y)

        def move(self):
            '''
            Move a car around the screen
            '''
            self.x += self.velocity
            if self.x - self.width / 2 < 0:
                self.x = self.width / 2
                self.velocity *= -1
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.x + self.width / 2 > screen_width:
                self.x = screen_width - self.width / 2
                self.velocity *= -1
                self.image = pygame.transform.rotate(self.image, 180)

    class Screen(pygame.sprite.Sprite):
        '''
        A class to add a background
        '''
        def __init__(self):
            '''
            Initialize the screen class base
            '''
            pygame.sprite.Sprite.__init__(self)
            self.image1 = load_image("bg1.png")
            self.image1 = pygame.transform.scale(self.image1, (screen_width, screen_height))
            self.image = self.image1
            self.x = 0
            self.y = 0
            self.rect = self.image.get_rect()

        def update(self):
            '''
            Set the background
            '''
            self.rect.topleft = (self.x, self.y)

    class Money(pygame.sprite.Sprite):
        '''
        A class to represent a points
        '''
        def __init__(self, number):
            '''
            Initialize the money class base
            :param number: (int) a number that determines the position of the coin
            '''
            pygame.sprite.Sprite.__init__(self)
            self.number = number

            if self.number == 1:
                self.image = load_image("coin.png", True)
                self.visible = False
                self.y = 50
            else:
                self.image = load_image("coin.png", True)
                self.visible = True
                self.y = 600

            self.x = screen_width / 2
            self.width = 70
            self.height = 55
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()

        def update(self):
            '''
            Perform the actions possible for money
            '''
            if self.visible:
                self.collision()
                self.rect.center = (self.x, self.y)

        def collision(self):
            '''
            Check the collision between the turtle and a coin
            '''
            global points
            money_touch = pygame.sprite.spritecollide(self, turtleSprite, False)
            if money_touch:
                coinFX.play()
                self.visible = False
                if self.number == 1:
                    coin2.visible = True
                    score()
                else:
                    coin1.visible = True

    class Explosion(object):
        '''
        A class to represent a explosion
        '''
        def __init__(self):
            '''
            Initialize the explosion class base
            '''
            self.gif_of_explosion = 1
            self.width = 90
            self.height = 90
            self.image = load_image('exp' + str(self.gif_of_explosion) + '.png', True)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        def explode(self, x, y):
            '''
            Show the explosion at the collision point
            :param x: (int) distance x
            :param y: (int) distance y
            '''
            delete_turtle()
            explodeFX.play()
            while self.gif_of_explosion < 6:
                self.image = load_image('exp' + str(self.gif_of_explosion) + '.png', True)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                screen.blit(self.image, (x, y))
                pygame.display.update()

                self.gif_of_explosion += 1
                time.sleep(0.2)

    def redraw_screen():
        '''
        Refresh the screen
        '''
        Button1.draw(screen, dark_green)

    pygame.init()
    screen_width = 590
    screen_height = 700
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    coinFX = load_sound("coin.wav")
    explodeFX = load_sound("explosion.wav")

    font_score = pygame.font.SysFont("Calibri", 20)
    background = Screen()
    screenSprite = pygame.sprite.Group()
    screenSprite.add(background)

    turtle = Turtle()
    turtleSprite = pygame.sprite.Group()
    turtleSprite.add(turtle)

    if mode == 1:
        car1 = Car(1)
        car2 = Car(2)
        car3 = Car(3)
        carSprite = pygame.sprite.Group()
        carSprite.add(car1, car2, car3)
    else:
        car1 = Car(1)
        car2 = Car(2)
        car3 = Car(3)
        car4 = Car(4)
        car5 = Car(5)
        carSprite = pygame.sprite.Group()
        carSprite.add(car1, car2, car3, car4, car5)

    coin1 = Money(1)
    coin2 = Money(2)
    moneySprite = pygame.sprite.Group()
    moneySprite.add(coin1, coin2)
    money = [coin1, coin2]

    explosion = Explosion()
    pygame.display.flip()
    Button1 = Button(yellow_green, 400, 620, 150, 40, "Exit")
    running = True
    while running:
        redraw_screen()
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button1.check(mouse):
                    menu()
            if event.type == pygame.MOUSEMOTION:
                if Button1.check(mouse):
                    Button1.color = pale_green
                else:
                    Button1.color = yellow_green

        screenSprite.draw(screen)
        score_display()
        if mode == 1:
            high_score(pickle.load(open('high_score_e1.dat', 'rb')))
        else:
            high_score(pickle.load(open('high_score_h1.dat', 'rb')))
        get_money()

        carSprite.draw(screen)
        turtleSprite.draw(screen)
        moneySprite.draw(screen)

        carSprite.update()
        turtleSprite.update()
        moneySprite.update()
        screenSprite.update()

    pygame.quit()

menu()
