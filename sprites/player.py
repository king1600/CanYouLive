import pygame
import colors

from sprite import Sprite

class Player(Sprite):
    def __init__(self, game):
        super(Player, self).__init__(game)
        self.block_id = "player"

        self.MAX_HP   = 100
        self.HP       = self.MAX_HP

        self.speed    = 10

        _size         = (96, 96)
        self.frames[str(self.DIR.RIGHT)] = self.resize_frames(self.game.dragon_frames, _size)
        self.frames[str(self.DIR.LEFT)]  = self.resize_frames(self.game.dragon_frames_flipped, _size)