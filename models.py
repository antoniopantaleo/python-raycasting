import pygame


class Scene:

    def __init__(self, size):
        self.background = (30, 30, 30)
        self.screen = pygame.display.set_mode((size, size))
        self.walls = []
        self.__add_walls()
        self.ray = Ray(self.screen, (160, 250), (320, 250))
        pygame.init()

    def __add_walls(self):
        self.walls.append(Wall(self.screen, (400, 100), (400, 400)))

    def draw(self):
        RUNNING = True
        while RUNNING:
            self.screen.fill(self.background)
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    RUNNING = False
            for wall in self.walls:
                wall.draw()
                print(f"** DEBUG: Hit result {self.ray.intersect(wall)}")
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
                         (self.x1, self.y1), (self.x2, self.y2))


class Source:
    pass


class Ray:

    def __init__(self, screen, pos, dir):
        self.screen = screen
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = dir[0]
        self.y2 = dir[1]

    def draw(self):
        pygame.draw.line(self.screen, (255, 255, 255),
                         (self.x1, self.y1), (self.x2, self.y2))

    def intersect(self, wall):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        x3 = wall.x1
        y3 = wall.y1
        x4 = wall.x2
        y4 = wall.y2

        denom = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))

        t = (((x1-x3)*(y3-y4))-((y1-y3)*(x3-x4)))/denom
        u = (((x2-x1)*(y1-y3))-((y2-y1)*(x1-x3)))/denom

        return t >= 0 and t <= 1 and u >= 0
