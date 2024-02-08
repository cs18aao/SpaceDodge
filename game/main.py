import pygame
import time  # this is the speed of the game.
import random
pygame.font.init()


# the window of the game
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# there is a function to re scale an image if it does not fit the window. i just downloaded the right size
BG = pygame.image.load("space.jpg")

# player character variables
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5

# projectile variable
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

# this function draws the brackground of the game and the player etc, a peremeter within a function means the variable will be edited within another function


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time:  {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red",  player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()
    # DON'T FORGET THE UPDATE


# main game loop to keep the game running (the variables here are objects, which are variables that are built with other variables)
def main():
    run = True
    # hint: subtracting the height of the player from the screen allows me to grab the coordinates for the bottom
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    # get the current time
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000  # milliseconds
    star_count = 0  # this alerts the code that the variable above's time has ran out

    stars = []  # projectile
    hit = False
    while run:
        # clock.tick are the frames per second. projectile counts how many miliseconds occur since the last clock tick
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # generate star
        if star_count > star_add_increment:  # when star count finishes
            for i in range(3):  # add three stars
                # random positions on the x axis and moving the projectile down the y axis
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)  # added to star array list[ ]

                # generates projectiles faster over time max(min, max)
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

        # while running wait for
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break  # finish events. use break if i dont need the computer to keep rechecking in a loop

        # movements. The "and" is for detecting collission
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

 # a copy of the stars list [:] is used because modifying the original list can lead to errors due to the list already rendering the stars falling.  this is a modified copy of the list used to remove stars
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:  # if star hits ground
                stars.remove(star)
             # if star hits player
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        # the player loses
        if hit:
            lost_text = FONT.render("you lost!", 1, "white")
            # THIS IS JUST TEXT PLACEMENT
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width() /
                     2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()  # change scene
            pygame.time.delay(2000)  # frrezes game to view text
            break

        draw(player, elapsed_time, stars)  # keep this in the while loop

    pygame.quit()


if __name__ == "__main__":
    main()
