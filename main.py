import sys
import os
import time
import random

import pygame
import colors
import camera

from spritesheet import spritesheet
from sprites import Player
from sprites import FireBall

class Game:
    WIDTH      = 720
    HEIGHT     = WIDTH / 12 * 9 #16:9 Aspect ratio
    SIZE       = (WIDTH, HEIGHT)

    MAP_WIDTH  = 1920
    MAP_HEIGHT = 1080
    MAP_SIZE   = (MAP_WIDTH, MAP_HEIGHT)

    FPS        = 60
    TIME_LIMIT = 60
    GAME_OVER  = False
    HAS_WON    = False
    HAS_LAST   = False

    BALL_ADD   = 3
    BALL_SPAWN = 10

    def __init__(self):
        self.running  = True
        self.lasted   = 0
        self.last_num = None

        pygame.init()

        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Can You Live?")

        self.clock  = pygame.time.Clock()
        self.camera = camera.Camera(self.SIZE, self.MAP_SIZE)

        self.create_resources()
        self.create_sprites()
        self.create_text()

    """ Creation Functions """

    # cache resources once to not re-use
    def create_resources(self):
        # set image paths
        self.bg_path = os.path.join("images","background.jpg")
        self.dragon_path = os.path.join("images","dragon_red.png")
        self.fire_path = os.path.join("images","fire.png")

        # transparent color for sprite sheets
        ckey = colors.BLACK

        # create dragon frames from sprite sheet
        ss = spritesheet( self.dragon_path )
        self.dragon_frames = []
        self.dragon_frames.append(ss.image_at((0, 160, 280, 240),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((280, 160, 280, 240),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((590, 140, 280, 260),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((880, 180, 280, 240),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((1160, 180, 280, 240),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((1440, 180, 280, 240),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((1760, 180, 280, 240),colorkey=ckey))
        self.dragon_frames.append(ss.image_at((2050, 180, 280, 240),colorkey=ckey))
        self.dragon_frames_flipped = self.generate_flipped_frames(self.dragon_frames)

        # create fire frames from sprite sheet
        ss = spritesheet( self.fire_path )
        self.fire_frames = []
        self.fire_frames.append(ss.image_at((130, 0, 75, 45),colorkey=ckey))
        self.fire_frames.append(ss.image_at((130, 45, 75, 45),colorkey=ckey))
        self.fire_frames.append(ss.image_at((130, 90, 75, 45),colorkey=ckey))
        self.fire_frames.append(ss.image_at((130, 130, 75, 45),colorkey=ckey))
        self.fire_frames_flipped = self.generate_flipped_frames(self.fire_frames)

    # create sprites for game
    def create_sprites(self):
        self.entities = pygame.sprite.Group()

        self.bg = pygame.image.load(self.bg_path).convert()
        self.bg = pygame.transform.smoothscale(self.bg, self.MAP_SIZE)
        self.bg_rect = self.bg.get_rect()

        self.player = Player(self)
        self.entities.add( self.player )

    # Render text only once
    def create_text(self):
        self.time_font      = pygame.font.Font(None, 30)
        self.gameover_font  = pygame.font.Font(None, 120)
        self.last_font      =  pygame.font.Font(None, 90)

        # generate rendered numbers so don't have to re-render
        self.numbers = {}
        for x in range(self.TIME_LIMIT + 1):
            self.numbers[str(x)] = self.time_font.render(str(x), 1, colors._BLACK)

        # generate cached text
        self.over_text = self.gameover_font.render("Game Over!", 1, colors._BLACK)
        self.win_text  = self.gameover_font.render("You Win!", 1, colors._BLACK)

        self.won_bg, self.lost_bg = pygame.Surface(self.SIZE), pygame.Surface(self.SIZE)
        self.won_bg.fill((10, 185, 13))
        self.lost_bg.fill((155, 0, 0))

    # generate animation flipped frames
    def generate_flipped_frames(self, frames):
        return [pygame.transform.flip(frame, True, False) for frame in frames]

    # generate random fireball
    def gen_rand_fireball(self, damage=None):
        coords = [0, 0]
        coords[0] = random.randint( self.WIDTH/2 ,self.MAP_WIDTH)
        coords[1] = random.randint(0 ,self.MAP_HEIGHT)
        self.spawn_fireball( coords, damage)

    # add more fireballs
    def add_fireballs(self):
        print "adding {} fireballs".format(self.BALL_ADD)
        for x in range( self.BALL_ADD ):
            self.gen_rand_fireball()

        self.BALL_ADD += int(self.BALL_ADD/3)

    # create a new fireball
    def spawn_fireball(self, coords, damage=None):
        fireball = FireBall(self)
        fireball.set_pos(coords)
        self.entities.add( fireball )

    # kill a fireball object
    def kill_ball(self, fireball):
        self.entities.remove( fireball )
        fireball.kill()
        del fireball

    # check fireball collisions and deal damage
    def check_collisions(self):
        fireballs = [e for e in self.entities.sprites() if e.block_id != "player"]
        fire_rects = [e.rect for e in fireballs]

        collision = self.player.rect.collidelist( fire_rects )
        if collision > -1:
            fireball = fireballs[ collision ]
            self.player.HP -= fireball.damage
            self.kill_ball( fireball )

    # clear left over memory because game is over :)
    def clear_all(self):
        for e in self.entities.sprites():
            self.kill_ball( e )

        del self.bg
        del self.bg_rect
        del self.entities
        del self.camera
        del self.player
        del self.numbers
        del self.time_font

    """ Drawing Functions """

    # Lose screen
    def draw_game_over(self):
        if not self.HAS_LAST:
            self.last_text = self.last_font.render("Lasted {} secs".format(self.lasted), 1, colors._BLACK)
            self.HAS_LAST = True

        self.screen.blit(self.lost_bg, (0,0))
        self.screen.blit(self.over_text, (self.WIDTH/2-240, self.HEIGHT/2-120))
        self.screen.blit(self.last_text, (self.WIDTH/2-240, self.HEIGHT/2))

    # Win screen
    def draw_win(self):
        self.screen.blit(self.won_bg, (0,0))
        self.screen.blit(self.win_text, (self.WIDTH/2-180, self.HEIGHT/2-120))

    # Health Bar
    def draw_health(self):
        # calculate color
        if self.player.HP > 60:
            color = colors.H_GREEN
        elif self.player.HP > 30:
            color = colors.H_YELLOW
        else:
            color = colors.H_RED

        # calculate bar size
        bar_width = 200.0
        percent_left = (self.player.HP * bar_width) / (self.player.MAX_HP*1.0)
        percent_lost = ((self.player.MAX_HP-self.player.HP) * bar_width) / (self.player.MAX_HP*1.0)

        # draw remaining health
        pygame.draw.rect(self.screen, color, (5, 5, percent_left, 20))

        # draw lost health
        pygame.draw.rect(self.screen, colors.BLACK,
            (5+percent_left, 5, percent_lost, 20))

    """ Game Functions """

    def run(self):
        start = time.time() # start timer

        while self.running:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if not self.GAME_OVER: self.player.update_stop(event)

            if not self.GAME_OVER:
                # update objects and screen
                self.camera.update(self.player)
                self.entities.update()
                self.check_collisions()

                # draw images
                self.screen.fill(colors.BLACK)
                self.screen.blit(self.bg, self.camera.apply(self.bg_rect))
                for e in self.entities.sprites():
                    if e.block_id != "player":
                        self.screen.blit(e.image, self.camera.apply(e.rect))
                
                self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
                self.draw_health()

                # spawn fireballs
                if self.last_num != self.lasted:
                    self.last_num = self.lasted
                    if self.lasted % self.BALL_SPAWN == 0:
                        self.add_fireballs()

                # keep constant amount of fireballs on screen
                sprite_num = len(self.entities.sprites())
                if sprite_num < self.BALL_ADD:
                    to_add = self.BALL_ADD - sprite_num
                    for x in range(to_add):
                        self.gen_rand_fireball()

                # calculate & draw time
                elapsed = round(time.time() - start, 1)
                self.lasted = int(elapsed)
                if self.lasted >= self.TIME_LIMIT:
                    self.GAME_OVER = True
                    self.HAS_WON   = True
                    self.clear_all()

                if not self.GAME_OVER:
                    self.screen.blit( self.numbers[str(self.lasted)], (self.WIDTH-80, 10))

                # handle game over
                if not self.GAME_OVER:
                    if self.player.HP <= 0:
                        self.GAME_OVER = True
                        self.clear_all()

            else:
                if self.HAS_WON:
                    self.draw_win()
                else:
                    self.draw_game_over()

            # update pygame
            self.clock.tick( self.FPS )
            pygame.display.flip()

        self.exit()

    def exit(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()