from .lexer import Lexer
from .node import Assignment, BinOp, Node, Float, UnaryOp, Var, StatementList, Empty
from .tokens import Token, TokenType


class ParserException(Exception):
    pass

class Parser():
    
    def __init__(self):
        self._current_token: Token = None
        self._lexer = Lexer()

    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            raise ParserException(f"invalid token order. Found \"{self._current_token.value}\", expected {type_}")

    def _factor(self) -> Node:
        token = self._current_token
        if token.type_ == TokenType.MINUS:
            self._check_token_type(TokenType.MINUS)
            return UnaryOp(token, self._factor())
        if token.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
            return UnaryOp(token, self._factor())
        if token.type_ == TokenType.FLOAT:
            self._check_token_type(TokenType.FLOAT)
            return Float(token)
        if token.type_ == TokenType.LPAREN:
            self._check_token_type(TokenType.LPAREN)
            result = self._expr()
            self._check_token_type(TokenType.RPAREN)
            return result
        if token.type_ == TokenType.VAR:
            return self._variable()
        raise ParserException("invalid factor")

    def _term(self) -> Node:
        result=self._factor()
        ops = [TokenType.MUL, TokenType.DIV]
        while self._current_token.type_ in ops:
            token = self._current_token
            if token.type_ == TokenType.MUL:
                self._check_token_type(TokenType.MUL)
            else:
                self._check_token_type(TokenType.DIV)
            result = BinOp(result, token, self._factor())
        return result
        
    def _expr(self) -> Node:
        result = self._term()
        ops = [TokenType.PLUS, TokenType.MINUS]
        while self._current_token.type_ in ops:
            token = self._current_token
            if token.type_ == TokenType.PLUS:
                self._check_token_type(TokenType.PLUS)
            else:
                self._check_token_type(TokenType.MINUS)
            result = BinOp(result, token, self._term())
        return result
    
    def _variable(self) -> Node:
        token = self._current_token
        self._check_token_type(TokenType.VAR)
        variable = Var(token)
        return variable

    def _assignment(self) -> Node:
        variable = self._variable()
        op = self._current_token
        self._check_token_type(TokenType.ASSIGN)
        expr = self._expr()
        return Assignment(variable, op, expr)

    def _statement(self) -> Node:
        if self._current_token.type_ == TokenType.COMMAND and self._current_token.value=="BEGIN":
            return self._complex_statement()
        elif self._current_token.type_ == TokenType.VAR:
            return self._assignment()
        else:
            return Empty()

    def _statement_list(self) -> Node:
        result = StatementList()
        result.list.append(self._statement())
        while self._current_token.type_ == TokenType.DOTCOM:
            self._check_token_type(TokenType.DOTCOM)
            if self._current_token.type_ != TokenType.COMMAND or self._current_token.value!="END":
                result.list.append(self._statement())
            else:
                return result
        return result

    def _complex_statement(self) -> Node:        
        if(self._current_token.type_==TokenType.COMMAND and self._current_token.value=="BEGIN"):
            self._current_token=self._lexer.next()
            result = self._statement_list()
            if(self._current_token.type_==TokenType.COMMAND and self._current_token.value=="END"):
                self._current_token=self._lexer.next()
                return result
            else:
                raise ParserException(f"invalid token order. Found \"{self._current_token.value}\", expected END")
        else:
            raise ParserException(f"invalid token order. Found \"{self._current_token.value}\", expected BEGIN")

    def _program(self) -> Node:
        result = self._complex_statement()
        self._check_token_type(TokenType.DOT)
        return result

    def __call__(self, text : str) -> Node:
        return self.parse(text)

    def parse(self, text : str) -> Node:
        self._lexer.init(text)
        self._current_token = self._lexer.next()
        return self._program()
