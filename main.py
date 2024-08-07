import pygame
import os
import sys
pygame.init()
pygame.mixer.init()
# music and sfx
pygame.mixer.music.load('Assets/bg music.mp3')
pygame.mixer.music.set_volume(0.1)
death_sound = pygame.mixer.Sound('Assets/death effect.mp3')
pygame.mixer.Sound.set_volume(death_sound, 0.1)
# images
player_img = pygame.image.load(os.path.join('Assets/player.png'))
spike_man_img = pygame.image.load(os.path.join('Assets/spike.png'))
moving_spike_man_img = pygame.image.load(os.path.join('Assets/moving spike.png'))
moving_spike_man_handle_img = pygame.image.load(os.path.join('Assets/moving spike handle.png'))
flag_img = pygame.image.load(os.path.join('Assets/flag.png'))
play_button_img = pygame.image.load(os.path.join('Assets/play button.png'))
pause_button_img = pygame.image.load(os.path.join('Assets/pause button.png'))
resume_button_img = pygame.image.load(os.path.join('Assets/resume button.png'))
muted_button_img = pygame.image.load(os.path.join('Assets/muted button.png'))
unmuted_button_img = pygame.image.load(os.path.join('Assets/unmuted button.png'))
menu_button_img = pygame.image.load(os.path.join('Assets/menu button.png'))
icon = pygame.image.load(os.path.join('Assets/icon.png'))

# screen
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Get To The Goal V3')
pygame.display.set_icon(icon)

