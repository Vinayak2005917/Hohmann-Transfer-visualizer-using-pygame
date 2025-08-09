import pygame
import numpy as np
import time
import math
from orbit import Orbit
from utils import InputBox, Text, Button

pygame.init()

# Font for live-updating text
font = pygame.font.SysFont(None, 28)

# Colors
button_color = (150, 150, 150)
button_hover_color = (100, 100, 100)

# Set up the display
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hohmann Transfer Visualizer")

# Input boxes
apogee_box = InputBox(20, HEIGHT - 120, 140, 40)
perigee_box = InputBox(20, HEIGHT - 50, 140, 40)

# Buttons
burn1_button = Button(10, 240, 100, 50, "Burn 1", font, button_color, button_hover_color)
burn2_button = Button(10, 300, 100, 50, "Burn 2", font, button_color, button_hover_color)
stop_burn_button = Button(10, 360, 100, 50, "Stop Burn", font, button_color, button_hover_color)
reset_orbit_button = Button(10, 420, 110, 50, "Reset Orbit", font, button_color, button_hover_color)

start_sat_button = Button(420, 620, 100, 50, "Start Sat", font, button_color, button_hover_color)
stop_sat_button = Button(550, 620, 100, 50, "Stop Sat", font, button_color, button_hover_color)
reset_sat_button = Button(680, 620, 100, 50, "Reset Sat", font, button_color, button_hover_color)

# Text headers
satellite_controls_text = Text("Satellite Controls", WIDTH // 2 - 50, HEIGHT - 120, font, (255, 255, 255), center=True)

# Constants
earth_radius = 63.71
zerox = WIDTH // 2
zeroy = HEIGHT // 2

# Orbits
Orbit1 = Orbit(15000, 0.5)
Orbit2 = Orbit(8000, 0.1)

# True anomaly for the satellite
theta = 0

# Points for the orbit
def update_points(orbit):
    pts = []
    for i in range(0, 628):
        ang = i / 100
        r = (orbit.semi_major_axis * (1 - (orbit.eccentricity ** 2))) / (1 + orbit.eccentricity * np.cos(ang))
        x = int((r * np.cos(ang) / 100) + zerox)
        y = int((r * np.sin(ang) / 100) + zeroy)
        pts.append((x, y))
    return pts

pointslist = update_points(Orbit1)

run_sat = False
Burn1 = False
Burn2 = False

# Main loop
running = True
while running:
    if theta > 6.28:
        theta = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        apogee_result = apogee_box.handle_event(event)
        perigee_result = perigee_box.handle_event(event)
        if apogee_result is not None:
            apogee_value = apogee_result
        if perigee_result is not None:
            perigee_value = perigee_result

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    window.fill((0, 0, 0))

    # Earth
    pygame.draw.circle(window, (0, 0, 255), (zerox, zeroy), int(earth_radius))

    # Satellite
    r = (Orbit1.semi_major_axis * (1 - (Orbit1.eccentricity ** 2))) / (1 + Orbit1.eccentricity * np.cos(theta))
    sat_x = int((r * np.cos(theta) / 100) + zerox)
    sat_y = int((r * np.sin(theta) / 100) + zeroy)

    # Satellite controls header
    satellite_controls_text.draw(window)

    # Satellite movement
    if run_sat:
        time.sleep(0.01)
        theta += 0.01

    if Burn1:
        if abs(theta - 0) > 0.1:
            theta += 0.01
        if abs(theta - 0) < 0.1:
            theta = 0
            current_perigee = Orbit1.semi_major_axis * (1 - Orbit1.eccentricity)
            current_apogee = Orbit1.semi_major_axis * (1 + Orbit1.eccentricity)
            Orbit1.apogee = current_apogee
            Orbit1.perigee = current_perigee

            if Orbit1.apogee > Orbit2.apogee:
                increment = 100
                new_apogee = current_apogee - increment
                Orbit1.semi_major_axis = (current_perigee + new_apogee) / 2
                Orbit1.eccentricity = (new_apogee - current_perigee) / (new_apogee + current_perigee)
                pointslist = update_points(Orbit1)
            else:
                Burn1 = False

    if Burn2:
        if theta > 3.1415:
            theta -= 0.01
        if theta < 3.1415:
            theta += 0.01
        if abs(theta - 3.1415) < 0.1:
            theta = 3.1415
            current_perigee = Orbit1.semi_major_axis * (1 - Orbit1.eccentricity)
            current_apogee = Orbit1.semi_major_axis * (1 + Orbit1.eccentricity)
            Orbit1.apogee = current_apogee
            Orbit1.perigee = current_perigee

            if Orbit1.perigee > Orbit2.perigee + 10:
                increment = 100
                new_perigee = current_perigee - increment
                Orbit1.semi_major_axis = (new_perigee + current_apogee) / 2
                Orbit1.eccentricity = (current_apogee - new_perigee) / (current_apogee + new_perigee)
                pointslist = update_points(Orbit1)
            else:
                Burn2 = False

    # Draw orbits and satellite
    pygame.draw.polygon(window, (255, 255, 255), pointslist, width=2)
    pygame.draw.circle(window, (255, 0, 0), (sat_x, sat_y), 5)

    # Current Orbit text
    current_orbit_lines = [
        f"Current Orbit",
        f"Semi Major axis = {Orbit1.semi_major_axis:.2f}",
        f"eccentricity = {Orbit1.eccentricity:.3f}",
        f"True anomaly = {theta:.3f}",
        f"sat_x = {sat_x}",
        f"sat_y = {sat_y}",
        f"Apogee = {Orbit1.apogee:.2f}",
        f"Perigee = {Orbit1.perigee:.2f}"
    ]
    for i, line in enumerate(current_orbit_lines):
        Text(line, 10, 10 + i * 28, font).draw(window)

    # Target Orbit text
    target_orbit_lines = [
        "Target Orbit",
        f"Semi Major axis = {Orbit2.semi_major_axis:.2f}",
        f"eccentricity = {Orbit2.eccentricity:.3f}",
        f"Apogee = {Orbit2.apogee:.2f}",
        f"Perigee = {Orbit2.perigee:.2f}"
    ]
    for i, line in enumerate(target_orbit_lines):
        Text(line, 1000, 10 + i * 28, font).draw(window)

    # Button logic
    burn1_button.draw(window, mouse_pos)
    if burn1_button.is_clicked(mouse_pos, mouse_pressed):
        Burn1 = True

    burn2_button.draw(window, mouse_pos)
    if burn2_button.is_clicked(mouse_pos, mouse_pressed):
        Burn2 = True

    start_sat_button.draw(window, mouse_pos)
    if start_sat_button.is_clicked(mouse_pos, mouse_pressed):
        run_sat = True

    stop_burn_button.draw(window, mouse_pos)
    if stop_burn_button.is_clicked(mouse_pos, mouse_pressed):
        run_sat = False
        Burn1 = False
        Burn2 = False

    stop_sat_button.draw(window, mouse_pos)
    if stop_sat_button.is_clicked(mouse_pos, mouse_pressed):
        run_sat = False

    reset_sat_button.draw(window, mouse_pos)
    if reset_sat_button.is_clicked(mouse_pos, mouse_pressed):
        run_sat = False
        theta = 0

    reset_orbit_button.draw(window, mouse_pos)
    if reset_orbit_button.is_clicked(mouse_pos, mouse_pressed):
        Burn1 = False
        Burn2 = False
        Orbit1 = Orbit(15000, 0.5)
        pointslist = update_points(Orbit1)

    # Input boxes
    apogee_box.draw(window)
    perigee_box.draw(window)

    pygame.display.flip()

pygame.quit()
