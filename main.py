# main.py
import pygame

def neuron(inputs, weights, bias):
    weighted_sum = 0
    for i in range(len(inputs)):
        weighted_sum += inputs[i] * weights[i]
    output = weighted_sum + bias
    return 1 if output > 0 else -1

pygame.init()

P1_SCORE = 0
P2_SCORE = 0

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Table Tennis | Score: {P1_SCORE} - {P2_SCORE}")
BG_COLOR = (255, 255, 255)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 50)

BALL_RADIUS = 10
BALL_SIZE = BALL_RADIUS * 2

BALL_X = WIDTH // 2
BALL_Y = HEIGHT // 2

BALL_SPEED_X = 4
BALL_SPEED_Y = 4
BALL_COLOR = (200, 50, 50)

BALL = pygame.Rect(BALL_X, HEIGHT//2, BALL_SIZE, BALL_SIZE)

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 10
PADDLE_SPEED = 4
PADDLE_COLOR = (50, 50, 200)

P1_X = 50
P1_Y = HEIGHT // 2 - PADDLE_HEIGHT // 2
P1 = pygame.Rect(P1_X, P1_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

P2_X = WIDTH - 50 - PADDLE_WIDTH
P2_Y = HEIGHT // 2 - PADDLE_HEIGHT // 2
P2 = pygame.Rect(P2_X, P2_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

weights = [0.05, 1.0, -0.05]
bias = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pygame.display.set_caption(f"Table Tennis | Score: {P1_SCORE} - {P2_SCORE}")

    screen.fill(BG_COLOR)

    BALL.x += BALL_SPEED_X
    BALL.y += BALL_SPEED_Y

    if BALL.top <= 0  or BALL.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1
    
    key = pygame.key.get_pressed()

    if key[pygame.K_w] and P1.top > 0:
        P1.y -= PADDLE_SPEED
    if key[pygame.K_s] and P1.bottom < HEIGHT:
        P1.y += PADDLE_SPEED
    
    inputs = [BALL.centery, BALL_SPEED_Y, P2.centery]
    move = neuron(inputs, weights, bias)  # -1 = UP, 1 = DOWN

    if move == 1:
        P2.y += PADDLE_SPEED
    else:
        P2.y -= PADDLE_SPEED

    # Keep paddle inside screen
    P2.y = max(0, min(P2.y, HEIGHT - PADDLE_HEIGHT))

    """ # Manual control for P2
    if key[pygame.K_UP] and P2.top > 0:
        P2.y -= PADDLE_SPEED
    if key[pygame.K_DOWN] and P2.bottom < HEIGHT:
        P2.y += PADDLE_SPEED
    """
    if BALL.left <= 0:
        P2_SCORE += 1
        BALL.center = (WIDTH // 2, HEIGHT // 2)
    
    if BALL.right >= WIDTH:
        P1_SCORE += 1
        BALL.center = (WIDTH // 2, HEIGHT // 2)

    if BALL.colliderect(P1) or BALL.colliderect(P2):
        BALL_SPEED_X *= -1
    
    pygame.draw.circle(screen, BALL_COLOR, BALL.center, BALL_RADIUS)
    pygame.draw.rect(screen, PADDLE_COLOR, P1)
    pygame.draw.rect(screen, PADDLE_COLOR, P2)

    pygame.display.flip()
    clock.tick(60)
