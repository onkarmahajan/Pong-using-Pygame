import pygame
import sys
import random

def ball_animation(ball_speed_x, ball_speed_y):

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    return ball_speed_x, ball_speed_y

def check_collisions(ball_speed_x, ball_speed_y, score, misses):
    if player.colliderect(ball) or opponent.colliderect(ball): 
        score_sound.play()
        if player.colliderect(ball):
            score += 1
        ball_speed_x *= -1
    elif ball.right >= screen_width or ball.left <= 0:
        if ball.right >= screen_width:
            misses += 1
        ball.center = (screen_width/2, screen_height/2)
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))


    return ball_speed_x, ball_speed_y, score, misses

def player_movement(player_speed):
    player.y += player_speed

    if player.bottom >= screen_height:
        player.bottom = screen_height
    if player.top <= 0:
        player.top = 0

def opponent_ai(opponent_speed):

    if ball.y > opponent.top:
        opponent.y += opponent_speed
    if ball.y < opponent.bottom:
        opponent.y -= opponent_speed

    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height
    if opponent.top <= 0:
        opponent.top = 0

def display_score(score, highscore, misses, game_state):
    if highscore < score:
        highscore = score
    
    if game_state == "on":
        miss_surface = game_font.render(f'Misses: {misses}', True, (255, 255, 255))
        miss_rect = miss_surface.get_rect(center = (screen_width/2, 100))
        screen.blit(miss_surface, miss_rect)

        end_surface = game_font.render('Press Enter to End Game', True, (255, 255, 255))
        end_rect = end_surface.get_rect(center = (screen_width/2, 500))
        screen.blit(end_surface, end_rect)

    if game_state == "off":
        highscore_surface = game_font.render(f'High Score: {highscore}', True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center = (screen_width/2, screen_height - 50))
        screen.blit(highscore_surface, highscore_rect)

        play_again_surface = game_font.render('Press SpaceBar to Play', True, (255, 255, 255))
        play_again_rect = play_again_surface.get_rect(center = (screen_width/2, 400))
        screen.blit(play_again_surface, play_again_rect)


    score_surface = game_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (screen_width/2, 50))
    screen.blit(score_surface, score_rect)

    return score, highscore, misses

def restart():
    end_sound.play()
    ball.center = (screen_width/2, screen_height/2)
    player.center = (screen_width - 2.5, screen_height/2)
    opponent.center = (2.5, screen_height/2)


pygame.init()
screen_width = 960
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

#Game Font
game_font = pygame.font.Font("04B_19__.TTF", 20)

#Game Colours
bg_colour = pygame.Color("grey12")
comp_colour = (200, 200, 200)

#Game Components
ball = pygame.Rect(screen_width/2 - 10, screen_height/2 - 10, 20, 20)
player = pygame.Rect(screen_width - 5, screen_height/2 - 70, 5, 90)
opponent = pygame.Rect(0, screen_height/2 - 70, 5, 90)

#Game Sound
score_sound = pygame.mixer.Sound("audio_point.wav")
end_sound = pygame.mixer.Sound("audio_die.wav")

#Game variables
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))
player_speed = 0
opponent_speed = 8
score = 0
highscore = 0
misses = 0
game_on = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 5
            if event.key == pygame.K_UP:
                player_speed -= 5
            if event.key == pygame.K_SPACE and game_on == False:
                game_on = True
                score = 0
                misses = 0
            if event.key == pygame.K_RETURN:
                game_on = False
                restart()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 5
            if event.key == pygame.K_UP:
                player_speed += 5

    screen.fill(bg_colour)
    pygame.draw.ellipse(screen, comp_colour, ball)
    pygame.draw.rect(screen, comp_colour, player)
    pygame.draw.rect(screen, comp_colour, opponent)
    pygame.draw.aaline(screen, comp_colour, (screen_width/2, 0), (screen_width/2, screen_height))

    if game_on:
        ball_speed_x, ball_speed_y = ball_animation(ball_speed_x, ball_speed_y)
        ball_speed_x, ball_speed_y, score, misses = check_collisions(ball_speed_x, ball_speed_y, score, misses)
        player_movement(player_speed)
        opponent_ai(opponent_speed)
        score, highscore, misses = display_score(score, highscore, misses, "on")
        
        if misses == 5:
            game_on = False
            restart()
    else:
        score, highscore, misses = display_score(score, highscore, misses, "off")        
        

    pygame.display.update()
    clock.tick(60)
