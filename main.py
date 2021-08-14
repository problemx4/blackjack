import pygame
import sys
import copy
from pygame.locals import *

from spritehandler import Spritehandler
from button import Button
from text import Text
from card import Card
from hand import Hand

def main():
    pygame.mixer.pre_init(16000, -16, 2, 4000)
    pygame.init()

    #colors
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GRAY = (50,50,50)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)

    #Fps and clock
    FPS = 15
    CLOCK = pygame.time.Clock()

    #other control variables and display
    SPEED = .25
    DEFAULTMONEY = 1000
    WIDTH = 1000
    HEIGHT = 800
    DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("follow @problemx4")
    blackjack = False

    #game element variables
    money = DEFAULTMONEY
    pot = 0
    PlayDeck = []
    Buttons = []
    Texts = []
    dealerHand = Hand(200)
    playerHand = Hand(600)

    #load sounds
    pygame.mixer.music.load(r'Sounds\soundTrack.wav')
    pygame.mixer.music.set_volume(0.01)
    chipSound = pygame.mixer.Sound(r'Sounds\chipSound.wav')
    drawSound = pygame.mixer.Sound(r'Sounds\drawSound.wav')
    lossSound = pygame.mixer.Sound(r'Sounds\lossSound.wav')
    shuffleSound = pygame.mixer.Sound(r'Sounds\shuffleSound.wav')

    #loading images and spritesheets
    buttonSprite = Spritehandler(r'Sprites\Buttons.png')
    cardSprite = Spritehandler(r'Sprites\Cards.png')
    cardNames = list(cardSprite.data["frames"].keys())
    menuBackg = pygame.image.load(r'Images\Menu background.png').convert()  # make menu backg dirt darker lol
    bettingBackg = pygame.image.load(r'Images\Betting background.png').convert()
    dealingBackg = pygame.image.load(r'Images\Dealing background.png').convert()
    dispBackg = menuBackg
    cardBack = pygame.image.load(r'Images\Back.png').convert()

    #setting up fonts
    xlargeFont = pygame.font.SysFont("Onyx", 600)
    largeFont = pygame.font.SysFont("Onyx", 400)
    mediumFont = pygame.font.SysFont("Onyx", 200)
    smallFont = pygame.font.SysFont("Onyx", 100)

    #setting up button images
    min500Img = (buttonSprite.parse_sprite("-500 clicked.png"),buttonSprite.parse_sprite("-500 hovered.png"),buttonSprite.parse_sprite("-500 neutral.png"))
    plu500Img = (buttonSprite.parse_sprite("+500 clicked.png"),buttonSprite.parse_sprite("+500 hovered.png"),buttonSprite.parse_sprite("+500 neutral.png"))
    min100Img = (buttonSprite.parse_sprite("-100 clicked.png"),buttonSprite.parse_sprite("-100 hovered.png"),buttonSprite.parse_sprite("-100 neutral.png"))
    plu100Img = (buttonSprite.parse_sprite("+100 clicked.png"),buttonSprite.parse_sprite("+100 hovered.png"),buttonSprite.parse_sprite("+100 neutral.png"))
    dealImg = (buttonSprite.parse_sprite("Deal clicked.png"),buttonSprite.parse_sprite("Deal hovered.png"),buttonSprite.parse_sprite("Deal neutral.png"))
    doubleImg = (buttonSprite.parse_sprite("Double clicked.png"),buttonSprite.parse_sprite("Double hovered.png"),buttonSprite.parse_sprite("Double neutral.png"))
    hitImg = (buttonSprite.parse_sprite("Hit clicked.png"),buttonSprite.parse_sprite("Hit hovered.png"),buttonSprite.parse_sprite("Hit neutral.png"))
    standImg = (buttonSprite.parse_sprite("Stand clicked.png"),buttonSprite.parse_sprite("Stand hovered.png"),buttonSprite.parse_sprite("Stand neutral.png"))
    quitImg = (buttonSprite.parse_sprite("quit hovered.png"),buttonSprite.parse_sprite("quit hovered.png"),buttonSprite.parse_sprite("quit neutral.png"))
    startImg = (buttonSprite.parse_sprite("Start button clicked.png"),buttonSprite.parse_sprite("Start button hovered.png"),buttonSprite.parse_sprite("Start button neutral.png"))

    #functions
    def update(): #call after draw everytime, ticks fps
        pygame.event.get()
        pygame.display.update()
        CLOCK.tick(FPS)

    def draw():#draws everything in quotes
        DISPLAY.blit(dispBackg,(0,0))
        for deck in PlayDeck:
            deck.draw(DISPLAY)
        for text in Texts:
            text.draw(DISPLAY)
        for button in Buttons:
            button.draw(DISPLAY)
        dealerHand.draw(DISPLAY)
        playerHand.draw(DISPLAY)

    def defeat():#visuals for losing
        #flashing lights and big text
        whiteBroke = xlargeFont.render("BROKE", True, WHITE)
        blackBroke = xlargeFont.render("BROKE", True, BLACK)
        brokeRect = blackBroke.get_rect(center = (500,400))

        lossSound.play()

        for x in range(int(.3 * FPS)): #half of how many seconds to wait
            DISPLAY.fill(WHITE)
            DISPLAY.blit(blackBroke, brokeRect)
            update()
            DISPLAY.fill(BLACK)
            DISPLAY.blit(whiteBroke, brokeRect)
            update()

        lossSound.stop()

    def resetVars():
        Buttons.clear()
        Texts.clear()
        dealerHand.hold.clear()
        playerHand.hold.clear()

    #functions for card management
    def mainDraw(hand): #draws card
        drawSound.play()

        hand.cardDraw(PlayDeck)
        positions = hand.setpos()
        for x in range(FPS * 1): #number of seconds drawing takes
            hand.move(positions, SPEED)
            draw()
            update()

    #Flash warning intro screen
    wText1 = largeFont.render("WARNING",True,WHITE)
    wText2 = smallFont.render("flashing lights and loud noises", True, WHITE)

    DISPLAY.fill(BLACK)
    DISPLAY.blit(wText1, wText1.get_rect(center = (500,300)))
    DISPLAY.blit(wText2, wText2.get_rect(center = (500,600)))
    update()
    pygame.time.delay(1000)

    #music
    pygame.mixer.music.play(-1)

    #game loop
    while True:
        #RESET
        resetVars()
        PlayDeck.clear()
        money = DEFAULTMONEY
        #SET UP MENU
        dispBackg = menuBackg
        Buttons.append(Button(quitImg, buttonSprite.data["frames"]["quit neutral.png"]["frame"], (925,75)))
        Buttons.append(Button(startImg, buttonSprite.data["frames"]["Start button neutral.png"]["frame"], (500,325)))
        Buttons.append(Button(min500Img, buttonSprite.data["frames"]["-500 neutral.png"]["frame"], (275,650)))
        Buttons.append(Button(min100Img, buttonSprite.data["frames"]["-100 neutral.png"]["frame"], (425,650)))
        Buttons.append(Button(plu100Img, buttonSprite.data["frames"]["+100 neutral.png"]["frame"], (575,650)))
        Buttons.append(Button(plu500Img, buttonSprite.data["frames"]["+500 neutral.png"]["frame"], (725,650)))
        Texts.append(Text(smallFont, "Money: " + str(money), True, (500,485), WHITE))

        #MENU LOOP
        while True:
            draw()
            update()
            #CHECK MENU EVENTS
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: #go through each button
                    if Buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                        #quit button
                        pygame.quit()
                        sys.exit()
                    if Buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                        #start button
                        if money != 0:
                            shuffleSound.play()
                            break

                    moneyChange = 0
                    if Buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                        #-500
                        if (money - 500) >= 0:
                            moneyChange = -500
                        else:
                            moneyChange = money * -1

                        chipSound.play()
                    if Buttons[3].rect.collidepoint(pygame.mouse.get_pos()):
                        #-100
                        if (money - 100) >= 0:
                            moneyChange = -100

                        chipSound.play()
                    if Buttons[4].rect.collidepoint(pygame.mouse.get_pos()):
                        #+100
                        moneyChange = +100

                        chipSound.play()
                    if Buttons[5].rect.collidepoint(pygame.mouse.get_pos()):
                        #+500
                        moneyChange = +500

                        chipSound.play()

                    money += moneyChange
                    Texts[0].changetext("Money: " + str(money))
            else:
                continue
            break

        #PLAYING LOOP
        while True:
            #RESET -- include game deck here
            resetVars()
            #setting up deck
            PlayDeck.clear()
            for x in range(0,len(cardNames)):
                val = (x % 13) + 1
                if val > 10:
                    val = 10
                PlayDeck.append(Card(cardSprite.parse_sprite(cardNames[x]),cardBack,val))

            pot = 0
            #SET UP Betting
            dispBackg = bettingBackg
            Buttons.append(Button(dealImg, buttonSprite.data["frames"]["Deal neutral.png"]["frame"], (700,400)))
            Buttons.append(Button(min500Img, buttonSprite.data["frames"]["-500 neutral.png"]["frame"], (140,720)))
            Buttons.append(Button(min100Img, buttonSprite.data["frames"]["-100 neutral.png"]["frame"], (290,720)))
            Buttons.append(Button(plu100Img, buttonSprite.data["frames"]["+100 neutral.png"]["frame"], (240,570)))
            Buttons.append(Button(plu500Img, buttonSprite.data["frames"]["+500 neutral.png"]["frame"], (90,570)))
            Texts.append(Text(smallFont, "Bet: " + str(pot), False, (25,425), BLACK))
            Texts.append(Text(smallFont, "Money: " + str(money), False, (25,325), BLACK))

            #BETTING LOOP
            while True:
                draw()
                update()
                #CHECK BETTING EVENTS
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if Buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                            #deal
                            break #play sound here?

                        potChange = 0
                        moneyChange = 0
                        if Buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                            #-500
                            if (pot - 500) >= 0:
                                potChange = -500
                                moneyChange = +500
                            else:
                                potChange = pot * -1
                                moneyChange = pot

                            chipSound.play()
                        if Buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                            #-100
                            if (pot - 100) >= 0:
                                potChange = -100
                                moneyChange = +100
                            else:
                                potChange = pot * -1
                                moneyChange = pot

                            chipSound.play()
                        if Buttons[3].rect.collidepoint(pygame.mouse.get_pos()):
                            #+100
                            if (money - 100) >= 0:
                                potChange = +100
                                moneyChange = -100
                            else:
                                potChange = money
                                moneyChange = money * -1

                            chipSound.play()
                        if Buttons[4].rect.collidepoint(pygame.mouse.get_pos()):
                            #+500
                            if (money - 500) >= 0:
                                potChange = +500
                                moneyChange = -500
                            else:
                                potChange = money
                                moneyChange = money * -1

                            chipSound.play()

                        pot += potChange
                        money += moneyChange
                        Texts[0].changetext("Bet: " + str(pot))
                        Texts[1].changetext("Money: " + str(money))
                else:
                    continue
                break

            #RESET
            Buttons.clear()
            #SET UP Dealing
            dispBackg = dealingBackg
            Buttons.append(Button(hitImg, buttonSprite.data["frames"]["Hit neutral.png"]["frame"], (110,600)))
            Buttons.append(Button(standImg, buttonSprite.data["frames"]["Stand neutral.png"]["frame"], (260,700)))
            if (money - pot) >= 0:
                Buttons.append(Button(doubleImg, buttonSprite.data["frames"]["Double neutral.png"]["frame"], (700,400)))
            Texts.append(Text(smallFont, str(0), True, (450,200), WHITE)) # dealer value, 2nd index
            Texts.append(Text(smallFont, str(0), True, (450,600), WHITE)) # player value, 3rd index

            #draw first 2 cards
            mainDraw(dealerHand)
            mainDraw(dealerHand)
            dealerHand.hold[1].show()
            if dealerHand.hold[1].value == 1:
                Texts[2].changetext(str(11))
            else:
                Texts[2].changetext(str(dealerHand.hold[1].value))
            draw()
            update()

            blackjack = False

            mainDraw(playerHand)
            playerHand.hold[0].show()
            Texts[3].changetext(str(playerHand.detVal()))
            draw()
            update()
            mainDraw(playerHand)
            playerHand.hold[1].show()
            Texts[3].changetext(str(playerHand.detVal()))
            draw()
            update()

            if playerHand.detVal() == 21:
                blackjack = True

            #DEALING LOOP
            if not blackjack:
                while playerHand.detVal() <= 21:
                    draw()
                    update()
                    #CHECK DEALING EVENTS
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if Buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                                #Hit
                                if len(Buttons) == 3:
                                    Buttons.pop(2)

                                mainDraw(playerHand)
                                playerHand.hold[len(playerHand.hold) - 1].show()
                                Texts[3].changetext(str(playerHand.detVal()))
                            if Buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                                #Stand, play sound
                                break
                            if len(Buttons) == 3:
                                if Buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                                    money -= pot
                                    pot *= 2

                                    Texts[0].changetext("Bet: " + str(pot))
                                    Texts[1].changetext("Money: " + str(money))

                                    mainDraw(playerHand)
                                    playerHand.hold[len(playerHand.hold) - 1].show()
                                    Texts[3].changetext(str(playerHand.detVal()))

                                    break
                    else:
                        continue
                    break

                #dealer draws until over 16
                if (playerHand.detVal() <= 21):

                    dealerHand.hold[0].show()
                    Texts[2].changetext(str(dealerHand.detVal()))
                    for x in range(int(FPS * .5)): #idle draw for half second
                        draw()
                        update()

                    while dealerHand.detVal() < 17:
                        mainDraw(dealerHand)
                        dealerHand.hold[len(dealerHand.hold) - 1].show()
                        Texts[2].changetext(str(dealerHand.detVal()))
                        draw()
                        update()

            for x in range(int(FPS * .5)): #idle draw for half second
                draw()
                update()

            #determine results and adjust, display, reset
            pVal = playerHand.detVal()
            dVal = dealerHand.detVal()

            #add to text list or draw manually
            if blackjack:
                gain = int(pot*2.5)
                money += gain

                resText1 = smallFont.render("+" + str(gain), True, YELLOW)
                resRect1 = resText1.get_rect(center = (500,600))

                resText2 = mediumFont.render("BLACKJACK", True, YELLOW)
                resRect2 = resText2.get_rect(center = (500,250))
            elif (pVal > dVal or dVal > 21) and (pVal <= 21):
                #player wins
                gain = pot*2
                money += gain

                resText1 = smallFont.render("+" + str(gain), True, GREEN)
                resRect1 = resText1.get_rect(center = (500,600))

                resText2 = largeFont.render("WIN", True, GREEN)
                resRect2 = resText2.get_rect(center = (500,250))
            elif (pVal < dVal or pVal > 21):
                #dealer wins
                loss = pot

                if pVal > 21:
                    type = "BUST"
                else:
                    type = "LOSE"

                resText1 = smallFont.render("-" + str(loss), True, RED)
                resRect1 = resText1.get_rect(center = (500,600))

                resText2 = largeFont.render(type, True, RED)
                resRect2 = resText2.get_rect(center = (500,250))
            elif (pVal == dVal):
                #push
                push = pot
                money += push

                resText1 = smallFont.render("+" + str(push), True, BLUE)
                resRect1 = resText1.get_rect(center = (500,600))

                resText2 = largeFont.render("PUSH", True, BLUE)
                resRect2 = resText2.get_rect(center = (500,250))

            #display results
            dealResetPos = []
            playResetPos = []
            for x in range(len(dealerHand.hold)):
                dealResetPos.append((125,150))
            for x in range(len(playerHand.hold)):
                playResetPos.append((125,150))
            #remove text in the way
            Texts.pop(3)
            Texts.pop(2)

            shuffleSound.play()

            for x in range(FPS * 2): # how many seconds wait
                dealerHand.move(dealResetPos, SPEED)
                playerHand.move(playResetPos, SPEED)
                draw()
                DISPLAY.blit(resText1,resRect1)
                DISPLAY.blit(resText2,resRect2)
                update()

            #IF BROKE: BREAK
            if money <= 0:
                defeat()
                break

if __name__ == "__main__":
    main()
