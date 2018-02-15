'''Universal python wrappers.

    Imports:
    random

    Key functions:
    get_unique_random_numbers -- Return a list of random integers between a specified range.
                                 Also exclude a set of specified numbers from the returned list.
    file_len                  -- Return (as an int) the number of lines a specified file has.
'''
from random import seed, randint

def get_unique_random_numbers(amount, start, end, exclude=[None]):
    '''Return a list of random integer numbers between a start number and an end number (both inclusive)
    that are a unique set (ie. no duplicates in the list). Also exclude specified numbers from this set.

    Keyword arguments:
    amount -- amount of numbers required. Eg. setting this to 4 will return a list of 4 numbers.
    start -- smallest integer number allowed to be in the returned list.
    end -- largest integer number allowed to be in the returned list.
    exclude -- list of numbers that should not appear in the returned list (default [None]).
    '''
    #Use system clock to generate random numbers
    seed(None)
    numbers = []
    for i in range(amount):
        n = randint(start, end)
        while (n in numbers) or (n in exclude):
            n = randint(start, end)
        numbers.append(n)
    return numbers

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
