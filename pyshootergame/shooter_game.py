#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

font.init()

font1 = font.SysFont("Arial", 80)
win = font1.render("YOU WIN!", True, (255,255,255))
lose = font1.render("YOU LOSE!", True, (180,0,0))
font2 = font.SysFont("Arial", 36) 


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_asteroids = "asteroid.png"

score = 0
lost = 0
goal = 10 #how many ships need to be shot down to win
lost = 0 #ships missed
max_lost = 3 #lose if you miss that many
life = 3

num_fire = 0
real_time = False

#parent class for sprites
class GameSprite(sprite.Sprite):
   #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
       super().__init__()
       # each sprite must store an image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # each sprite must store the rect property it is inscribed in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            

win_width = 700
win_height = 500
display.set_caption("shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height-100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,6):
    asteroid = Asteroid(img_asteroids, randint(80, win_width-80), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)


bullets = sprite.Group()

finish = False

run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        #event of pressing the spacebar - the sprite shoots
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               if num_fire < 5 and real_time == False:
                   num_fire = num_fire + 1
                   fire_sound.play()
                   ship.fire()

               if num_fire >= 5 and real_time == False:
                   last_time = timer()
                   real_time = True


    #the game itself: actions of sprites, checking the rules of the game, redrawing
    if not finish:
        #update the background
        window.blit(background,(0,0))


        #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        #update them in a new location in each loop iteration
        ship.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)

        if real_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render("wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260,480))
            else:
                num_fire = 0
                real_time = False     
                   #check for a collision between a bullet and monsters (both monster and bullet disappear upon a touch)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #this loop will repeat as many times as the number of monsters hit
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters,True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        #possible lose: missed too many monsters or the character collided with an enemy
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True #lose, set the background and no longer control the sprites.
            window.blit(lose, (200, 200))


        #win checking: how many points scored?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font2.render("life: " + str(life), 1, (255, 255, 255))
        window.blit(text_life, (10, 80))

        display.update()
      
    time.delay(50)