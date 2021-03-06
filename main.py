import pygame
import os
import sys
import random
import sqlite3
import time


# Загрузка всехкартинок происходит только через эту функцию, она обрабатывает все ошибки, автоматически
# переходит в папку data, в которой теперь мы должны хранить все картинки, поля, звуки и т.д.
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        raise Exception(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def snowflakes(snow_list):
    for i in range(len(snow_list)):
        pygame.draw.circle(screen, (110, 173, 245), snow_list[i], 3)

        snow_list[i][1] += 1

        if snow_list[i][1] > 550:
            y = random.randrange(-50, -10)
            snow_list[i][1] = y
            x = random.randrange(0, 550)
            snow_list[i][0] = x


def terminate():
    pygame.quit()
    sys.exit()


# Инициализация первого окна (заставки)
def start_screen():
    sound.play(-1)
    screen.fill((255, 255, 255))
    fon = load_image('logo.png')
    start = Button(WIDTH // 2 - 91, 420, 'start.png')
    screen.blit(fon, (20, 0))
    all_sprites.draw(screen)

    snow_list = []
    for i in range(130):
        x = random.randrange(0, 550)
        y = random.randrange(0, 550)
        snow_list.append([x, y])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if start.rect.collidepoint(pos):
                    button.play(0)
                    sound.stop()
                    return

        screen.fill((255, 255, 255))
        screen.blit(fon, (20, 0))

        snowflakes(snow_list)

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(80)


# Инициализация второго окна (выбор уровня)
def third_screen():
    sound.play(-1)
    screen.fill((255, 255, 255))
    fon = load_image('menu_levels.png')
    lvl1 = Button(70, 150, 'lvl1.png')
    lvl2 = Button(150, 150, 'lvl2.png')
    screen.blit(fon, (30, 70))
    all_sprites.draw(screen)

    snow_list = []
    for i in range(130):
        x = random.randrange(0, 550)
        y = random.randrange(0, 550)
        snow_list.append([x, y])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if lvl1.rect.collidepoint(pos):
                    sound.stop()
                    button.play(0)
                    return '1'
                elif lvl2.rect.collidepoint(pos):
                    sound.stop()
                    button.play(0)
                    return '2'

                elif 505 < event.pos[0] < 535 and 75 < event.pos[1] < 100:
                    terminate()

        screen.fill((255, 255, 255))
        snowflakes(snow_list)
        screen.blit(fon, (30, 70))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(80)


def loose_screen():
    screen.fill((255, 255, 255))
    fon = load_image('menu_levels.png')
    screen.blit(fon, (30, 70))

    font = pygame.font.SysFont(None, 80)
    font2 = pygame.font.SysFont(None, 30)
    font3 = pygame.font.SysFont(None, 50)

    text = font.render(str('You loose!'), True, (0, 0, 0))
    text2 = font2.render(str(f'your time: {game_time} sec'), True, (0, 0, 0))
    text3 = font3.render(str(f'Play again!'), True, (255, 0, 0))

    btn_rect = text3.get_rect(topleft=(110, 340))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return

        screen.fill((255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)

        screen.blit(fon, (30, 100))
        screen.blit(text, (110, 180))
        screen.blit(text2, (110, 260))
        screen.blit(text3, btn_rect)

        pygame.display.flip()
        clock.tick(25)


# Инициализация финального окна (результаты)
def win_screen():
    screen.fill((255, 255, 255))
    fon = load_image('menu_levels.png')
    screen.blit(fon, (30, 70))

    history = cursor.execute("SELECT time FROM results WHERE status='True'").fetchall()

    all_time = []
    for i in history:
        all_time.append(i[0])

    print(history)

    font = pygame.font.SysFont(None, 80)
    font2 = pygame.font.SysFont(None, 30)
    font3 = pygame.font.SysFont(None, 50)

    text = font.render(str('You win!'), True, (0, 0, 0))
    text2 = font2.render(str(f'your time: {game_time} sec'), True, (0, 0, 0))
    text3 = font2.render(str(f'best time: {min(all_time)} sec'), True, (0, 0, 0))
    text4 = font3.render(str(f'Play again!'), True, (255, 0, 0))
    btn_rect = text4.get_rect(topleft=(110, 340))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return

        screen.fill((255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)

        screen.blit(fon, (30, 100))
        screen.blit(text, (110, 180))
        screen.blit(text2, (110, 260))
        screen.blit(text3, (110, 290))
        screen.blit(text4, btn_rect)

        pygame.display.flip()
        clock.tick(25)


# загружает поля из файла формата txt с именем filename, в результате возвращает list
# В файле filename.txt приняты условные обозначения
# "#" - граница (коробка)
# "@" - кубик льда
# "." - пустое поле, просто снег
# "_" - главный игрок
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, filename):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(filename)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, axis):
        super().__init__(tiles_group, all_monsters)
        scale = (80, 70)
        self.schet = 0
        self.all_im = [pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_000.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_001.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_002.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_003.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_004.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_005.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_006.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_007.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_008.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_009.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_010.png'), scale),
                       pygame.transform.scale(load_image('monster\Wraith_01_Moving Forward_011.png'), scale)]

        self.ind_im = 0
        self.axis = axis
        self.napr = 0
        self.image = self.all_im[self.ind_im]
        self.coef = random.choice([-1, 1])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 10, tile_height * pos_y - 7)

    def update(self):
        if self.axis == 'y':
            self.rect.y += 2 * self.coef
            if self.schet % 15 == 0:
                self.ind_im = (self.ind_im + 1) % len(self.all_im)
                if self.coef == -1:
                    self.image = pygame.transform.flip(self.all_im[self.ind_im], 1, 0)

                else:
                    self.image = self.all_im[self.ind_im]

        if self.axis == 'x':
            self.rect.x += 2 * self.coef
            if self.schet % 15 == 0:
                self.ind_im = (self.ind_im + 1) % len(self.all_im)
                if self.coef == -1:
                    self.image = pygame.transform.flip(self.all_im[self.ind_im], 1, 0)

                else:
                    self.image = self.all_im[self.ind_im]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, control='k'):
        super().__init__(player_group, all_players)
        self.image = player_image
        self.control = control
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

        self.mask = pygame.mask.from_surface(self.image)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(player_group, all_fruits)
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 10)


