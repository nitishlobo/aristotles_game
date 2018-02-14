'''Pygame wrappers.

    Imports:
    pygame

    Key functions:
    get_text_surf_and_pos -- Return a surface object, its location, width and
                              height on which text/string can be displayed on.
'''
import pygame

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
