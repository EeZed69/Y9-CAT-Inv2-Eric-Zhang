import math

def float_check(a):
    try:
      float(a)
      return True
    except ValueError:
      return False

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
        splitted_inp = inp.replace(" ", "").split("")
        if len(splitted_inp) != 2:
            return False, f"Error: Invalid number of arguments for vertex {name}, expected 2, got {len(splitted_inp)}"
        xcoord, ycoord = splitted_inp
        validity = False
        error= None
        xfloatness = float_check(xcoord)
        yfloatness = float_check(ycoord)
        if not xfloatness and yfloatness:
            error = f"Error: Invalid x and y coordinates for vertex {name}, expected float, got {xcoord} and {ycoord}"
        elif not xfloatness:
            error = f"Error: Invalid x coordinate for vertex {name}, expected float, got {xcoord}"
        elif not yfloatness:
            error = f"Error: Invalid y coordinate for vertex {name}, expected float, got {ycoord}"
        else:
            validity = True
        if not validity:
            return False, error
        vertexresult = float(xcoord), float(ycoord)
        if vertexresult in vertices:
            return False, f"Error: Vertex {vertexresult} already exists"