#TODO: CTRL+FIND ALL THE TODO'S AND DO THEM
#TODO: ADD A FILE DESCRIPTION

#TODO: CREATE A WIKI INSTRUCTION SET ON HOW TO PLAY THE GAME

from random import seed, randint
import linecache
import pygame
from universal_python_libraries import python_wrapper as pw
from universal_python_libraries import pygame_wrapper as gw
from universal_python_libraries import colours

#English words dictionary.
DICTIONARY_FILE = 'common_words_dictionary.csv'
SCORE = ['Score to win: ', 'Team 1: ', 'Team 2: ']
GAME_BACKGROUND_COLOUR = colours.WHITE

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
        tsurf, trect = gw.get_text_surf_and_pos(str(self.word), colours.WHITE, \
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

def update_score(display, font_size, win_score, score_t1, score_t2):
    '''Display score needed to win and also each teams score.

    Keywords arguments:
    display -- display surface of the game
    score_text -- list of score texts to display
    win_score -- score needed to win
    score_t1 -- team 1 score
    score_t2 -- team 2 score
    '''
    #Create surface and rectangular objects from text
    win_surf, win_rect = gw.get_text_surf_and_pos(SCORE[0]+str(win_score), colours.BLACK, font_size, 2, font_size/2, 'left')
    sc1_surf, sc1_rect = gw.get_text_surf_and_pos(SCORE[1]+str(score_t1), colours.BLACK, font_size, 2, int(font_size*1.25), 'left')
    sc2_surf, sc2_rect = gw.get_text_surf_and_pos(SCORE[2]+str(score_t2), colours.BLACK, font_size, 2, int(font_size*2), 'left')

    #Clear current scores on the screen by drawing a blank square (ie. same colour as the background) on top of it.
    clear_win_surf = win_surf.copy()
    clear_sc1_surf = sc1_surf.copy()
    clear_sc2_surf = sc2_surf.copy()
    clear_win_surf.fill(GAME_BACKGROUND_COLOUR)
    clear_sc1_surf.fill(GAME_BACKGROUND_COLOUR)
    clear_sc2_surf.fill(GAME_BACKGROUND_COLOUR)
    display.blit(clear_win_surf, win_rect)
    display.blit(clear_sc1_surf, sc1_rect)
    display.blit(clear_sc2_surf, sc2_rect)

    #Display the scores on top of the cleared scores
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

def game_over(display):
    game_over_surf, game_over_rect = gw.get_text_surf_and_pos('Game over! Death word was chosen.', colours.BLACK, font_size,
                                                                display.get_width()/2, display.get_height()/2)
    #TODO: FINISH THIS SECTION TO DRAW A POP-UP BOX PROVIDING THE USER TO SELECT AN 'OK' OPTION
    display.blit(game_over_surf, game_over_rect)
    pygame.display.update()
    poll_for_exit()
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
                        #TODO: END GAME WHEN ONE OF THE TEAM WINS (ie. team score >= score to win).
                        if c.team == 1:
                            score_t1 += 1
                        elif c.team == 2:
                            score_t2 += 1
                        elif c.team == -1:
                            game_over(display)
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
    game_display.fill(GAME_BACKGROUND_COLOUR)

    #Display error if the dictionary file is missing or if there are not enough words.
    dict_count = pw.file_len(DICTIONARY_FILE)
    font_size = 30
    error_msg = "Error: Insufficient dictionary words to play the game!"
    if dict_count < 20:
        if dict_count == -1:
            error_msg = "Error: could not find the dictionary file!"
        esurf, erect = gw.get_text_surf_and_pos(game_display, error_msg, colours.PRIMARY_RED, \
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
        deaths = pw.get_unique_random_numbers(2, 0, rows*cols-1)
    else:
        deaths = pw.get_unique_random_numbers(1, 0, rows*cols-1)

    #Assign 40% of total words to each team
    score_to_win = int((2*rows*cols)/5)
    team_1 = pw.get_unique_random_numbers(score_to_win, 0, rows*cols-1, deaths)
    team_2 = pw.get_unique_random_numbers(score_to_win, 0, rows*cols-1, deaths + team_1)

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

    #TODO: CREATE A CLASS CALLED GAME AND HAVE SCORE COUNTER VARIABLES, SCORE STRINGS ALL IN THERE.
    #   FILES TO SPLIT INTO SO THAT THIS PROGRAM IS MORE OOP:
    #       1) GENERIC PYTHON LIBRARIES (eg. colours, reading from files, etc.)
    #       2) GENERIC PYGAME RELATED FUNCTIONS & CLASSES (eg: displaying text, etc...)
    #       3) PYGAME CLASSES RELATED ONLY SPECIFICALLY TO THIS GAME

    #TODO: CREATE A 'NEW GAME' BUTTON WHICH RESTARTS THE GAME.

    #Run the game
    game_loop(game_display, score_to_win, cell_list)
