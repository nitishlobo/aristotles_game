#TODO: CTRL+FIND ALL THE TODO'S AND DO THEM
#TODO: ADD A FILE DESCRIPTION

from random import seed, randint
import linecache
import pygame
import colours

#English words dictionary.
DICTIONARY_FILE = 'dictionary.csv'
SCORE = ['Score to win: ', 'Team 1: ', 'Team 2: ']

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
    def __init__(self, surf, left, top, width, height, init_col, word, team, team_col, font_size=30, cell_border=0):
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
        tsurf, trect = get_text_surf_and_pos(str(self.word), colours.WHITE, \
                                            self.font_size, self.left + (self.width/2), \
                                            self.top + (self.height/2), frame=(self.width, self.height))

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



def get_text_surf_and_pos(string, colour, font_size, x, y, align='center', font=None, frame=(0, 0)):
    '''Return a surface object, its location, width and
    height on which text/string can be displayed on.

    Keyword arguments:
    string -- bytes type string to display onto screen.
    colour -- colour of the string.
    font_size -- font size of the string.
    x -- pixel from the left of the screen on which the middle of the string will be.
    y -- pixel from the top of the screen on which the vertical middle of the string will be.
    align -- either 'left' or 'center' alignment of text. (default 'center')
            Indicates whether the x argument given is left or center.
    font -- font type of the string. None uses inbuilt default pygame font. (default None)
    frame -- shrink text to be within the specified frame (width, height). (default (0, 0)
             0 for width and/or height will mean that particular parameter
             is ignored as a shrink parameter.
    '''
    f = pygame.font.Font(font, font_size)
    #Shrink text to be within frame if frame is defined
    if frame[0] > 0 or frame[1] > 0:
        while (f.size(string)[0] > frame[0] and frame[0] != 0) \
        or (f.size(string)[1] > frame[1] and frame[1] != 0):
            font_size -= 1
            f = pygame.font.Font(font, font_size)

    #Get an invisible rectangular surface for the word and configure its location.
    text_surf = f.render(string, True, colour)
    text_rect = text_surf.get_rect()
    if align.lower() == 'left':
        text_rect.left = x
        text_rect.centery = y
    else:
        text_rect.center = (x, y)
    return text_surf, text_rect

def update_score(display, font_size, win_score, score_t1, score_t2):
    '''Display score needed to win and also each teams score.

    Keywords arguments:
    display -- display surface of the game
    score_text -- list of score texts to display
    win_score -- score needed to win
    score_t1 -- team 1 score
    score_t2 -- team 2 score
    '''
    #TODO: BUGFIX - WHEN A CELL IS CLICKED, NEW SCORE IS OVERLAYED ON TOP OF THE PREVIOUS SCORE.
    #   NEED TO BLIT THAT PART OF THE SCREEN TO A BLANK BACKGROUND FIRST.
    win_surf, win_rect = get_text_surf_and_pos(SCORE[0]+str(win_score), colours.BLACK, font_size, 2, font_size/2, 'left')
    sc1_surf, sc1_rect = get_text_surf_and_pos(SCORE[1]+str(score_t1), colours.BLACK, font_size, 2, int(font_size*1.25), 'left')
    sc2_surf, sc2_rect = get_text_surf_and_pos(SCORE[2]+str(score_t2), colours.BLACK, font_size, 2, int(font_size*2), 'left')
    display.blit(win_surf, win_rect)
    display.blit(sc1_surf, sc1_rect)
    display.blit(sc2_surf, sc2_rect)
    pygame.display.update()
    return

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

