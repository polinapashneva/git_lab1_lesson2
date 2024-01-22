import os
import sys
import pygame

FPS = 50
MONEY = 0
PROMO = [['12345', 10, 0]]
LEVEL = 1
KH = 0
Z = 0


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('заставочка.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def zast():
    fon = pygame.transform.scale(load_image('заставка.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ['ИГРАТЬ', str(MONEY), "ВЫХОД"]
    text_coord = 50
    coordkn = []
    for line in intro_text:
        if line != str(MONEY):
            text_coord += 10
            pygame.draw.rect(screen, (120, 132, 73), (60, text_coord, WIDTH // 5, 60))
            coordkn.append([60, text_coord, text_coord + 60])
            font = pygame.font.SysFont(None, 50)
            string_rendered = font.render(line, 1, pygame.Color('black'))
            text_coord += 12
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            text_coord = text_coord - 12 + 80
            intro_rect.x = 70
            screen.blit(string_rendered, intro_rect)
        else:
            text_coord += 10
            pygame.draw.rect(screen, (120, 132, 73), (60, text_coord, WIDTH // 5, 60))
            coordkn.append([120, text_coord, text_coord + 60])
            image = pygame.transform.scale(load_image('символ.png'), (58, 58))
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (61, text_coord + 1))
            font = pygame.font.SysFont(None, 50)
            string_rendered = font.render(line, 1, pygame.Color('black'))
            text_coord += 12
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            text_coord = text_coord - 12 + 80
            intro_rect.x = 130
            screen.blit(string_rendered, intro_rect)

    c = [[]]
    while True:
        if 60 <= pygame.mouse.get_pos()[0] <= 60 + WIDTH // 5:
            for i in coordkn:
                if i[1] <= pygame.mouse.get_pos()[1] <= i[2]:
                    c.append(i[::])
                    font = pygame.font.SysFont(None, 50)
                    string_rendered = font.render(intro_text[coordkn.index(i)], 1, pygame.Color('white'))
                    text_coord = i[1] + 12
                    intro_rect = string_rendered.get_rect()
                    intro_rect.top = text_coord
                    intro_rect.x = i[0] + 10
                    screen.blit(string_rendered, intro_rect)
                    if i[0] != 60:
                        image = pygame.transform.scale(load_image('символ2.png'), (58, 58))
                        image.set_colorkey((0, 0, 0))
                        screen.blit(image, (61, i[1] + 1))
                else:
                    font = pygame.font.SysFont(None, 50)
                    string_rendered = font.render(intro_text[coordkn.index(i)], 1, pygame.Color('black'))
                    text_coord = i[1] + 12
                    intro_rect = string_rendered.get_rect()
                    intro_rect.top = text_coord
                    intro_rect.x = i[0] + 10
                    screen.blit(string_rendered, intro_rect)
                    if i[0] != 60:
                        image = pygame.transform.scale(load_image('символ.png'), (58, 58))
                        image.set_colorkey((255, 255, 255))
                        screen.blit(image, (61, i[1] + 1))
        else:
            if c[-1] != []:
                font = pygame.font.SysFont(None, 50)
                string_rendered = font.render(intro_text[coordkn.index(c[-1])], 1, pygame.Color('black'))
                text_coord = c[-1][1] + 12
                intro_rect = string_rendered.get_rect()
                intro_rect.top = text_coord
                intro_rect.x = c[-1][0] + 10
                screen.blit(string_rendered, intro_rect)
                if c[-1][0] != 60:
                    image = pygame.transform.scale(load_image('символ.png'), (58, 58))
                    image.set_colorkey((255, 255, 255))
                    screen.blit(image, (61, c[-1][1] + 1))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 60 <= event.pos[0] <= 60 + WIDTH // 5:
                    for i in coordkn:
                        if i[1] <= event.pos[1] <= i[2]:
                            if intro_text[coordkn.index(c[-1])] == "ВЫХОД":
                                terminate()
                            elif intro_text[coordkn.index(c[-1])] == str(MONEY):
                                promo()
                            elif intro_text[coordkn.index(c[-1])] == 'ИГРАТЬ':
                                return
                                # 23
        pygame.display.flip()
        clock.tick(FPS)


def promo():
    global MONEY
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100))
    font = pygame.font.SysFont(None, 40)
    string_rendered = font.render("Введите промокод", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = HEIGHT // 2 - 290
    intro_rect.x = WIDTH // 2 - 140
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 140, HEIGHT // 2, 280, 40))
    pc = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for i in PROMO:
                    if i[0] == pc and i[-1] == 0:
                        MONEY += int(i[1])
                        PROMO[PROMO.index(i)][-1] = 1
                    zast()
            elif event.type == pygame.KEYDOWN:
                pc = pc + str(event.unicode)
                font = pygame.font.SysFont(None, 30)
                string_rendered = font.render(pc, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = HEIGHT // 2 + 5
                intro_rect.x = WIDTH // 2 - 135
                screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, a):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(load_image('платформа.png'), (a, 30))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(pos[0], pos[1])


class Player(pygame.sprite.Sprite):
    def __init__(self, w, h, z):
        super().__init__(char_group, all_sprites)
        print(w, h)
        self.image = pygame.transform.scale(load_image('челик стоит.png'), (w - 45, h - 30))
        self.image.set_colorkey((255, 255, 255))
        print(HEIGHT)
        self.rect = self.image.get_rect().move(70, HEIGHT - h + 50 - z)


class Fon(pygame.sprite.Sprite):
    def __init__(self, h):
        super().__init__(fon_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f'{LEVEL}.png'), (h, HEIGHT))
        self.rect = self.image.get_rect().move(0, 0)
        pygame.display.flip()
        clock.tick(FPS)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
char_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()


def generate_level_1():
    global KH, Z
    new_player = None
    if WIDTH <= 5356:
        m = round(5356 / WIDTH / 3)
        h = round(1080 / m)
        z = round(75 / m)
    else:
        m = WIDTH / 5356 / 3
        h = round(1080 * m)
        z = round(75 * m)
        m = round(m)
    Z = z
    kh = round((HEIGHT - z) / 7) + 20
    KH = kh
    xc = round(WIDTH / 10)
    crd = [(xc, kh * 5), (xc * 2, kh * 4), (xc * 3, kh * 3), (xc * 5, kh * 3), (xc * 6, kh * 2), (xc * 7, kh),
           (xc * 7, kh * 5), (xc * 8, kh * 4), (xc * 9, kh * 3), (xc * 10, kh * 2), (xc * 10, kh * 5),
           (xc * 10, kh), (xc * 10, kh * 4), (xc * 12, kh * 3), (xc * 15, kh * 5), (xc * 15, kh * 3),
           (xc * 15, kh), (xc * 16, kh * 4), (xc * 16, kh * 2), (xc * 17, kh), (xc * 18, kh * 2),
           (xc * 18, kh * 4), (xc * 19, kh * 3), (xc * 19, kh * 5), (xc * 20, kh * 4)]
    for i in crd:
        Tile(i, xc)
    new_player = Player(xc, kh, z)
    fon = Fon(WIDTH * 3)
    # вернем игрока, а также размер поля в клетках
    return new_player, WIDTH, HEIGHT, fon


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - Z)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT)


try:
    pygame.init()
    pygame.display.set_caption('Голос сердца')
    infoObject = pygame.display.Info()
    size = width, height = WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 50
    tile_images = {
        '1': load_image('заставка.png')
    }
    player_image = load_image('челик стоит.png', -1)
    tile_width = tile_height = 50

    start_screen()
    zast()
    print(1)
    player, level_x, level_y, fon = generate_level_1()
    # camera = Camera()
    running = True
    print(2)

    p = 0
    r = False
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= 7
        elif keys[pygame.K_RIGHT]:
            player.rect.x += 7
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    t = KH // 9 * 2 + 5
                    if t % 2 != 0:
                        t += 1
                    r = True
        if r:
            p += 1
            if p <= t // 2:
                player.rect.y -= 9
            else:
                player.rect.y += 9
            if p == t:
                p = 0
                r = False


        # # изменяем ракурс камеры
        # camera.update(player)
        # # обновляем положение всех спрайтов
        # for sprite in all_sprites:
        #     camera.apply(sprite)

        screen.fill((0,0,0))
        fon_group.draw(screen)
        tiles_group.draw(screen)
        char_group.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
except:
    print('Error')