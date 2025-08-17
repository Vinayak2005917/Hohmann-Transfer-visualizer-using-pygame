# Hohmann Transfer Visualizer

A simple Python application using Pygame to visualize Hohmann transfer orbits.

## Features
- Interactive input for initial and target orbit parameters
- Real-time visualization of satellite movement and orbit changes
- Controls for burns, satellite movement, and orbit reset

## Key Modules
- `utils.py`: Contains reusable UI components (Button, InputBox, Text) for Pygame, making the interface interactive and user-friendly.
- `orbit.py`: Defines the `Orbit` class, encapsulating orbital mechanics calculations and properties.

## Formulas Used
- **Orbit Radius**:  
  \( r = \frac{a(1 - e^2)}{1 + e \cos(\theta)} \)  
  where \( a \) is the semi-major axis, \( e \) is eccentricity, \( \theta \) is true anomaly.
- **Apogee/Perigee**:  
  \( \text{Apogee} = a(1 + e) \)  
  \( \text{Perigee} = a(1 - e) \)
- **Velocity**:  
  \( v = \sqrt{\mu \left( \frac{2}{r} - \frac{1}{a} \right)} \)  
  where \( \mu \) is Earth's gravitational parameter.

## Usage
1. Install dependencies: `pip install pygame numpy`
2. Run `main.py` to start the visualizer.

---
Created by Vinayak2005917
