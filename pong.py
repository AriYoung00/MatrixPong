import time


class DrawableRect(object):
    pos = (0, 0)
    velocity = (0, 0)
    height = 0
    width = 0

    def __init__(self, height = 1, width = 1, velocity = (0, 0), initial_pos = (0, 0)):
        self.height = height
        self.width = width
        self.pos = initial_pos
        self.velocity = velocity

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def set_pos(self, position):
        self.pos = position

    def move_x(self, dist):
        self.pos[0] += dist

    def move_y(self, dist):
        self.pos[1] += dist

    def move(self, dist):
        self.pos[0] += dist[0]
        self.pos[1] += dist[1]


class RGBMatrixOptions():
    pass

class MatrixWrapper(object):
    matrix = None
    matrix_prefs = None

    def __init__(self, brightness):
        self.matrix_prefs = RGBMatrixOptions()
