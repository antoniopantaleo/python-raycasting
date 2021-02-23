import pygame
from math import sqrt, cos, sin, pi, inf
from random import randint


class Scene:

    def __init__(self, size):
        self.background = (30, 30, 30)
        self.screen = pygame.display.set_mode((size, size))
        self.walls = []
        self.__add_walls()
        self.source = Source(self.screen, (150, 250))
        pygame.init()

    def __add_walls(self):
        def r(): return randint(0, 500)
        for _ in range(0, 3):
            self.walls.append(Wall(self.screen, (r(), r()), (r(), r())))
        # BOUNDS
        self.walls.append(Wall(self.screen, (0, 0), (0, 500)))
        self.walls.append(Wall(self.screen, (0, 0), (500, 0)))
        self.walls.append(Wall(self.screen, (500, 0), (500, 500)))
        self.walls.append(Wall(self.screen, (0, 500), (500, 500)))
        # ---

    def draw(self):
        RUNNING = True
        while RUNNING:
            self.screen.fill(self.background)
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    RUNNING = False
            mouse_pos = pygame.mouse.get_pos()
            self.source.update(mouse_pos)
            for wall in self.walls:
                wall.draw()
            self.source.draw(self.walls)

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


class Ray:

    def __init__(self, screen, pos, angle):
        self.screen = screen
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = self.x1 + (1000*cos(angle))
        self.y2 = self.y1 + (1000*sin(angle))
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


class Source:

    def __init__(self, screen, center):
        self.screen = screen
        self.center = center
        self.rays = []
        self.__init_rays()

    @staticmethod
    def rad2deg(rad):
        return rad * pi / 180

    def __init_rays(self):
        for a in range(0, 360, 3):
            a = Source.rad2deg(a)
            self.rays.append(
                Ray(self.screen, self.center, a))

    def update(self, pos):
        self.center = pos
        self.rays = []
        self.__init_rays()

    def draw(self, walls):
        for r in self.rays:
            point = None
            dis = inf
            for wall in walls:
                p = r.cast(wall)
                if p != None:
                    curr_dist = sqrt(
                        (self.center[0]-p[0])**2+(self.center[1]-p[1])**2)
                    if curr_dist < dis:
                        point = p
                        dis = curr_dist
            if point != None:
                pygame.draw.line(self.screen, (255, 255, 255),
                                 self.center, point)
