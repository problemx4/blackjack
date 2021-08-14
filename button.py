import pygame

class Button:
    def __init__(self,images,frame,position): #call with the images returned from sprite handler along with the frame of the first image
        self.clicked = images[0]
        self.hovered = images[1]
        self.neutral = images[2]
        self.image = self.neutral
        self.surf = pygame.Surface((frame["w"], frame["h"]))
        self.rect = self.surf.get_rect(center = (position[0], position[1]))

    def draw(self, display):
        left, middle, right = pygame.mouse.get_pressed()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if left:
                self.image = self.clicked
            else:
                self.image = self.hovered
        else:
            self.image = self.neutral

        display.blit(self.image, self.rect)
