# CISS 145 Introduction to Python Programming
# Final Project: Dinosaur Game
# By Yijun Wu

import pygame
import random

# pygame initialization
pygame.init()

# initialize the window of the game.
# 800 is the width of the window and it fits the best
# 300 is the height of the window
WIN_X = 800
WIN_Y = 300
screen = pygame.display.set_mode(  (WIN_X, WIN_Y)  )

# set the window caption
pygame.display.set_caption("Dinosaur Game")

# set the starting speed of game to 10
speed = 10

# set the clock to refresh
clock = pygame.time.Clock()

# the background of the game contains two parts: track and clouds
# the background keeps on moving make the dinosaur looks like running

# track class
# make track continue on moving forever by using two alternatively, 
# when one image moving out of the screen, put it after the other image
class Track():
    def __init__(self, track_x = 0):
        # load the image of track
        self.track_image = pygame.image.load("image/Track.png")
        # initialize the x and y axis of track image
        self.track_x = track_x
        self.track_y = WIN_Y - self.track_image.get_height()
        self.image_width = self.track_image.get_width()
    
    def move(self):
        # make the track moving by the game speed
        self.track_x -= speed
        # if the track image move out of the screen completely, 
        # put it after the second image.
        if self.track_x <= - self.image_width:
            self.track_x = self.image_width
    
    #draw the track onto the surface.
    def draw(self):
        screen.blit(self.track_image, (self.track_x, self.track_y))

# create the two tracks, so the screen will always have a track on it
track1 = Track()
track2 = Track(2404)
# 2404 is the width of the track image

# cloud class
# the idea is the same as the track, keep the cloud image moving 
# until it is completely out of the screen, 
# then put it back to its original position
class Cloud:
    def __init__(self, x, y):
        # load the image of cloud
        self.image = pygame.image.load("image/Cloud.png")
        # set the x and y axis of cloud
        self.x = x
        self.y = y
        self.x_original = x
        self.width = self.image.get_width()
    
    def move(self):
        # make the track moving by the game speed
        self.x -= speed
        # if the track image move out of the screen completely, 
        # put it back to its original position.
        if self.x <= - self.width:
            self.x = self.x_original
    
    # draw cloud
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# create two clouds, there will be two clouds on the background
# (700, 50) and (800, 100) are the initial axis of two clouds
cloud1 = Cloud(700, 50)
cloud2 = Cloud(800, 100)

# cactus class
class Cactus:
    def __init__(self):
        # load the images of cactus in a list 
        self.cactus_images = [pygame.image.load("image/CactusLarge1.png"),
                pygame.image.load("image/CactusLarge2.png"),
                pygame.image.load("image/CactusLarge3.png"),
                pygame.image.load("image/CactusSmall1.png"),
                pygame.image.load("image/CactusSmall2.png"),
                pygame.image.load("image/CactusSmall3.png")]
        # set the random number to select a cactus among the 6 cacti images
        self.n = random.randint(0,5)
        self.image = self.cactus_images[self.n]
        # get the height and width of the cactus
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        # set the x and y axis of the cactus
        self.x = WIN_X
        self.y = WIN_Y - 10 - self.image.get_height()
    
    def move(self):
        # let the cactus move by the game speed
        self.x -= speed
        # if the track image move out of the screen completely, 
        # create a new cactus
        # the screen will only have one cactus on it at the same time.
        if self.x <= - self.width:
            self.x = WIN_X
            # select a new cactus randomly from the 6 cacti list
            self.n = random.randint(0,5)
            self.image = self.cactus_images[self.n]
            self.y = WIN_Y - 10 - self.image.get_height()
            # 10 is decided based on the location of the track
    
    # draw cactus
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# create a cactus
cactus = Cactus()

dino_jump = False

# load the music for jumping
jump_sound = pygame.mixer.Sound("sound/jump.wav")

