import sys
import pygame
import time
import random
pygame.font.init()




WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Bombs!")

BG = pygame.transform.scale(pygame.image.load("assets/backg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 30
STAR_HEIGHT = 30
STAR_VEL = 3


FALLING_STAR_IMG = pygame.transform.scale(pygame.image.load("assets/bomb.png"), (STAR_WIDTH, STAR_HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("assets/shark.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))


FONT = pygame.font.SysFont("poppins bold", 30)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    WIN.blit(PLAYER_IMG, (player.x, player.y))

    for star in stars:
        WIN.blit(FALLING_STAR_IMG, (star.x, star.y))

    pygame.display.update()


def show_menu():
    menu_running = True

    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 30, 100, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 50)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if start_button.collidepoint(mouse_pos):
                    return  # Exit the menu and start the game

                elif exit_button.collidepoint(mouse_pos):
                    end_game = True
                    pygame.quit()
                    sys.exit()

        WIN.blit(BG, (0, 0))

        pygame.draw.rect(WIN, "green", start_button)
        pygame.draw.rect(WIN, "red", exit_button)

        start_text = FONT.render("Start", 1, "white")
        exit_text = FONT.render("Exit", 1, "white")

        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 15))
        WIN.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 45))

        pygame.display.update()




def main():
    end_game = False
    while end_game!=True:

        show_menu()

        run = True

        player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0

        star_add_increment = 2000
        star_count = 0

        stars = []
        hit = False

        while run:
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if star_count > star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)


                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL

            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break

            if hit:
                score_text = FONT.render("Game Over! " f"Your Score: {round(elapsed_time)}", 1, "white")
                WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2 - score_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(4000)
                break


            draw(player, elapsed_time, stars)

    


if __name__ == "__main__":
    main()