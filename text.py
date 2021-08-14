import pygame

class Text:
    def __init__(self,font,text,centered,position,color):
        self.font = font
        self.color = color
        self.disp = self.font.render(text, True, self.color)
        self.centered = centered
        self.position = position
        if self.centered:
            self.rect = self.disp.get_rect(center = (self.position[0],self.position[1]))
        else:
            self.rect = self.disp.get_rect(left = self.position[0], centery = self.position[1])

    def changetext(self,text):
        self.disp = self.font.render(text, True, self.color)
        if self.centered:
            self.rect = self.disp.get_rect(center = (self.position[0],self.position[1]))
        else:
            self.rect = self.disp.get_rect(left = self.position[0], centery = self.position[1])

    def draw(self, display):
        display.blit(self.disp, self.rect)
