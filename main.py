import time
import random
import pygame
import turtle
import os
from tkinter import *
from tkinter import messagebox

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
CYAN = (0, 100, 100)
WIDTH = 1100
HEIGHT = 700
TITLE = "game game"

# ----- SCREEN PROPERTIES
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE)

pygame.init()


# A function to write text on the screen
def write_text(text, x, y, font_size):
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text_surface = font.render(text, False, BLACK)
    screen.blit(text_surface, (x, y))


# SPRITES
all_sprites_group = pygame.sprite.Group()
npc_sprites_group = pygame.sprite.Group()
blast_sprites_group = pygame.sprite.Group()
vertblast_sprites_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        # Keeping player in the screen
        # Top and bottom
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        # Left and right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.Surface([25, 25])
        # self.image.fill((0, 255, 0))
        self.image = pygame.image.load('./DVD.png')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.y_vel = random.choice([3, -3])  # 3 pixels per tick
        self.x_vel = random.choice([3, -3])

        self.rect.x, self.rect.y = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

    def update(self):
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.x_vel = -self.x_vel
        if self.rect.left < 0:
            self.rect.left = 0
            self.x_vel = -self.x_vel

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.y_vel = -self.y_vel
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_vel = -self.y_vel


# Lasers through the entire screen. Program movement for it?
class Blast(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tick = 0
        self.image = pygame.Surface([WIDTH, 25])
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.image.set_alpha(128)

        self.rect.x, self.rect.y = (0), random.randrange(0, HEIGHT)

    def update(self):
        self.tick += 1
        if self.tick == 0.5 * 60:
            self.image.set_alpha(255)
            self.image.fill((255, 0, 0))
            blast_sprites_group.add(self)
        if self.tick == 1 * 60:
            self.kill()


class VertBlast(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tick = 0
        self.image = pygame.Surface([25, HEIGHT])
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.image.set_alpha(128)

        self.rect.x, self.rect.y = random.randrange(0, WIDTH), (0)

    def update(self):
        self.tick += 1
        if self.tick == 0.5 * 60:
            self.image.set_alpha(255)
            self.image.fill((255, 0, 0))
            vertblast_sprites_group.add(self)
        if self.tick == 1 * 60:
            self.kill()


def spawn(sprite_group, sprite):
    sprite_group.add(sprite)


def main():
    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    npc_last_spawn_time = 0
    time_since_blast_spawn = 0
    hp = 25
    direction = 1
    time_since_last_dash = 500
    score = 0

    # Create our player Sprite
    player = Player()

    # Some other sprite
    some_other_sprite = NPC()
    blast = Blast()
    vertblast = VertBlast()
    # # Change its location
    # some_other_sprite.rect.x += 40
    # some_other_sprite.image.fill((0, 255, 0)) #green

    # Create a new group of sprites
    npc_sprites_group.add(some_other_sprite)
    all_sprites_group.add(player)
    all_sprites_group.add(some_other_sprite)
    all_sprites_group.add(blast)
    all_sprites_group.add(vertblast)
    # time management (New spawns and more!)
    # pygame.time.set_timer(spawn(, 5000, loops = 500)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pressed = pygame.key.get_pressed()

        # ----- LOGIC
        if pressed[pygame.K_w]:
            player.rect.y -= 10  # moves the player upward
            direction = 1
        elif pressed[pygame.K_s]:
            player.rect.y += 10
            direction = 2
        elif pressed[pygame.K_a]:
            player.rect.x -= 10
            direction = 3
        elif pressed[pygame.K_d]:
            player.rect.x += 10
            direction = 4
        if pressed[pygame.K_SPACE] and time_since_last_dash > 1 * 30:
            time_since_last_dash = 0
            if direction == 1:
                player.rect.y -= 100
            elif direction == 2:
                player.rect.y += 100
            elif direction == 3:
                player.rect.x -= 100
            elif direction == 4:
                player.rect.x += 100

        # Collision detection
        collided_sprites = pygame.sprite.spritecollide(player, npc_sprites_group, dokill=False)
        blast_collided_sprites = pygame.sprite.spritecollide(player, blast_sprites_group, dokill=False)
        vertblast_collided_sprites = pygame.sprite.spritecollide(player, vertblast_sprites_group, dokill=False)
        # Check npc collision
        for npc in npc_sprites_group:
            for blast in blast_sprites_group:
                if pygame.sprite.collide_rect(npc, blast):
                    # do something because these two have collided
                    # Bounce the npc off the blast
                    # change npc vel ---> how it hit the blast
                    pass

        if len(collided_sprites) > 0:
            hp -= 1
            print("Collided")
        if len(blast_collided_sprites) > 0:
            hp -= 1
            print("Collided")
        if len(vertblast_collided_sprites) > 0:
            hp -= 1
            print("Collided")

        all_sprites_group.update()
        npc_sprites_group.update()
        print(npc_last_spawn_time)

        # NEW ENEMIES BABY
        # Every 5 seconds (5000ms) create a new npc
        if npc_last_spawn_time > 5 * 60:
            npc_last_spawn_time = pygame.time.get_ticks()  # set the time to now
            # create a new npc
            npc = NPC()

            # add them to the some sprites list
            npc_sprites_group.add(npc)
            # add them to the all sprites list
            all_sprites_group.add(npc)

            npc_last_spawn_time = 0

            # Speed up over time!
            # Every 5 seconds, speed goes up, and direction is randomized.
            for npc in npc_sprites_group:
                npc.x_vel = npc.x_vel * random.choice([1, -1, 1.2, -1.2])
                npc.y_vel = npc.y_vel * random.choice([1, -1, 1.2, -1.2])

        # ----- DRAW
        screen.fill(WHITE)
        all_sprites_group.draw(screen)
        write_text("score:", 20, 20, 25)
        write_text(str(score), 100, 20, 25)
        write_text(str(hp), 75, 525, 25)
        write_text("HP:", 20, 525, 25)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)
        npc_last_spawn_time += 1
        pygame.display.set_caption("survive.")
        time_since_last_dash += 1
        time_since_blast_spawn += 1
        score += 0.5
        if random.randrange(1, 200) == 50:
            blast = Blast()
            all_sprites_group.add(blast)
        if random.randrange(1, 200) == 50:
            vertblast = VertBlast()
            all_sprites_group.add(vertblast)

        # Lose condition
        if hp == 0:
            Tk().wm_withdraw()  # to hide the main window
            messagebox.showinfo('YOU LOSE', 'Aww... darn')
            pygame.display.set_caption("LOSE")
            done = True


if __name__ == "__main__":
    main()
