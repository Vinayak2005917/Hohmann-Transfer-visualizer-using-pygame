import pygame

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hohmann Transfer Visualizer")



# Main loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	window.fill((0, 0, 0))
	



	pygame.display.flip()
pygame.quit()
