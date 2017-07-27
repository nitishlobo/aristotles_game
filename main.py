import pygame
import colours

class Cell(object):
    '''Rectangular cell with the game word and game properties.

    Keyword arguments:
    surf -- display surface of pygame.
    left -- pixel from the left of the screen for the left edge of the rectangular cell.
    top -- pixel from the top of the screen for the top edge of the rectangular cell.
    width -- width of the rectanglular cell.
    height -- height of the rectanglular cell.
    word -- game word of the cell.
    cell_colour -- initial cell colour.
    cell_border -- border of the cell.
    '''
    def __init__(self, surf, left, top, width, height, word, cell_colour, cell_border=0):
        self.surf = surf
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.cell_colour = cell_colour
        self.cell_border = cell_border

    def draw_rect(self):
        '''Draw a shaded rectangle.'''
        pygame.draw.rect(self.surf, self.colour, (self.left, self.top, self.width, self.height), self.border)

def game_loop(game_display):
    exit_game = False
    while exit_game is False:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
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
