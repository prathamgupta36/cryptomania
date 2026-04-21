from fractions import Fraction

class Point(): 
    def __init__(self, curve, x, y): 
        self.curve = curve
        self.x = x 
        self.y = y 

        if not curve.testPoint(x, y): 
            raise Exception(f"The given point {self} is not on the curve {curve}")
        
    def __str__(self): 
        return f"({self.x}, {self.y})"

class ECC(): 
    def __init__(self, a, b): 
        self.a = a 
        self.b = b

    def testPoint(self, x, y): 
        return (y*y).__round__() == (x*x*x + (self.a * x) + self.b).__round__()

    def __str__(self): 
        return f"y^2 = x^3 + {self.a}x + {self.b}"

def ecc_addition(curve: ECC, point_p: Point, point_q: Point) -> tuple: 
    p_x = point_p.x
    p_y = point_p.y
    q_x = point_q.x 
    q_y = point_q.y

    if (p_x, p_y) != (q_x, q_y): 
        lambda_ecc = (q_y - p_y) / (q_x - p_x)
    else: 
        lambda_ecc = (3*(p_x**2) + curve.a) / (2*p_y)

    x_final = lambda_ecc**2 - p_x - q_x 
    y_final = lambda_ecc*(p_x - x_final) - p_y

    return (Fraction(x_final).limit_denominator(100), Fraction(y_final).limit_denominator(100))
