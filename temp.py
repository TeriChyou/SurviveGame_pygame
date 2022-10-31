from cProfile import run
from email.header import Header
from email.headerregistry import Group
from inspect import GEN_CLOSED
import pygame
import random
import os # for better importing

### constant setup

##COLORS

BLACK = (0, 0, 0) #R,G,B
WHITE = (255, 255 ,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
AMBER = (255, 191, 0)

##ELEMETS

# CONSTANT
FPS = 60
WIDTH = 1660
HEIGHT = 900

# initial stats

score = 0
fucked = 0

### initialize and setup for the games

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #x,y = width, height
clock = pygame.time.Clock()
pygame.display.set_caption("NTHU Survival") #Game screen title setup

# IMG 
nthu_icon = pygame.image.load(r'Python_Project\pygame_survival\textures\icon\nthu_icon_1.jpg').convert()
background_img = pygame.image.load(r'Python_Project\pygame_survival\textures\background\background_1.png').convert()
zhidai_img = pygame.image.load(r'Python_Project\pygame_survival\textures\char\zhidai.png').convert()
ayu_img = pygame.image.load(r'Python_Project\pygame_survival\textures\mobs\ayu_1.png').convert()
ramen_img = pygame.image.load(r'Python_Project\pygame_survival\textures\weapon\ramen.png').convert()

# FONT

font_name = pygame.font.match_font('arial')
def texting(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

### boolean or other setup

running = True


### Sprites (Objects that display on the screen)
## Player(ZhiDai)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(zhidai_img, (64, 64)) # sprite elements
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # sprite location fixed
        self.radius = 32
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
    
    def shoot(self):
        ramen = Ramen(self.rect.centerx, self.rect.centery)
        all_sprites.add(ramen)
        skills.add(ramen)


## Enemies

# Ayu
class Ayu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ayu_img, (64, 64)) # sprite elements
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # sprite location fixed
        self.radius = 32
        randomNum = random.randrange(1, 4) # Dice for 1 to 4 condition
        if randomNum == 1:
            self.rect.x = random.randrange(-40, -32)
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
        elif randomNum == 2:
            self.rect.x = random.randrange(WIDTH + 32, WIDTH + 40)
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
        elif randomNum == 2:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-40, -32)
        elif randomNum == 4:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(HEIGHT + 32, HEIGHT +40)
        self.speedx = random.randrange(1, 2)
        self.speedy = random.randrange(1, 2)

    def update(self):
        if self.rect.centerx > player.rect.centerx: # movement judge
            self.rect.centerx -= self.speedx 
        else:
            self.rect.centerx += self.speedx 
        
        if self.rect.centery > player.rect.centery:
            self.rect.centery -= self.speedy 
        else:
            self.rect.centery += self.speedy

## Skills

# Ramen(Auto attack)
class Ramen(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ramen_img, (32, 32)) # sprite elements
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # sprite location fixed
        self.radius = 16
        self.rect.centerx = x
        self.rect.centery = y
        randomNum = random.randrange(1, 4) # Dice for 1 to 4 condition
        if randomNum == 1:
            self.speedx = random.randrange(1, 2)
            self.speedy = random.randrange(1, 2)
        elif randomNum == 2:
            self.speedx = random.randrange(1, 2) 
            self.speedy = random.randrange(-2, -1)
        elif randomNum == 3:
            self.speedx = random.randrange(-2, -1) 
            self.speedy = random.randrange(-2, -1)
        elif randomNum == 4:
            self.speedx = random.randrange(-2, -1) 
            self.speedy = random.randrange(1, 2)

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        
        if self.rect.centerx > WIDTH or self.rect.centery > HEIGHT or self.rect.centerx < 0 or self.rect.centery <  0:
            self.kill()

### Sprite Creating Process

all_sprites = pygame.sprite.Group() #create the player at first
players = pygame.sprite.Group()
ayus = pygame.sprite.Group()
skills = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
players.add(player)


for i in range(8):
    ayu = Ayu() # create entity
    all_sprites.add(ayu) # put into the sprite list
    ayus.add(ayu) # put into the ayus list


### Game Loop

while running:
    clock.tick(FPS)

    ##get import
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #should be fixed soon
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    ##game update
    
    all_sprites.update() # update the sprites
    # skills hit enemies
    hits = pygame.sprite.groupcollide(ayus, skills, True, True, pygame.sprite.collide_circle) 
    for hit in hits:
        score += 1
        ayu = Ayu()
        all_sprites.add(ayu)
        ayus.add(ayu)

    
    player_hits = pygame.sprite.groupcollide(players, ayus, False, True, pygame.sprite.collide_circle)
    if player_hits:
        fucked += 1
        ayu = Ayu()
        all_sprites.add(ayu)
        ayus.add(ayu)

    ##screen display
    
    screen.fill(BLACK) 
    screen.blit(background_img, (0,0))

    all_sprites.draw(screen)

    texting(screen, "AYU HAS EATEN " + str(score) + "RAMEN", 32, WIDTH / 2, 10, BLUE)
    texting(screen, "ZhiDai GOT FUCKED BY AYU " + str(fucked) + "TIMES", 32, WIDTH / 2, 48, RED)

    pygame.display.update() #put to the last unless need to cal for var next loop

pygame.quit()