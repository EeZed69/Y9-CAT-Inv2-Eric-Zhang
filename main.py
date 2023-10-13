import math

def get_input(message: str, handler, context=None):
     while True:
        inp = input(message)
        result = handler(inp, context)
        if result[0]:
           return result[1]
        elif result[0] == False:
           print(result[1])
           