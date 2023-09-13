class Color:
    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b

    def __add__(self, other: 'Color'):
        if not isinstance(other, Color):
            raise TypeError(f'Can\'t add {type(other).__name__} to Color')

        return Color(self.r + other.r, self.g + other.g, self.b + self.b)

    def __sub__(self, other: 'Color'):
        if not isinstance(other, Color):
            raise TypeError(f'Can\'t subtract {type(other).__name__} from Color')

        return Color(self.r - other.r, self.g - other.g, self.b - self.b)

    def __mul__(self, other: int | float):
        return Color(
            round(self.r * other), round(self.g * other), round(self.b * other)
        )

    def __truediv__(self, other: int | float):
        return Color(
            round(self.r / other), round(self.g / other), round(self.b / other)
        )

    def __divmod__(self, other: int | float):
        return Color(
            round(self.r / other), round(self.g / other), round(self.b / other)
        ), 0

    def __index__(self):
        return int(self.as_hex(), 16)

    def __str__(self):
        return f'Color({self.r}, {self.g}, {self.b})'

    def __repr__(self):
        return f'{self}'

    def as_hex(self):
        return ''.join(f'{round(x):0>2x}' for x in (self.r, self.g, self.b))


def evaluate_color(expression: str, color: dict,
                   columns: dict[str] = None) -> Color:
    result = eval(expression.format(**columns if columns else {}))

    match color["type"]:
        case 'continuous':
            start, end = Color(*color["start"]), Color(*color["end"])
            path = end - start
            return start + (path * result)
        case 'discontinuous':
            return Color(*color["list"][round(result)])

