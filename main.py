import math

def get_input(message: str, handler, context=None):
     while True:
        inp = input(message)
        result = handler(inp, context)
        if result[0]:
           return result[1]
        elif result[0] == False:
           print(result[1])
           
class inpContext:
   name: str
   vertices: list[tuple[int, int]]
   def __init__(self, name, vertices):
       self.name = name
       self.vertices = vertices

def main_input():
   def validation(inp: str, cont: inpContext):
      name = cont.name
      vertices = cont.vertices
      split = inp.replace(" ", "").split("")