'''
Arithmology
-----------
Tool for translating numerical terms into the numbers they represent and 
vice versa.

There are six categories of terms:

Polyad: Greek nouns for describing n-sized groups
Tonal: Greek adjectives describing structures with n-tones
Basal: Latin adjectives describing structures of every n-th member of a group
Cardinal: English numerals for counting n-number of items
Ordinal: English numerals describing n-th position in a sequence
Uple: Latin adjectives describing n-sized groups

Examples
--------
Get a keyword by encoding a number in a particular category:
>>> encode(1, "ordinal")
'one'
>>> encode(2, "tonal")
'ditonic'
>>> encode(3, "polyad")
'triad'
>>> encode(7, "basal")
'septimal'
>>> encode(5, "uple")
'quintuple'

Get a number by decoding a keyword:
>>> decode("triskaidecad")
13
>>> decode("four")
4
>>> decode("seventh")
7
>>> decode("pentatonic")
5
>>> decode("tertial")
3
>>> decode("triple")
3

Get a keyword by encoding a number using a shortcut method:
>>> polyad(3)
'triad'
>>> tonal(7)
'heptatonic'
>>> ordinal(13)
'thirteenth'
>>> uple(8)
'octuple'
>>> cardinal(6)
'six'
'''

__all__ = [
    'columns', 
    'rows', 
    'decode', 
    'encode', 
    'polyad', 
    'tonal', 
    'basal', 
    'cardinal', 
    'uple'
]

POLYAD = 'polyad'
TONAL = 'tonal'
BASAL = 'basal'
CARDINAL = 'cardinal'
ORDINAL = 'ordinal'
UPLE = 'uple'

__table = [
    ['polyad', 'tonal', 'basal', 'cardinal', 'ordinal', 'uple'],
    ['monad', 'monotonic', 'primal', 'one', 'first', 'single'],
    ['dyad', 'ditonic', 'secundal', 'two', 'second', 'double'],
    ['triad', 'tritonic', 'tertial', 'three', 'third', 'triple'],
    ['tetrad', 'tetratonic', 'quartal', 'four', 'fourth', 'quadruple'],
    ['pentad', 'pentatonic', 'quintal', 'five', 'fifth', 'quintuple'],
    ['hexad', 'hexatonic', 'sextal', 'six', 'sixth', 'sextuple'],
    ['heptad', 'heptatonic', 'septimal', 'seven', 'seventh', 'septuple'],
    ['octad', 'octatonic', 'octonal', 'eight', 'eighth', 'octuple'],
    ['ennead', 'enneatonic', 'nonal', 'nine', 'ninth', 'nonuple'],
    ['decad', 'decatonic', 'decimal', 'ten', 'tenth', 'decuple'],
    ['hendecad', 'hendecatonic', 'undecimal',
        'eleven', 'eleventh', 'hendecuple'],
    ['duodecad', 'duodecatonic', 'duodecimal',
        'twelve', 'twelfth', 'duodecuple'],
    ['triskaidecad', 'triskaidecatonic', 'tredecimal',
        'thirteen', 'thirteenth', 'tredecuple'],
    ['tettarakaidecad', 'tettarakaidecatonic', 'quattuordecimal',
        'fourteen', 'fourteenth', 'quattuordecuple'],
    ['pentekaidecad', 'pentekaidecatonic', 'quindecimal',
        'fifteen', 'fifteenth', 'quindecuple']
]


def columns() -> list[str]:
    '''Return the headings of the table.'''
    return __table[0]


def rows() -> list[list[str]]:
    '''Return the values of the table'''
    return [__table[x] for x in range(1, len(__table))]

def decode(keyword: str) -> int:
    '''Return the number represented by the given keyword.'''
    for i, row in enumerate(__table):
        for word in row:
            if keyword == word:
                return i
    raise ValueError(f"Unknown keyword: {keyword}")

def encode(category: str, number: int) -> str:
    '''Return the keyword that represents the given number in the given 
    category.
    '''
    if not category in columns():
        raise ValueError(f"Unknown category: {category}")
    if not number in range(1, len(__table)):
        raise ValueError(f"Cannot encode number: {number}")
    i = columns().index(category)
    return __table[number][i]

def polyad(number: int) -> str:
    '''Return the polyad keyword for the given number.'''
    return encode("polyad", number)


def tonal(number: int) -> str:
    '''Return the tonal keyword for the given number.'''
    return encode("tonal", number)

def basal(number: int) -> str:
    '''Return the basal keyword for the given number.'''
    return encode("basal", number)


def cardinal(number: int) -> str:
    '''Return the cardinal keyword for the given number.'''
    return encode("cardinal", number)


def uple(number: int) -> str:
    '''Return the -uple keyword for the given number.'''
    return encode("uple", number)
