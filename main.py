import math

inf = float("inf")


def float_check(a) -> bool:
    try:
        float(a)
        return True
    except ValueError:
        return False


class inpContext:
    name: str
    vertices: list[tuple[int, int]]

    def __init__(self, name, verts):
        self.name = name
        self.vertices = verts


def get_input(message: str, handler, context=None):
    while True:
        inp = input(message)
        result = handler(inp, context)

        if result[0]:
            return result[1]
        else:
            print(result[1])


def main_input() -> list[tuple[float, float]]:
    print("Enter comma-separated coordinates in any order:")

    def validation(inp: str, cont: inpContext):
        name = cont.name
        verts = cont.vertices

        splitted_inp = inp.replace(" ", "").split(",")

        if len(splitted_inp) != 2:
            return (
                False,
                f"Error: Invalid number of arguments for vertex {name}, expected 2, got {len(splitted_inp)}",
            )
        xcoord, ycoord = splitted_inp

        validity = False
        error = None
        xfloatness = float_check(xcoord)
        yfloatness = float_check(ycoord)

        if not xfloatness and yfloatness:
            error = (
                f"Error: Invalid x and y coordinates for vertex {name}, enter floats."
            )
        elif not xfloatness:
            error = f"Error: Invalid x coordinate for vertex {name}, enter a float."
        elif not yfloatness:
            error = f"Error: Invalid y coordinate for vertex {name}, enter a float."
        else:
            validity = True

        if not validity:
            return False, error

        vertexresult = float(xcoord), float(ycoord)

        if vertexresult in verts:
            return (
                False,
                f"Error: Vertex {vertexresult} already exists. Enter a different vertex.",
            )

        return True, vertexresult

    vertices = []
    for name in ["A", "B", "C", "D"]:
        vertices.append(
            get_input(f"Vertex {name}: ", validation, inpContext(name, vertices))
        )

    return vertices


def point_dist_calc(a, b) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class Side:
    length: float
    sidestart: tuple[float, float]
    sideend: tuple[float, float]
    slope: float

    def __init__(
        self, sidestart: tuple[float, float], sideend: tuple[float, float]
    ) -> None:
        self.sidestart = sidestart
        self.sideend = sideend
        self.length = point_dist_calc(sidestart, sideend)

        try:
            self.slope = float(sideend[1] - sidestart[1]) / float(
                sideend[0] - sidestart[0]
            )
        except ZeroDivisionError:
            self.slope = inf

    def __repr__(self) -> str:
        return f"Side({self.sidestart}, {self.sideend}), length={self.length}, slope={self.slope})"


def sidelistfromvertices(vertices: list[tuple[float, float]]) -> list:
    sides = []
    for i in range(len(vertices)):
        sides.append(Side(vertices[i], vertices[(i + 1) % len(vertices)]))
    return sides


def comparefloats(a: float, b: float, tolerance: float = None) -> bool:
    tolerance = tolerance or 1e-6
    return (a == inf and b == inf) or abs(a - b) < tolerance


def parallel_check(a: Side, b: Side) -> bool:
    return comparefloats(a.slope, b.slope)


def sidenamefromindex(index: int):
    return ["AB", "BC", "CD", "DA"][index]


def anglenamefromindex(index: int):
    return ["DAB", "ABC", "BCD", "CDA"][index]


def vertexnamefromindex(index: int):
    return ["A", "B", "C", "D"][index]


def linefrompoints(a, b):
    return vertexnamefromindex(a) + vertexnamefromindex(b)


def one_parallel_pair(sides: list[Side]) -> bool:
    for a in range(len(sides)):
        for b in range(a + 1, len(sides)):
            if parallel_check(sides[a], sides[b]) and a != b:
                return (True, [a, b])
    return (False, None)


def two_pairs_of_parallel_sides(sides: list[Side]) -> bool:
    pairs = set()
    for a in range(len(sides)):
        for b in range(a + 1, len(sides)):
            if parallel_check(sides[a], sides[b]) and a != b:
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
        True
        if (a.slope == inf and b.slope == 0) or (a.slope == 0 and b.slope == inf)
        else comparefloats(a.slope * b.slope, -1)
    )


