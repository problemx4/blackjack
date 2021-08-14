import pygame
import random

class Hand:
    def __init__(self, yval):
        self.hold = []
        self.y = yval

    def move(self, positions, speed): #LURPS ONLY ONCE, USE MULTIPLE TIMES WITH LOOP IN MAIN, USE ALONG SIDE SETPOS IN MAIN AFTER DRAWING, CREATE RESET FUNCTION IN MAIN
        for x in range(len(self.hold)):
            self.hold[x].lurp(positions[x], speed)
        else:
            pass

    def setpos(self):
        handposleft = 500
        handposright = 900
        handsize = handposright - handposleft

        positions = []
        interval = handsize / (len(self.hold) + 1)
        for x in range(len(self.hold)):
            positions.append((handposleft + (interval * (x + 1)), self.y))
        return positions

    def cardDraw(self,deck):
        pick = random.randrange(0, len(deck))
        self.hold.append(deck.pop(pick))

    def detVal(self):
        aces = False
        value = 0
        for card in self.hold:
            value += card.value
            if card.value == 1:
                aces = True
        if aces and ((value + 10) <= 21):
            value += 10
        return value

    def draw(self, display):
        for card in self.hold:
            card.draw(display)
        else:
            pass
