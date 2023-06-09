import sys
import pygame
import color
import random
import os
from pygame.locals import *
import math
import numpy as np

class Text:
    def __init__(self, text, text_color, font_type, size):
        self.text = text
        self.text_color = text_color
        self.font_type = font_type
        self.size = size

        font = pygame.font.SysFont(self.font_type, self.size)
        self.text_image = font.render(self.text, True, self.text_color).convert_alpha()

        self.text_width = self.text_image.get_width()
        self.text_height = self.text_image.get_height()

    def display(self, surface: pygame.Surface, center_x, center_y):
        x = center_x - self.text_width / 2
        y = center_y - self.text_height / 2
        surface.blit(self.text_image, (x, y))


class SurfaceColor:
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height

        self.color_image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.color_image.fill(self.color)

    def display(self, surface: pygame.Surface, center_x, center_y):
        x = center_x - self.width / 2
        y = center_y - self.height / 2
        surface.blit(self.color_image, (x, y))


class Button_Text(Text):
    def __init__(self, text, text_color, font_type, size):
        super().__init__(text, text_color, font_type, size)

        self.rect = self.text_image.get_rect()

    def display(self, surface: pygame.Surface, center_x, center_y):
        super().display(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command()


class Button_Surface(SurfaceColor):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.rect = self.color_image.get_rect()

    def display(self, surface: pygame.Surface, center_x, center_y):
        super().display(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command()


def background(title):
    pygame.display.set_caption('Color Memory Game')

    screen = pygame.display.set_mode((500, 500))
    screen.fill((250, 240, 230))
    size = 500, 500

    t = pygame.font.SysFont('arial', 30)

    text = t.render(title, True, (112, 128, 144))
    text_rect = text.get_rect()

    text_rect.center = (250, 40)



    screen.blit(text, text_rect)

    return size, screen

# white_s = rect
# red_s = circle
# green_s = ellipse
# blue_s = line
# yellow_s = arc
# orange_s = polygon_3
# purple_s = none

class InterFace:
    rounds = "1"
    def __init__(self):
        pygame.init()

    def shape(self, fun, pos, screen):
        if fun == "white":
            rp = (pos[0]-15, pos[1]-15)
            return pygame.draw.rect(screen, (0,0,0), Rect(rp, (15,15)))
        elif fun == "red":
            return pygame.draw.circle(screen, (225,225,225), pos, 15)
        elif fun == "green":
            rp = (pos[0] - 15, pos[1] - 15)
            return pygame.draw.ellipse(screen, (225,225,225), Rect(rp,(15,15)))
        elif fun == "blue":
            return pygame.draw.line(screen, (225,225,225), (pos[0]-10, pos[1]), (pos[0]+10, pos[1]))
        elif fun == "yellow":
            return pygame.draw.arc(screen, (0,0,0), (pos[0]-25, pos[1]-15, 50, 25), math.radians(45), math.radians(180))
        elif fun == "orange":
            vertices = [(pos[0], pos[1]-15), (pos[0]-10, pos[1]-5), (pos[0]+10, pos[1]-5)]
            return pygame.draw.polygon(screen, (0,0,0), vertices)




    def home_interface(self):
        if os.path.exists("data_color.txt"):
            os.remove(r'data_color.txt')
        size, screen = background("Remember the order of the colors")
        width, height = size

        button_start = Button_Text('Ready', (25, 202, 173), 'arial', 25)
        button_start.display(screen, 250, 250)

        content = Text("There are ten levels with a gradually increasing Difficulty.", (105, 105, 105), 'arial', 12)
        content.display(screen, 250, 100)

        content_2 = Text(f"You only have {time} seconds to remember.", (105, 105, 105), 'arial', 12)
        content_2.display(screen, 250, 120)

        content_3 = Text("Press ""Ready"" to start", (112, 128, 144), 'arial', 19)
        content_3.display(screen, 250, 200)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.start_interface()

            pygame.display.update()

    def start_interface(self):
        if os.path.exists("data_color.txt"):
            os.remove(r'data_color.txt')
        size, screen = background(f"Round {round_no}")
        width, height = size

        color_3 = random.sample(colors, 3)
        with open('data_color.txt', 'w') as f:
            f.write('\n'.join(color_3))

        face_1 = SurfaceColor(color_3[0], 50, 50)
        face_1.display(screen, 125, 100)
        self.shape(color_3[0], (125, 100), screen)

        face_2 = SurfaceColor(color_3[1], 50, 50)
        face_2.display(screen, 250, 100)
        self.shape(color_3[1], (250, 100), screen)

        face_3 = SurfaceColor(color_3[2], 50, 50)
        face_3.display(screen, 375, 100)
        self.shape(color_3[2], (375, 100), screen)

        # button_start = Button_Text('Start', (25, 202, 173), 'arial', 25)
        # button_start.display(screen, 250, 250)

        countdown_seconds = time
        TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMER_EVENT, 1000)

        text_position = (width // 2, height // 2)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                elif event.type == TIMER_EVENT:
                    countdown_seconds -= 1
                    if countdown_seconds <= 0:
                        self.game_interface_1()

            font = pygame.font.SysFont('arialunicode', 35)
            countdown_text = font.render(str(countdown_seconds), True, (47, 79, 79))
            screen.blit(countdown_text, countdown_text.get_rect(center=text_position))

            screen.fill((250, 240, 230), countdown_text.get_rect(center=text_position))
            screen.blit(countdown_text, countdown_text.get_rect(center=text_position))

            pygame.display.flip()

    def game_interface_1(self):
        pygame.display.set_caption('Color Memory Game')

        screen = pygame.display.set_mode((500, 500))
        screen.fill((250, 240, 230))

        t = pygame.font.SysFont('arialunicode', 20)

        text = t.render("which one is the first color?", True, color.gray, color.cyan)
        text_rect = text.get_rect()

        text_rect.center = (250, 20)

        screen.blit(text, text_rect)
        data_display = []

        f = open("data_color.txt", "r")
        data_1 = f.readlines()[0].strip()
        data_display.append(data_1)
        f.close()

        random_1 = color.allColor
        print(color.allColor)
        random_1.remove(data_1)
        data_display.append(random.sample(random_1, 1)[0])

        random.shuffle(data_display)
        button_1 = Button_Surface(data_display[0], 50, 50)
        button_2 = Button_Surface(data_display[1], 50, 50)
        button_1.display(screen, 150, 100)
        button_2.display(screen, 300, 100)
        self.shape(data_display[0], (150, 100), screen)
        self.shape(data_display[1], (300, 100), screen)

        random_1.append(data_1)
        sign = None
        while True:
            # detect
            # classify
            # output = 'L'


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    button_1 = Button_Surface(data_display[0], 50, 50)
                    button_2 = Button_Surface(data_display[1], 50, 50)
                    button_1.display(screen, 150, 100)
                    button_2.display(screen, 300, 100)
                    self.shape(data_display[0], (150, 100), screen)
                    self.shape(data_display[1], (300, 100), screen)
                    if event.key == K_LEFT:
                        sign = button_1.color
                        # button_d = SurfaceColor((0, 0, 0), 60, 60)
                        # button_d.display(screen, 150, 100)
                        # button_1.display(screen, 150, 100)
                        # self.shape(data_display[0], (150, 100), screen)

                        button_c = Button_Text('Selected', color.gray, 'arialunicode', 12)
                        button_c.display(screen, 150, 100)
                    elif event.key == K_RIGHT:


                        sign = button_2.color
                        # button_d = SurfaceColor((0, 0, 0), 60, 60)
                        # button_d.display(screen, 300, 100)
                        # button_2.display(screen, 300, 100)
                        # self.shape(data_display[1], (300, 100), screen)

                        button_c = Button_Text('Selected', color.gray, 'arialunicode', 12)
                        button_c.display(screen, 300, 100)
                    elif event.key == K_SPACE and sign is not None:
                        if sign == data_1:
                            self.game_interface_2()
                        else:
                            self.errorWin("0%")


            pygame.display.update()

    def game_interface_2(self):

        pygame.display.set_caption('Color Memory Game')

        screen = pygame.display.set_mode((500, 500))
        screen.fill((250, 240, 230))

        t = pygame.font.SysFont('arialunicode', 20)

        text = t.render("which one is the second color?", True, color.gray, color.cyan)
        text_rect = text.get_rect()

        text_rect.center = (250, 20)

        screen.blit(text, text_rect)
        data_display = []
        f = open("data_color.txt", "r")
        data_2 = f.readlines()[1].strip()
        data_display.append(data_2)
        f.close()

        random_2 = color.allColor
        print(color.allColor)
        random_2.remove(data_2)
        data_display.append(random.sample(random_2, 1)[0])

        random.shuffle(data_display)
        button_1 = Button_Surface(data_display[0], 50, 50)
        button_2 = Button_Surface(data_display[1], 50, 50)
        button_1.display(screen, 150, 100)
        self.shape(data_display[0], (150, 100), screen)
        button_2.display(screen, 300, 100)
        self.shape(data_display[1], (300, 100), screen)
        random_2.append(data_2)
        sign = None
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    button_1 = Button_Surface(data_display[0], 50, 50)
                    button_2 = Button_Surface(data_display[1], 50, 50)
                    button_1.display(screen, 150, 100)
                    self.shape(data_display[0], (150, 100), screen)
                    button_2.display(screen, 300, 100)
                    self.shape(data_display[1], (300, 100), screen)
                    if event.key == K_LEFT:
                        sign = button_1.color
                        button_c = Button_Text('Selected', color.gray, 'arialunicode', 12)
                        button_c.display(screen, 150, 100)
                    elif event.key == K_RIGHT:
                        sign = button_2.color
                        button_c = Button_Text('Selected', color.gray, 'arialunicode', 12)
                        button_c.display(screen, 300, 100)
                    elif event.key == K_SPACE and sign is not None:
                        if sign == data_2:
                            self.game_interface_3()
                        else:
                            self.errorWin("17%")


            pygame.display.update()

    def game_interface_3(self):

        pygame.display.set_caption('Color Memory Game')

        screen = pygame.display.set_mode((500, 500))
        screen.fill((250, 240, 230))

        t = pygame.font.SysFont('arialunicode', 20)

        text = t.render("which one is the third color?", True, color.gray, color.cyan)
        text_rect = text.get_rect()

        text_rect.center = (250, 20)

        screen.blit(text, text_rect)
        data_display = []
        f = open("data_color.txt", "r")
        data_3 = f.readlines()[2].strip()
        data_display.append(data_3)
        f.close()

        random_3 = color.allColor
        print(color.allColor)
        random_3.remove(data_3)
        data_display.append(random.sample(random_3, 1)[0])

        random.shuffle(data_display)
        button_1 = Button_Surface(data_display[0], 50, 50)
        button_2 = Button_Surface(data_display[1], 50, 50)
        button_1.display(screen, 150, 100)
        self.shape(data_display[0], (150, 100), screen)
        button_2.display(screen, 300, 100)
        self.shape(data_display[1], (300, 100), screen)

        random_3.append(data_3)
        sign = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    button_1 = Button_Surface(data_display[0], 50, 50)
                    button_2 = Button_Surface(data_display[1], 50, 50)
                    button_1.display(screen, 150, 100)
                    self.shape(data_display[0], (150, 100), screen)
                    button_2.display(screen, 300, 100)
                    self.shape(data_display[1], (300, 100), screen)
                    if event.key == K_LEFT:
                        sign = button_1.color
                        button_c = Button_Text('Selected', color.gray, 'arialunicode', 12)
                        button_c.display(screen, 150, 100)
                    elif event.key == K_RIGHT:
                        sign = button_2.color
                        button_c = Button_Text('Selected', color.gray, 'arialunicode', 12)
                        button_c.display(screen, 300, 100)
                    elif event.key == K_SPACE and sign is not None:
                        if sign == data_3:
                            global time
                            time = time - 1
                            global round_no
                            round_no = round_no + 1
                            if time <= 0:
                                self.win()
                            else:
                                self.home()
                        else:
                            self.errorWin("33%")


            pygame.display.update()

    def home(self):
        if os.path.exists("data_color.txt"):
            os.remove(r'data_color.txt')
        size, screen = background(f"Round {round_no}")
        width, height = size

        button_start = Button_Text('Ready', (25, 202, 173), 'arial', 25)
        button_start.display(screen, 250, 250)

        content = Text(f"You only have {time} seconds to remember 3 colors.", (105, 105, 105), 'arial', 16)
        content.display(screen, 250, 100)

        content_3 = Text("Press ""Ready"" to start", (112, 128, 144), 'arial', 19)
        content_3.display(screen, 250, 200)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.start_interface()

            pygame.display.update()
            
    def win(self):
        pygame.display.set_caption('Color Memory Game')

        screen = pygame.display.set_mode((500, 500))
        screen.fill((118, 77, 57))

        t = pygame.font.SysFont('arialunicode', 30)

        text = t.render("You Win!!!", True, (161, 23, 21), (229, 187, 129))
        text_rect = text.get_rect()

        text_rect.center = (250, 30)

        screen.blit(text, text_rect)

        button_new = Button_Text('New Game', (34, 8, 7), 'arialunicode', 30)
        button_new.display(screen, 250, 250)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.home_interface()


            pygame.display.update()

    def errorWin(self, acc):
        pygame.display.set_caption('Color Memory Game')

        screen = pygame.display.set_mode((500, 500))
        screen.fill((211, 211, 211))

        t = pygame.font.SysFont('arialunicode', 20)

        text = t.render("Wrong choice!", True, (123, 104, 238))
        text_rect = text.get_rect()

        text_rect.center = (250, 20)

        screen.blit(text, text_rect)

        accuracy = Text("Your Accuracy: "+acc, (123, 104, 238), 'arial', 21)
        accuracy.display(screen, 250, 100)

        button_new = Button_Text('New Game', (72, 61, 139), 'arialunicode', 23)
        button_new.display(screen, 250, 250)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.remove(r'data_color.txt')
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.home_interface()

            pygame.display.update()


if __name__ == '__main__':
    time = 5
    round_no = 1
    colors = color.allColor
    game = InterFace()
    game.home_interface()