class Dinosaur():
    def __init__(self):
        # load the images of dinosaur
        self.image_start = pygame.image.load("image/DinoStart.png")
        self.image_run = [pygame.image.load("image/DinoRun1.png"),
                            pygame.image.load("image/DinoRun2.png")]
        self.image_jump = pygame.image.load("image/DinoJump.png")
        self.index = 0
        self.image = self.image_run[0]
        # set the jump speed
        self.jump_velocity = 8.5
        self.dino_rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dino_y = WIN_Y - 5 - self.height
        # 5 is used to set dianosor looks higher than the window's edge
    
    def run(self):
        # the dinosaur images are not moving, make it looks like running 
        # by moving the background (track and clouds)
        # so the x and y axis of dinosaur images will not change
        # let the dinosaur run by placing two images alternatively
        if self.index == 10:
            self.index = 0
        if self.index < 5:
            self.image = self.image_run[0]
        elif self.index < 10:
            self.image = self.image_run[1]
        self.index += 1
    
    def jump(self):
        global dino_jump
        self.image = self.image_jump
        # the higher the dinosaur jump, the slower the y will decrease
        # when the jump_velocity < 0, the y axis will add up,
        # the dinosaur will fall back to the ground
        if dino_jump:
            # index 2 is decided because 3 jumps too high
            # and 1 jumps too low for the cactus
            self.dino_y -= self.jump_velocity * 2
            self.jump_velocity -= 0.5
        # when the dinosaur back on the ground, 
        # the jump action finish, and reset the jump_velocity
        if self.jump_velocity < - 8:
            dino_jump = False
            self.jump_velocity = 8.5
            # make sure the dinosuar is on the original y axis.
            self.dino_y = WIN_Y - 5 - self.image.get_height()
    
    # draw the dinosaur on the screen
    def draw(self):
        screen.blit(self.image, (80, self.dino_y))

# create a dinosaur
dinosaur = Dinosaur()

dino_run = False

# load the image and sound when game ends
image_dead = pygame.image.load("image/DinoDead.png")
dead_sound = pygame.mixer.Sound("sound/gameover.wav")

scores = 0
index = 0

# the score system
def score():
    global scores, index, speed
    score_font = pygame.font.SysFont("menlo", 20)
    index += 1
    # every 100 index, the score increases by one
    if index % 100 == 0:
        scores += 1
    # every 5 scores, whicih is 100 index,the speed of the game increase by 1
    # the speed is also the game difficulty,
    # the diffilculty of the game increase while the score raises
    if index % 500 == 0:
        speed += 1
    # display the score on the screen so the player can know it
    score_text = score_font.render(f"Score: {scores}", True, (0, 0, 0))
    screen.blit(score_text, (650, 20))

# read and save the highest scores of the game
def highest_score(name, score):
    global high_score_text
    new_name = name
    new_score = score
    highest_score_font = pygame.font.SysFont("menlo", 20)

    # read the old high score list from text file
    myfile = open("scores.txt", "r")
    lines = myfile.readlines()

    scores = []
    for l in lines:
        n = l.split()[0]
        s = l.split()[1]
        scores.append((n, int(s)))
    
    # compare the new score with the old high score list
    # put the new score and new name into the score list from high to low
    i = 0
    inserted = False
    for v in scores:
        if v[1] < new_score:
            scores.insert(i, (new_name, new_score))
            inserted = True
            break
        i += 1
    if (not inserted):
        scores.append((new_name, new_score))

    # write the new high score list into the text file
    myfile = open("scores.txt", "w")
    # set the x and y axis of high score list
    board_x = 400
    board_y = 50
    # display the high score title on the screen
    high_score_title = highest_score_font.render("Highest Score", True, (0, 0, 0))
    screen.blit(high_score_title, (board_x, board_y))
    # display the first 3 high scores
    for v in scores[0:3]:
        myfile.write(f"{v[0]}     {v[1]} \n")
        board_y += 50
        high_score_text = highest_score_font.render(f"{v[0]} {v[1]}", True, (0, 0, 0))
        screen.blit(high_score_text, (board_x, board_y))
    myfile.close()