angle_decimal_precision = 3


def angle_calc(sides):
    angles = []
    for i in range(len(sides)):
        previoussideindex = i - 1
        if previoussideindex < 0:
            previoussideindex = len(sides) - 1

        previousside = sides[previoussideindex]
        currentside = sides[i]
        a, b, c = (
            previousside.length,
            currentside.length,
            point_dist_calc(previousside.sidestart, currentside.sideend),
        )
        angles.append(
            round(
                math.degrees(
                    math.acos((a**2 + b**2 - c**2) / (2 * a * b))
                    if a != 0 and b != 0
                    else 0
                ),
                angle_decimal_precision,
            )
        )
    return angles


def all90deg(sides: list[Side]) -> bool:
    angles = angle_calc(sides)
    for angle in angles:
        if not comparefloats(angle, 90, 10**-angle_decimal_precision):
            return False
    return True


def two_adjacent_equal_sides(sides: list[Side]):
    pairs = 0
    pairs_cache = []
    sides_cache = []
    for a in range(len(sides)):
        b = (a + 1) % len(sides)
        notdupe = a not in sides_cache and b not in sides_cache
        if comparefloats(sides[a].length, sides[b].length) and a != b and notdupe:
            pairs += 1
            pairs_cache.append((a, b))
            sides_cache.append(a)
            sides_cache.append(b)

    return (pairs == 2, pairs_cache)


def perpendiculardiagonals(sides: list[Side]):
    perpendicular_angles = []
    diagonal_a = Side(sides[0].sidestart, sides[2].sidestart)
    diagonal_b = Side(sides[1].sidestart, sides[3].sidestart)
    if perpendicularcheck(diagonal_a, diagonal_b):
        perpendicular_angles.append(linefrompoints(0, 2))
        perpendicular_angles.append(linefrompoints(1, 3))
    return (len(perpendicular_angles) > 0, perpendicular_angles)


def a_diagonal_bisects_other(sides: list[Side]):
    bisecting_angles = []
    for a in [0, 1]:
        target_corner_one = sides[0 + a].sidestart
        target_corner_two = sides[2 + a].sidestart

        relative_corner_one = sides[1 + a].sidestart
        relative_corner_two = sides[3 + a if 3 + a < 4 else 0].sidestart

        target_point = (
            (relative_corner_one[0] + relative_corner_two[0]) / 2,
            (relative_corner_one[1] + relative_corner_two[1]) / 2,
        )

        line_a = Side(target_corner_one, target_point)
        line_b = Side(target_corner_two, target_point)

        if comparefloats(line_a.slope, line_b.slope):
            bisecting_angles.append(linefrompoints(a, 2 + a))

    return (len(bisecting_angles) > 0, bisecting_angles)


def one_diagonal_bisecting_other(sides: list[Side]):
    hasdiagonalbisectingother, bisecting_diagonals = a_diagonal_bisects_other(sides)
    return (
        hasdiagonalbisectingother and len(bisecting_diagonals) >= 1,
        bisecting_diagonals,
    )


def two_diagonals_bisecting_other(sides: list[Side]):
    hasdiagonalbisectingother, bisecting_diagonals = a_diagonal_bisects_other(sides)
    return (
        hasdiagonalbisectingother and len(bisecting_diagonals) >= 2,
        bisecting_diagonals,
    )


