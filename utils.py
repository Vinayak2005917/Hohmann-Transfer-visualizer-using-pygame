import pygame
from pygame.locals import *
pygame.init()
font = pygame.font.SysFont(None, 28)

class Button:
    def __init__(self, x, y, w, h, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]
    
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active if clicked
            self.active = self.rect.collidepoint(event.pos)
            self.color = (0, 255, 0) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # return text on Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        # Draw text and box
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Text:
    def __init__(self, text, x, y, font, color=(255, 255, 255), center=False):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.center = center
        self.update_surface()

    def update_surface(self):
        """Rerender the text surface after changes."""
        self.surface = self.font.render(str(self.text), True, self.color)
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)

    def set_text(self, new_text):
        """Change the displayed text."""
        self.text = new_text
        self.update_surface()

    def set_color(self, new_color):
        """Change text color."""
        self.color = new_color
        self.update_surface()

    def draw(self, screen):
        """Draw text to the screen."""
        screen.blit(self.surface, self.rect)
