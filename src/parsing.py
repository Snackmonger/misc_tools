"""
Simple base classes for building text and token crawlers.

These classes provide the boilerplate code for situations in which you want to
roll your own tokenizer/lexer or parser. You must provide the main tokenize()
or parse() functions in your subclass. 
"""
from enum import Enum
from typing import Optional


class Token:
    """Generic token."""
    def __init__(self, token_type: Enum, lexeme: str) -> None:
        self.token_type = token_type
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f"<{self.token_type}: {self.lexeme}>"


class Tokenizer:
    """Base functions for a generic tokenizer."""
    def __init__(self):
        self.text: str = ""
        self.current: int = 0
        self.start: int = 0
        self.tokens: list[Token] = []
        self.line: int = 0
        self.line_chars: int = 0

    def advance(self) -> str:
        """Advance the tokenizer and return the new current character."""
        char = self.peek
        self.current += 1
        self.line_chars += 1
        return char

    @property
    def is_at_end(self) -> bool:
        """Signal whether we have reached the end of the stream."""
        return self.current >= len(self.text)

    @property
    def peek(self) -> str:
        """Return the current character without consuming it."""
        if self.is_at_end:
            return "\0"
        return self.text[self.current]

    @property
    def previous(self) -> str:
        """Peek at the previous character."""
        return self.text[self.current - 1]


class Parser:
    """Base functions for a generic parser."""

    def __init__(self) -> None:
        self.tokens: list[Token] = []
        self.current: int = 0
        self.start: int = 0
        self.errors: list[str] = []

    def advance(self) -> Token:
        """Move the cursor forward and return the now-previous token."""
        token = self.tokens[self.current]
        self.current += 1
        return token

    @property
    def is_at_end(self) -> bool:
        """Flag whether all tokens have been parsed."""
        return self.current >= len(self.tokens) - 1

    @property
    def previous(self) -> Token:
        """Return the token at the previous index, if it exists."""
        if self.current >= 1:
            return self.tokens[self.current - 1]
        raise RuntimeError("Called previous at index 0.")

    @property
    def peek(self) -> Token:
        """Return the token at the current index without moving the cursor."""
        return self.tokens[self.current]

    @property
    def peek_next(self) -> Optional[Token]:
        """Return the token at the next index without moving the cursor."""
        if not self.is_at_end:
            return self.tokens[self.current + 1]
        return None

    def match(self, *args: Enum) -> bool:
        """Test whether the given token(s)' type matches the type of the next
        token in the stream. If so, also advance the cursor.
        """
        for arg in args:
            if self.check(arg):
                self.advance()
                return True
        return False

    def check(self, token_type: Enum) -> bool:
        """Test whether the given token type is the same as the type at the 
        current index.
        """
        return self.peek.token_type == token_type

    def consume(self, token_type: Enum, message: str) -> Optional[Token]:
        """Consume a token."""
        if self.check(token_type):
            return self.advance()
        self.error(message)
        return None

    def error(self, message: str) -> None:
        """Register an error."""
        self.errors.append(message)