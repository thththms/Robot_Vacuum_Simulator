import pygame
import os
import sys
from random import randint


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def converter(size, axis):
    if axis == 'x':
        return size / 1920 * width
    else:
        return size / 1080 * height


pygame.init()
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

robot_sprite = pygame.sprite.Group()
trash_sprites = pygame.sprite.Group()
robot_base_sprites = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()
furniture_sprites = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
cistern_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()
lvl_button_sprites = pygame.sprite.Group()

fps = 30
v = 120
can_eat_trash = True
all_trash_pieces = 0


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__(floor_sprites)
        if type == '0':
            self.image = pygame.transform.scale(load_image("светлый пол.png"), (converter(80, 'x'), converter(80, 'y')))
        elif type == '3':
            self.image = pygame.transform.scale(load_image("темно-светлый пол.png"), (converter(80, 'x'), converter(80, 'y')))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * int(converter(80, 'x'))
        self.rect.y = int(converter(20, 'y')) + pos[1] * int(converter(80, 'y'))


class RobotBase(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(robot_base_sprites)
        self.image = pygame.transform.scale(load_image("мусорка.png"), (converter(70, 'x'), converter(70, 'y')))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * converter(80, 'x')
        self.rect.y = converter(20, 'y') + pos[1] * converter(80, 'y')


class Cistern(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cistern_sprites)
        self.image = pygame.transform.scale(load_image('Лоу.png'), (converter(80, 'x'), converter(100, 'y')))
        self.rect = self.image.get_rect()
        self.rect.x = converter(1735, 'x')
        self.rect.y = converter(50, 'y')

    def update(self, level):
        self.image = pygame.transform.scale(load_image(level), (converter(130, 'x'), converter(150, 'y')))


cistern = Cistern()


class Board(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(borders)
        global data
        self.width = width
        self.height = height

        self.board = data
        self.cell_size_x = int(converter(80, 'x'))
        self.cell_size_y = int(converter(80, 'y'))
        self.add(borders)
        self.image = pygame.Surface([self.cell_size_x, self.cell_size_y])
        self.rect = pygame.Rect(self.width * self.cell_size_x, int(converter(20, 'y')) + self.height * self.cell_size_y,
                                self.cell_size_x, self.cell_size_y)


class Trash(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("trash_piece.png"), (converter(4, 'x'), converter(4, 'y')))

    def __init__(self, pos):
        super().__init__(trash_sprites)
        self.image = Trash.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def trash_box_maker(pos, box_size, type):
    global width, height
    box_width = box_size[0]
    box_height = box_size[1]
    if type == 'q':
        k = 1 if width == 1920 and height == 1080 else 3
        coef1 = k * width * height * 350 / (1920 * 1080)
        coef2 = converter(24, 'x')
        coef3 = k * width * height * 450 / (1920 * 1080)
    elif type == 'w':
        k = 1 if width == 1920 and height == 1080 else 2
        coef1 = k * width * height * 1000 / (1920 * 1080)
        coef2 = converter(35, 'x')
        coef3 = k * width * height * 900 / (1920 * 1080)
    elif type == 'e':
        k = 1 if width == 1920 and height == 1080 else 4
        coef1 = k * width * height * 1100 / (1920 * 1080)
        coef2 = converter(45, 'x')
        coef3 = k * width * height * 1200 / (1920 * 1080)
    for i in range(0, box_height, 5):
        for j in range(box_width - (box_width // box_height * i), 0, -box_width // 16):
            a = randint(0, i * j)
            if a > coef1 and j < box_width - coef2 and i > 10:
                Trash((pos[0] + j, pos[1] + i))

    for i in range(box_height, 0, -5):
        for j in range(0, box_width - (box_width // box_height * i), box_width // 16):
            a = randint(0, i * j)
            if a > coef3 and j > coef2 and i < box_height - 10:
                Trash((pos[0] + box_width - j, pos[1] + box_height - i))


def map_trash_box_maker(pos, type):
    if type == 'q':
        cell_size1 = int(converter(80, 'x'))
        cell_size2 = int(converter(80, 'y'))
    if type == 'w':
        cell_size1 = int(converter(160, 'x'))
        cell_size2 = int(converter(80, 'y'))
    if type == 'e':
        cell_size1 = int(converter(160, 'x'))
        cell_size2 = int(converter(160, 'y'))
    trash_box_maker((pos[0] * converter(80, 'x'),
                     converter(5, 'y') + pos[1] * converter(80, 'y')), (cell_size1, cell_size2), type)


class Furniture(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__(furniture_sprites)

        if type == 't':
            self.image = pygame.transform.scale(load_image("tv.png"), (converter(120, 'x'), converter(110, 'y')))
            self.rect = self.image.get_rect()
            self.rect.x = pos[0] * converter(80, 'x')
            self.rect.y = converter(20, 'y') + pos[1] * converter(80, 'y')
            self.mask = pygame.mask.from_surface(self.image)
        if type == 'ш':
            self.image = pygame.transform.scale(load_image("шкаф.png"), (converter(80, 'x'), converter(130, 'y')))
            self.rect = self.image.get_rect()
            self.rect.x = pos[0] * converter(80, 'x')
            self.rect.y = converter(20, 'y') + pos[1] * converter(80, 'y')
            self.mask = pygame.mask.from_surface(self.image)
        if type == 'а':
            self.image = pygame.transform.scale(load_image("аквариум.png"), (converter(80, 'x'), converter(100, 'y')))
            self.rect = self.image.get_rect()
            self.rect.x = pos[0] * converter(80, 'x')
            self.rect.y = converter(70, 'y') + pos[1] * converter(80, 'y')
            self.mask = pygame.mask.from_surface(self.image)
        if type == 'и':
            self.image = pygame.transform.scale(load_image("игровой автомат.png"), (converter(80, 'x'),
                                                                                    converter(120, 'y')))
            self.rect = self.image.get_rect()
            self.rect.x = pos[0] * converter(80, 'x')
            self.rect.y = converter(50, 'y') + pos[1] * converter(80, 'y')


class LvlButton(pygame.sprite.Sprite):
    def __init__(self, number, pos, type=1):
        super().__init__(lvl_button_sprites)
        self.image = pygame.transform.scale(load_image(f'{number}_уровень.png'), (150, 50))
        self.number = number
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, pos):
        global running, data, board, curr_level, v, can_eat_trash, all_trash_pieces

        if self.rect.collidepoint(pos):
            curr_level = self.number
            with open(f'map{self.number}.txt', 'r', encoding='utf8') as f:
                data = f.readlines()
            if self.type == 1:
                running = False
            robot_sprite.remove(robot_sprite.sprites())
            trash_sprites.remove(trash_sprites.sprites())
            robot_base_sprites.remove(robot_base_sprites.sprites())
            button_sprites.remove(button_sprites.sprites())
            furniture_sprites.remove(furniture_sprites.sprites())
            floor_sprites.remove(floor_sprites.sprites())
            borders.remove(borders.sprites())
            lvl_button_sprites.remove(lvl_button_sprites.sprites())

            for i in range(1, 10):
                LvlButton(i, (converter(1720, 'x'), converter(350 + i * 65, 'y')), type=2)
            for y in range(13):
                for x in range(21):
                    if data[y][x] != '2' and data[y][x] != '1' and data[y][x] != '3':
                        Floor((x, y), '0')
                    elif data[y][x] == data[y][x] != '2' and data[y][x] != '1' and data[y][x] != '0':
                        Floor((x, y), '3')
                    if data[y][x] == '.':
                        Floor((x, y), '3')
                        map_trash_box_maker((x, y), 'q')
                    if data[y][x] == '1':
                        board = Board(x, y)
                    if data[y][x] == 'q':
                        map_trash_box_maker((x, y), 'q')
                    if data[y][x] == 'w':
                        map_trash_box_maker((x, y), 'w')
                    if data[y][x] == 'e':
                        map_trash_box_maker((x, y), 'e')
                    if data[y][x] == 't':
                        Furniture((x, y), 't')
                    if data[y][x] == 'ш':
                        Furniture((x, y), 'ш')
                    if data[y][x] == 'а':
                        Furniture((x, y), 'а')
                    if data[y][x] == 'и':
                        Furniture((x, y), 'и')
                    if data[y][x] == 'м':
                        RobotBase((x, y))

            v = 120

            all_trash_pieces = len(trash_sprites.sprites())

            can_eat_trash = True
            cistern.update('Лоу.png')

            Robot(robot_sprite)
            screen.fill('white')


class Robot(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("robot_frame_2.png") , (converter(65, 'x'), converter(65, 'y')))

    def __init__(self, *group):
        super().__init__(*group)
        global curr_level
        self.rect = self.image.get_rect()
        self.rect.x = converter(800, 'x')
        self.rect.y = converter(500, 'y') if curr_level == 6 else converter(650, 'y') if \
            curr_level == 7 or curr_level == 3 else converter(650, 'y') if curr_level == 9 else converter(300, 'y')
        self.frames = [f'robot_frame_{i}.png' for i in range(1, 13)]
        self.cur_frame = 0
        self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]), (converter(65, 'x'), converter(65, 'y')))
        self.rotation = 'w'
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x, y, rot):
        global v, key, all_trash_pieces, can_eat_trash
        self.mask = pygame.mask.from_surface(self.image)
        if can_eat_trash:
            if pygame.sprite.spritecollide(self, trash_sprites, True):
                if v > 60:
                    v -= 1
        if pygame.sprite.spritecollideany(self, robot_base_sprites):
            v = 120
            can_eat_trash = True
        if pygame.sprite.spritecollideany(self, borders) or pygame.sprite.spritecollideany(self, furniture_sprites):
            if key == 'w':
                y = 2
                x = 0
            elif key == 's':
                y = -2
                x = 0
            elif key == 'a':
                y = 0
                x = 2
            elif key == 'd':
                y = 0
                x = -2
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]), (converter(65, 'x'), converter(65, 'y')))
        self.rect.x += x
        self.rect.y += y
        if rot == 'w':
            self.image = pygame.transform.scale(pygame.transform.rotate(load_image(self.frames[self.cur_frame]), 0), (converter(65, 'x'), converter(65, 'y')))
        if rot == 'a':
            self.image = pygame.transform.scale(pygame.transform.rotate(load_image(self.frames[self.cur_frame]), 90), (converter(65, 'x'), converter(65, 'y')))
        if rot == 's':
            self.image = pygame.transform.scale(pygame.transform.rotate(load_image(self.frames[self.cur_frame]), 180), (converter(65, 'x'), converter(65, 'y')))
        if rot == 'd':
            self.image = pygame.transform.scale(pygame.transform.rotate(load_image(self.frames[self.cur_frame]), -90), (converter(65, 'x'), converter(65, 'y')))
        self.rotation = rot