def a_diagonal_bisects_angle(sides: list[Side]):
    bisecting_angles = []
    for a in [0, 1]:
        target_corner_one = sides[0 + a].sidestart
        target_corner_two = sides[2 + a].sidestart

        relative_corner_one = sides[1 + a].sidestart
        relative_corner_two = sides[3 + a if 3 + a < 4 else 0].sidestart

        target_point = (
            (relative_corner_one[0] + relative_corner_two[0]) / 2,
            (relative_corner_one[1] + relative_corner_two[1]) / 2,
        )

        line_a = Side(target_corner_one, target_point)
        line_b = Side(target_corner_two, target_point)

        reference_line = Side(relative_corner_one, relative_corner_two)
        is_perpendicular = perpendicularcheck(
            line_a, reference_line
        ) and perpendicularcheck(line_b, reference_line)
        if is_perpendicular:
            reference_line_angle_a = anglenamefromindex(a)
            reference_line_angle_b = anglenamefromindex(2 + a)

            bisecting_angles.append(
                [
                    linefrompoints(a, 2 + a),
                    reference_line_angle_a,
                    reference_line_angle_b,
                ]
            )

    return (len(bisecting_angles) > 0, bisecting_angles)


def one_diagonal_bisecting_angles_pass_through(sides: list[Side]):
    (
        hasbisectingdiagonal,
        bisecting_diagonals,
    ) = a_diagonal_bisects_angle(sides)
    return (
        hasbisectingdiagonal and len(bisecting_diagonals) >= 1,
        bisecting_diagonals,
    )


def two_diagonal_bisecting_angles_pass_through(sides: list[Side]):
    (
        hasbisectingdiagonal,
        bisecting_diagonals,
    ) = a_diagonal_bisects_angle(sides)
    return (
        hasbisectingdiagonal and len(bisecting_diagonals) >= 2,
        bisecting_diagonals,
    )


def equaldiaglength(sides: list[Side]):
    diagonal_a = Side(sides[0].sidestart, sides[2].sidestart)
    diagonal_b = Side(sides[1].sidestart, sides[3].sidestart)
    if comparefloats(diagonal_a.length, diagonal_b.length):
        return (True, diagonal_a.length, [(0, 2), (1, 3)])
    return (False, 0, [])


def trapezium_diagonals(sides: list[Side]):
    return (True, None)


PROPERTIES = {
    "trapezium": [
        # side
        one_parallel_pair_exactly,
        # diagonals
        trapezium_diagonals,
    ],
    "kite": [
        # side
        two_adjacent_equal_sides,
        # diagonals
        perpendiculardiagonals,
        one_diagonal_bisecting_other,
        one_diagonal_bisecting_angles_pass_through,
    ],
    "parallelogram": [
        # side
        one_parallel_pair,
        two_pairs_of_parallel_sides,
        # diagonals
        one_diagonal_bisecting_other,
        two_diagonals_bisecting_other,
    ],
    "rectangle": [
        # side
        one_parallel_pair,
        two_pairs_of_parallel_sides,
        all90deg,
        # diagonals
        one_diagonal_bisecting_other,
        two_diagonals_bisecting_other,
        equaldiaglength,
    ],
    "rhombus": [
        # side
        one_parallel_pair,
        two_pairs_of_parallel_sides,
        allequallength,
        # diagonals
        perpendiculardiagonals,
        one_diagonal_bisecting_other,
        two_diagonals_bisecting_other,
        one_diagonal_bisecting_angles_pass_through,
        two_diagonal_bisecting_angles_pass_through,
    ],
    "square": [
        # side
        one_parallel_pair,
        two_pairs_of_parallel_sides,
        allequallength,
        all90deg,
        # diagonals
        two_adjacent_equal_sides,
        one_diagonal_bisecting_other,
        two_diagonals_bisecting_other,
        one_diagonal_bisecting_angles_pass_through,
        two_diagonal_bisecting_angles_pass_through,
        equaldiaglength,
    ],
}


def decimal_round(x: float, decpoin: int) -> float:
    return round(x * (10**decpoin)) / (10**decpoin)


def getproofsstring(function, values: tuple) -> str:
    match function.__name__:
        case "one_parallel_pair":
            return f"One pair of parallel sides: {sidenamefromindex(values[0][0])} and {sidenamefromindex(values[0][1])}"
        
        case "two_pairs_of_parallel_sides":
            return f"Two pairs of parallel sides: {sidenamefromindex(values[0][1][0])} and {sidenamefromindex(values[0][1][1])}"
        
        case "one_parallel_pair_exactly":
            return f"Exactly one pair of parallel sides: {sidenamefromindex(values[0][0])} and {sidenamefromindex(values[0][1])}"
        
        case "allequallength":
            return f"All sides equal: {decimal_round(values[0][0], 2)} units ({', '.join(values[0][1])})"
        
        case "all90deg":
            return f"All angles 90 degrees: {', '.join(anglenamefromindex(i) for i in range(4))}"
        
        case "two_adjacent_equal_sides":
            return f"Two pairs of adjacent equal sides: {sidenamefromindex(values[0][0][0])} and {sidenamefromindex(values[0][0][1])}, {sidenamefromindex(values[0][1][0])} and {sidenamefromindex(values[0][1][1])}"
        
        case "two_adjacent_equal_sides":
            return f"Diagonals are perpendicular: {values[0][0]}, {values[0][1]}"
        
        case "one_diagonal_bisecting_other":
            return f"One diagonal bisecting another: {values[0][0]}"
        
        case "two_diagonals_bisecting_other":
            return f"Two diagonals bisecting another: also {values[0][1]}"
        
        case "one_diagonal_bisecting_angles_pass_through":
            return f"One diagonal bisecting angles pass through: {values[0][0][0]} bisects {values[0][0][1]}, {values[0][0][2]}"
        
        case "two_diagonal_bisecting_angles_pass_through":
            return f"Two diagonals bisecting angles pass through: also {values[0][1][0]} bisects {values[0][1][1]}, {values[0][1][2]}"
        
        case "equaldiaglength":
            diagonal_a = linefrompoints(*values[1][0])
            diagonal_b = linefrompoints(*values[1][1])
            return f"Diagonals equal in length: {diagonal_a}, {diagonal_b} = {decimal_round(values[0], 2)} units"
        
        case "trapezium_diagonals":
            return None
        
        case other:
            return f"unimplemented reason for {other}: {values}"


import functools
@functools.cmp_to_key
def sort_props(a: list, b: list):
    if len(a) > len(b):
        return 1
    elif len(a) < len(b):
        return -1
    else:
        return 0


def id_shape(sides: list[Side]):
    validshapes = []
    
    for shape in PROPERTIES:
        properties = PROPERTIES[shape]
        allpropertiesvalid = True
        propertiesreason = []
        
        for property in properties:
            result = property(sides)
            validity = result[0] if type(result) == tuple else result
            rest = result[1:] if type(result) == tuple else None
            if not validity:
                allpropertiesvalid = False
                break
            if reason := getproofsstring(property, rest):
                propertiesreason.append(reason)
                
        if allpropertiesvalid:
            validshapes.append((shape, str.join("\n", propertiesreason)))
            
    result = list(sorted(validshapes, key=sort_props, reverse=True))
    
    if len(result) > 0:
        return result[-1]
    
    return None


def print_idd_shape(sides: list[Side]):
    print(
        f"Side, angle and diagonal properties for {sides[0].sidestart}, {sides[1].sidestart}, {sides[2].sidestart}, and {sides[3].sidestart}:"
    )

    result = id_shape(sides)
    if not result:
        print("CONCLUSION: No shape found")
        return
    (shape, reason) = result
    print(f"{reason}")
    print(f"CONCLUSION: The quadrilateral is a {shape.upper()}")


def sort_vertices(vertices: list) -> list:
    mean_center = (
        sum([vertex[0] for vertex in vertices]) / len(vertices),
        sum([vertex[1] for vertex in vertices]) / len(vertices),
    )

    return sorted(
        vertices,
        key=lambda vertex: math.atan2(
            vertex[1] - mean_center[1], vertex[0] - mean_center[0]
        ),
    )


if __name__ == "__main__":
    vertices = main_input()
    vertices = sort_vertices(vertices)
    print(vertices)
    sides = sidelistfromvertices(vertices)
    print_idd_shape(sides)
