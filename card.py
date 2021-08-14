import pygame

class Card:
    def __init__(self,image,back,value):
        deckpos = (125,150)
        self.front = image
        self.back = back
        self.image = self.back
        self.value = value
        self.surface = pygame.Surface((150,200))
        self.rect = self.surface.get_rect(center = deckpos)

    def hide(self):
        self.image = self.back

    def show(self):
        self.image = self.front

    def lurp(self,destination,speed):
        self.rect.centerx = int(self.rect.centerx + ((destination[0] - self.rect.centerx) * speed))
        self.rect.centery = int(self.rect.centery + ((destination[1] - self.rect.centery) * speed))

    def draw(self,display):
        display.blit(self.image, self.rect)
