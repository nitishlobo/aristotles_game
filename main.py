#TODO: CTRL+FIND ALL THE TODO'S AND DO THEM
#TODO: ADD A FILE DESCRIPTIONS
#TODO: BREAK THIS FILE INTO MULTIPLE FILES IN MULTIPLE DIRECTORIES. \
#   ONE OF THE DIRECTORIES WOULD BE COMMON PYGAME FUNCTIONS.

from random import seed, randint
import linecache
import pygame
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
    init_colour -- initial cell colour
    word -- game word of the cell
    team -- which team the word belongs too. 0 - netural, -1 - death word, 1 - team A, 2 - team B.
    team_col -- colour of the team that the word in the cell belongs to.
    font_size = font size of the game word (default 24)
    cell_border -- border of the cell (default 0)
    '''
    def __init__(self, surf, left, top, width, height, init_col, word, team, team_col, font_size=24, cell_border=0):
        self.surf = surf
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.init_col = init_col
        self.word = word
        self.team = team
        self.team_col = team_col
        self.font_size = font_size
        self.cell_border = cell_border

    def draw_rect(self):
        '''Draw a shaded rectangle.'''
        pygame.draw.rect(self.surf, self.init_col, \
                        (self.left, self.top, self.width, self.height), self.cell_border)
        return

    def display_word(self):
        '''Display the game word.'''
        #Get an invisible rectangular surface for the word and configure its location.
        tsurf, trect = get_text_surf_and_pos(str(self.word), colours.WHITE, self.font_size, \
                            self.left + (self.width/2), self.top + (self.height/2))

        #Overlay current word onto the game display surface and display it.
        self.surf.blit(tsurf, trect)
        pygame.display.update()
        return

    def reveal_team(self):
        '''Colour the cell with the colour of the team that the word belongs to.'''
        pygame.draw.rect(self.surf, self.team_col, \
                        (self.left, self.top, self.width, self.height), self.cell_border)
        self.display_word()
        return

def get_indexes(amount, game_size, exclude=[None]):
    '''Return a list of random indexes indicating the position of words.
    For example, if amount of neutral words needed is 4 for a game size of 30,
    then pass a list of indexes that have already been assigned for death words
    so that these can be excluded.

    Keyword arguments:
    amount -- number of indexes required.
    game_size -- total number of words in the game.
    exclude -- list of forbidden indexes.
    '''
    seed(None)
    indexes = []
    for i in range(amount):
        new_index = randint(0, game_size-1)
        while (new_index in indexes) or (new_index in exclude):
            new_index = randint(0, game_size-1)
        indexes.append(new_index)
    return indexes

def file_len(fname):
    '''Return an int for the number of lines a specified file has.
    Otherwise return -1 if specified file does not exist.
    '''
    #For empty files
    line_count = -1
    #Verify file exists
    try:
        f = open(fname, 'rb')
    except IOError:
        return -1

    #Open file and read the lines
    with f:
        for line_count, line in enumerate(f):
            pass
    return line_count + 1

#TODO: BUGFIX - PROVIDE OPTION TO RESIZE THE TEXT TO FIT WITHIN A
#   SPECIFIED RECTANGULAR WIDTH & HEIGHT
def get_text_surf_and_pos(string, colour, font_size, x, y, font=None):
    '''Return a surface object, its location, width and
    height on which text/string can be displayed on.

    Keyword arguments:
    string -- bytes type string to display onto screen.
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

def get_team_colour(team):
    '''Returns the colour of a team.'''
    #Death 'team'
    if team == -1:
        return colours.BLACK
    elif team == 1:
        return colours.PRIMARY_BLUE
    elif team == 2:
        return colours.PRIMARY_GREEN
    #Neutral 'team'
    return colours.SILVER

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

def game_loop():
    '''Main game loop.'''
    exit_game = False
    while exit_game is False:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT \
            or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()

            # if event.type == pygame.MOUSEBUTTONDOWN:
                #TODO: IF PLAYER CLICKS ON CELL, THEN REVEAL THE CELL'S TEAM COLOUR.

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
    dict_count = file_len(DICTIONARY_FILE)
    error_msg = "Error: Insufficient dictionary words to play the game!"
    if dict_count < 20:
        if dict_count == -1:
            error_msg = "Error: could not find the dictionary file!"
        esurf, erect = get_text_surf_and_pos(game_display, error_msg, colours.PRIMARY_RED, \
                                                    35, window_w/2, window_h/2)

        #Overlay current message onto the game display surface and display it.
        game_display.blit(esurf, erect)
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

    #Use system clock to generate random numbers
    seed(None)
    #Randomly assign each word to 1 of 2 teams
    teams = [randint(1, 2) for i in range(rows*cols)]
    #Assign 2 words to death 'team' if game has more than 25 words.
    if rows*cols > 25:
        deaths = get_indexes(2, rows*cols)
    else:
        deaths = get_indexes(1, rows*cols)

    for i in deaths:
        teams[i] = -1

    #Assign words to neutral 'team'
    neutrals = get_indexes(int(((rows*cols)/5) - len(deaths)), rows*cols, deaths)
    for i in neutrals:
        teams[i] = 0

    cell_list = []
    for i in range(rows):
        for j in range(cols):
            #Get a word from the dictionary and clear the cache afterwords
            w = linecache.getline(DICTIONARY_FILE, randint(1, dict_count)).strip('\n\r\t')
            linecache.clearcache()

            #Generate a cell and display the game words
            cell_list.append(Cell(game_display, margin_w + cell_w*j + gap_w*j, \
                margin_h + cell_h*i + gap_h*i, cell_w, cell_h, \
                colours.ROYAL_PURPLE, w, \
                teams[i*cols + j], get_team_colour(teams[i*cols + j])))
            cell_list[-1].draw_rect()
            cell_list[-1].display_word()

    # for i in range(rows*cols):
        # cell_list[i].reveal_team()

    #Run the game
    game_loop()
