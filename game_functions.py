import random
import pygame
from piece import Piece

def create_grid(bg_c, locked_positions = {}):
    '''Создаёт сетку игры и прорисовывает квадраты фиугр'''
    grid = [ [ bg_c for _ in range(10) ] for _ in range(20) ]
    for i in range( len(grid) ):
        for j in range( len(grid[i]) ):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def get_shape(shapes_list, colors_list):
    '''Возвращает класс рандомной фигуры'''
    return Piece(5, 0, random.choice(shapes_list), random.choice(colors_list))

def draw_window(screen, sett, grid, next_piece):
    '''Отрисовка окна'''
    screen.fill(sett.bg_color)
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, sett.black)
    screen.blit(label, 
        (sett.top_left_x + sett.zone_width // 2 - (label.get_width() // 2), 
        30))
    for i in range( len(grid) ):
        for j in range( len(grid[i]) ):
            pygame.draw.rect(screen, grid[i][j], 
                        (sett.top_left_x + j*sett.brick_s, 
                        sett.top_left_y + i*sett.brick_s,
                        sett.brick_s,
                        sett.brick_s), 0)
    #Рисует сетку игры
    draw_grid(screen, sett, 20, 10)
    pygame.draw.rect(screen, 
                    sett.blue, 
                    (sett.top_left_x, sett.top_left_y, 
                    sett.zone_width, sett.zone_height), 6)

    #Рисует справа следующую фигуру
    draw_next_shape(screen, next_piece, sett)
    pygame.display.update()
    
def draw_grid(screen, sett, row, col):
    '''Рисуем линии сетки на экране'''
    for i in range(row):
        pygame.draw.line(screen,
                        sett.grey, 
                        [sett.top_left_x, sett.top_left_y + i*sett.brick_s],
                        [sett.top_left_x + sett.zone_width, sett.top_left_y + i*sett.brick_s],
                        1)
        for j in range(col):
            pygame.draw.line(screen,
                            sett.grey,
                            [sett.top_left_x + j*sett.brick_s, sett.top_left_y],
                            [sett.top_left_x + j*sett.brick_s, sett.top_left_y + sett.zone_height],
                            1)

def convert_shapes(shape):
    '''Конвертация координат фигуры в координаты сетки'''
    positions = []
    formt = shape.shape[ shape.rotation % len(shape.shape) ]
    for i, line in enumerate(formt):
        for j, column in enumerate(list(line)):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))               
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid, sett):
    '''Проверка на свободные места в сетке'''
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == sett.white] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shapes(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    '''Проверка конца игры'''
    for pos in positions:
        if pos[1] < 1:
            return True
    return False

def end_game(screen, score, sett):
    '''Показывает очки в конце игры и выход из игры'''
    screen.fill(sett.black)
    font = pygame.font.SysFont('comicsans', 60)
    score_text = font.render(f"SCORE: {score}", 1, sett.white)
    screen.blit(score_text, 
        (sett.top_left_x + sett.zone_width // 2 - (score_text.get_width() // 2), 
        30))
    font = pygame.font.SysFont('comicsans', 80)
    game_over = font.render('GAME OVER', 1, sett.white)
    screen.blit(game_over,
                (sett.top_left_x + sett.zone_width // 2 - (game_over.get_width() // 2),
                sett.H // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    exit()

def draw_next_shape(screen, shape, sett):
    '''Отображение следущей фигуры на экране'''
    font = pygame.font.SysFont('comicsnas', 30)
    label = font.render('Next figure', 1, sett.black)

    x = sett.top_left_x + sett.zone_width + 50
    y = sett.top_left_y + sett.zone_height // 2 - 100

    frmt = shape.shape[ shape.rotation % len(shape.shape) ]
    for i, line in enumerate(frmt):
        for j, col, in enumerate(list(line)):
            if col == '0':
                pygame.draw.rect(screen, 
                                shape.color, 
                                (x+j*sett.brick_s, 
                                y+i*sett.brick_s,
                                sett.brick_s,
                                sett.brick_s), 0)
    screen.blit(label, (x+10, y - 30))
    
def clearing_rows(grid, lock, sett):
    '''Очистка строк'''
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if sett.white not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del lock[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(lock), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                lock[new_key] = lock.pop(key)
    return inc

def falling_animation(shape, clock, grid, sett):
    '''Анимация падения'''
    fall_speed = 0.27
    sett.fall_time += clock.get_rawtime()
    clock.tick()
    if sett.fall_time / 1000 >= fall_speed:
        sett.fall_time = 0
        shape.y += 1
        if not valid_space(shape, grid, sett) and \
                shape.y > 0:
            shape.y -= 1
            sett.change_piece = True