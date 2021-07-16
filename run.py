from models import Scene
import sys


size = 550

if __name__ == "__main__":
    angle = None
    try:
        angle = int(sys.argv[1])
    except IndexError as e:
        print(f"IndexError: {e.args} - No argument passed in command line")
    finally:
        if angle is None:
            angle = 1
    scene = Scene(size, angle)
    scene.draw()
