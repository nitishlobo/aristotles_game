'''Universal python wrappers.

    Imports:
    --

    Key functions:
    file_len -- Return (as an int) the number of lines a specified file has.
'''

def file_len(fname):
    '''Return an int indicating the number of lines a specified file has.
    Otherwise return -1 if specified file does not exist.

    Keyword arguments:
    fname -- either file name or path to file.

    Examples:
    lines = file_len('dictionary.csv')
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
