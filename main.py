import pygame
import sys
from random import randint

pygame.init()

class Body(pygame.sprite.Sprite):
    def __init__(self, size=(100, 100), x=0, y=0, filename=None):
        super().__init__()
        self.maxprotection = 10
        self.protection = self.maxprotection
        self.file = filename
        self.image = pygame.image.load(self.file)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_object(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Cannon(Body):
    def __init__(self, size=(100, 100), x=0, y=0, rot_speed=1, filename=None):
        super().__init__(size, x, y, filename)
        self.angle = 0
        self.mvector = pygame.math.Vector2(0, -1)
        self.image_copy = self.image
        self.copy_rect = self.image_copy.get_rect()
        self.rotate = rot_speed
        self.controller = (0, 0)
        self.center = [x, int(y + self.rect.height/8)]
        self.k = self.rect.y - self.center[1]

    def rotate_ob(self, direct):
        self.angle += self.rotate * direct
        self.mvector = self.mvector.rotate(self.rotate * direct)
        self.image_copy = pygame.transform.rotate(self.image, self.angle)

    def check_angle(self):
        mx, my = pygame.mouse.get_pos()
        mousev = pygame.math.Vector2(self.center[0] - mx, my - self.center[1]).as_polar()
        mangle = mousev[1] - self.mvector.as_polar()[1]
        if (-self.rotate) <= mangle <= self.rotate:
            self.angle += mangle
            self.mvector = self.mvector.rotate(mangle)
            self.image_copy = pygame.transform.rotate(self.image, self.angle)
        elif mangle < self.rotate:
            self.rotate_ob(-1)
        elif mangle > self.rotate:
            self.rotate_ob(1)
        else:
            pass

    def draw_copy(self):
        self.controller = (self.rect.x - self.copy_rect.width/2 - self.mvector.x*6, self.rect.y - self.copy_rect.height/2 + self.mvector.y*6)
        self.copy_rect = self.image_copy.get_rect()
        screen.blit(self.image_copy, self.controller)

    def shoot(self, size, filename):
        bullet = Bullet(size, self.center[0] - self.mvector.x*30, self.center[1] + self.mvector.y*30, 10, self.angle, filename)
        bullets.add(bullet)

class Bullet(Body):
    def __init__(self, size=(20, 50), x=0, y=0, speed=1, angle=0, filename=None):
        super().__init__(size, x, y, filename)
        self.x = x
        self.y = y
        self.move_vector = pygame.math.Vector2(0, -1) * speed
        self.move_vector = self.move_vector.rotate(angle)
        self.image = pygame.transform.rotate(self.image, angle)

    def move_bullet(self):
        self.rect.x -= self.move_vector.x
        self.rect.y += self.move_vector.y

def move_ship(x, y):
    player.rect.x += x
    tower.rect.x += x
    tower.center[0] += x
    player.rect.y += y
    tower.rect.y += y
    tower.center[1] += y

def check_ship(hit=False):
    if hit and player.protection/player.maxprotection < 0.7:
        if 0.4 < player.protection/player.maxprotection < 0.7:
            file = 'image\Body_damaged1.png'
            file2 = 'image\Cannon_damaged1.png'
        elif player.protection/player.maxprotection <= 0.4:
            file = 'image\Body_damaged2.png'
            file2 = 'image\Cannon_damaged2.png'
        player.image = pygame.image.load(file)
        player.image = pygame.transform.scale(player.image, sizes[0])
        tower.image = pygame.image.load(file2)
        tower.image = pygame.transform.scale(tower.image, sizes[1])
        tower.image_copy = pygame.transform.rotate(tower.image, tower.angle)

def check_bullets():
    for bullet in bullets:
        bullet.move_bullet()
        bullet.draw_object()
        if bullet.x < -100 or bullet.x > s_size[0] + 100 or bullet.y < -100 or bullet.y > s_size[1] + 100:
            bullet.kill()
            bullet = None
    for asteroid in asteroids:
        asteroid.move_bullet()
        asteroid.draw_object()
        if asteroid.x < -100 or asteroid.x > s_size[0] + 100 or asteroid.y < -300 or asteroid.y > s_size[1] + 100:
            asteroid.kill()

def check_effects():
    for effect in effects:
        if effect.fade:
            effect.fading()
        elif effect.ap:
            effect.appearing()

def spawn_asteroid():
    image = ast_pics[randint(0, 4)]
    x = randint(0, s_size[0])
    angle = int(180 + (s_size[0]/2 - x)/s_size[0]*45)
    move_angle = randint(angle - 10, angle + 10)
    speed = randint(2, 6)
    size = (randint(sizes[3][0] - 50, sizes[3][0] + 50), randint(sizes[3][1] - 50, sizes[3][1] + 50))
    asteroid = Bullet(size, x, -200, speed, move_angle, image)
    asteroid.add(asteroids)

def set_sizes():
    org_size = pygame.image.load('image\Body.png').get_size()
    org_size2 = pygame.image.load('image\Cannon.png').get_size()
    org_size3 = pygame.image.load('image\Bullet.png').get_size()
    org_size4 = pygame.image.load('image\Ast1.png').get_size()
    p_w = int(s_size[0] * 0.25)
    resize = p_w / org_size[0]
    p_h = int(org_size[1] * resize)
    t_w = int(org_size2[0] * resize)
    t_h = int(org_size2[1] * resize)
    b_w = int(org_size3[0] * resize)
    b_h = int(org_size3[1] * resize)
    ast_w = int(org_size4[0] * resize)
    ast_h = int(org_size4[1] * resize)
    return ((p_w, p_h), (t_w, t_h), (b_w, b_h), (ast_w, ast_h))

s_size = (700, 700)
sizes = set_sizes()
fps = 60
p_x, p_y = (s_size[0] - sizes[0][0]) / 2, s_size[1] - 50 - sizes[0][1]
t_x, t_y = p_x + sizes[0][0]/2, p_y + sizes[0][1] * 0.33

screen = pygame.display.set_mode(s_size)
pygame.display.set_caption('Игра')
clock = pygame.time.Clock()

ast_pics = ['image\Ast1.png', 'image\Ast2.png', 'image\Ast3.png', 'image\Ast4.png', 'image\Ast5.png']
ast_delayer = 0

player = Body(sizes[0], p_x, p_y, 'image\Body.png')
tower = Cannon(sizes[1], t_x, t_y, 4, 'image\Cannon.png')

bullets = pygame.sprite.Group()
bullet_delayer = 0

asteroids = pygame.sprite.Group()
effects = list()

background = pygame.image.load('image\Background.png')
y = randint(0, 1000)
damaged = 0
not_over = True

while not_over:
    if player.protection <= 0:
        not_over = False
    screen.blit(background, (0, -y))
    tower.check_angle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.rect.y > 200:
        move_ship(0, -1)
    if keys[pygame.K_s] and player.rect.y < s_size[1] - player.rect.height:
        move_ship(0, 1)
    if keys[pygame.K_a] and player.rect.x > 0:
        move_ship(-1, 0)
    if keys[pygame.K_d] and player.rect.x < s_size[0] - player.rect.width:
        move_ship(1, 0)
    mousekeys = pygame.mouse.get_pressed()
    if mousekeys[0]:
        if bullet_delayer == 0:
            tower.shoot(sizes[2], 'image\Bullet.png')
            bullet_delayer = 5
        bullet_delayer -= 1
    if len(asteroids.sprites()) < 10:
        if ast_delayer <= 0:
            spawn_asteroid()
            ast_delayer = randint(0, 30)
        ast_delayer -= 1
    collided = pygame.sprite.groupcollide(bullets, asteroids, True, True)
    hits = pygame.sprite.spritecollide(player, asteroids, True)
    for h in hits:
        h.kill()
        player.protection -= 1
        check_ship(True)
    player.draw_object()
    check_bullets()
    tower.draw_copy()

    clock.tick(fps)
    pygame.display.update()