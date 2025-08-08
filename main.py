import pygame
import numpy as np
import time
import math
from orbit import Orbit

pygame.init()

# Font for live-updating text
font = pygame.font.SysFont(None, 28)

# Set up the display
WIDTH, HEIGHT = 1280,720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hohmann Transfer Visualizer")

#constants
earth_radius = 63.71
zerox = WIDTH // 2
zeroy = HEIGHT // 2

#orbits
Orbit1 = Orbit(15000,0.5)

#True anomaly for the satellite
theta = 0

#List to hold the points of the orbit
pointslist = []
for i in range(0,628):
	i = i / 100
	r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(i))
	x = int((r*np.cos(i)/100)+zerox)
	y = int((r*np.sin(i)/100)+zeroy)
	pointslist.append((x,y))


# Main loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	window.fill((0, 0, 0))
	
	#earth
	pygame.draw.circle(window, (0, 0, 255), (zerox, zeroy), earth_radius)
	
	#Orbit
	pygame.draw.polygon(window, (255, 255, 255), pointslist, width=2)

	#Satellite
	r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(theta))
	sat_x = int((r*np.cos(theta)/100)+zerox) 
	sat_y = int((r*np.sin(theta)/100)+zeroy)

	# Live-updating text (top left)
	text_lines = [
		f"Semi Major axis = {Orbit1.semi_major_axis:.2f}",
		f"eccentricity = {Orbit1.eccentricity:.3f}",
		f"True anomaly = {theta:.3f}",
		f"sat_x = {sat_x}",
		f"sat_y = {sat_y}"
	]
	for i, line in enumerate(text_lines):
		text_surface = font.render(line, True, (255, 255, 255))
		window.blit(text_surface, (10, 10 + i * 28))

		
	time.sleep(0.01)
	theta += 0.01
	pygame.draw.circle(window, (255, 0, 0), (sat_x,sat_y), 5)
	pygame.display.flip()

pygame.quit()
