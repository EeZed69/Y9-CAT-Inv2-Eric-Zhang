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
        
        return True, vertexresult
    
    print("Enter comma-separated coordinates in any order:")
    vertices = []
    for name in ["A", "B", "C", "D"]:
        vertices.append(get_input(f"Vertex {name}: ", validation, inpContext(name, vertices)))

def point_dist_calc(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

class Side:
    length: float
    sidestart: tuple[float, float]
    sideend: tuple[float, float]
    slope: float
    
    def __init__(self, sidestart: tuple[float, float], sideend: tuple[float, float]) -> None:
        self.sidestart = sidestart
        self.sideend = sideend
        self.length = point_dist_calc(sidestart, sideend)
        
        try:
            self.slope = float(sideend[1] - sidestart[1]) / float(sideend[0] - sidestart[0])
        except ZeroDivisionError:
            self.slope = float("inf")
            
    def __repr__(self) -> str:
        return (f"Side({self.sidestart}, {self.sideend}), length={self.length}, slope={self.slope})")

def sidelistfromvertices(vertices: list[tuple[float, float]]):
    sides = []
    for i in range(len(vertices)):
        sides.append(Side(vertices[i], vertices[(i+1) % len(vertices)]))
    return sides

def comparefloats(a: float, b: float, tolerance: float = None):
    tolerance = tolerance or 1e-6
    inf = float("inf")
    return (a == inf and b == inf) or abs(a-b) < tolerance 

def parallel_check(a: Side, b: Side):
    return comparefloats(a.slope, b.slope)

def sidenamefromindex(index: int):
    return ["AB", "BC", "CD" "DA"][index]

def anglenamefromindex(index: int):
    return ["DAB", "ABC", "BCD", "CDA"][index]
                                        
def vertexnamefromindex(index:int):
    return ["A", "B", "C", "D"][index]

def linefrompoints(a, b):
    return vertexnamefromindex(a)+vertexnamefromindex(b)

def one_parallel_pair(sides: list[Side]) -> bool:
    for a in range(len(sides)):
        for b in range(a+1,len(sides)):
            if parallel_check(sides[a], sides[b]) and a!=b:
                return (True, [a, b])
    return (False, None)

def two_pairs_of_parallel_sides(sides: list[Side]) -> bool:
    pairs = set()
    for a in range(len(sides)):
        for b in range(a + 1, len(sides)):
            if parallel_check(sides[a], sides[b]) and a!=b:
                pairs.add((a, b))
    return len(pairs) == 2, list(pairs)