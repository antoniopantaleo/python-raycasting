import pygame
from math import sqrt
from random import randint


class Scene:

    def __init__(self, size):
        self.background = (30, 30, 30)
        self.screen = pygame.display.set_mode((size, size))
        self.walls = []
        self.__add_walls()
        self.ray = Ray(self.screen, (100, 250), (0, -100))
        pygame.init()

    def __add_walls(self):
        def r(): return randint(0, 500)
        for _ in range(0, 5):
            self.walls.append(Wall(self.screen, (r(), r()), (r(), r())))

    def draw(self):
        RUNNING = True
        while RUNNING:
            self.screen.fill(self.background)
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    RUNNING = False
            self.ray.lookAt(pygame.mouse.get_pos())
            for wall in self.walls:
                wall.draw()
                point = self.ray.cast(wall)
                if point != None:
                    pygame.draw.circle(self.screen, (255, 255, 255), point, 5)

            self.ray.draw()
            pygame.display.update()


class Wall:

    def __init__(self, screen, start, end):
        self.screen = screen
        self.x1 = start[0]
        self.y1 = start[1]
        self.x2 = end[0]
        self.y2 = end[1]

    def draw(self):
        pygame.draw.line(self.screen, (255, 255, 255),
                         (self.x1, self.y1), (self.x2, self.y2), 3)


class Source:
    pass


class Ray:

    def __init__(self, screen, pos, dir):
        self.screen = screen
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = self.x1 + dir[0]
        self.y2 = self.y1 + dir[1]
        self.color = (255, 255, 255)

    def draw(self):
        pygame.draw.line(self.screen, self.color,
                         (self.x1, self.y1), (self.x2, self.y2))

    def lookAt(self, pos):
        x = pos[0]
        y = pos[1]

        V = int(sqrt(x**2 + y**2))
        V = 1
        if V > 0:
            self.x2 = (self.x1 + (x - self.x1) // V)
            self.y2 = (self.y1 + (y - self.y1) // V)
            print(f"** DEBUG: ray: {(self.x1,self.y1,self.x2,self.y2)}")

    def cast(self, wall):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        x3 = wall.x1
        y3 = wall.y1
        x4 = wall.x2
        y4 = wall.y2

        point = None

        denom = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))

        if denom == 0:
            return point

        u = (((x1-x3)*(y3-y4))-((y1-y3)*(x3-x4)))/denom
        t = (((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3)))/denom

        if t >= 0 and t <= 1 and u >= 0:
            point = (x1 + u*(x2-x1), y1 + u*(y2-y1))

        return point
