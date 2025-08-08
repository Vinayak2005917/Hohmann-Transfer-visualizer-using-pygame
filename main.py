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

#Burn 1 button
Burn1_button_rect = pygame.Rect(10, 240, 100, 50)
Burn1_button_text = font.render('Burn 1', True, (255, 255, 255))

#Burn 2 button
Burn2_button_rect = pygame.Rect(10, 300, 100, 50)
Burn2_button_text = font.render('Burn 2', True, (255, 255, 255))

#start button
start_button_rect = pygame.Rect(10, 360, 100, 50)
start_button_text = font.render('Start', True, (255, 255, 255))

#stop button
stop_button_rect = pygame.Rect(10, 420, 100, 50)
stop_button_text = font.render('Stop', True, (255, 255, 255))

#reset button
reset_button_rect = pygame.Rect(10, 480, 100, 50)
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
Orbit2 = Orbit(8000,0.1)

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

run_sat = False
Burn1 = False
Burn2 = False
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
	

	#Satellite
	r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(theta))
	sat_x = int((r*np.cos(theta)/100)+zerox) 
	sat_y = int((r*np.sin(theta)/100)+zeroy)

	#updating the sat position
	if run_sat:	
		time.sleep(0.01)
		theta += 0.01

	if Burn1:
		theta = 0

		# Recalculate current perigee/apogee first
		current_perigee = Orbit1.semi_major_axis * (1 - Orbit1.eccentricity)
		current_apogee = Orbit1.semi_major_axis * (1 + Orbit1.eccentricity)
		Orbit1.apogee = current_apogee
		Orbit1.perigee = current_perigee

		if Orbit1.apogee > Orbit2.apogee:
			
			# Decrease apogee gradually
			increment = 100
			new_apogee = current_apogee - increment
			
			Orbit1.semi_major_axis = (current_perigee + new_apogee) / 2
			Orbit1.eccentricity = (new_apogee - current_perigee) / (new_apogee + current_perigee)


			pointslist = []
			for i in range(0,628):
				i = i / 100
				r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(i))
				x = int((r*np.cos(i)/100)+zerox)
				y = int((r*np.sin(i)/100)+zeroy)
				pointslist.append((x,y))
		else:
			Burn1 = False
	if Burn2:
		# Recalculate current perigee/apogee first
		current_perigee = Orbit1.semi_major_axis * (1 - Orbit1.eccentricity)
		current_apogee = Orbit1.semi_major_axis * (1 + Orbit1.eccentricity)
		Orbit1.apogee = current_apogee
		Orbit1.perigee = current_perigee

		if Orbit1.perigee > Orbit2.perigee+10:#tolerance of 10
			theta = 3.1415
			
			# Decrease apogee gradually
			increment = 100
			new_perigee = current_perigee - increment
			
			Orbit1.semi_major_axis = (new_perigee + current_apogee) / 2
			Orbit1.eccentricity = (current_apogee - new_perigee) / (current_apogee + new_perigee)


			pointslist = []
			for i in range(0,628):
				i = i / 100
				r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(i))
				x = int((r*np.cos(i)/100)+zerox)
				y = int((r*np.sin(i)/100)+zeroy)
				pointslist.append((x,y))
		else:
			Burn2 = False


		
	
	pygame.draw.polygon(window, (255, 255, 255), pointslist, width=2)
	pygame.draw.circle(window, (255, 0, 0), (sat_x,sat_y), 5)



	# Current Orbit
	text_lines_current_orbit = [
		"Current Orbit",
		f"Semi Major axis = {Orbit1.semi_major_axis:.2f}",
		f"eccentricity = {Orbit1.eccentricity:.3f}",
		f"True anomaly = {theta:.3f}",
		f"sat_x = {sat_x}",
		f"sat_y = {sat_y}",
		f"Apogee = {Orbit1.apogee:.2f}",
		f"Perigee = {Orbit1.perigee:.2f}"
	]
	for i, line in enumerate(text_lines_current_orbit):
		text_surface = font.render(line, True, (255, 255, 255))
		window.blit(text_surface, (10, 10 + i * 28))

	#Target orbit
	text_lines_target_orbit = [
		"Target Orbit",
		f"Semi Major axis = {Orbit2.semi_major_axis:.2f}",
		f"eccentricity = {Orbit2.eccentricity:.3f}",
		f"Apogee = {Orbit2.apogee:.2f}",
		f"Perigee = {Orbit2.perigee:.2f}"

	]
	for i, line in enumerate(text_lines_target_orbit):
		text_surface = font.render(line, True, (255, 255, 255))
		window.blit(text_surface, (1000, 10 + i * 28))



	# Burn 1 button
	if Burn1_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, Burn1_button_rect)
		if mouse_pressed[0]:
			Burn1 = True
			theta = 0
	else:
		pygame.draw.rect(window, button_color, Burn1_button_rect)
	text_rect = Burn1_button_text.get_rect(center=Burn1_button_rect.center)
	window.blit(Burn1_button_text, text_rect)


	# Burn 2 button
	if Burn2_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, Burn2_button_rect)
		if mouse_pressed[0]:
			Burn2 = True
			theta = 3.1415
	else:
		pygame.draw.rect(window, button_color, Burn2_button_rect)
	text_rect = Burn2_button_text.get_rect(center=Burn2_button_rect.center)
	window.blit(Burn2_button_text, text_rect)

	# Start button
	if start_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, start_button_rect)
		if mouse_pressed[0]:
			run_sat = True
	else:
		pygame.draw.rect(window, button_color, start_button_rect)
	text_rect = start_button_text.get_rect(center=start_button_rect.center)
	window.blit(start_button_text, text_rect)

	# Stop button
	if stop_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, stop_button_rect)
		if mouse_pressed[0]:
			run_sat = False
			Burn1 = False
			Burn2 = False
	else:
		pygame.draw.rect(window, button_color, stop_button_rect)
	text_rect = stop_button_text.get_rect(center=stop_button_rect.center)
	window.blit(stop_button_text, text_rect)

	# Reset button
	if reset_button_rect.collidepoint(mouse_pos):
		pygame.draw.rect(window, button_hover_color, reset_button_rect)
		if mouse_pressed[0]:
			run_sat = False
			theta = 0

			Burn1 = False
			Burn2 = False
			Orbit1 = Orbit(15000,0.5)
			pointslist = []
			for i in range(0,628):
				i = i / 100
				r = (Orbit1.semi_major_axis*(1-(Orbit1.eccentricity**2)))/(1+Orbit1.eccentricity*np.cos(i))
				x = int((r*np.cos(i)/100)+zerox)
				y = int((r*np.sin(i)/100)+zeroy)
				pointslist.append((x,y))
	else:
		pygame.draw.rect(window, button_color, reset_button_rect)
	text_rect = reset_button_text.get_rect(center=reset_button_rect.center)
	window.blit(reset_button_text, text_rect)

	pygame.display.flip()

pygame.quit()
