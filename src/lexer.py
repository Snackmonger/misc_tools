'''
A simple lexer to parse text into token classes.

This program is basically a simplified version of:
https://github.com/lark-parser/lark/blob/master/lark/lexer.py

Example
-------
>>> templates_ = (
...     TokenTemplate('IDENTIFIER', r"[a-z_][a-z0-9_]*"),
...     TokenTemplate('TOKEN', r"[A-Z_][A-Z0-9_]*"),
...     TokenTemplate('LITERAL', r"'[ A-Za-z_0-9.,!\\"'\\$]+'"),
...     TokenTemplate('LITERAL', r'"[ A-Za-z_0-9.,!"\\'\\$]+"'),
...     TokenTemplate('LITERAL', r'\\d+', int),
...     TokenTemplate('OPERATOR', r"::="),
...     TokenTemplate('OPERATOR', r"\\*"),
...     TokenTemplate('OPERATOR', r"\\?"),
...     TokenTemplate('OPERATOR', r"\\+"),
...     TokenTemplate('OPERATOR', r"\\|"),
...     TokenTemplate('DELIMITER', r"\\)"),
...     TokenTemplate('DELIMITER', r"\\("),
...     TokenTemplate('WHITESPACE', r" "),
...     TokenTemplate("NEWLINE", r"\\n", lambda _: "\\n"),
...     TokenTemplate("FOR", r"for")
... )
>>> text_ = """
... name ::= definition ("," definition)*
... definition ::= TOKEN
... TOKEN ::= "literal" | "other 'nested' literal"
... forget ::= (for ::= forget for get)
... """
>>> lexer_ = Lexer(templates_)
>>> for x in lexer_.tokenize(text_, filter_types=['NEWLINE', 'WHITESPACE']):
...     print(x)
Token(IDENTIFIER, name, 2[1])
Token(OPERATOR, ::=, 2[6])
Token(IDENTIFIER, definition, 2[10])
Token(DELIMITER, (, 2[21])
Token(LITERAL, ",", 2[22])
Token(IDENTIFIER, definition, 2[26])
Token(DELIMITER, ), 2[36])
Token(OPERATOR, *, 2[37])
Token(IDENTIFIER, definition, 3[1])
Token(OPERATOR, ::=, 3[12])
Token(TOKEN, TOKEN, 3[16])
Token(TOKEN, TOKEN, 4[1])
Token(OPERATOR, ::=, 4[7])
Token(LITERAL, "literal", 4[11])
Token(OPERATOR, |, 4[21])
Token(LITERAL, "other 'nested' literal", 4[23])
Token(IDENTIFIER, forget, 5[1])
Token(OPERATOR, ::=, 5[8])
Token(DELIMITER, (, 5[12])
Token(FOR, for, 5[13])
Token(OPERATOR, ::=, 5[17])
Token(IDENTIFIER, forget, 5[21])
Token(FOR, for, 5[28])
Token(IDENTIFIER, get, 5[32])
Token(DELIMITER, ), 5[35])
'''
from __future__ import annotations
import re
from typing import Any, Callable, Optional, Sequence

NEWLINE = "\n"

class UnknownSymbolError(Exception):
    '''Error signifying that the lexer could not parse the symbol at the
    current program counter index'''
    def __init__(self, text: str, line: int, col: int) -> None:
        excerpt = text.split(NEWLINE)[line - 1]
        diagram = "-" * (col - 1) + "^"
        errmsg = f"""Unable to parse symbol at position {col} on line {line}.\n\tNear here:\n\t\t{excerpt}\n\t\t{diagram}"""
        super().__init__(errmsg)

class Token:
    '''
    The lexical category to which a text segment belongs, as well as
    its location in the source text, both literally and when newlines are
    considered.
    '''
    __slots__ = "token_type", "lexeme", "start", "end", "line", "column"

    def __init__(self,
                 token_type: str,
                 lexeme: Any,
                 start: int,
                 end: int,
                 line: int,
                 column: int
                 ) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.start = start
        self.end = end
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"Token({self.token_type}, {self.lexeme}, {self.line}[{self.column}])"
    
    def __len__(self) -> int:
        return len(str(self.lexeme))

