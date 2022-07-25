import pygame, os
from states.state import State
from states.pause_menu import PauseMenu

class Game_World(State):
    def __init__(self, game):
        State.__init__(self,game)
        self.player = pygame.sprite.GroupSingle(Player(self.game))
        self.grass_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))

    def update(self,delta_time, actions):
        # Check if the game was paused 
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
        
    def render(self, display):
        display.blit(self.grass_img, (0,0))
        self.player.render(display)
        # player.draw(screen)
        # player.update()
        # pygame.display.update()
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             sys.exit()
        #             pygame.quit()
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_UP:
        #                 player.sprite.get_health(200)
        #             if event.key == pygame.K_DOWN:
        #                 player.sprite.get_damage(200)


class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = 200,200
        self.current_frame, self.last_frame_update = 0,0
        self.image = pygame.Surface((40,40))
        self.image.fill((200,30,30))
        self.rect = self.image.get_rect(center = (400,400))
        self.current_health = 200
        self.target_health = 500
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5
  
    def get_health(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health
   
    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def update(self, delta_time, actions):
        self.basic_health()
        self.advanced_health()
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]
        # Update the position
        self.position_x += 100 * delta_time * direction_x
        self.position_y += 100 * delta_time * direction_y
        # Animate the sprite
        self.animate(delta_time,direction_x,direction_y)
        
    def basic_health(self):
        pygame.draw.rect(screen,(255,0,0),(10,10,self.target_health / self.health_ratio,25))
        pygame.draw.rect(screen,(255,255,255),(10,10,self.health_bar_length,25),4)
    
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0,255,0)
            
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)
            
        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(10,45,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,45,transition_width,25)
		
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)
        pygame.draw.rect(screen,(255,255,255),(10,45,self.health_bar_length,25),4)
  
    def render(self, display):
        display.blit(self.curr_image, (self.position_x,self.position_y))
        
    def animate(self, delta_time, direction_x, direction_y):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not (direction_x or direction_y): 
            self.curr_image = self.curr_anim_list[0]
            return
        # If an image was pressed, use the appropriate list of frames according to direction
        if direction_x:
            if direction_x > 0: self.curr_anim_list = self.right_sprites
            else: self.curr_anim_list = self.left_sprites
        if direction_y:
            if direction_y > 0: self.curr_anim_list = self.front_sprites
            else: self.curr_anim_list = self.back_sprites
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        # Get the diretory with the player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [],[],[],[]
        # Load in the frames for each direction
        self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back1.png")))
        # for i in range(1,5):
        #     self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) +".png")))
        #     self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) +".png")))
        #     self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) +".png")))
        #     self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) +".png")))
        # Set the default frames to facing front
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites