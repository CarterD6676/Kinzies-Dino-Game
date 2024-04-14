import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kinzie's Dino Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)

clock = pygame.time.Clock()
fps = 60
start = False
run = True
allInvisible = False
songChoice = 1
collision = False

songPlay = False
lovestory = "lovestory.mp3"
piano ="piano.mp3"
perfect = "Perfect.mp3"

highScore = 0

def switch_music(track):
    pygame.mixer.music.stop()  # Stop the current playing track
    pygame.mixer.music.load(track)  # Load the new track
    pygame.mixer.music.play(-1)  # Play the new track on loop

def stop():
    pygame.mixer.music.stop()

class Character:
    def __init__(self, images, x, y):
        self.images = [pygame.image.load(image) for image in images]
        self.current_costume_index = 0
        self.image = self.images[self.current_costume_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = float(x)
        self.y = float(y)
        self.move_speed = 2

    def update(self, wall1, wall2):
        self.rect.x = int(self.x)

        if self.rect.colliderect(wall1):
            self.rect.left = wall1.right
            self.x = self.rect.x

        if self.rect.colliderect(wall2):
            self.rect.right = wall2.left
            self.x = self.rect.x

    def move_left(self):
        self.x -= self.move_speed

    def move_right(self):
        self.x += self.move_speed

    def set_costume(self, index):
        if 0 <= index < len(self.images):
            self.current_costume_index = index
            self.image = self.images[self.current_costume_index]

    def draw(self, screen):
        self.rect.x = int(self.x)
        screen.blit(self.image, self.rect)

    def teleport(self, new_x, new_y):
        self.x = float(new_x)
        self.y = float(new_y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
x_range = (55, 245)

class FallingObject:
    def __init__(self, image, x):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = -self.rect.height  
        self.fall_speed = 3  # fall speed 
        self.visible = not allInvisible



    def update(self):
        self.rect.y += self.fall_speed
        global collision, songPlay
        if self.rect.colliderect(player.rect):
            self.reset_position()
            global collected
            collected = collected + 1
            print("collision has occurred")
            collision = True



    
    def toggle_visibility(self):
        self.visible = not self.visible

    def reset_position(self):
        self.rect.y = -self.rect.height  
        self.rect.x = random.randint(x_range[0], x_range[1])

    def draw(self, screen):
        global allInvisible
        if self.visible and not allInvisible: 
            screen.blit(self.image, self.rect)
            

class DottedLine(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, falling_objects):
        global allInvisible, songPlay, highScore, highScoreShow
        for obj in falling_objects:
            if self.rect.colliderect(obj.rect) and not allInvisible:
                allInvisible = True
                songPlay = False






class Instructions:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)


class YouLost:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = False  
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def set_visible(self, visible):
        self.visible = visible

class Button:
    def __init__(self, image_path, x, y, width, height, action=None):
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = False
        self.action = action

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def set_visible(self, visible):
        self.visible = visible

    def handle_event(self, event):
        global current_time, collected, title_image_visible, score_visible, allInvisible, falling_objects, freeplayShow, loveStoryShow, highScoreShow, perfectShow, songPlay
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if allInvisible:
                    lostMessage.set_visible(False)
                    retry.set_visible(False)
                    current_time = 0
                    for falling_object in falling_objects:  # Reset falling object
                        falling_object.reset_position()
                    allInvisible = False
                    player.teleport(150, 400)  # Reset player pos
                    falling_objects = []
                    collected = 0
                    title_image_visible = False
                    score_visible = True
                    player.set_costume(0)  # Reset player costume
                    freeplayShow = False
                    loveStoryShow = False
                    perfectShow = False
                    musicToggle.set_visible(False)
                    songPlay = True  
                    highScoreShow = False






class Button2:
    def __init__(self, image_path, x, y, width, height, action = None):
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = True 
        self.action = action

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def set_visible(self, visible):
        self.visible = visible

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                global toggleSwitcher, loveStoryShow, freeplayShow, perfectShow, songChoice, current_time
                toggleSwitcher = toggleSwitcher + 1
                if toggleSwitcher >= 4:
                    toggleSwitcher = 1
                
                if toggleSwitcher == 1:
                    loveStoryShow = True
                    freeplayShow = False
                    perfectShow = False
                    songChoice = 1
            
                if toggleSwitcher == 2:
                    loveStoryShow = False
                    freeplayShow = True
                    perfectShow = False  
                    songChoice = 2             
                if toggleSwitcher == 3:
                    loveStoryShow = False
                    freeplayShow = False
                    perfectShow = True
                    songChoice = 3
                current_time = 0    
                print(songChoice)
                if self.action:
                    self.action()


class hsbubble:
    def __init__(self, image_path, width, height, x=0, y=0):
        self.image = pygame.image.load(image_path)  # Load custom image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale image to desired dimensions
        self.width = width
        self.height = height
        self.visible = True  # Default to visible
        self.x = x  # Initial x position
        self.y = y  # Initial y position

    def hide(self):
        self.visible = False  # Hide the sprite

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))  # Draw the image at current 

