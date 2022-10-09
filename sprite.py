import framebuf
import time

GROUND = 128
GRAVITY = 0.15
JUMP_VELOCITY = -4
MULTIPLIER = 0.1

def create_img_buffer(path):
    with open(path, "rb") as f:
        img_type = f.readline()
        if img_type != b"P4\n":
            raise Exception("Image type not supported")
        f.readline()
        dimensions = f.readline()
        w, h = [int(x) for x in dimensions.split(b" ")]
        img = bytearray(f.read())
    img_buffer = framebuf.FrameBuffer(img, w, h, framebuf.MONO_HLSB)
    return img_buffer, w, h

class Sprite():
    def __init__(self, x, path):
        self.bitmap, self.width, self.height = create_img_buffer(path)
        self.x = x
        self.y = GROUND - self.height

class Dino():
    def __init__(self, x):
        self.last_update = 0
        self.sprite = Sprite(x, './dino.pbm')
        self.movement_y = 0

    def jump(self):
        self.movement_y = JUMP_VELOCITY

    def can_jump(self):
        return self.sprite.y == GROUND - self.sprite.height

    def do_update(self, now):
        diff = time.ticks_diff(now, self.last_update)

        self.movement_y +=  GRAVITY * diff * MULTIPLIER
        self.sprite.y = self.sprite.y + self.movement_y * diff * MULTIPLIER

        if self.sprite.y >= GROUND - self.sprite.height:
            self.sprite.y = GROUND - self.sprite.height
            self.movement_y = 0

        self.last_update = now

class Tree():
    def __init__(self, x, now):
        self.last_update = now
        self.sprite = Sprite(x, './cactus.pbm')
        self.movement_x = -1.5

    def do_update(self, now):
        diff = time.ticks_diff(now, self.last_update)
        self.sprite.x = self.sprite.x + self.movement_x * diff * MULTIPLIER
        print(self.sprite.x)
        self.last_update = now



def check_collision(dino, obstacles):
    for obstacle in obstacles:
        if (dino.sprite.x + dino.sprite.width >= obstacle.sprite.x and obstacle.sprite.x + obstacle.sprite.width >= dino.sprite.x and
            dino.sprite.y + dino.sprite.height >= obstacle.sprite.y and obstacle.sprite.y + obstacle.sprite.height >= dino.sprite.y):
            return True
    return False

def render(display, element):
    display.blit(element.sprite.bitmap, int(element.sprite.x), int(element.sprite.y), framebuf.MONO_VLSB)
