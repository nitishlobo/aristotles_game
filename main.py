import pygame
import linecache
import colours

#English words dictionary.
DICTIONARY_FILE = 'dictionary.csv'

class Cell(object):
    '''Rectangular cell with the game word and game properties.

    Keyword arguments:
    surf -- display surface of pygame.
    left -- pixel from the left of the screen for the left edge of the rectangular cell.
    top -- pixel from the top of the screen for the top edge of the rectangular cell.
    width -- width of the rectanglular cell
    height -- height of the rectanglular cell
    cell_colour -- initial cell colour
    word -- game word of the cell
    font_size = font size of the game word (default 24)
    cell_border -- border of the cell (default 0)
    '''
    def __init__(self, surf, left, top, width, height, cell_colour, word, font_size=24, cell_border=0):
        self.surf = surf
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.cell_colour = cell_colour
        self.word = word
        self.font_size = font_size
        self.cell_border = cell_border

    def draw_rect(self):
        '''Draw a shaded rectangle.'''
        pygame.draw.rect(self.surf, self.cell_colour, (self.left, self.top, self.width, self.height), self.cell_border)
        return

    def display_word(self):
        '''Display the game word.'''
        #Get an invisible rectangular surface for the word and configure its location.
        text_surf, text_rect = get_text_surf_and_pos(self.surf, self.word, colours.WHITE, \
                                                    self.font_size, self.left + (self.width/2), self.top + (self.height/2))

        #Overlay current word onto the game display surface and display it.
        self.surf.blit(text_surf, text_rect)
        pygame.display.update()
        return

def file_len(fname):
    '''Return an int for the number of lines a specified file has.
    Otherwise return -1 if specified file does not exist.
    '''
    #For empty files
    i = -1
    #Verify file exists
    try:
        f = open(fname, 'rb')
    except IOError:
        return -1

    #Open file and read the lines
    with f:
        for i, line in enumerate(f):
            pass
    return i + 1

def get_text_surf_and_pos(surf, string, colour, font_size, x, y, font=None):
    '''Return a surface object, its location, width and
    height on which text/string can be displayed on.

    Keyword arguments:
    surf -- surface to display the string on.
    string -- string to display onto screen.
    colour -- colour of the string.
    font_size -- font size of the string.
    x -- pixel from the left of the screen on which the middle of the string will be.
    y -- pixel from the top of the screen on which the vertical middle of the string will be.
    font -- font type of the string. None uses inbuilt default pygame font. (default None)
    '''
    font = pygame.font.Font(font, font_size)
    #Get an invisible rectangular surface for the word and configure its location.
    text_surf = font.render(string, True, colour)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    return text_surf, text_rect

def poll_for_exit():
    '''Runs an infinite loop waiting for user to exit pygame.'''
    while True:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT \
                or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()
    return

def game_loop(game_display):
    '''Main game loop.'''
    exit_game = False
    while exit_game is False:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT \
                or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()

        pygame.display.update()
    return

#Main code begins
if __name__ == '__main__':
    pygame.init()

    #Launch game window
    window_w = 700
    window_h = 400
    game_display = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
    game_display.fill(colours.WHITE)

    #Display error if the dictionary file is missing or if there are not enough words.
    word_count = file_len(DICTIONARY_FILE)
    error_msg = "Error: Too few words in the dictionary file to play the game!"
    if word_count < 20:
        if word_count == -1:
            error_msg = "Error: could not find the dictionary file!"
        text_surf, text_rect = get_text_surf_and_pos(game_display, error_msg, colours.PRIMARY_RED, \
                                                    45, window_w/2, window_h/2)

        #Overlay current message onto the game display surface and display it.
        game_display.blit(text_surf, text_rect)
        pygame.display.update()
        #Wait for user to exit pygame
        poll_for_exit()

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

    print("dictionary.csv file has", file_len(DICTIONARY_FILE), "lines")
    print("empty.csv file has", file_len("empty.csv"), "lines")
    print("yellow.csv file has", file_len("yellow.csv"), "lines")

    line = linecache.getline(DICTIONARY_FILE, 20278)
    print(line)

    word = 'hello'
    cell_list = []
    for i in range(0, rows):
        for j in range(0, cols):
            cell_list.append(Cell(game_display, margin_w + cell_w*j + gap_w*j, margin_h + cell_h*i + gap_h*i, cell_w, cell_h, colours.PRIMARY_RED, word))
            cell_list[-1].draw_rect()
            cell_list[-1].display_word()

    #Run the game
    game_loop(game_display)
