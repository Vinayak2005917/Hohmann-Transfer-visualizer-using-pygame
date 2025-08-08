import pygame
import numpy as np
import time
import math
from orbit import Orbit

pygame.init()

# Font for live-updating text
font = pygame.font.SysFont(None, 28)

# buttons
button_color = (150,150,150)
button_hover_color = (100,100,100)

#start button
start_button_rect = pygame.Rect(10, 200, 100, 50)
start_button_text = font.render('Start', True, (255, 255, 255))

#stop button
stop_button_rect = pygame.Rect(10, 260, 100, 50)
stop_button_text = font.render('Stop', True, (255, 255, 255))

#reset button
reset_button_rect = pygame.Rect(10, 320, 100, 50)
reset_button_text = font.render('Reset', True, (255, 255, 255))

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

run = False
# Main loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()
	window.fill((0, 0, 0))
	
	#earth
	pygame.draw.circle(window, (0, 0, 255), (zerox, zeroy), earth_radius)
	
	#Orbit
	pygame.draw.polygon(window, (255, 255, 255), pointslist, width=2)

	#Satellite
	r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(theta))
	sat_x = int((r*np.cos(theta)/100)+zerox) 
	sat_y = int((r*np.sin(theta)/100)+zeroy)

	#updating the sat position
	if run:	
		time.sleep(0.01)
		theta += 0.01
	pygame.draw.circle(window, (255, 0, 0), (sat_x,sat_y), 5)



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

	# Start button
	if start_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, start_button_rect)
		if mouse_pressed[0]:
			run = True
	else:
		pygame.draw.rect(window, button_color, start_button_rect)
	text_rect = start_button_text.get_rect(center=start_button_rect.center)
	window.blit(start_button_text, text_rect)

	# Stop button
	if stop_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, stop_button_rect)
		if mouse_pressed[0]:
			run = False
	else:
		pygame.draw.rect(window, button_color, stop_button_rect)
	text_rect = stop_button_text.get_rect(center=stop_button_rect.center)
	window.blit(stop_button_text, text_rect)

	# Reset button
	if reset_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, reset_button_rect)
		if mouse_pressed[0]:
			run = False
			theta = 0
	else:
		pygame.draw.rect(window, button_color, reset_button_rect)
	text_rect = reset_button_text.get_rect(center=reset_button_rect.center)
	window.blit(reset_button_text, text_rect)

	pygame.display.flip()

pygame.quit()
