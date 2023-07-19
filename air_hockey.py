import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH = 800
HEIGHT = 400
GOAL_WIDTH = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
PADDLE_SPEED = 5
PUCK_RADIUS = 10
AI_DIFFICULTY = 0.6
GAME_DURATION = 90

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0,255)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey Game")

clock = pygame.time.Clock()

# Initialize game variables
player_score = 0
ai_score = 0
game_start_time = 0

# Create the paddles
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the puck
puck = pygame.Rect(WIDTH // 2 - PUCK_RADIUS // 2, HEIGHT // 2 - PUCK_RADIUS // 2, PUCK_RADIUS, PUCK_RADIUS)
puck_speed_x = random.choice([-2, 2])
puck_speed_y = random.choice([-2, 2])

# Game loop
running = True
game_start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.y > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.y < HEIGHT - PADDLE_HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # AI paddle movement
    if puck.y < ai_paddle.y and ai_paddle.y > 0:
        ai_paddle.y -= PADDLE_SPEED * AI_DIFFICULTY
    if puck.y > ai_paddle.y + PADDLE_HEIGHT and ai_paddle.y < HEIGHT - PADDLE_HEIGHT:
        ai_paddle.y += PADDLE_SPEED * AI_DIFFICULTY

    # Update puck position
    puck.x += puck_speed_x
    puck.y += puck_speed_y

    # Check collision with walls
    # if puck.y > HEIGHT - PUCK_RADIUS or puck.y < 0:
    #     puck_speed_y *= -1
    if puck.y > HEIGHT - PUCK_RADIUS or puck.y < 0:
        puck_speed_y *= -1
    if puck.x > WIDTH - PUCK_RADIUS or puck.x < 0:
        puck_speed_x *= -1

    # Check collision with paddles
    if puck.colliderect(player_paddle) or puck.colliderect(ai_paddle):
        puck_speed_x *= -1

    # Check goal scored
    # if puck.x < 0:
    #     ai_score += 1
    #     puck.x = WIDTH // 2 - PUCK_RADIUS // 2
    #     puck.y = HEIGHT // 2 - PUCK_RADIUS // 2
    #     puck_speed_x = random.choice([-2, 2])
    #     puck_speed_y = random.choice([-2, 2])
    # elif puck.x > WIDTH - PUCK_RADIUS:
    #     player_score += 1
    #     puck.x = WIDTH // 2 - PUCK_RADIUS // 2
    #     puck.y = HEIGHT // 2 - PUCK_RADIUS // 2
    #     puck_speed_x = random.choice([-2, 2])
    #     puck_speed_y = random.choice([-2, 2])
    if puck.x < 0 and GOAL_WIDTH <= puck.y <= HEIGHT - GOAL_WIDTH:
        ai_score += 1
        puck.x = WIDTH // 2 - PUCK_RADIUS // 2
        puck.y = HEIGHT // 2 - PUCK_RADIUS // 2
        puck_speed_x = random.choice([-2, 2])
        puck_speed_y = random.choice([-2, 2])
    elif puck.x > WIDTH - PUCK_RADIUS and GOAL_WIDTH <= puck.y <= HEIGHT - GOAL_WIDTH:
        player_score += 1
        puck.x = WIDTH // 2 - PUCK_RADIUS // 2
        puck.y = HEIGHT // 2 - PUCK_RADIUS // 2
        puck_speed_x = random.choice([-2, 2])
        puck_speed_y = random.choice([-2, 2])

    # Clear the screen
    window.fill(GREEN)

    # Draw center line segment and center circle
    pygame.draw.line(window, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.circle(window, WHITE, (WIDTH // 2, HEIGHT // 2), 50, 2)

    # Draw the goalposts
    pygame.draw.rect(window, WHITE, pygame.Rect(0, HEIGHT // 2 - 60, GOAL_WIDTH, 120))
    pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH - GOAL_WIDTH, HEIGHT // 2 - 60, GOAL_WIDTH, 120))

    # Draw the paddles and puck
    pygame.draw.rect(window, RED, player_paddle)
    pygame.draw.rect(window, BLUE, ai_paddle)
    pygame.draw.ellipse(window, WHITE, puck)

    # Draw the scores
    font = pygame.font.Font(None, 36)
    player_score_text = font.render("Player: " + str(player_score), True, WHITE)
    ai_score_text = font.render("AI: " + str(ai_score), True, WHITE)
    window.blit(player_score_text, (50, 50))
    window.blit(ai_score_text, (WIDTH - 150, 50))

    # Draw the timers
    time_elapsed = time.time() - game_start_time
    time_remaining = max(0, GAME_DURATION - time_elapsed)
    timer_text = font.render("Time: " + "{:.1f}".format(time_remaining), True, WHITE)
    window.blit(timer_text, (WIDTH // 2 - 60, 50))

    # Update the display
    pygame.display.flip()

    # Check game duration
    if time.time() - game_start_time > GAME_DURATION:
        running = False

    # Control the game speed
    clock.tick(60)


# Game over
print("Game Over")
pygame.quit()