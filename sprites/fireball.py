import pygame
import colors

from sprite import Sprite

class FireBall(Sprite):
    def __init__(self, game):
        super(FireBall, self).__init__(game)

        self.block_id    = "fireball"
        self.damage      = 10
        self.speed       = 3
        self.player      = self.game.player
        self.direction   = self.DIR.LEFT

        self.react_delay = 2
        self.react_count = 0

        _size            = (64, 64)
        self.frames[str(self.DIR.RIGHT)] = self.resize_frames(self.game.fire_frames, _size)
        self.frames[str(self.DIR.LEFT)]  = self.resize_frames(self.game.fire_frames_flipped, _size)

    def set_pos(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def follow(self):

        ###### Go up ######
        if self.player.rect.y < self.rect.y: # go up
            if self.vspeed > -self.speed:
                if self.vspeed >= -self.speed + self.accel:

                    # delay the seeking to seem realistic
                    if self.react_count <= self.react_delay:
                        self.react_count += 1
                    else:
                        self.react_count = 0
                        self.vspeed -= self.accel

        ###### Go down ######
        elif self.player.rect.y > self.rect.y:
            if self.vspeed < self.speed:
                if self.vspeed <= self.speed - self.accel:
                        
                    # delay the seeking to seem realistic
                    if self.react_count <= self.react_delay:
                        self.react_count += 1
                    else:
                        self.react_count = 0
                        self.vspeed += self.accel

        ##### no vertical change #####
        else:
            self.vspeed = 0

        self.rect.y += self.vspeed # update vertical movement

    def movement(self):
        # move fireball
        if self.direction == self.DIR.RIGHT:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def update(self):
        self.follow()
        self.movement()

        # kill if reaches end of screen
        limit_width, limit_height = self.game.MAP_SIZE
        if self.rect.x < 0: self.game.kill_ball(self)
        if self.rect.x + self.WIDTH > limit_width: self.game.kill_ball(self)

        self.animate()
