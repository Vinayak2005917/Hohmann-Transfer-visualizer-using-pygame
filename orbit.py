class Orbit:
    def __init__(self, semi_major_axis, eccentricity):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
    def __str__(self):
        return f"Orbit with semi-major axis: {self.semi_major_axis}, eccentricity: {self.eccentricity}"