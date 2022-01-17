from enum import Enum, auto


class TokenType(Enum):
    FLOAT = auto()
    PLUS = auto()
    MINUS = auto()
    LPAREN = auto()
    RPAREN = auto()
    MUL = auto()
    DIV = auto()
    VAR = auto()
    COMMAND = auto()
    ASSIGN = auto()
    DOTCOM = auto()
    DOT = auto()
    EOS = auto()

class Token():
    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type_}, {self.value})"

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return(self.type_ == other.type_ and self.value == other.value)