class Particle():
    def __init__(self, startx, starty, col):
        self.x = startx
        self.y = random.randint(0, starty)
        self.col = col
        self.sx = startx
        self.sy = starty

    def move(self):
        if self.y < 0:
            self.x = self.sx
            self.y = self.sy

        else:
            self.y -= 1

        self.x += random.randint(-2, 2)


def generate_level(level):
    new_player, x, y = None, None, None
    monsters = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '_':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '@':
                Tile('ice', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                if monsters == 2:
                    Monster(x, y, 'x')

                elif monsters == 1 or monsters == 3:
                    Monster(x, y, 'y')

                else:
                    Monster(x, y, 'x')
                monsters += 1
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def generate_fruits(level, fruit):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Fruit(pygame.transform.scale(fruit, (30, 30)), x, y)


def main(lvl_num):
    global game_time
    levels_music.play(-1)
    screen = pygame.display.set_mode(SIZE)
    screen.fill((0, 0, 0))

    time_delay = 1000
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)
    counter = 0

    player, level_x, level_y = generate_level(load_level(f"lvl{lvl_num}_map.txt"))
    generate_fruits(load_level(f"lvl{lvl_num}_fruits1.txt"), random.choice(list(fruit_images.values())))

    fruits_flag = True

    while True:
        all_sprites.draw(screen)
        all_fruits.draw(screen)
        screen.blit(player_image, (player.rect.x, player.rect.y))
        for monster in all_monsters:
            screen.blit(monster.image, (monster.rect.x, monster.rect.y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == timer_event:
                counter += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rect.x -= 50
            for i in all_sprites:
                if i.image != tile_images['empty'] and i.rect.colliderect(player.rect) and i.image != player_image:
                    player.rect.x += 50
            for i in all_fruits:
                if i.rect.colliderect(player.rect):
                    all_fruits.remove(i)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rect.x += 50
            for i in all_sprites:
                if i.image != tile_images['empty'] and i.rect.colliderect(player.rect) and i.image != player_image:
                    player.rect.x -= 50
            for i in all_fruits:
                if i.rect.colliderect(player.rect):
                    all_fruits.remove(i)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.rect.y -= 50
            for i in all_sprites:
                if i.image != tile_images['empty'] and i.rect.colliderect(player.rect) and i.image != player_image:
                    player.rect.y += 50
            for i in all_fruits:
                if i.rect.colliderect(player.rect):
                    all_fruits.remove(i)

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.rect.y += 50
            for i in all_sprites:
                if i.image != tile_images['empty'] and i.rect.colliderect(player.rect) and i.image != player_image:
                    player.rect.y -= 50
            for i in all_fruits:
                if i.rect.colliderect(player.rect):
                    all_fruits.remove(i)

        if len(all_fruits) == 0 and fruits_flag:
            generate_fruits(load_level(f"lvl{lvl_num}_fruits2.txt"), random.choice(list(fruit_images.values())))
            fruits_flag = False
        if len(all_fruits) == 0 and not fruits_flag:
            levels_music.stop()
            game_time = counter
            cursor.execute(f"INSERT INTO results (time, status) VALUES ('{counter}', 'True');")
            win_screen()
            return

        for monster in all_monsters:
            monster.update()
            for i in all_sprites:
                if i.image != tile_images['empty'] and i.image != player_image and pygame.sprite.collide_mask(i,
                                                                                                              monster):
                    monster.coef *= -1

            for i in all_players:
                if pygame.sprite.collide_mask(i, monster) and not keys[pygame.K_g]:
                    levels_music.stop()

                    cursor.execute(f"INSERT INTO results (time, status) VALUES ('{counter}', 'False');")
                    game_time = counter

                    loose_screen()
                    return

        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
pygame.mixer.init()
SIZE = WIDTH, HEIGHT = 550, 550
screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))
tile_width = tile_height = 50
FPS = 20
clock = pygame.time.Clock()

# все изобра`жения для карты заносим в словарь
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('snow.png'),
    'ice': load_image('ice2.png')
}
fruit_images = {
    'limon': load_image('fruits\limon.png'),
    'cherry': load_image('fruits\cherry.png'),
    'dragon': load_image('fruits\dragon-fruit.png'),
    'durian': load_image('fruits\durian.png'),
    'strawberry': load_image('fruits\strawberry.png')
}
player_image = load_image('wm3.png')

# музыка
pygame.mixer.music.load('sound.mp3')
sound = pygame.mixer.Sound("sound.mp3")
sound.set_volume(0.1)

pygame.mixer.music.load('music_levels.mp3')
levels_music = pygame.mixer.Sound("music_levels.mp3")
levels_music.set_volume(0.1)

pygame.mixer.music.load('button.mp3')
button = pygame.mixer.Sound("button.mp3")
button.set_volume(0.5)

pygame.mixer.music.load('win.mp3')
win = pygame.mixer.Sound("win.mp3")
win.set_volume(0.5)

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

start_screen()

game = True

while game:
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    level = third_screen()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    all_fruits = pygame.sprite.Group()
    all_monsters = pygame.sprite.Group()
    all_players = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    connect = sqlite3.connect("data_base.db")
    cursor = connect.cursor()

    game_time = 0
    main(level)