class TokenTemplate:
    '''
    The formula for generating a token.

    This class is used by the lexer to generate tokens according to the 
    current input. Each token template associates a [regular_expression] 
    with a [token_type] key name. An optional [callback] allows the template
    to transform the literal value of the matching lexeme.

    Example
    -------
    >>> x = TokenTemplate('LITERAL', r'\\d+', int)
    >>> y = x.match("1234567890", 0, 0, 0)
    >>> y
    Token(LITERAL, 1234567890, 0[0])
    >>> assert isinstance(y.lexeme, int)
    '''
    __slots__ = "token_type", "regular_expression", "callback"

    def __init__(self,
                 token_type: str,
                 regular_expression: str,
                 callback: Optional[Callable[[str], Any]] = None
                 ) -> None:
        self.token_type = token_type
        self.regular_expression = re.compile(regular_expression)
        self.callback = callback

    def match(self,
              text: str,
              start: int,
              line: int,
              column: int
              ) -> Optional[Token]:
        '''
        Check if a match can be made at the current position in the source
        [text] and generate a token if so, or None if not.
        '''
        matched = self.regular_expression.match(text, start)
        if not matched:
            return None
        end = matched.end()
        value = matched.group()
        for char in value:
            if char == NEWLINE:
                line += 1
                column = 1
        if self.callback:
            value = self.callback(value)
        return Token(self.token_type, value, start, end, line, column)


class ProgramCounter:
    '''The counter that keeps track of where the lexer is looking when reading
    the source text. 
    
    The token templates update the tokens with their own positional and size
    information, so the counter is only responsible for updating according
    to the data of the single token that is actually accepted.
    '''

    __slots__ = 'line', 'column', 'start', 'newline_char'

    def __init__(self):
        self.start = 0
        self.line = 1
        self.column = 1

    def current(self) -> tuple[int, int, int]:
        '''Return a the current position of the counter.'''
        return self.line, self.start, self.column

    def accept(self, token: Token) -> None:
        '''Accept the given token and adjust the counter according to
        the token's location data.'''
        if token.line != self.line:
            self.column = 1
        else:
            self.column += token.end - token.start
        self.start = token.end
        self.line = token.line


class Lexer:
    '''The reader that converts the raw text into lexical categories.
    
    The lexer is initialized with a list of [templates]. Then, the ``tokenize``
    method is called on a source text. The lexer crawls through the source
    text and uses the templates to seek matches at the current position.
    If no match is found, the program crashes. If multiple matches are found,
    the match with the longest literal is accepted. When a match is accepted,
    the program counter moves forward according to the length of the matching
    literal.
    '''
    __slots__ = "templates", "tokens", "line_counter"

    def __init__(
            self,
            templates: Sequence[TokenTemplate]
            ) -> None:
        self.templates = templates or tuple()
        self.tokens: list[Token]
        self.line_counter: ProgramCounter

    def __best(self, best: Token, other: Token) -> Token:
        # this could be a strategy passed in at runtime...?
        return best if len(best.lexeme) > len(other.lexeme) else other

    def __accept(self, token: Token) -> None:
        self.tokens.append(token)
        self.line_counter.accept(token)

    @property
    def __start(self) -> int:
        return self.line_counter.start

    @property
    def __line(self) -> int:
        return self.line_counter.line

    @property
    def __column(self) -> int:
        return self.line_counter.column

    def tokenize(self, text: str, filter_types: Optional[Sequence[str]] = None) -> tuple[Token, ...]:
        '''Attempt to sort a source [text] into lexical categories, represented
        as tokens.
        
        IMPORTANT: The lexer does not ignore whitespaces, newlines, tabs, etc. 
        by default. You must define a token template to capture unwanted 
        characters, then you can add them to the a list of [filter_types],
        which will omit tokens with those labels from the final return.
        '''
        filter_types = filter_types or []
        self.tokens: list[Token] = []
        self.line_counter = ProgramCounter()
        while not self.__start == len(text):
            best: Optional[Token] = None
            for template in self.templates:
                token = template.match(
                    text, self.__start,  self.__line, self.__column)
                if not token:
                    continue
                if not best:
                    best = token
                else:
                    best = self.__best(best, token)
            if not best:
                raise UnknownSymbolError(text, self.__line, self.__column)
            self.__accept(best)
        return tuple(x for x in self.tokens if not x.token_type in filter_types)

