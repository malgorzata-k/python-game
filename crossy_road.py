import pygame
from pygame.locals import *
import os.path
import time
import random

SCREEN_WIDTH = 580
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


def load_image(name, use_color_key=False):
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if use_color_key is True:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image


def score():
    global points
    if car1.velocity > 0:
        car1.velocity += 1
    else:
        car1.velocity -= 1
    if car2.velocity > 0:
        car2.velocity += 1
    else:
        car2.velocity -= 1
    if car3.velocity > 0:
        car3.velocity += 1
    else:
        car3.velocity -= 1

    points += 1


def score_display():
    score_text = font_score.render('Score: ' + str(points), True, (0, 0, 0))
    screen.blit(score_text, (20, 660))


def get_money():
    for coin in money:
        if not coin.visible:
            coin.kill()
        else:
            if not coin.alive():
                moneySprite.add(coin)


def delete_turtle():
    global turtle
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = SCREEN_WIDTH / 2
        self.y = 30
        self.velocity = 2
        self.width = 90
        self.height = 60
        self.turtle1 = load_image("turtle_r1.png", True)
        self.turtle2 = load_image("turtle_l1.png", True)
        self.turtle1 = pygame.transform.scale(self.turtle1, (self.width, self.height))
        self.turtle2 = pygame.transform.scale(self.turtle2, (self.width, self.height))
        self.image = self.turtle1
        self.rect = self.image.get_rect()

    def update(self):
        self.move()
        self.correction()
        self.check_collision()
        self.rect.center = (self.x, self.y)

    def move(self):
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
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2
        elif self.x + self.width / 2 > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width / 2
        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
        elif self.y + self.height / 2 > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.width / 2

    def check_collision(self):
        if pygame.sprite.groupcollide(carSprite, turtleSprite, True, True):
            explosion.explode(self.x, self.y)


class Car(pygame.sprite.Sprite):
    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        if number == 1:
            self.y = 148
            self.image = load_image('car1.png', True)
            self.velocity = -1.2
        elif number == 2:
            self.y = 230
            self.image = load_image('car2.png', True)
            self.velocity = 1.5
        else:
            self.y = 315
            self.image = load_image("car3.png", True)
            self.velocity = -2

        self.x = random.randint(100, 400)
        self.width = 95
        self.height = 55
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        self.move()
        self.rect.center = (self.x, self.y)

    def move(self):
        self.x += self.velocity
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2
            self.velocity *= -1
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.x + self.width / 2 > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width / 2
            self.velocity *= -1
            self.image = pygame.transform.rotate(self.image, 180)


class Screen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = load_image("bg1.png")
        self.image1 = pygame.transform.scale(self.image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image = self.image1
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)


class Money(pygame.sprite.Sprite):
    def __init__(self, number):
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

        self.x = SCREEN_WIDTH / 2
        self.width = 70
        self.height = 55
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.visible:
            self.collision()
            self.rect.center = (self.x, self.y)

    def collision(self):
        global points, turtle
        money_touch = pygame.sprite.spritecollide(self, turtleSprite, False)
        if money_touch:
            self.visible = False
            if self.number == 1:
                coin2.visible = True
                score()
            else:
                coin1.visible = True


class Explosion(object):
    def __init__(self):
        self.gif_of_explosion = 1
        self.width = 90
        self.height = 90
        self.image = load_image('exp' + str(self.gif_of_explosion) + '.png', True)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def explode(self, x, y):
        delete_turtle()
        while self.gif_of_explosion < 6:
            self.image = load_image('exp' + str(self.gif_of_explosion) + '.png', True)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            screen.blit(self.image, (x, y))
            pygame.display.update()

            self.gif_of_explosion += 1
            time.sleep(0.2)


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Crossy Road")
clock = pygame.time.Clock()


points = 0
font_score = pygame.font.SysFont("Calibri", 40)
background = Screen()
screenSprite = pygame.sprite.Group()
screenSprite.add(background)

turtle = Turtle()
turtleSprite = pygame.sprite.Group()
turtleSprite.add(turtle)

car1 = Car(1)
car2 = Car(2)
car3 = Car(3)
carSprite = pygame.sprite.Group()
carSprite.add(car1, car2, car3)

coin1 = Money(1)
coin2 = Money(2)
moneySprite = pygame.sprite.Group()
moneySprite.add(coin1, coin2)
money = [coin1, coin2]

explosion = Explosion()

running = True
while running:
    clock.tick(65)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screenSprite.draw(screen)
    score_display()
    get_money()

    carSprite.draw(screen)
    turtleSprite.draw(screen)
    moneySprite.draw(screen)

    carSprite.update()
    turtleSprite.update()
    moneySprite.update()
    screenSprite.update()
    pygame.display.update()

pygame.quit()
