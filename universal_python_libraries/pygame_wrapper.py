'''Pygame wrappers.

    Imports:
    pygame

    Key class:
    Rectangle -- Draw a rectangle on an existing surface

    Key functions:
    get_text_surf_and_pos -- Return a surface object, its location, width and
                              height on which text/string can be displayed on.
'''
import pygame

class Rectangle(object):
    '''Draw a rectangle on an existing surface

    Keyword arguments:
    surf -- display the rectangle on top of this surface.
    left -- pixel from the left of the screen for the left edge of the rectangular cell.
    top -- pixel from the top of the screen for the top edge of the rectangular cell.
    width -- width of the rectanglular cell
    height -- height of the rectanglular cell
    init_colour -- initial cell colour
    text -- text to display inside this rectangle
    font_size = font size of the game word (default 30)
    cell_border -- border of the cell (default 0)
    '''
    def __init__(self, surf, left, top, width, height, init_col, text, font_size=30, cell_border=0):
        self.surf = surf
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.init_col = init_col
        self.text = text
        self.font_size = font_size
        self.cell_border = cell_border

    def draw_rect(self):
        '''Draw a shaded rectangle.'''
        pygame.draw.rect(self.surf, self.init_col, \
                        (self.left, self.top, self.width, self.height), self.cell_border)
        return

    def display_text(self):
        '''Display the text.'''
        #Get an invisible rectangular surface for the word and configure its location.
        tsurf, trect = get_text_surf_and_pos(str(self.text), colours.WHITE, \
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

def get_text_surf_and_pos(string, colour, font_size, x, y, align='center', font=None, frame=(0, 0)):
    '''Return a surface object, its location, width and
    height on which text/string can be displayed on.

    Keyword arguments:
    string -- bytes-type string to display onto screen.
    colour -- colour of the string.
    font_size -- font size of the string.
    x -- pixel from the left of the screen on which the top/middle of the string will be depending on the align parameter.
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
