import pygame
import colors

""" Direction Facing """
class DirectionEnum:
    LEFT   = 0x00
    RIGHT  = 0x01

class Sprite(pygame.sprite.Sprite):
    SIZE     = WIDTH, HEIGHT = 64, 64
    block_id = None

    vspeed    = 0
    hspeed    = 0
    speed     = 5
    accel     = .5
    v_decel   = False
    h_decel   = False
    s_limit   = 1

    UP          = pygame.K_w
    DOWN      = pygame.K_s
    LEFT      = pygame.K_a
    RIGHT     = pygame.K_d

    DIR       = DirectionEnum()
    direction = DIR.RIGHT

    def __init__(self, game):
        super(Sprite, self).__init__()
        self.game = game

        self.create_basics()

        self.image = pygame.Surface(self.SIZE)
        self.image.fill(colors.BLUE)
        self.rect  = self.image.get_rect()

    def create_basics(self):
        self.ani_frame = 0
        self.ani_count = 0
        self.ani_delay = 5
        self.frames = {
            str(self.DIR.LEFT): [],
            str(self.DIR.RIGHT): []
        }

    def update(self):
        # move player
        self.movement()

        # limit player to borders
        limit_width, limit_height = self.game.MAP_SIZE
        if self.rect.x < 0: self.rect.x = 0
        if self.rect.x + self.WIDTH > limit_width: self.rect.x = limit_width - self.WIDTH
        if self.rect.y < 0: self.rect.y = 0
        if self.rect.y + self.HEIGHT > limit_height: self.rect.y = limit_height - self.HEIGHT

        # animate player
        self.animate()

        # update player movement
        self.update_deceleration()
        if self.block_id == "player":
            self.update_movement()

    # animate the sprite from array of frames
    def animate(self):
        if self.ani_count <= self.ani_delay:
            self.ani_count += 1
        else:
            self.ani_count = 0
            frames = self.frames[str(self.direction)]
            if frames != []:
                if self.ani_frame < len(frames) - 1:
                    self.ani_frame += 1
                else:
                    self.ani_frame = 0
                self.image = frames[self.ani_frame]

    # set sprite hitbox size
    def set_hitbox_size(self, size):
        self.rect = pygame.Rect((self.rect.x, self.rect.y), size)
        self.SIZE = self.WIDTH, self.HEIGHT = size

    # resize frames
    def resize_frames(self, frames, size):
        return [pygame.transform.smoothscale(f, size) for f in frames]

    """ Move Sprite """
    def movement(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed

    """ Handle sprite acceleration """
    def update_movement(self, _keys=None):
        # update movement by keys
        keys = pygame.key.get_pressed()
        if _keys is not None:
            keys = _keys

        # update direction
        if keys[self.RIGHT]: self.direction = self.DIR.RIGHT
        if keys[self.LEFT]: self.direction = self.DIR.LEFT

        # update deceleration
        if keys[self.UP] or keys[self.DOWN]:
            self.v_decel = False
        if keys[self.LEFT] or keys[self.RIGHT]:
            self.h_decel = False

        # update acceleration
        if keys[self.DOWN]:
            if self.vspeed < self.speed:
                if self.vspeed <= self.speed - self.accel:
                    self.vspeed += self.accel

        if keys[self.UP]:
            if self.vspeed > -self.speed:
                if self.vspeed >= -self.speed + self.accel:
                    self.vspeed -= self.accel

        if keys[self.RIGHT]:
            if self.hspeed < self.speed:
                if self.hspeed <= self.speed - self.accel:
                    self.hspeed += self.accel

        if keys[self.LEFT]:
            if self.hspeed > -self.speed:
                if self.hspeed >= -self.speed + self.accel:
                    self.hspeed -= self.accel

    """ Handle sprite deceleration """
    def update_deceleration(self):
        # Deceleration
        if self.v_decel:
            # Gradual Vertical deceleration
            if self.vspeed > 0 and self.vspeed > self.s_limit:
                self.vspeed -= self.accel * 1.5
            if self.vspeed < 0 and self.vspeed < -self.s_limit:
                self.vspeed += self.accel * 1.5
            if self.vspeed <= self.s_limit or self.vspeed >= self.s_limit:
                self.vspeed = 0

        if self.h_decel:
            # Gradual horizontal deceleration
            if self.hspeed > 0 and self.hspeed > self.s_limit:
                self.hspeed -= self.accel * 1.5
            if self.hspeed < 0 and self.hspeed < -self.s_limit:
                self.hspeed += self.accel * 1.5
            if self.hspeed <= self.s_limit or self.hspeed >= self.s_limit:
                self.hspeed = 0

    """ Decrease Player movement """
    def update_stop(self, event):
        if event is not None and event.type == pygame.KEYUP:
            if event.key in [self.UP, self.DOWN]:
                self.v_decel = True

            if event.key in [self.LEFT, self.RIGHT]:
                self.h_decel = True