def game_loop(display, win_score, cells):
    '''Main game loop

    Keyword arguments:
    display -- game_display
    win_score -- score needed to win
    cells -- list of the 'cell' class for the game
    '''
    #Initialise scores
    score_t1 = 0
    score_t2 = 0
    score_font_size = 30
    update_score(display, score_font_size, win_score, score_t1, score_t2)

    exit_game = False
    while exit_game is False:
        for event in pygame.event.get():
            #Exit pygame display and python script
            if event.type == pygame.QUIT \
            or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()

            #Reveal the cell's team colour when player clicks on it.
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for c in cells:
                    if c.left < x < c.left+c.width and c.top < y <  c.top+c.height:
                        c.reveal_team()
                        #Update score
                        #TODO: END GAME IF DEATH WORD HAS BEEN DISCOVERED.
                        #   KEEP THE WORDS FOR THE TEAM TO BE ABLE TO DISCUSS WHAT WENT DOWN.
                        if c.team == 1:
                            score_t1 += 1
                        elif c.team == 2:
                            score_t2 += 1
                            update_score(display, score_font_size, win_score, score_t1, score_t2)

        pygame.display.update()
    return

#Main code begins
if __name__ == '__main__':
    pygame.init()

    #Launch game window
    window_w = 900
    window_h = 600
    game_display = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
    game_display.fill(colours.WHITE)

    #Display error if the dictionary file is missing or if there are not enough words.
    dict_count = file_len(DICTIONARY_FILE)
    font_size = 30
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
    score_h = font_size*3
    cell_w = window_w/(cols+3)
    cell_h = (window_h - score_h)/(rows+3)

    #Determine grid 'white' space border size
    margin_w = cell_w/2
    margin_h = cell_h/2 + score_h

    #Determine gap sizes between cells in the grid
    gap_w = (cell_w*2)/(cols-1)
    gap_h = (cell_h*2)/(rows-1)

    #Use system clock to generate random numbers
    seed(None)
    #Assign all words to neutral 'team'
    teams = [0 for i in range(rows*cols)]

    #Assign 2 words to death 'team' if game has more than 25 words.
    if rows*cols > 25:
        deaths = get_indexes(2, rows*cols)
    else:
        deaths = get_indexes(1, rows*cols)

    #Assign 40% of total words to each team
    score_to_win = int((2*rows*cols)/5)
    team_1 = get_indexes(score_to_win, rows*cols, deaths)
    team_2 = get_indexes(score_to_win, rows*cols, deaths + team_1)

    #Finish team assignments
    for i in deaths:
        teams[i] = -1
    for i in team_1:
        teams[i] = 1
    for i in team_2:
        teams[i] = 2

    cell_list = []
    for i in range(rows):
        for j in range(cols):
            #Get a word from the dictionary and clear the cache afterwords
            w = linecache.getline(DICTIONARY_FILE, randint(1, dict_count)).strip('\n\r\t')
            linecache.clearcache()

            #Generate a cell and display the game words
            cell_list.append(Cell(game_display, margin_w + cell_w*j + gap_w*j, \
                                margin_h + cell_h*i + gap_h*i, cell_w, \
                                cell_h, colours.ROYAL_PURPLE, \
                                w, teams[i*cols + j], \
                                get_team_colour(teams[i*cols + j])))
            cell_list[-1].draw_rect()
            cell_list[-1].display_word()

    #TODO: BREAK THIS FILE INTO MULTIPLE FILES IN MULTIPLE DIRECTORIES. \
    #   ONE OF THE DIRECTORIES WOULD BE COMMON PYGAME FUNCTIONS.
    #TODO: CREATE A CLASS CALLED GAME AND HAVE SCORE COUNTER VARIABLES, SCORE STRINGS ALL IN THERE.
    #   FILES TO SPLIT INTO SO THAT THIS PROGRAM IS MORE OOP:
    #       1) GENERIC PYTHON LIBRARIES (eg. colours, reading from files, etc.)
    #       2) GENERIC PYGAME RELATED FUNCTIONS & CLASSES (eg: displaying text, etc...)
    #       3) PYGAME CLASSES RELATED ONLY SPECIFICALLY TO THIS GAME
    #Run the game
    game_loop(game_display, score_to_win, cell_list)
