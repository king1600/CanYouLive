import pygame

""" Camera Scrolling for Player """
class Camera(object):
    def __init__(self, window_size, map_size):
        self.update_camera(window_size, map_size)

    def update_camera(self, window_size, map_size):
        self._size = window_size
        self.state = pygame.Rect(0, 0, map_size[0], map_size[1])

    def apply(self, target):
        return target.move(self.state.topleft)

    def update(self, target):
        self.state = self.complex_camera(target.rect)

    def complex_camera(self, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = self.state
        l, t, _, _ = -l + self._size[0]/2, -t + self._size[1]/2, w, h

        # stop scrolling at the left edge
        l = min(0, l)
        # stop scrolling at the right edge
        l = max(-(self.state.width - self._size[0]), l)
        # stop scrolling at the bottom
        t = max(-(self.state.height - self._size[1]), t)
        # stop scrolling at the top
        t = min(0, t)

        return pygame.Rect(l, t, w, h)