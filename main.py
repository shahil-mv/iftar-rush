import pygame
import sys
import random
import time
from constants import *
from entities import Player, Item, ScorePopup, Colleague

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Iftar Rush: Office Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Outfit", 32, bold=True)
        self.large_font = pygame.font.SysFont("Outfit", 72, bold=True)
        
        # Load Assets
        try:
            self.day_bg = pygame.image.load("assets/images/day_bg.png").convert()
            self.day_bg = pygame.transform.scale(self.day_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_bg = pygame.image.load("assets/images/night_bg.png").convert()
            self.night_bg = pygame.transform.scale(self.night_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.day_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.day_bg.fill(SKY_BLUE)
            self.night_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.night_bg.fill(MIDNIGHT_BLUE)

        # Sounds
        try:
            self.adhan_sound = pygame.mixer.Sound("assets/sounds/adhan.mp3")
        except:
            self.adhan_sound = None

        # Game State
        self.high_score = 0
        self.state = "START" # START, PLAYING, GAMEOVER
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.items = pygame.sprite.Group()
        self.popups = pygame.sprite.Group()
        self.colleagues = pygame.sprite.Group()
        
        # Initialize Colleagues
        for name, pos in COLLEAGUE_POSITIONS.items():
            col = Colleague(name, pos)
            self.colleagues.add(col)
            self.all_sprites.add(col)
        
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.current_phase = "DAY"  # DAY or NIGHT
        self.phase_start_time = time.time()
        
        self.difficulty_mult = 1.0
        self.boost_active = False
        self.boost_end_time = 0

    def toggle_phase(self):
        if self.current_phase == "DAY":
            self.current_phase = "NIGHT"
            if self.adhan_sound:
                self.adhan_sound.play()
            else:
                print("ADHAN: Night Phase Started!")
        else:
            self.current_phase = "DAY"
        self.phase_start_time = time.time()

    def spawn_item(self):
        # Weighted random selection
        keys = list(ITEM_DATA.keys())
        weights = [ITEM_DATA[k][1] for k in keys]
        item_key = random.choices(keys, weights=weights)[0]
        
        # Select colleague associated with the item (or random if not direct match)
        # In this game, item_key matches colleague name in COLLEAGUE_POSITIONS
        thrower = None
        for c in self.colleagues:
            if c.name == item_key:
                thrower = c
                break
        
        if not thrower:
            thrower = random.choice(self.colleagues.sprites())
            
        thrower.throw()
        
        speed_mult = 1.0 if not self.boost_active else 2.0
        # Target the general area of the player
        target_x = self.player.rect.centerx + random.randint(-50, 50)
        
        new_item = Item(item_key, ITEM_DATA[item_key], target_x, thrower.rect.center, speed_mult)
        self.items.add(new_item)
        self.all_sprites.add(new_item)

    def handle_collision(self, item):
        points = item.points
        if self.boost_active:
            points *= 2
            
        color = GREEN
        prefix = "+"
        
        if self.current_phase == "DAY":
            self.score -= points
            color = RED
            prefix = "-"
        else:
            self.score += points
            
        # Special case: Anad's Protein Powder
        if item.type == "anand" and self.current_phase == "NIGHT":
            self.boost_active = True
            self.boost_end_time = time.time() + BOOST_DURATION

        # Create popup
        popup = ScorePopup(item.rect.centerx, item.rect.centery, f"{prefix}{points}", color)
        self.popups.add(popup)
        self.all_sprites.add(popup)
        item.kill()

    def update(self):
        if self.state != "PLAYING":
            return

        # Time Management
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        remaining_time = TOTAL_TIME - elapsed_seconds
        
        if remaining_time <= 0 or self.score < MIN_SCORE_LIMIT:
            self.state = "GAMEOVER"
            if self.score > self.high_score:
                self.high_score = self.score

        # Phase Management
        if time.time() - self.phase_start_time >= PHASE_DURATION:
            self.toggle_phase()

        # Difficulty Scaling (every 30 seconds)
        self.difficulty_mult = 1.0 + (elapsed_seconds // 30) * 0.2

        # Boost Management
        if self.boost_active and time.time() > self.boost_end_time:
            self.boost_active = False

        # Input
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        # Spawning
        spawn_rate = 30 if not self.boost_active else 10
        if random.randint(1, int(spawn_rate)) == 1:
            self.spawn_item()

        # Update Sprites
        self.player.update(keys, mouse_pos)
        self.items.update()
        self.popups.update()
        self.colleagues.update()

        # Collisions
        hits = pygame.sprite.spritecollide(self.player, self.items, False, pygame.sprite.collide_mask)
        for hit in hits:
            self.handle_collision(hit)

    def draw_phase_icon(self):
        center_x = SCREEN_WIDTH // 2
        center_y = 60
        radius = 30
        
        if self.current_phase == "DAY":
            # Draw Sun
            pygame.draw.circle(self.screen, SUN_YELLOW, (center_x, center_y), radius)
            # Rays
            for i in range(8):
                angle = i * (360 / 8)
                import math
                rad = math.radians(angle)
                start_dist = radius + 5
                end_dist = radius + 15
                start_p = (center_x + math.cos(rad) * start_dist, center_y + math.sin(rad) * start_dist)
                end_p = (center_x + math.cos(rad) * end_dist, center_y + math.sin(rad) * end_dist)
                pygame.draw.line(self.screen, SUN_YELLOW, start_p, end_p, 3)
        else:
            # Draw Moon
            pygame.draw.circle(self.screen, MOON_SILVER, (center_x, center_y), radius)
            # Inner circle to make it a crescent
            pygame.draw.circle(self.screen, MIDNIGHT_BLUE, (center_x + 10, center_y - 5), radius - 5)

    def draw(self):
        # Background
        bg = self.day_bg if self.current_phase == "DAY" else self.night_bg
        self.screen.blit(bg, (0, 0))
        
        # Sprites
        self.all_sprites.draw(self.screen)

        # Sprites
        self.all_sprites.draw(self.screen)
        
        # HUD Panel
        panel_height = 100
        hud_panel = pygame.Surface((SCREEN_WIDTH, panel_height), pygame.SRCALPHA)
        hud_panel.fill(PANEL_BG)
        self.screen.blit(hud_panel, (0, 0))

        # Phase Icon (Sun/Moon)
        self.draw_phase_icon()
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BOOST_GOLD)
        self.screen.blit(high_score_text, (20, 60))
        
        timer_text = self.font.render(f"Time: {max(0, TOTAL_TIME - (pygame.time.get_ticks() - self.start_ticks)//1000)}s", True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))
        
        phase_color = RED if self.current_phase == "DAY" else GREEN
        phase_label = "FASTING" if self.current_phase == "DAY" else "IFTAR"
        phase_text = self.font.render(f"Phase: {phase_label}", True, phase_color)
        self.screen.blit(phase_text, (SCREEN_WIDTH // 2 - 100, 20))

        if self.boost_active:
            boost_text = self.large_font.render("⚡ BOOST", True, BOOST_GOLD)
            self.screen.blit(boost_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        # Transition Flash Text
        if time.time() - self.phase_start_time < 2:
            msg = "IFTAR TIME! 🌙" if self.current_phase == "NIGHT" else "FASTING STARTED! ☀️"
            color = GREEN if self.current_phase == "NIGHT" else RED
            flash_text = self.large_font.render(msg, True, color)
            self.screen.blit(flash_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100))

        if self.state == "START":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            title_text = self.large_font.render("IFTAR RUSH: OFFICE EDITION", True, BOOST_GOLD)
            sub_title = self.font.render("Office Edition", True, WHITE)
            instr = self.font.render("Catch food at NIGHT (+pts) | Avoid food at DAY (-pts)", True, WHITE)
            start_btn = self.font.render("Press SPACE to Start", True, GREEN)
            
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(sub_title, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 70))
            self.screen.blit(instr, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
            self.screen.blit(start_btn, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100))

        if self.state == "GAMEOVER":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            go_text = self.large_font.render("GAME OVER", True, RED)
            self.screen.blit(go_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            self.screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            
            retry_text = self.font.render("Press 'R' to Restart", True, WHITE)
            self.screen.blit(retry_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.state == "START" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = "PLAYING"

                if self.state == "GAMEOVER" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = "PLAYING"

            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
