import math
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, radius=PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.ship_img = pygame.image.load("./images/ship_small.png")
        self.ship_rect = self.ship_img.get_rect()
        self.angle = 0
    
    def draw(self, screen):
        self.ship_rect.center = self.position
        rotated_ship_img = pygame.transform.rotate(self.ship_img, self.angle)
        new_ship_rect = rotated_ship_img.get_rect(center = self.ship_img.get_rect(center = self.position).center)
        screen.blit(rotated_ship_img, new_ship_rect)

    def update(self, dt):
        self.timer -= dt

        self.rotate()

        keys = pygame.key.get_pressed()
        b1, b2, b3 = pygame.mouse.get_pressed(num_buttons=3)
        
        if keys[pygame.K_a]:
            self.move_x(-dt)
        if keys[pygame.K_d]:
            self.move_x(dt)
        if keys[pygame.K_s]:
           self.move_y(-dt)
        if keys[pygame.K_w]:
           self.move_y(dt)
        if b1 == True or keys[pygame.K_SPACE]:
            self.shoot()

    def rotate(self):
        mousex, mousey = pygame.mouse.get_pos()
        mousey -= self.position.y
        mousex -= self.position.x
        if mousey <= 1 and mousey >= 0 and mousex <= 1 and mousex >= 0:
            mousey = 0
        if mousex <= 1 and mousex >= 0 and mousey <= 1 and mousey >= 0:
            mousex = 0
        if mousey >= -1 and mousey <= 0 and mousex >= -1 and mousex <= 0:
            mousey = 0
        if mousex >= -1 and mousey <= 0 and mousey >= -1 and mousey <= 0:
            mousex = 0
        angle = math.atan2(mousey, mousex) * (180/math.pi)
        self.angle = -angle
        if angle < 0:
            angle += 360
        angle -= 90
        self.rotation = angle
#        self.rotation += PLAYER_TURN_SPEED * dt
#        self.rotation %= 360

    def move_y(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def move_x(self, dt):
        horizontal = pygame.Vector2(1, 0).rotate(self.rotation)
        self.position += horizontal * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN
    