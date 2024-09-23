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
        self.has_left_gun = False
        self.has_right_gun = False
    
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

    def get_nose_position(self):
        # Convert angle from degrees to radians
        angle_radians = math.radians(self.rotation + 90)
        
        # Calculate the X and Y offset for the nose position, ensuring it's offset by the radius
        nose_offset_x = math.cos(angle_radians) * (PLAYER_RADIUS + 4)  # +10 to ensure it's slightly in front
        nose_offset_y = math.sin(angle_radians) * (PLAYER_RADIUS + 4)
        
        # Calculate the final position of the nose based on the player's current position
        nose_position_x = self.position.x + nose_offset_x
        nose_position_y = self.position.y + nose_offset_y
        
        return pygame.Vector2(nose_position_x, nose_position_y)
    
    def get_side_positions(self):
        # Convert angle from degrees to radians
        angle_radians = math.radians(self.rotation + 90)
        
        # Perpendicular angles for the right and left sides
        right_angle_radians = angle_radians + math.pi / 2   # 90 degrees to the right
        left_angle_radians = angle_radians - math.pi / 2  # 90 degrees to the left
        
        # Calculate the X and Y offset for the right position
        right_offset_x = math.cos(right_angle_radians) * (PLAYER_RADIUS)
        right_offset_y = math.sin(right_angle_radians) * (PLAYER_RADIUS)
        right_position_x = self.position.x + right_offset_x
        right_position_y = self.position.y + right_offset_y
        
        # Calculate the X and Y offset for the left position
        left_offset_x = math.cos(left_angle_radians) * (PLAYER_RADIUS)
        left_offset_y = math.sin(left_angle_radians) * (PLAYER_RADIUS)
        left_position_x = self.position.x + left_offset_x
        left_position_y = self.position.y + left_offset_y
        
        return pygame.Vector2(right_position_x, right_position_y), pygame.Vector2(left_position_x, left_position_y)



    def move_y(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def move_x(self, dt):
        horizontal = pygame.Vector2(1, 0).rotate(self.rotation)
        self.position += horizontal * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        
        # Shoot from the nose (tip of the ship)
        nose_position = self.get_nose_position()
        adjusted_rotation = self.rotation + 90
        shot = Shot(nose_position.x, nose_position.y)
        shot.velocity = pygame.Vector2(math.cos(math.radians(adjusted_rotation)), 
                                    math.sin(math.radians(adjusted_rotation))) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN
        
        right_position, left_position = self.get_side_positions()

        if self.has_right_gun:
            
            # right gun shot
            right_shot = Shot(right_position.x, right_position.y)
            right_shot.velocity = pygame.Vector2(math.cos(math.radians(adjusted_rotation)), 
                                                math.sin(math.radians(adjusted_rotation))) * PLAYER_SHOOT_SPEED
            
        if self.has_left_gun:
            # left gun shot
            left_shot = Shot(left_position.x, left_position.y)
            left_shot.velocity = pygame.Vector2(math.cos(math.radians(adjusted_rotation)), 
                                                math.sin(math.radians(adjusted_rotation))) * PLAYER_SHOOT_SPEED

    