"""
Calculates the area of circle
"""
class Circle:
    def __init__(self, R):
        if R <= 0:
            raise ValueError("RADIUS MUST BE POSITIVE")
        self.RADIUS = float(R)

    def Area(self):
        return 3.14 * (self.RADIUS ** 2)

print("AREA:", Circle(2).Area())