import math

def get_input(message: str, handler, context=None):
     while True:
        inp = input(message)
        result = handler(inp, context)