curr_level = 1


def text_maker(font, txt, pos, scale=100, color=(0, 0, 0)):
    font1 = pygame.font.Font(font, int(converter(scale, 'x')))
    text1 = font1.render(txt, True, color)
    screen.blit(text1, pos)


running = True
counter = 10
pygame.time.set_timer(pygame.USEREVENT, 100)
txt_pos1 = (converter(634, 'x'), converter(216, 'y'))
txt_pos2 = (converter(1037, 'x'), converter(216, 'y'))
txt_pos3 = (converter(768, 'x'), converter(486, 'y'))

while running:
    for event in pygame.event.get():
        screen.fill('white')

        if event.type == pygame.USEREVENT:
            counter -= 1
        if counter < 0:
            text_maker(None, "ROBO", txt_pos1)
        if counter < -5:
            text_maker(None, "VACUUM", txt_pos2)
        if counter < -10:
            text_maker(None, "SIMULATOR", txt_pos3)
        if counter < -20:
            screen.fill('white')
            text_maker('BlackAndWhitePicture-Regular.ttf', "ROBO", txt_pos1)
            text_maker(None, "VACUUM", txt_pos2)
            text_maker(None, "SIMULATOR", txt_pos3)
        if counter < -30:
            screen.fill('white')
            text_maker('BlackAndWhitePicture-Regular.ttf', "ROBO", txt_pos1)
            text_maker('RubikBurned-Regular.ttf', "VACUUM", txt_pos2)
            text_maker(None, "SIMULATOR", txt_pos3)
        if counter < -40:
            screen.fill('white')
            text_maker('BlackAndWhitePicture-Regular.ttf', "ROBO", txt_pos1)
            text_maker('RubikBurned-Regular.ttf', "VACUUM", txt_pos2)
            text_maker('ShadowsIntoLight-Regular.ttf', "SIMULATOR", txt_pos3)
        if counter < -50:
            screen.fill('white')
            text_maker('RubikDoodleShadow-Regular.ttf', "ROBO", txt_pos1)
            text_maker('Lemon-Regular.ttf', "VACUUM", txt_pos2)
            text_maker('Pacifico-Regular.ttf', "SIMULATOR", txt_pos3)
        if counter < -60:
            screen.fill('white')
            text_maker('MooLahLah-Regular.ttf', "ROBO", txt_pos1)
            text_maker('LeckerliOne-Regular.ttf', "VACUUM", txt_pos2)
            text_maker('KaushanScript-Regular.ttf', "SIMULATOR", txt_pos3)
        if counter < -70:
            screen.fill('white')
            text_maker('Itim-Regular.ttf', "ROBO", txt_pos1)
            text_maker('ShadowsIntoLight-Regular.ttf', "VACUUM", txt_pos2)
            text_maker('BlackAndWhitePicture-Regular.ttf', "SIMULATOR", txt_pos3)
        if counter < -80:
            screen.fill('white')
            text_maker(None, "ROBO", txt_pos1)
            text_maker(None, "VACUUM", txt_pos2)
            text_maker(None, "SIMULATOR", txt_pos3)

        img = pygame.transform.scale(load_image('Кнопка старта.png'), (converter(200, 'x'), converter(65, 'y')))
        screen.blit(img, (converter(845, 'x'), converter(691, 'y')))

        if event.type == pygame.MOUSEBUTTONUP:
            if converter(845, 'x') <= event.pos[0] <= converter(192, 'x') + converter(845, 'x'):
                if converter(691, 'y') <= event.pos[1] <= converter(65, 'y') + converter(691, 'y'):
                    running = False
                    screen.fill('white')
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

