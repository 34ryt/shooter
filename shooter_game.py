#Создай собственный Шутер!
# импорт модулей
from pygame import *
from random import randint
from time import time as tm
mixer.init()
# классы
class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_speed, pl_w, pl_h, pl_x, pl_y):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (pl_w, pl_h))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
    def shoot(self):
        pass
    def fire(self):
        bullet = Bullet('bullet.png', 10, 10, 30, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
killed = 0
lost = 0
lives = 3
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lives
        global lost
        if self.rect.y == 500:
            self.rect.y = -10
            self.rect.x = randint(0, 635)
            lost += 1
            lives -= 1
            skip = mixer.Sound('skipped.ogg')
            skip.play()
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lives
        if self.rect.y == 500:
            self.rect.y = -10
            self.rect.x = randint(0, 635)
player = Player('rocket.png', 10, 65, 65, 50, 420)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(1, 5), 80, 65, randint(0, 635), -10)
    monsters.add(monster)
for d in range(3):
    asteroid = Asteroid('asteroid.png', randint(1, 3), 80, 65, randint(0, 635), -10)
    asteroids.add(asteroid)
# переменные
num_fire = 0
rel_time = False
# создание окна
window = display.set_mode((700, 500))
display.set_caption('Space Invaders')
# создание сцены
background = transform.scale(image.load('galaxy.png'), (700, 500))
# создание музыки mixer
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
mixer.music.play()
# ИЦ
font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 70)
font3 = font.SysFont('Arial', 35)
fps = 60
speed = 10
clock = time.Clock()
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE and not(finish):
            if num_fire < 5 and not(rel_time):
                player.fire()
                fire.play()
                num_fire += 1
            if num_fire >= 5 and not(rel_time):
                rel_time = True
                wait = tm()
    if finish != True:
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        window.blit(background, (0, 0))
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        sprites_list1 = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list2 = sprite.spritecollide(player, monsters, True)
        sprites_list3 = sprite.spritecollide(player, asteroids, True)
        for b in sprites_list1:
            killed += 1
            monster = Enemy('ufo.png', randint(1, 5), 80, 65, randint(0, 635), -10)
            monsters.add(monster)
        if killed >= 10:
            you_win = font2.render('YOU WIN!', True, (255, 255, 255))
            window.blit(you_win, (250, 230))
            finish = True
        if len(sprites_list2) >= 1 or len(sprites_list3) >= 1:
            lives -= 1
        elif lives <= 0:
                you_lost = font2.render('YOU LOSE!', True, (255, 255, 255))
                window.blit(you_lost, (250, 230))
                finish = True
        kill_l = font1.render('KILLED: ' + str(killed), 1, (255, 255, 255))
        lost_l = font1.render('LOST: ' + str(lost), 1, (255, 255, 255))
        life_l = font1.render('LIVES: ' + str(lives), 1, (255, 255, 255))
        if lives == 3:
            life_l = font1.render('LIVES: ' + str(lives), 1, (40, 255, 15))
        elif lives == 2:
            life_l = font1.render('LIVES: ' + str(lives), 1, (241, 255, 15))
        else:
            life_l = font1.render('LIVES: ' + str(lives), 1, (250, 5, 0))
        window.blit(kill_l, (20, 20))
        window.blit(lost_l, (20, 40))
        window.blit(life_l, (20, 60))
        if rel_time == True:
            wait_again = tm()
            if wait_again - wait < 3:
                wait_l = font3.render('WAIT, RELOAD!', True, (255, 255, 255))
                window.blit(wait_l, (250, 450))
            else:
                num_fire = 0
                rel_time = False
    display.update()
    clock.tick(fps)