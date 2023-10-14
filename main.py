import math

inf = float("inf")

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
            self.slope = inf
            
    def __repr__(self) -> str:
        return (f"Side({self.sidestart}, {self.sideend}), length={self.length}, slope={self.slope})")

def sidelistfromvertices(vertices: list[tuple[float, float]]):
    sides = []
    for i in range(len(vertices)):
        sides.append(Side(vertices[i], vertices[(i+1) % len(vertices)]))
    return sides

def comparefloats(a: float, b: float, tolerance: float = None):
    tolerance = tolerance or 1e-6
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

def one_parallel_pair_exactly(sides: list[Side]) -> bool:
    hasone, result = one_parallel_pair(sides)
    hastwo, _ = two_pairs_of_parallel_sides(sides)
    return hasone and not hastwo, result

def allequallength(sides: list[Side]) -> bool:
    randlength = sides[0].length
    for a in range(len(sides)):
        if not comparefloats(sides[a].length, randlength):
            return False, None
    return True, [randlength, list(sidenamefromindex(a) for a in range(len(sides)))]

def perpendicularcheck(a: Side, b: Side) -> bool:
    return (
        True if
        (a.slope == inf and b.slope == 0) or
        (a.slope == 0 and b.slope == inf) else
        comparefloats(a.slope * b.slope, -1)
    )

angle_decimal_precision = 3
    
def angle_calc(sides):
    angles = []
    for i in range(len(sides)):
        previoussideindex = i-1
        if previoussideindex < 0:
            previoussideindex = len(sides) - 1
        
        previousside = sides[previoussideindex]
        currentside = sides[i]
        a, b, c = (
            previousside.length, currentside.length, point_dist_calc(previousside.side, currentside.end)
        )
        angles.append(
            round(
                math.degrees(
                    math.acos((a**2+b**2-c**2)/(2*a*b))
                    if a!= 0 and b!= 0
                    else 0
                ),
                angle_decimal_precision
            )
        )
    return angles

def all90deg(sides: list[Side]) -> bool:
    angles = angle_calc(sides)
    for angle in angles:
        if not comparefloats(angle, 90, 10**-angle_decimal_precision):
            return False
    return True

def twoadjacentequalsides(sides: list[Side]):
    pairs = 0
    pairs_cache = []
    sides_cache = []
    for a in range(len(sides)):
        b = (a+1) % len(sides)
        notdupe = a not in sides_cache and b not in sides_cache
        if (
            comparefloats(sides[a].length, sides[b].length)
            and a!=b
            and notdupe
        ):
            pairs+=1
            pairs_cache.append((a,b))
            sides_cache.append(a)
            sides_cache.append(b)
            
    return (pairs == 2, pairs_cache)

def perpendiculardiagonals(sides: list[Side]):
    perpendicular_angles = []
    diagonal_a = Side(sides[0].start, sides[2].start)
    diagonal_b = Side(sides[1].start, sides[3].start)
    if perpendicularcheck(diagonal_a, diagonal_b):
        perpendicular_angles.append(linefrompoints(0, 2))
        perpendicular_angles.append(linefrompoints(1, 3))
    return (len(perpendicular_angles) > 0, perpendicular_angles)

def a_diagonal_bisects_other(sides: list[Side]):
    bisecting_angles = []
    for a in [0, 1]:
        target_corner_one = sides[0 + a].start
        target_corner_two = sides[2 + a].start

        relative_corner_one = sides[1 + a].start
        relative_corner_two = sides[3 + a if 3 + a < 4 else 0].start

        target_point = (
            (relative_corner_one[0] + relative_corner_two[0]) / 2,
            (relative_corner_one[1] + relative_corner_two[1]) / 2,
        )

        line_a = Side(target_corner_one, target_point)
        line_b = Side(target_corner_two, target_point)

        if comparefloats(line_a.slope, line_b.slope):
            bisecting_angles.append(linefrompoints(a, 2 + a))

    return (len(bisecting_angles) > 0, bisecting_angles)

def one_diagonal_bisecting_another(sides: list[Side]):
    hasdiagonalbisectingother, bisecting_diagonals = a_diagonal_bisects_other(sides)
    return (
        hasdiagonalbisectingother and len(bisecting_diagonals) >= 1,
        bisecting_diagonals
    )