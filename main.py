from interpreter import Interpreter

if __name__ == "__main__":
    interpreter = Interpreter()
    text='BEGIN\n x:= 2 + 3 * (2 + 3);\n y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));\n END.'
    print(interpreter(text))
    print(interpreter(text,mode='1'))
    print(interpreter(text,mode='2'))