import math
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, radius=PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        self.timer -= dt

        self.rotate()

        keys = pygame.key.get_pressed()
        b1, b2, b3 = pygame.mouse.get_pressed(num_buttons=3)
#
#        if keys[pygame.K_a]:
#            self.rotate(-dt)
#        if keys[pygame.K_d]:
#            self.rotate(dt)
        if keys[pygame.K_s]:
           self.move(-dt)
        if keys[pygame.K_w]:
           self.move(dt)
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
        print(f"mousey: {mousey}\n mousex: {mousex}")
        angle = math.atan2(mousey, mousex) * (180/math.pi)
        if angle < 0:
            angle += 360
        angle -= 90
        self.rotation = angle
#        self.rotation += PLAYER_TURN_SPEED * dt
#        self.rotation %= 360

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN
    