# font?
font = pygame.font.SysFont("Arial", 50, bold=True, italic=False)
font2 = pygame.font.SysFont("Arial", 20, bold=False, italic=False)
font3 = pygame.font.SysFont("Arial", 45, bold=False, italic=False)
font4 = pygame.font.SysFont("Arial", 100, bold=True, italic=False)
font5 = pygame.font.SysFont("Arial", 200, bold=True, italic=False)
# some variables or smth
game_started = False
completed_level = False
current_level = 1
winning_text = font3.render("Level Complete! Press ENTER to go to the next level", True, (255, 255, 255))
final_winning_text = font3.render("You Win! Press ENTER to return to the main menu", True, (255, 255, 255))
game_restarted = False
game_paused = False
song_muted = False
restarted = False
song_unmuted = True
# movement
class Player():
    def __init__(self, x, y, vel, img, spikes, moving_spikes, flag):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.spikes = spikes
        self.moving_spikes = moving_spikes
        self.flag = flag

    def draw(self):
        global restarted
        global completed_level
        global current_level
        global level_has_moving_spikes
        keys = pygame.key.get_pressed()
        
        if completed_level == False:
            
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if self.x > self.vel:
                    self.x -= self.vel
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if self.x < 900 - self.vel - 100:
                    self.x += self.vel
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if self.y > self.vel:
                    self.y -= self.vel
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.y < 500 - 100 - self.vel:
                    self.y += self.vel
            
        for spike in self.spikes:
            if current_level not in [1, 5, 6, 7, 9] and game_paused == False:
                if self.check_collision_spike(spike):
                    if completed_level == False:
                        pygame.mixer.Sound.play(death_sound)
                        self.x = 20
                        self.y = 200
                        break
            
        for moving_spike in self.moving_spikes:
            if current_level not in [1, 2, 3, 4]:
                if self.check_collision_moving_spike(moving_spike):
                    if completed_level == False:
                        pygame.mixer.Sound.play(death_sound)
                        self.x = 20
                        self.y = 200
                        break
        
        if restarted and completed_level:
            self.x = 20
            self.y = 200
            restarted = False
            completed_level = False
        
        if self.check_collision_flag(self.flag):
            completed_level = True
        
        screen.blit(self.img, (self.x, self.y))
    
    def check_collision_spike(self, spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        spike_rect = spike.img.get_rect(topleft=(spike.x + 15, spike.y + 15), width=70, height=70)
        return player_rect.colliderect(spike_rect)
    
    def check_collision_moving_spike(self, moving_spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        moving_spike_rect = moving_spike.img.get_rect(topleft=(moving_spike.x + 15, moving_spike.y + 15), width=70, height=70)
        return player_rect.colliderect(moving_spike_rect)
    
    def check_collision_flag(self, flag):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        flag_rect = flag.img.get_rect(topleft=(flag.x + 50, flag.y + 50), width=1, height=100)
        return player_rect.colliderect(flag_rect)
    
    def check(self):
        global completed_level
        global current_level
        global game_started
        global game_restarted
        keys = pygame.key.get_pressed()
        if completed_level:
            if current_level < 15:
                screen.blit(winning_text, (15, 200))
                if keys[pygame.K_RETURN]:
                    self.x = 20
                    self.y = 200
                    current_level += 1
                    completed_level = False
            else:
                screen.blit(final_winning_text, (15, 200))
                if keys[pygame.K_RETURN]:
                    current_level = 1
                    completed_level = False
                    game_started = False
                    game_restarted = True
                    self.x = 20
                    self.y = 200
class Button():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = img.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self):
        action = False
        
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                
        screen.blit(self.img, (self.x, self.y))
        
        return action
class Spike():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
class Moving_Spike():
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.direction = 1
    def draw(self):
        global game_paused
        if game_paused == False:
            if self.y <= 0:
                self.direction = 1
            elif self.y >= 400:
                self.direction = -1
            self.y += self.speed * self.direction
        
        screen.blit(moving_spike_man_handle_img, (self.x + 45, 0))
        screen.blit(self.img, (self.x, self.y))
        
class Flag():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
class Level():
    def __init__(self, level, flag):
        global game_started
        global game_restarted
        self.level = level
        self.flag = flag
        self.spikes = []
        self.moving_spikes = []
        if game_started and game_restarted:
            level = 1
            self.level = 1
        if level == 1:
            self.spikes = []
            self.moving_spikes = []
        elif level == 2:
            self.spikes = [Spike(400, 200, spike_man_img)]
            self.moving_spikes = []
        elif level == 3:
            self.spikes = [Spike(350, 200, spike_man_img), 
                           Spike(450, 200, spike_man_img)]
            self.moving_spikes = []
        elif level == 4:
            self.spikes = [Spike(200, 20, spike_man_img),
                           Spike(200, 380, spike_man_img),
                           Spike(400, 200, spike_man_img),
                           Spike(600, 20, spike_man_img),
                           Spike(600, 380, spike_man_img)]
            self.moving_spikes = []
        elif level == 5:
            self.spikes = []
            self.moving_spikes = [Moving_Spike(500, 200, moving_spike_man_img, 4)]
        elif level == 6:
            self.spikes = []
            self.moving_spikes = [Moving_Spike(350, 200, moving_spike_man_img, 4),
                                Moving_Spike(450, 200, moving_spike_man_img, 4)]
        elif level == 7:
            self.spikes = []
            self.moving_spikes = [Moving_Spike(350, 200, moving_spike_man_img, 3),
                                Moving_Spike(500, 200, moving_spike_man_img, 7)]
        elif level == 8:
            self.spikes = [Spike(400, 200, spike_man_img)]
            self.moving_spikes = [Moving_Spike(500, 200, moving_spike_man_img, 7),
                                Moving_Spike(300, 400, moving_spike_man_img, 8)]
        elif level == 9:
            self.spikes = []
            self.moving_spikes = [Moving_Spike(200, 250, moving_spike_man_img, 7),
                                Moving_Spike(400, 400, moving_spike_man_img, 5),
                                Moving_Spike(600, 100, moving_spike_man_img, 8)]
        elif level == 10:
            self.spikes = [Spike(300, 0, spike_man_img),
                           Spike(500, 400, spike_man_img),
                           Spike(700, 0, spike_man_img),
                           Spike(700, 400, spike_man_img)]
            self.moving_spikes = [Moving_Spike(200, 0, moving_spike_man_img, 3),
                                  Moving_Spike(400, 0, moving_spike_man_img, 7),
                                  Moving_Spike(600, 0, moving_spike_man_img, 10)]
        elif level == 11:
            self.spikes = [Spike(200, 20, spike_man_img),
                           Spike(200, 380, spike_man_img),
                           Spike(400, 200, spike_man_img),
                           Spike(600, 20, spike_man_img),
                           Spike(600, 380, spike_man_img)]
            self.moving_spikes = [Moving_Spike(300, 0, moving_spike_man_img, 6),
                                  Moving_Spike(400, 0, moving_spike_man_img, 5),
                                  Moving_Spike(500, 400, moving_spike_man_img, 6)]
        elif level == 12:
            self.spikes = [Spike(200, 200, spike_man_img), 
                           Spike(300, 200, spike_man_img),
                           Spike(400, 200, spike_man_img),
                           Spike(500, 200, spike_man_img),
                           Spike(600, 200, spike_man_img),
                           Spike(700, 200, spike_man_img)]
            self.moving_spikes = [Moving_Spike(200, 400, moving_spike_man_img, 7),
                                  Moving_Spike(300, 0, moving_spike_man_img, 7),
                                  Moving_Spike(400, 400, moving_spike_man_img, 7),
                                  Moving_Spike(500, 0, moving_spike_man_img, 7),
                                  Moving_Spike(600, 400,  moving_spike_man_img, 7),
                                  Moving_Spike(700, 0, moving_spike_man_img, 7)]
        elif level == 13:
            self.spikes = [Spike(400, 200, spike_man_img),
                           Spike(200, 100, spike_man_img),
                           Spike(200, 300, spike_man_img),
                           Spike(600, 400, spike_man_img),
                           Spike(600, 300, spike_man_img)]
            self.moving_spikes = [Moving_Spike(200, 200, moving_spike_man_img, 7),
                                  Moving_Spike(400, 0, moving_spike_man_img, 10),
                                  Moving_Spike(600, 100, moving_spike_man_img, 8)]
        elif level == 14:
            self.spikes = [Spike(200, 0, spike_man_img),
                           Spike(300, 0, spike_man_img),
                           Spike(400, 0, spike_man_img),
                           Spike(500, 0, spike_man_img),
                           Spike(600, 0, spike_man_img),
                           Spike(700, 0, spike_man_img),
                           Spike(800, 0, spike_man_img),
                           Spike(200, 400, spike_man_img),
                           Spike(300, 400, spike_man_img),
                           Spike(400, 400, spike_man_img),
                           Spike(500, 400, spike_man_img),
                           Spike(600, 400, spike_man_img),
                           Spike(700, 400, spike_man_img),
                           Spike(800, 400, spike_man_img)]
            self.moving_spikes =  [Moving_Spike(200, 0, moving_spike_man_img, 3),
                                  Moving_Spike(300, 0, moving_spike_man_img, 4),
                                  Moving_Spike(500, 0, moving_spike_man_img, 6),
                                  Moving_Spike(600, 0, moving_spike_man_img, 7),
                                  Moving_Spike(800, 0, moving_spike_man_img, 9)]
        elif level == 15:
            self.spikes = [Spike(300, 0, spike_man_img),
                           Spike(300, 75, spike_man_img),
                           Spike(300, 150, spike_man_img),
                           Spike(500, 200, spike_man_img),
                           Spike(500, 300, spike_man_img),
                           Spike(500, 400, spike_man_img),
                           Spike(700, 0, spike_man_img),
                           Spike(700, 100, spike_man_img),
                           Spike(700, 300, spike_man_img),
                           Spike(700, 400, spike_man_img),]
            self.moving_spikes = [Moving_Spike(200, 0, moving_spike_man_img, 8),
                                  Moving_Spike(400, 0, moving_spike_man_img, 5),
                                  Moving_Spike(600, 0, moving_spike_man_img, 6),
                                  Moving_Spike(800, 400, moving_spike_man_img, 5)]
    
    def run(self):
        global game_started
        global completed_level
        global game_paused
        global song_muted, song_unmuted
        global restarted
        if self.level == 1:
            # the level
            player_thing.draw()
            self.flag.draw()
            
            player_thing.check()
            
            # text
            level_1_text = font.render("Level 1", True, (0, 0, 0))
            level_1_description_1 = font2.render("Welcome to Gttg v3", True, (0, 0, 0))
            level_1_description_2 = font2.render("You move with WASD or arrow keys", True, (0, 0, 0))
            level_1_description_3 = font2.render("Go to the flag to win", True, (0, 0, 0))
            screen.blit(level_1_text, (400, 0))
            screen.blit(level_1_description_1, (50, 50))
            screen.blit(level_1_description_2, (50, 75))
            screen.blit(level_1_description_3, (50, 100))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
                    
        elif self.level == 2:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            for spike in self.spikes:
                spike.draw()
                
            player_thing.check()
            
            # text
            level_2_text = font.render("Level 2", True, (0, 0, 0))
            level_2_description_1 = font2.render("Don't touch the spike", True, (0, 0, 0))
            level_2_description_2 = font2.render("I think it kills you", True, (0, 0, 0))
            screen.blit(level_2_text, (400, 0))
            screen.blit(level_2_description_1, (50, 50))
            screen.blit(level_2_description_2, (50, 75))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 3:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            for spike in self.spikes:
                spike.draw()
                
            player_thing.check()
            
            # text
            level_3_text = font.render("Level 3", True, (0, 0, 0))
            level_3_description = font2.render("More spikes", True, (0, 0, 0))
            screen.blit(level_3_text, (400, 0))
            screen.blit(level_3_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 4:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            for spike in self.spikes:
                spike.draw()
            
            player_thing.check()
            
            # text
            level_4_text = font.render("Level 4", True, (0, 0, 0))
            level_4_description = font2.render("Go through", True, (0, 0, 0))
            screen.blit(level_4_text, (400, 0))
            screen.blit(level_4_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 5:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
                
            player_thing.check()
            
            # text
            level_5_text = font.render("Level 5", True, (0, 0, 0))
            level_5_description = font2.render("A moving spike moves", True, (0, 0, 0))
            screen.blit(level_5_text, (400, 0))
            screen.blit(level_5_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 6:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
                
            player_thing.check()
            
            # text
            level_6_text = font.render("Level 6", True, (0, 0, 0))
            level_6_description = font2.render("More moving spikes", True, (0, 0, 0))
            screen.blit(level_6_text, (400, 0))
            screen.blit(level_6_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
        
        elif self.level == 7:
            # the player flag
            player_thing.draw()
            self.flag.draw()

            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
                
            player_thing.check()
            
            # text
            level_7_text = font.render("Level 7", True, (0, 0, 0))
            level_7_description = font2.render("Different speeds", True, (0, 0, 0))
            screen.blit(level_7_text, (400, 0))
            screen.blit(level_7_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 8:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
                
            player_thing.check()
            
            # text
            level_8_text = font.render("Level 8", True, (0, 0, 0))
            level_8_description = font2.render("Moving spikes and spikes", True, (0, 0, 0))
            screen.blit(level_8_text, (400, 0))
            screen.blit(level_8_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 9:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
            
            player_thing.check()
            
            # text
            level_9_text = font.render("Level 9", True, (0, 0, 0))
            level_9_description = font2.render("No room for improvement", True, (0, 0, 0))
            screen.blit(level_9_text, (400, 0))
            screen.blit(level_9_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 10:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
            
            player_thing.check()
            
            # text
            level_10_text = font.render("Level 10", True, (0, 0, 0))
            level_10_description = font2.render("Climax", True, (0, 0, 0))
            screen.blit(level_10_text, (400, 0))
            screen.blit(level_10_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 11:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
            
            player_thing.check()
            
            # text
            level_11_text = font.render("Level 11", True, (0, 0, 0))
            level_11_description = font2.render("Deja Vu", True, (0, 0, 0))
            screen.blit(level_11_text, (400, 0))
            screen.blit(level_11_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 12:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
            
            player_thing.check()
            
            # text
            level_12_text = font.render("Level 12", True, (0, 0, 0))
            level_12_description = font2.render("Slow and steady", True, (0, 0, 0))
            screen.blit(level_12_text, (400, 0))
            screen.blit(level_12_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
                    
        elif self.level == 13:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
                
            player_thing.check()
            
            # text
            level_13_text = font.render("Level 13", True, (0, 0, 0))
            level_13_description = font2.render("Chaos", True, (0, 0, 0))
            screen.blit(level_13_text, (400, 0))
            screen.blit(level_13_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 14:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
            
            player_thing.check()
            
            # text
            level_14_text = font.render("Level 14", True, (0, 0, 0))
            level_14_description = font2.render("Hard", True, (0, 0, 0))
            screen.blit(level_14_text, (400, 0))
            screen.blit(level_14_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
        elif self.level == 15:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            player_thing.spikes = self.spikes
            player_thing.moving_spikes = self.moving_spikes
            for spike in self.spikes:
                spike.draw()
            for moving_spike in self.moving_spikes:
                moving_spike.draw()
                
            player_thing.check()
            
            # text
            level_15_text = font.render("Level 15", True, (0, 0, 0))
            level_15_description = font2.render("The end.", True, (0, 0, 0))
            screen.blit(level_15_text, (400, 0))
            screen.blit(level_15_description, (50, 50))
            if pause_button.draw():
                game_paused = True
            
            if game_paused:
                paused_text = font5.render("Paused", True, (255, 255, 255))
                screen.fill((0, 0, 0))
                screen.blit(paused_text, (160, 50))
                if resume_button.draw():
                    game_paused = False
                if song_muted:
                    if muted_button.draw():
                        song_unmuted = True
                        song_muted = False
                elif song_unmuted:
                    if unmuted_button.draw():
                        song_unmuted = False
                        song_muted = True
                if menu_button.draw():
                    game_paused = False
                    game_started = False
                    restarted = True
                    
            if song_muted:
                pygame.mixer.music.pause()
            if song_unmuted:
                pygame.mixer.music.unpause()
            
flag = Flag(775, 300, flag_img)
player_thing = Player(20, 200, 5, player_img, [], [], flag)
play_button = Button(350, 300, play_button_img)
pause_button = Button(825, 25, pause_button_img)
resume_button = Button(300, 300, resume_button_img)
muted_button = Button(775, 25, muted_button_img)
unmuted_button = Button(775, 25, unmuted_button_img)
menu_button = Button(600, 300, menu_button_img)
# level stuff
level_1 = Level(1, flag)
level_2 = Level(2, flag)
level_3 = Level(3, flag)
level_4 = Level(4, flag)
level_5 = Level(5, flag)
level_6 = Level(6, flag)
level_7 = Level(7, flag)
level_8 = Level(8, flag)
level_9 = Level(9, flag)
level_10 = Level(10, flag)
level_11 = Level(11, flag)
level_12 = Level(12, flag)
level_13 = Level(13, flag)
level_14 = Level(14, flag)
level_15 = Level(15, flag)
# main loop
pygame.mixer.music.play(-1)
while True:
    clock = pygame.time.Clock()
    clock.tick(60)
    screen.fill((0, 128, 255))
    if game_started == False:
        main_menu_text = font4.render("Get To The Goal V3", True, (0, 0, 0))
        screen.blit(main_menu_text, (75, 50))
        if play_button.draw():
            game_started = True
    if game_started:
        if current_level == 1:
            level_1.run()
        elif current_level == 2:
            level_2.run()
        elif current_level == 3:
            level_3.run()
        elif current_level == 4:
            level_4.run()
        elif current_level == 5:
            level_5.run()
        elif current_level == 6:
            level_6.run()
        elif current_level == 7:
            level_7.run()
        elif current_level == 8:
            level_8.run()
        elif current_level == 9:
            level_9.run()
        elif current_level == 10:
            level_10.run()
        elif current_level == 11:
            level_11.run()
        elif current_level == 12:
            level_12.run()
        elif current_level == 13:
            level_13.run()
        elif current_level == 14:
            level_14.run()
        elif current_level == 15:
            level_15.run()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()