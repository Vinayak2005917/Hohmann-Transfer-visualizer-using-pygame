class Orbit:
    def __init__(self, semi_major_axis, eccentricity):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.apogee = self.semi_major_axis * (1 + self.eccentricity)
        self.perigee = self.semi_major_axis * (1 - self.eccentricity)
    def __str__(self):
        return f"Orbit with semi-major axis: {self.semi_major_axis}, eccentricity: {self.eccentricity}"