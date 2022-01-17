from unittest import TestCase, main
from interpreter import Token, TokenType

class Token_test:
    def token_tests(self):
        token=Token(TokenType.DOT,'.')
        self.assertEqual(token.type_,TokenType.DOT)
        
        
        
if __name__ == "__main__":
    main()