for i in range(1, 10):
    LvlButton(i, (converter(i * 190 - 70, 'x'), converter(950, 'y')), type=1)
running = True

while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            lvl_button_sprites.update(event.pos)
    fon = pygame.transform.scale(load_image('Заставка.png'), (converter(1000, 'x'), converter(500, 'y')))
    screen.blit(fon, (converter(400, 'x'), converter(100, 'y')))
    lvl_button_sprites.draw(screen)
    pygame.display.flip()

running = True
clock = pygame.time.Clock()
key = 'w'
all_trash_pieces = len(trash_sprites.sprites())

while running:
    screen.fill('white')

    text_maker('minecraft-ten-font-cyrillic.ttf', "Уровни", (int(converter(1700, 'x')), int(converter(300, 'y'))),
               scale=40)

    floor_sprites.draw(screen)
    robot_base_sprites.draw(screen)
    
    trash_sprites.draw(screen)
    furniture_sprites.draw(screen)
    cistern_sprites.draw(screen)
    borders.draw(screen)
    robot_sprite.update(0, 0, key)
    robot_sprite.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            robot_sprite.update(0, -(v // fps), 'w')
            key = 'w'
        elif keys[pygame.K_a]:
            robot_sprite.update(-(v // fps), 0, 'a')
            key = 'a'
        elif keys[pygame.K_d]:
            robot_sprite.update(v // fps, 0, 'd')
            key = 'd'
        elif keys[pygame.K_s]:
            robot_sprite.update(0, v // fps, 's')
            key = 's'

        if event.type == pygame.MOUSEBUTTONUP:
            lvl_button_sprites.update(event.pos)
    lvl_button_sprites.draw(screen)
    if v > 100:
        cistern.update('Лоу.png')
    elif 100 > v > 80:
        cistern.update('Почти лоу.png')
    elif 80 > v > 60:
        cistern.update('Почти фулл.png')
    elif 61 > v:
        cistern.update('Фулл.png')
        can_eat_trash = False

    clock.tick(fps)

    if len(trash_sprites.sprites()) <= 2:
        pygame.draw.rect(screen, (0, 0, 0), (converter(300, 'x'), converter(400, 'y'), converter(1300, 'x'),
                                             converter(200, 'y')))
        text_maker('Honk-Regular-VariableFont_MORF,SHLN.ttf', "LEVEL COMPLETED", (int(converter(350, 'x')),
                                                                                  int(converter(400, 'y'))), scale=160,
                   color=(0, 255, 165))
    text_maker('minecraft-ten-font-cyrillic.ttf', f"Всего собрано", (int(converter(1710, 'x')),
                                                                     int(converter(230, 'y'))), scale=19)
    text_maker('minecraft-ten-font-cyrillic.ttf', f"{all_trash_pieces - len(trash_sprites.sprites())}",
               (int(converter(1770, 'x')), int(converter(255, 'y'))), scale=19)

    pygame.display.flip()
pygame.quit()
