import pygame
import random
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, WHITE, [0, 0, 64, 64])
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys, mouse_pos):
        # Helper to safely check key state
        def is_pressed(key):
            return key < len(keys) and keys[key]

        # Keyboard movement
        moved_via_key = False
        if is_pressed(pygame.K_LEFT) or is_pressed(pygame.K_a):
            self.rect.x -= self.speed
            moved_via_key = True
        if is_pressed(pygame.K_RIGHT) or is_pressed(pygame.K_d):
            self.rect.x += self.speed
            moved_via_key = True
        
        # Mouse movement (only if mouse moved significantly or is used)
        if not moved_via_key and mouse_pos:
            self.rect.centerx = mouse_pos[0]
            
        # Bounds check
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, data, target_x=None, start_pos=(0, 0), speed_multiplier=1.0):
        super().__init__()
        self.type = item_type
        self.points, _, self.img_name = data
        
        try:
            self.original_image = pygame.image.load(f"assets/images/{self.img_name}").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (48, 48))
        except:
            self.original_image = pygame.Surface((48, 48))
            self.original_image.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.mask = pygame.mask.from_surface(self.image)
        
        # Physics setup
        target_x = target_x if target_x is not None else random.randint(100, SCREEN_WIDTH - 100)
        
        # Calculate horizontal distance and air time
        dx = target_x - start_pos[0]
        self.vx = (dx / 120) * speed_multiplier # Approx 2 seconds air time
        self.vy = -random.uniform(5, 8) # Initial upward toss
        
        self.angle = 0
        self.rot_speed = random.randint(-5, 5)

    def update(self):
        # Apply physics
        self.vy += GRAVITY
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Rotation
        self.angle += self.rot_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = self.image.get_rect(center=self.rect.center)
        self.rect = new_rect
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Colleague(pygame.sprite.Sprite):
    def __init__(self, name, pos):
        super().__init__()
        self.name = name
        try:
            self.image_orig = pygame.image.load(f"assets/images/{name}.png").convert_alpha()
            self.image_orig = pygame.transform.scale(self.image_orig, (80, 80))
        except:
            self.image_orig = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(self.image_orig, (100, 100, 100), (40, 40), 40)
            
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.mask = pygame.mask.from_surface(self.image)
        
        self.scale_factor = 1.0
        self.is_throwing = False
        self.throw_timer = 0

    def throw(self):
        self.is_throwing = True
        self.throw_timer = 20 # frames of scale animation

    def update(self):
        if self.is_throwing:
            self.throw_timer -= 1
            if self.throw_timer > 10:
                self.scale_factor = 1.2
            else:
                self.scale_factor = 1.0
            
            if self.throw_timer <= 0:
                self.is_throwing = False
                self.scale_factor = 1.0
                
            new_size = (int(80 * self.scale_factor), int(80 * self.scale_factor))
            self.image = pygame.transform.scale(self.image_orig, new_size)
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)

class ScorePopup(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.alpha = 255
        self.timer = 60 # 1 second at 60 FPS

    def update(self):
        self.rect.y -= 1
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
