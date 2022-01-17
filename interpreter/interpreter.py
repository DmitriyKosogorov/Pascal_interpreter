import operator
from typing import Union
from .node import Assignment, BinOp, Node, Float, UnaryOp, Var, StatementList, Empty
from .tokens import TokenType
from .parser import Parser


class InterpreterException(Exception):
    pass

class Interpreter():

    def __init__(self) -> None:
        self.var_list = {}

    def __call__(self, tree: Node, mode:str='1') -> dict:
        return self.interpret(tree,mode)
    
    def interpret(self, text:str,mode:str='1') -> dict:
        if(mode in ['1','2']):
            parser = Parser()
            tree=parser(text)
            if(mode=='2'):
                return(tree)
            self._visit(tree)
            return self.var_list
        else:
            raise InterpreterException("invalid mode")

    def _visit(self, node: Node):
        if isinstance(node, Float):
            return self._visit_float(node)
        elif isinstance(node, BinOp):
            return self._visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self._visit_unop(node)
        elif isinstance(node, Empty):
            return self._visit_empty(node)
        elif isinstance(node, Assignment):
            return self._visit_assignment(node)
        elif isinstance(node, Var):
            return self._visit_variable(node)
        elif isinstance(node, StatementList):
            return self._visit_statement_list(node)
        raise InterpreterException("invalid node")

    def _visit_float(self, node: Float) -> Union[int, float]:
        try:
            return int(node.token.value)
        except ValueError:
            return float(node.token.value)

    def _visit_unop(self, node: UnaryOp) -> Union[int, float]:
        op = node.op
        if op.type_ == TokenType.MINUS:
            return -self._visit(node.right)
        elif op.type_ == TokenType.PLUS:
            return self._visit(node.right)
        raise InterpreterException("invalid unary operator")

    def _visit_binop(self, node: BinOp) -> Union[int, float]:
        op = node.op
        binop = {TokenType.PLUS: operator.add,
                 TokenType.MINUS: operator.sub,
                 TokenType.DIV: operator.truediv,
                 TokenType.MUL: operator.mul}.get(op.type_)
        if binop:
            return binop(self._visit(node.left), self._visit(node.right))
        raise InterpreterException("invalid operator")
    
    def _visit_empty(self, node: Empty) -> None:
        pass

    def _visit_assignment(self, node: Assignment) -> None:
        self.var_list[node.left.token.value] = self._visit(node.right)

    def _visit_variable(self, node: Var) -> Union[int, float]:
        if node.token.value not in self.var_list:
            raise InterpreterException(f"name '{node.token.value}' is not defined")
        return self.var_list[node.token.value]

    def _visit_statement_list(self, node: StatementList) -> None:
        for item in node.list:
            self._visit(item)
