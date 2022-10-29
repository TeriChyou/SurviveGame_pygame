from email.header import Header
import pygame
import random


#constant setup

FPS = 60
WIDTH = 1660
HEIGHT = 900

#initialize and setup for the games

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #x,y = width, height
clock = pygame.time.Clock()
pygame.display.set_caption("NTHU Survival") #Game screen title setup


#boolean or other setup

running = True

## sprites (Objects that display on the screen)
#Player(ZhiDai)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32)) # sprite elements
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect() # sprite location fixed
        self.rect.center = ((WIDTH / 2, HEIGHT / 2))
        self.speedx = 8
        self.speedy = 8
    
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

all_sprites = pygame.sprite.Group() #create the player at first
player = Player()
all_sprites.add(player)


class Ayu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32)) # sprite elements
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect() # sprite location fixed
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = 2
        self.speedy = 2

    def update(self):
        if self.rect.x > player.rect.x:
            self.rect.x = self.rect.x - self.speedx
        else:
            self.rect.x = self.rect.x + self.speedx
        
        if self.rect.y > player.rect.y:
            self.rect.y = self.rect.y - self.speedy
        else:
            self.rect.y = self.rect.y + self.speedy

for i in range(8):
    ayu = Ayu() # create entity
    all_sprites.add(ayu) # put into the sprite list


# Game Loop

while running:
    clock.tick(FPS)
    
    #get import
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #game update
    
    all_sprites.update() # update the sprites


    #screen display
    
    screen.fill((255, 0, 255)) #R,G,B

    all_sprites.draw(screen)

    pygame.display.update() #put to the last unless need to cal for var next loop

pygame.quit()