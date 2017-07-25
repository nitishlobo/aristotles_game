import pygame

def game_loop():
    exit_game = False
    while exit_game is False:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pygame.display.update()
    return

#Main code begins
pygame.init()

#Launch game window
screen_width = 700
screen_height = 400
game_display = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZEABLE)

game_loop()
