import pygame
from math import sqrt, cos, sin, pi, inf
from random import randint


class Scene:

    def __init__(self, size):
        self.background = (30, 30, 30)
        self.screen = pygame.display.set_mode((size+1, size+1))
        pygame.display.set_caption("Ray Casting")
        self.size = size
        self.walls = []
        self.__add_walls()
        self.source = Source(self.screen, (150, 250))
        pygame.init()

    def __add_walls(self):
        def r(): return randint(0, self.size)
        for _ in range(0, 4):
            self.walls.append(Wall(self.screen, (r(), r()), (r(), r())))
        # BOUNDS
        self.walls.append(Wall(self.screen, (0, 0), (0, self.size)))
        self.walls.append(Wall(self.screen, (0, 0), (self.size, 0)))
        self.walls.append(
            Wall(self.screen, (self.size, 0), (self.size, self.size)))
        self.walls.append(
            Wall(self.screen, (0, self.size), (self.size, self.size)))
        # END BOUNDS

    def draw(self):
        RUNNING = True
        while RUNNING:
            self.screen.fill(self.background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
        self.angle = angle
        self.__set_pos(pos)
        self.color = (255, 255, 255)

    def update(self, pos):
        self.__set_pos(pos)

    def __set_pos(self, pos):
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = self.x1 + (1000*cos(self.angle))
        self.y2 = self.y1 + (1000*sin(self.angle))

    def draw_until(self, point):
        pygame.draw.line(self.screen, self.color,
                         (self.x1, self.y1), (point[0], point[1]))

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
    def deg2rad(deg):
        return deg * pi / 180

    def __init_rays(self):
        for a in range(0, 360, 3):
            a = Source.deg2rad(a)
            self.rays.append(
                Ray(self.screen, self.center, a))

    def update(self, pos):
        self.center = pos
        for ray in self.rays:
            ray.update(pos)

    def draw(self, walls):
        for r in self.rays:
            point = None
            distance = inf
            for wall in walls:
                p = r.cast(wall)
                if p != None:
                    curr_dist = sqrt(
                        (self.center[0]-p[0])**2+(self.center[1]-p[1])**2)
                    if curr_dist < distance:
                        point = p
                        distance = curr_dist
            if point != None:
                r.draw_until(point)