falling_objects = []
num_objects = 4 # norm 4 bug testing
spawn_timer = 0
spawn_delay = 2500


font = pygame.font.SysFont('arial', 24)
smallfont = pygame.font.SysFont('arial', 20)


collected = 0

message_end_time = 0

toggleSwitcher = 0

lstext_surface = smallfont.render("Love Story (Kinzie's Version)", True, (0, 0, 0))
lstext_rect = lstext_surface.get_rect(center=(200, 100))
loveStoryShow = True

ptext_surface = smallfont.render("Perfect (Ed Sheeran)", True, (0, 0, 0))
ptext_rect = ptext_surface.get_rect(center=(200, 100))
perfectShow = False

fptext_surface = smallfont.render("Freeplay Music", True, (0, 0, 0))
fptext_rect = fptext_surface.get_rect(center=(200, 100))
freeplayShow = False

highScoreShow = True

score_visible = False
musicToggle = Button2("Music.png", 345, 545, 50 ,50)
retry = Button("button.png", 95, 200, 200, 100)
lostMessage = YouLost("lost.png", 150, 180)
line = DottedLine("line.png", 200, 450)
title_image = pygame.image.load("title.png")
title_rect = title_image.get_rect()
title_rect.center = (195, 100)
title_image_visible = True  

player = Character(["dino.png", "dinoflipped.png", "dino+1.png", "dino+2.png", "dinoflipped+1.png", "dinoflipped+2.png", "dinoflipped+infinite.png", "dino+infinite.png" , "dino+3.png", "dinoflipped+3.png", "dino+4.png","dinoflipped+4.png"], 150, 465)
                    #0              #1              #2              #3                #4                   #5                      #6                       #7              #8              #9                  #10             #11
floor = pygame.Rect(0, 500, SCREEN_WIDTH, 5)
wall1 = pygame.Rect(50, 0, 5, SCREEN_HEIGHT)
wall2 = pygame.Rect(340, 0, 5, SCREEN_HEIGHT)

Instruction = Instructions("Arrows.png", 120, 550,)

bubble = hsbubble("bubble.png", 250, 150, 40, 230)

htext_surface = smallfont.render(f"Highscore: {highScore}", True, (0, 0, 0))
htext_rect = htext_surface.get_rect(center=(190, 310))

text_surface = font.render(f"Score: {collected}", True, BLACK)
text_rect = text_surface.get_rect(center=(50, 15))


