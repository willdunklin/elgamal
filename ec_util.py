from util import mul_inv


# Elliptic Curve
class ECurve:
    def __init__(self, a: int, b: int, p: int):
        self.a, self.b, self.p = a, b, p

        if self.disc == 0:
            raise ValueError(f'Failed to construct ({self}). Discriminant == 0')

    def __repr__(self) -> str:
        return f'Elliptic Curve: y^2 = x^3 + {self.a}x + {self.b} (mod {self.p})'

    @property
    def disc(self):
        return (4*self.a**3 + 27*self.b**2) % self.p

    def valid(self, x, y):
        a, b, p = self.a, self.b, self.p
        return (y*y % p) == ((x*x*x + a*x + b) % p)

    def __call__(self, x):
        a, b, p = self.a, self.b, self.p
        y2 = (x*x*x + a*x + b) % p
        return y2

# Elliptic Curve Point
class ECPoint:
    def __init__(self, x: int, y: int, curve: ECurve, inf: bool = False):
        self.inf = inf
        self.x, self.y = x, y
        self.a, self.b, self.p = curve.a, curve.b, curve.p
        self.curve = curve

    def point_at_infinity(self):
        return ECPoint(0, 0, self.curve, inf=True)

    def __eq__(self, other: object) -> bool:
        if self.inf:
            return other.inf
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        if self.inf:
            return '[Point at Infinity]'
        return f'[{self.x}, {self.y}]'

    def valid(self) -> bool:
        if self.inf: return True # Always include the point at infinity
        return self.curve.valid(self.x, self.y)

    def __add__(self, other):
        if self.inf:
            return other
        if other.inf:
            return self

        # if not self.valid():
        #     raise ValueError(f'self: {self}, is not on curve {self.curve}')
        # if not other.valid():
        #     raise ValueError(f'other: {other}, is not on curve {self.curve}')

        if self.x == other.x and self.y == -other.y % self.p:
            return self.point_at_infinity()

        if self.x == other.x:
            m = ((3*self.x*self.x + self.a) * mul_inv(2*self.y, self.p)) % self.p
        else:
            m = ((other.y - self.y) * mul_inv(other.x - self.x, self.p)) % self.p
        c = (self.y - m*self.x) % self.p

        x = (m*m - (self.x + other.x)) % self.p
        y = (m*x + c) % self.p

        return ECPoint(x, self.p - y, self.curve)

    def __mul__(self, n: int):
        if not isinstance(n, int):
            raise TypeError(f'ECPoint multiplication is only defined on integers... {n} is not an integer')

        result = self.point_at_infinity()

        while n > 0:
            if n % 2 == 1:
                result += self
            n //= 2
            self += self

        return result

    __rmul__ = __mul__

    def __neg__(self):
        return ECPoint(self.x, -self.y % self.p, self.curve, self.inf)

    def __sub__(self, other):
        return self + (-other)

def str_to_point(s: str, curve: ECurve, comma: bool = False) -> ECPoint:
    if s == 'inf':
        return ECPoint(0, 0, curve, inf=True)

    parts = s.split(',' if comma else ' ')
    if len(parts) != 2:
        raise ValueError(f'Could not parse point {s}, there are not 2 "{"," if comma else " "}" separated values')

    return ECPoint(int(parts[0]), int(parts[1]), curve)

if __name__ == '__main__':
    e = ECurve(4, 34, 43)
    print(e)
    print('e disc',e.disc)
    print()

    g = ECPoint(12, 41, e)
    n = 4
    p = n * g

    print('g',g)
    print('p',p)
    print()

    c = ECPoint(12, 2, e)
    h = ECPoint(32, 32, e)

    f = n * h
    print('f',f)

    m = c - f
    print('m = c - f', m)
    print()

    print('c+g', c + g)
    print()

    print('2*m', 2 * m)
    print('c', c)
