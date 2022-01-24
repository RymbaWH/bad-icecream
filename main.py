import pygame
import os
import sys


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


def terminate():
    pygame.quit()
    sys.exit()


# Инициализация первого окна (заставки)
def start_screen():
    fon = load_image('logo.png')
    start = Button(WIDTH//2 - 91, 420, 'start.png')
    screen.blit(fon, (20, 0))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start.rect.collidepoint(pos):
                    return
        pygame.display.flip()
        clock.tick(FPS)


# Инициализация второго окна (выбор уровня)
def third_screen():
    screen.fill((255, 255, 255))
    fon = load_image('menu_levels.png')
    lvl1 = Button(70, 150, 'lvl1.png')
    lvl2 = Button(150, 150, 'lvl2.png')
    screen.blit(fon, (30, 70))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if lvl1.rect.collidepoint(pos):
                    return 1

                elif lvl2.rect.collidepoint(pos):
                    return 2
        pygame.display.flip()
        clock.tick(FPS)


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
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
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def main_game():
    screen = pygame.display.set_mode(SIZE)
    screen.fill((0, 0, 0))

    while True:
        player, level_x, level_y = generate_level(load_level('map.txt'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                pass

        all_sprites.draw(screen)

        pygame.display.flip()


pygame.init()
SIZE = WIDTH, HEIGHT = 550, 550
screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))
tile_width = tile_height = 50
FPS = 50
clock = pygame.time.Clock()

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

start_screen()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

level = third_screen()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# все изображения для карты заносим в словарь
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('snow.png'),
    'ice': load_image('ice2.png')
}
player_image = load_image('wm3.png')

main_game()
