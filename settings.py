class Settings:
    '''Класс настроек игры'''
    def __init__(self):
        # Размер одного квадрата
        self.brick_s = 30
        # Нстройки экрана
        self.W = 800
        self.H = 700
        self.FPS = 60
        # Настройки игровой зоны
        self.zone_width = 10*self.brick_s
        self.zone_height = 20*self.brick_s
        self.top_left_x = (self.W - self.zone_width) // 2
        self.top_left_y = self.H - self.zone_height
        # Цвета
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.light_blue = (0, 255, 255)
        self.yellow = (255, 255, 0)
        self.orange = (255, 165, 0)
        self.blue = (0, 0, 255)
        self.purple = (128, 0, 128)
        self.black = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.grey = (128,128,128)
        self.white = (255, 255, 255)
        # Переменные игры
        self.score = 0
        self.change_piece = False
        self.fall_time = 0
