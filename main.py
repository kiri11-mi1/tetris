import pygame
from settings import Settings
from shape_formats import Shapes
import game_functions as gf

def main():
    pygame.init()# Инициализация pygame
    game_sett = Settings()# Обьект настроек
    screen = pygame.display.set_mode((game_sett.W, game_sett.H))# Экран
    pygame.display.set_caption('Tetris')# Заголовок окна
    screen.fill(game_sett.bg_color)# Фон экрана
    pygame.display.update()# Обновление экрана
    clock = pygame.time.Clock()# Переменная времени

    score = 0# Перменная отбражения очков

    locked_pos = {}# Словарь свободных позиций в сетке
    grid = gf.create_grid(game_sett.bg_color, locked_pos)# Сетка

    sh = Shapes()
    shapes = sh.get_shapes_list()# Список фигур
    shape_colors = sh.get_colors_list(game_sett)# Список цветов
    
    current_shape = gf.get_shape(shapes, shape_colors)# Тек.фигура
    next_shape = gf.get_shape(shapes, shape_colors)# След.фигура

    while True:
        grid = gf.create_grid(game_sett.bg_color, locked_pos)# Сетка

        # Анимация падения фигур
        gf.falling_animation(current_shape, clock, grid, game_sett)

        # Обработка событий клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:# Влево
                    current_shape.x -= 1
                    if not gf.valid_space(current_shape, grid, game_sett):
                        current_shape.x += 1
                elif event.key == pygame.K_RIGHT:# Вправо
                    current_shape.x += 1
                    if not gf.valid_space(current_shape, grid, game_sett):
                        current_shape.x -= 1
                elif event.key == pygame.K_UP:# Поворот фигуры
                    current_shape.rotation = current_shape.rotation - 1 % len(current_shape.shape)
                    if not gf.valid_space(current_shape, grid, game_sett):
                        current_shape.rotation = current_shape.rotation - 1 % len(current_shape.shape)
                elif event.key == pygame.K_DOWN:# Ускорение вниз
                    current_shape.y += 1
                    if not gf.valid_space(current_shape, grid, game_sett):
                        current_shape.y -= 1
        
        # Добавление цвета фигуры в сетку для отрисовки
        shape_pos = gf.convert_shapes(current_shape)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_shape.color

        # Если фигура приземлилась на дно
        if game_sett.change_piece:
            for x, y in shape_pos:
                locked_pos[(x, y)] = current_shape.color
            current_shape = next_shape
            next_shape = gf.get_shape(shapes, shape_colors)
            game_sett.change_piece = False

            # Очистка заполненных линий
            score += gf.clearing_rows(grid, locked_pos, game_sett)*10
        

        # Отрисовка экрана, сетки, след. фигуры
        gf.draw_window(screen, game_sett, grid, next_shape)

        # Проверка конца игы
        if gf.check_lost(locked_pos):
            gf.end_game(screen, score, game_sett)

if __name__ == '__main__':
    main()
