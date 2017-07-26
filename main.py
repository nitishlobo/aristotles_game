import pygame
import colours

def game_loop(game_display):
    exit_game = False
    while exit_game is False:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        #print pygame.display.get_surface()
    return

#Main code begins
pygame.init()

#Launch game window
window_w = 700
window_h = 400
game_display = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
game_display.fill(colours.WHITE)

#Grid properties
rows = 5
cols = 5
cell_w = window_w/(cols+3)
cell_h = window_h/(rows+3)

#Determine grid 'white' space border size
margin_w = cell_w/2
margin_h = cell_h/2

#Determine gap sizes between cells in the grid
gap_w = (cell_w*2)/(cols-1)
gap_h = (cell_h*2)/(rows-1)

#Generate a grid of rectangles
for i in range(0, rows):
    for j in range(0, cols):
        pygame.draw.rect(game_display, colours.PRIMARY_RED, (margin_w + cell_w*j + gap_w*j, margin_h + cell_h*i + gap_h*i, cell_w, cell_h), 0)

#Run the game
game_loop(game_display)
