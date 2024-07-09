import pygame
import sys
import os
import math
from pix_player import Player, Platforms, Platforms2, Platforms3, Bullet, Mobs
from pix_player import player_sprites, mobs_sprites, plat_sprites, load_image
from button_game import Button
from settings import SIZE

pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self):
        with open(os.path.join('txt_files', 'record.txt')) as file_scores:
            scores = file_scores.read().strip()
        self.f = int(scores) if scores else 0
        self.botton_sound = pygame.mixer.Sound(os.path.join('data',
                                                            'click.mp3'))
        self.shot = pygame.mixer.Sound(os.path.join('data', 'shot.mp3'))
        self.gameover = pygame.mixer.Sound(os.path.join('data',
                                                        'GameOver.mp3'))
        pygame.mixer.music.load(os.path.join('data', 'music_gameplay.mp3'))
        self.botton_sound.set_volume(0.3)
        self.shot.set_volume(0.07)
        self.gameover.set_volume(0.2)
        pygame.mixer.music.set_volume(0.1)
        self.screen = pygame.display.set_mode(SIZE)
        self.image_menu = load_image("Fon_gl.png")
        self.image_play = load_image('gl.png')
        self.image_glock = load_image('glock_gl.png')
        self.ship_top = self.screen.get_height() - self.image_menu.get_height()
        self.ship_left = (self.screen.get_width() / 2
                          - self.image_menu.get_width() / 2)
        self.running2 = True
        pygame.mouse.set_visible(True)
        self.start = Button(self, 170, 65)
        self.exit_game = Button(self, 170, 70)
        self.fon_ino = pygame.sprite.Group()

    def print_text(self, massage, x, y, color=(0, 0, 0)):
        font_type = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font_type.render(massage, True, color)
        self.screen.blit(text, (x, y))

    def show_menu(self):
        screen = pygame.display.set_mode(SIZE)
        ship_top = screen.get_height() - self.image_menu.get_height()
        ship_left = screen.get_width() / 2 - self.image_menu.get_width() / 2
        running2 = True
        pygame.mouse.set_visible(True)
        self.start.width = 170
        fon_ino = pygame.sprite.Group()

        while running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.botton_sound.play()
            screen.blit(self.image_menu, (ship_left, ship_top))
            screen.blit(self.image_play, (1100, 600))
            screen.blit(self.image_glock, (1090, 650))
            mobs_sprites.update()
            fon_ino.draw(screen)
            self.print_text(f'Record: {self.f}', 155, 30, (255, 255, 100))
            self.print_text('D - Идти вправо', 780, 560, (255, 255, 130))
            self.print_text('A - Идти влево', 780, 590, (255, 255, 130))
            self.print_text('Spase - Прыжок', 780, 620, (255, 255, 130))
            self.print_text('ЛКМ - Выстрел', 780, 650, (255, 255, 130))
            self.start.draw(500, 200, "Играть", self.run_game, 50)
            self.exit_game.draw(500, 600, "Выход", terminate, 50)
            pygame.display.update()
        pygame.quit()

    def run_game(self):
        screen = pygame.display.set_mode(SIZE)

        image = load_image('fon.png')
        image2 = load_image('platforma_11.png')
        image3 = load_image('platforma_2.png')
        image4 = load_image('platforma_3.png')
        ship_top = screen.get_height() - image.get_height()
        ship_left = screen.get_width() / 2 - image.get_width() / 2

        image_jump = pygame.image.load(
            'Animation_super_player/player_left_jump.png')
        image_stay = pygame.image.load(
            'Animation_super_player/player_left_4.png')

        image_jump_right = pygame.image.load(
            'Animation_super_player/player_right_jump.png')
        image_stay_right = pygame.image.load(
            'Animation_super_player/player_right_4.png')

        flagbullets = True
        self.platf = []
        pl1 = Platforms()
        pl2 = Platforms2()
        pl3 = Platforms3()
        self.platf.append(pl1)
        self.platf.append(pl2)
        self.platf.append(pl3)
        up = False
        player = Player(self, 55, 55)
        left = False
        right = False
        flagshot = False
        ak47 = pygame.image.load("data/glock.png")
        ak47_2 = ak47.get_rect(center=screen.get_rect().center)

        def blit_point_to_mouse(target_surf, char_surf, x, y):
            mx, my = pygame.mouse.get_pos()
            dir = (mx - x, my - y)
            length = math.hypot(*dir)
            if length == 0.0:
                dir = (0, -1)
            else:
                dir = (dir[0] / length, dir[1] / length)
            angle = math.degrees(math.atan2(-dir[1], dir[0]))
            rotated_surface = pygame.transform.rotate(char_surf, angle)
            rotated_surface_location = rotated_surface.get_rect(
                center=(player.rect.x + 25, player.rect.y + 35))
            target_surf.blit(rotated_surface, rotated_surface_location)

        pygame.mouse.set_visible(False)
        running = True
        bullets = []
        # pos = (250, 250)
        pygame.mixer.music.play(-1)
        leftorright = False
        font = pygame.font.Font('data/font_super_game.ttf', 30)
        hp = 3
        hp_max = 5
        hp_x = 990
        hp_player = pygame.image.load('data/heart.png')
        self.score = 0
        bullets_count = 10

        def print_hp(hp, hp_x):
            if hp < hp_max:
                for i in range(hp):
                    screen.blit(hp_player, (hp_x, 630))
                    hp_x += 70

        while running:
            pygame.time.delay(17)
            ax, ay, bb, ss = player.rect
            pos = ax + 20, ay + 30
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.score > int(self.f):
                        with open('txt_files/record.txt', 'w') as scores_file:
                            scores_file.write(str(self.score))
                    terminate()
                    # running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        left = True
                    if event.key == pygame.K_d:
                        right = True
                    if event.key == pygame.K_SPACE:
                        up = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        left = False
                    if event.key == pygame.K_d:
                        right = False
                    if event.key == pygame.K_SPACE:
                        up = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and flagshot and bullets_count >= 0:
                        bull = Bullet(*pos)
                        bullets.append(bull)
                        player_sprites.add(bull)
                        self.shot.play()
                        bullets_count -= 1
                    elif not flagshot:
                        flagshot = True

            for i in bullets:
                plathits = pygame.sprite.spritecollideany(i, plat_sprites)
                if plathits:
                    bullets.remove(i)
                    flagbullets = True
                else:
                    flagbullets = False

            for bullet in bullets[:]:
                bullet.update()
                if not screen.get_rect().collidepoint(bullet.pos):
                    bullets.remove(bullet)
                    player_sprites.remove(bullet)
                    flagbullets = True
                else:
                    flagbullets = False

            screen.blit(image, (ship_left, ship_top))

            for bullet in bullets:
                bullet.draw(screen)

            playerhits = pygame.sprite.spritecollide(player, mobs_sprites,
                                                     False)
            for i in bullets:
                bullethits = pygame.sprite.spritecollideany(i, mobs_sprites)

                if bullethits:
                    bullets.remove(i)
                    mobs_sprites.remove(bullethits)
                    self.score += 1
                    bullets_count += 2

            if bullets_count <= 0 and flagbullets:
                pygame.mixer.music.stop()
                mobs_sprites.remove(mobs_sprites)
                self.you_lose()

            if bullets_count >= 0:
                text_bullets = font.render(f'Bullets:{bullets_count}', False,
                                           (0, 0, 0))
                screen.blit(text_bullets, (1000, 700))
            else:
                text_bullets = font.render(f'Bullets:{0}', False, (0, 0, 0))
                screen.blit(text_bullets, (1000, 700))

            text = font.render(f'Score:{self.score}', False, (0, 0, 0))
            screen.blit(text, (50, 700))

            screen.blit(image2, (95, 325))
            screen.blit(image3, (900, 270))
            screen.blit(image4, (450, 500))

            player.update(left, right, up)
            player.collide(306, 145, self.platf)

            if len(mobs_sprites) <= 3:
                Mobs(self)

            mobs_sprites.update()
            mobs_sprites.draw(screen)

            if left:
                if up:
                    screen.blit(image_jump, (player.rect.x, player.rect.y))
                else:
                    screen.blit(image_stay, (player.rect.x, player.rect.y))
                leftorright = True
            if right:
                if up:
                    screen.blit(image_jump_right,
                                (player.rect.x, player.rect.y))
                else:
                    screen.blit(image_stay_right,
                                (player.rect.x, player.rect.y))
                leftorright = False
            if up:
                if leftorright:
                    screen.blit(image_jump, (player.rect.x, player.rect.y))
                else:
                    screen.blit(image_jump_right,
                                (player.rect.x, player.rect.y))
            else:
                if leftorright:
                    screen.blit(image_stay, (player.rect.x, player.rect.y))
                else:
                    screen.blit(image_stay_right,
                                (player.rect.x, player.rect.y))

            cursor = load_image('cursor.png').convert_alpha()
            for i in mobs_sprites:
                x, y = pygame.mouse.get_pos()
                ax, ay, bx, by = i.rect
                for j in range(ax, ax + 80):
                    for k in range(ay, ay + 62):
                        if x == j and y == k:
                            cursor = load_image(
                                'cursorred.png').convert_alpha()
                            xxx, yyy = pygame.mouse.get_pos()
                            screen.blit(cursor, (xxx - 16, yyy - 16))

            if playerhits:
                player.rect.left = 600
                player.rect.top = 400
                hp -= 1

            if player.rect.top >= 1000:
                player.rect.left = 600
                player.rect.top = 400
                hp -= 1

            if hp <= 0:
                pygame.mixer.music.stop()
                mobs_sprites.remove(mobs_sprites)
                self.you_lose()

            print_hp(hp, hp_x)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                screen.blit(cursor, (x - 16, y - 16))
            blit_point_to_mouse(screen, ak47, *ak47_2.center)
            pygame.display.flip()
        pygame.quit()

    def you_lose(self):
        screen = pygame.display.set_mode(SIZE)
        image_menu = load_image("Fon_gl.png")
        ship_top = screen.get_height() - image_menu.get_height()
        ship_left = screen.get_width() / 2 - image_menu.get_width() / 2
        running2 = True
        pygame.mouse.set_visible(True)
        self.start.width = 300
        font = pygame.font.Font('data/font_super_game.ttf', 30)
        self.gameover.play()

        while running2:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.botton_sound.play()
            screen.blit(image_menu, (ship_left, ship_top))
            self.start.draw(145, 200, "Играть снова", self.run_game, 50)
            self.exit_game.draw(200, 350, "Главная", self.show_menu, 50)
            text = font.render(f'Score:{self.score}', False, (255, 0, 0))
            if self.score > int(self.f):
                open('txt_files/record.txt', 'w').write(str(self.score))
            screen.blit(text, (210, 120))
            self.print_text("GAME OVER", 185, 80, (255, 0, 0))
            pygame.display.update()


game = Game()
if __name__ == '__main__':
    game.show_menu()
