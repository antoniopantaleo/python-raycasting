from models import Scene
import sys


size = 550

if __name__ == "__main__":
    try:
        angle = int(sys.argv[1])
    except:
        angle = 1
    scene = Scene(size, angle)
    scene.draw()
