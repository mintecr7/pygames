import pygame
from dqn import DQN
import numpy as np
from objects import Paddle, Ball

pygame.init()

WIDTH, HEIGHT = 700, 500
FPS = 60 # frames per second
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE_FONT = pygame.font.SysFont("comicsans", 57)
WINNING_SCORE = 10
LEARNING_RATE = 0.001
pygame.display.set_caption("PONG")


def draw(win, paddles, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (3*(WIDTH//4) + right_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2-5, i, 10, HEIGHT//20))
    pygame.display.update()


def handle_paddle_movement(keys, left_paddle : Paddle, right_paddle: Paddle) -> None:
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move()
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VELOCITY <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move()
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VELOCITY <= HEIGHT:
        right_paddle.move(up=False)

def handle_paddle_movement_for_NN(paddle: Paddle,  predictition: int) -> None:
    if predictition == 1:
        paddle.move()
    else:
        paddle.move(up=False)

    
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        # bottom of the screen 
        ball.y_val *= -1
    elif ball.y - ball.radius <=0:
        # top of the screen
        ball.y_val *= -1
    
    if ball.x_val > 0:
        # right paddle 
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_val *= -1
                
                # handle y direction collision
                middle_y = right_paddle.y + right_paddle.height//2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2) / ball.MAX_VEL
                y_val = difference_in_y / reduction_factor
                ball.y_val = -1 * y_val
    else: 
        # left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_val *= -1

                # handle y direction collision
                middle_y = left_paddle.y + left_paddle.height//2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2) / ball.MAX_VEL
                y_val = difference_in_y / reduction_factor
                ball.y_val = -1* y_val
    
def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, 
                         PADDLE_HEIGHT, PADDLE_WIDTH)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH,
                          HEIGHT//2 - PADDLE_HEIGHT//2, 
                          PADDLE_HEIGHT, PADDLE_WIDTH)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0 
    player_1 = DQN(LEARNING_RATE, left_score, left_paddle)
    player_2 = DQN(LEARNING_RATE, right_score, right_paddle)
    while run:
        draw(WIN,[left_paddle, right_paddle, ball], left_score, right_score)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        # print(player_1.paddle.x)
        # if player_1.paddle.y <= ball.y:
        #     obs_left = 1
        # elif player_1.paddle.y + player_1.paddle.height >= ball.y:
        #     obs_left = 0
        # if player_2.paddle.y <= ball.y:
        #     obs_right = 1
        # elif player_2.paddle.y + player_2.paddle.height >= ball.y:
        #     obs_right = 0
        # player_1.train(states= np.array([[ball.x, ball.y], [player_1.paddle.x, player_1.paddle.y]]), observation=np.array([obs_left]))
        # player_2.train(states=np.array([[ball.x, ball.y], [player_2.paddle.x, player_2.paddle.y]]), observation=np.array([obs_right]))
        # player_1_pred = player_1.predict(states=np.array([[ball.x, ball.y], [player_1.paddle.x, player_1.paddle.y]]))
        # player_2_pred = player_2.predict(states=np.array([[ball.x, ball.y], [player_2.paddle.x, player_2.paddle.y]]))
        # print("Prediction are player_1:- {} and player_2:- {}".format(player_1_pred, player_2_pred))
        # player_1.move(player_1_pred[0][0])
        # player_2.move(player_2_pred[0][0])
        ball.move()
        handle_collision(ball, left_paddle, right_paddle )
        
        if ball.x < 0:
            right_score +=1
            player_2.score +=1
            ball.rest()
            
        elif ball.x > WIDTH:
            left_score +=1
            player_1.score +=1
            ball.rest()
            
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
            
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.rest()
            left_paddle.rest()
            right_paddle.rest()
            left_score = 0
            right_score = 0

    pygame.quit()



if __name__ == '__main__':
    main()