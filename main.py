import pygame
import os
pygame.font.init()
#pygame.mixer.init()

HEIGHT,WIDTH=700,1200
FPS = 60
VEL = 10
BULLET_VEL = 10
MAX_BULLETS = 3
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40
HEALTH_FONT_SIZE = 40
WINNER_FONT_SIZE = 100
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Hunter')

WHITE=(255,255,255)
SPACE_COLOUR=(96,20,155)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

RED_HIT = pygame.USEREVENT +1
YELLOW_HIT = pygame.USEREVENT +2


HEALTH_FONT = pygame.font.SysFont('comicsans',HEALTH_FONT_SIZE)
WINNER_FONT = pygame.font.SysFont('comicsans',WINNER_FONT_SIZE)


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
SPACE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space_image.png')),(WIDTH,HEIGHT))

#BULLET_SOUND = pygame.mixer.load(os.path.join('Assets','Gun+Silencer.mp3'))
#BULLET_HIT_SOUND = pygame.mixer.load(os.path.join('Assets','Grenade+1.mp3'))

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x-= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 20 <BORDER.x:
        yellow.x+= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y-= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height< HEIGHT-15:
        yellow.y+= VEL

def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x +BORDER.width:
        red.x-= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width <WIDTH:
        red.x+= VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y-= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height< HEIGHT-15:
        red.y+= VEL
        
def bullet_movement(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            
            red_bullets.remove(bullet) 
        if bullet.x < 0:
            red_bullets.remove(bullet)


        



def draw_window(yellow,red,yellow_bullets,red_bullets,red_health,yellow_health):
    WIN.blit(SPACE_IMAGE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render( "Health : " + str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render( "Health : " + str(yellow_health),1,WHITE)

    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))
    WIN.blit(yellow_health_text,(10,10))
    
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    pygame.display.update()

def draw_winner(text):
    winner_text = WINNER_FONT.render(text ,1,WHITE)
    WIN.blit( winner_text,(WIDTH/2 - winner_text.get_width() / 2, HEIGHT/2 -winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)
    


def main():

    yellow = pygame.Rect(300,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red = pygame.Rect(700,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow_bullets=[]
    red_bullets=[]
    clock = pygame.time.Clock()
    yellow_health = 100
    red_health = 100

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2 , 10 , 5) 
                    yellow_bullets.append(bullet)
                    #BULLET_SOUND.play()
                if event.key == pygame.K_RALT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2,10 , 5)
                    red_bullets.append(bullet)
                    #BULLET_SOUND.play()
            if event.type == RED_HIT and red_health > 0 :
                    #BULLET_HIT_SOUND.play()
                    red_health= red_health - 10
            if event.type == YELLOW_HIT and yellow_health > 0 :
                    #BULLET_HIT_SOUND.play()
                    yellow_health = yellow_health - 10



        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        bullet_movement(yellow_bullets,red_bullets,yellow,red)

        winner_text = ""
        if red_health <= 0:
            winner_text = "yellow wins !"
        if yellow_health <= 0:
            winner_text = "red wins ! "
        if winner_text != "":
            draw_winner(winner_text)
            break
        


        
        draw_window(yellow,red,yellow_bullets,red_bullets,red_health,yellow_health)
        
    main()

if __name__ == "__main__":
    main()