# the welcome screen is open once the game is open
show_welcome = True
running = True

def welcome():
    global dino_run, running, scores
    show_welcome = True
    
    while(show_welcome):
        # fill the screen with white
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dino_run = True
                    running = True
                    scores = 0
                    show_welcome = False
                    
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        
        # display the instruction of how to start
        start_font = pygame.font.SysFont("menlo", 30)
        start_screen = start_font.render("Press Enter to Start", True, (0, 0, 0))
        screen.blit(start_screen, (230, 220))
        # (230,220) is the location of the sentence, it's the lowest
        
        # write the instruction of how to play
        operate = pygame.font.SysFont("menlo", 15)
        operate_instruction = operate.render("Press Space to Jump", True, (0, 0, 0))
        screen.blit(operate_instruction, (290, 180))
        
        # draw a dinosaur on the welcom screen
        dinosaur_welcome_image = pygame.image.load("image/DinoStart.png")
        screen.blit(dinosaur_welcome_image, (350, 70))
        
        # refresh the screen
        clock.tick(60)
        pygame.display.update()

# the welcome starts when the game is open
welcome()

# the function is used when the game end
def gameOver():
    global running, show_welcome, speed
    show_game_over = True
    
    while (show_game_over):
        # fill the screen with white
        screen.fill ((255, 255, 255))
        screen.blit(image_dead, (200, 100))
        dead_sound.play()
        # ask the player to enter name to sort scores
        name = input("Enter your name: ")
        # place and the 3 highest scores
        highest_score(name, scores)
        
        # reset the x and y axis of cactus so it can appear again
        # on the right place when the game restart
        cactus.x = WIN_X
        cactus.y = WIN_Y - 10 - cactus.image.get_height()
        dinosaur.dino_y = WIN_Y - 5 - dinosaur.image.get_height()
        dinosaur.jump_velocity = 8.5
        speed = 10

        # display the instruction of how to restart
        restart_font = pygame.font.SysFont("menlo", 25)
        restart_instruction = restart_font.render("Press 1 to Restart", True, (0, 0, 0))
        screen.blit(restart_instruction, (230, 230))
        # refresh the screen
        clock.tick(60)
        pygame.display.update()
        # if the player want to play the game, restart the game
        stopsign = int(input("Enter 1 if you want to retry: "))
        if (stopsign == 1):
            show_welcome = True
            running = True
            welcome()
            show_game_over = False
        else:
            break

running = True

# this is the main loop
while (running):
    # fill the screen with white
    screen.fill((255, 255, 255))

    # the dinosaur start running when the enter is pressed
    if dino_run:
        # place the player score
        score()

        # draw the backgound: track and cloud
        # draw the track
        track1.move()
        track1.draw()
        track2.move()
        track2.draw()

        # draw the two cloud on the screen
        cloud1.move()
        cloud1.draw()
        cloud2.move()
        cloud2.draw()

        # draw cacti on the screen 
        cactus.move()
        cactus.draw()

        # draw the dinosaur
        dinosaur.run()
        dinosaur.draw()
    
    # the dinosaur jump when the space is pressed
    if dino_jump:
        dinosaur.jump()
        dinosaur.draw()
    
    # handle the event when keys are pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino_jump = True
                jump_sound.play()
            if event.key == pygame.K_ESCAPE:
                running = False
        
    # if dinosaur run into a cactus, the game ends
    # the collision happens when the rectangles of dinosaur and cactus meet
    rect_c = pygame.Rect(cactus.x, cactus.y, cactus.width-30, cactus.height-20)
    rect_d = pygame.Rect(80, dinosaur.dino_y, dinosaur.width-20, dinosaur.height-10)
    if (rect_d.colliderect(rect_c)):
        dino_run = False
        dino_jump = False
        running = False
        # jump to game over function
        gameOver()
    
    # refresh the screen
    clock.tick(60)
    pygame.display.update()
    
    # CISS 145, Fall Semester 2022
    # Finished on Dec. 14th, 2022