#Run_______________________________________________________________________________________________________________________________________
while run:
    screen.fill(PINK)
    pygame.draw.rect(screen, PINK, floor)
    pygame.draw.rect(screen, PINK, wall1)
    pygame.draw.rect(screen, PINK, wall2)
    if title_image_visible:
        screen.blit(title_image, title_rect)
    if score_visible:
        screen.blit(text_surface, text_rect)
    screen.blit(line.image, line.rect)
    Instruction.draw(screen)
    bubble.draw(screen)
    lostMessage.draw(screen)
    retry.draw(screen)
    musicToggle.draw(screen)

    if loveStoryShow:
        screen.blit(lstext_surface, lstext_rect)
    if perfectShow:
        screen.blit(ptext_surface, ptext_rect)
    if freeplayShow:
        screen.blit(fptext_surface, fptext_rect)
    
    if highScoreShow:
        screen.blit(htext_surface, htext_rect)

    if collected > highScore and not allInvisible:
        print(highScore)
        highScore = collected
        htext_surface = smallfont.render(f"Highscore: {highScore}", True, (0, 0, 0))

    if songPlay:
        if toggleSwitcher >= 4:
            toggleSwitcher = 1
        if toggleSwitcher == 1:

            songChoice = 1
        if toggleSwitcher == 2:
 
            songChoice = 2             
        if toggleSwitcher == 3:

            songChoice = 3

        if pygame.mixer.music.get_busy():
            pass
        else:
            if songChoice == 3:
                switch_music(perfect)
                print(f"songPlay: {songPlay}, songChoice: {songChoice}")
            if songChoice == 2:
                switch_music(piano)
                print(f"songPlay: {songPlay}, songChoice: {songChoice}")
            if songChoice== 1:
                switch_music(lovestory)
                print(f"songPlay: {songPlay}, songChoice: {songChoice}")
    else: 
        pygame.mixer.music.stop()

    if allInvisible == False:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
            start = True
            title_image_visible = False
            score_visible = True
            musicToggle.set_visible(False)
            freeplayShow = False
            loveStoryShow = False
            perfectShow = False
            songPlay = True
            highScoreShow = False
            bubble.hide()

            if collected == 0:
                player.set_costume(0) #og
            if collected == 1: 
                player.set_costume(2) #dino 1+
            if collected == 2: 
                player.set_costume(3) #dino 2+
            if collected == 3: 
                player.set_costume(8) #dino 3+
            if collected == 4: 
                player.set_costume(10) #dino4+
            if collected >= 5: 
                player.set_costume(7) #dino4infinite

        if keys[pygame.K_RIGHT]:
            player.move_right()
            start = True
            title_image_visible = False
            score_visible = True
            musicToggle.set_visible(False)
            freeplayShow = False
            loveStoryShow = False
            perfectShow = False
            songPlay = True
            highScoreShow = False
            bubble.hide()

            if collected == 0:
                player.set_costume(1) #dinoflipped
            if collected == 1: 
                player.set_costume(4) #dinoflipped 1+
            if collected == 2: 
                player.set_costume(5) #dinoflipped 2+
            if collected == 3: 
                player.set_costume(9) #dinoflipped+3
            if collected == 4: 
                player.set_costume(11)  #dinoflipped+4
            if collected >= 5: 
                player.set_costume(6)  #dinoinfinite
    if allInvisible:
        player.teleport(150, 400)
        lostMessage.set_visible(True)
        retry.set_visible(True)
        highScoreShow = True
        title_image_visible = True
        musicToggle.set_visible(True)
        score_visible = False
        if songChoice == 3:
            perfectShow = True
        else: 
            perfectShow = False
        if songChoice == 2:
            freeplayShow = True
        else: 
            freeplayShow = False
        if songChoice == 1:
            loveStoryShow = True
        else:
            loveStoryShow = False





    if collision:
        text_surface = font.render(f"Score: {collected}", True, (0, 0, 0))

 
    player.update(wall1, wall2)  
    player.draw(screen)

    if start:
        for falling_object in falling_objects:
            falling_object.update()
            falling_object.draw(screen)

        line.update(falling_objects)

        current_time = pygame.time.get_ticks()
        if len(falling_objects) < num_objects and current_time - spawn_timer > spawn_delay:
            print(f"Spawning new object at {current_time}")  # Debug print
            falling_object = FallingObject("object.png", random.randint(x_range[0], x_range[1]))
            falling_objects.append(falling_object)
            spawn_timer = current_time  # Reset timer
    pygame.display.update()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        Instruction.handle_event(event)
        musicToggle.handle_event(event)
        retry.handle_event(event)


pygame.quit()
sys.exit()