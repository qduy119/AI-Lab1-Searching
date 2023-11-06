# This is the file to declare the setting variables.
import pygame

# Window
APP_WIDTH, APP_HEIGHT = 610, 680
APP_CAPTION = r"Pacman"
FPS = 60

# Map
MAP_IMG = [r"../Assets/maps/map_1.png",
           r"../Assets/maps/map_2.png",
           r"../Assets/maps/map_3.png",
           r"../Assets/maps/map_4.png",
           r"../Assets/maps/map_5.png"]
MAP_INPUT_TXT = [[r"../Assets/levels/level_1/map_1.txt", r"../Assets/levels/level_1/map_2.txt", r"../Assets/levels/level_1/map_3.txt", r"../Assets/levels/level_1/map_4.txt", r"../Assets/levels/level_1/map_5.txt"],
                 [r"../Assets/levels/level_2/map_1.txt", r"../Assets/levels/level_2/map_2.txt", r"../Assets/levels/level_2/map_3.txt", r"../Assets/levels/level_2/map_4.txt", r"../Assets/levels/level_2/map_5.txt"],
                 [r"../Assets/levels/level_3/map_1.txt", r"../Assets/levels/level_3/map_2.txt", r"../Assets/levels/level_3/map_3.txt", r"../Assets/levels/level_3/map_4.txt", r"../Assets/levels/level_3/map_5.txt"],
                 [r"../Assets/levels/level_4/map_1.txt", r"../Assets/levels/level_4/map_2.txt", r"../Assets/levels/level_4/map_3.txt", r"../Assets/levels/level_4/map_4.txt", r"../Assets/levels/level_4/map_5.txt"]]
MAP_NUM = len(MAP_IMG)


# Background
HOME_BACKGROUND = r"../Assets/bg/home_bg.jpg"
ABOUT_BACKGROUND = r"../Assets/bg/about_bg.jpg"
GAMEOVER_BACKGROUND = r"../Assets/bg/gameover_bg.jpg"
VICTORY_BACKGROUND = r"../Assets/bg/victory_bg.jpg"


# Screen state
STATE_HOME = "home"
STATE_PLAYING = "playing"
STATE_ABOUT = "about"
STATE_LEVEL = "level"
STATE_MAP = "map"
STATE_SETTING = "setting"
STATE_GAMEOVER = "gameover"
STATE_VICTORY = 'victory'


# Home screen
HOME_BG_WIDTH, HOME_BG_HEIGHT = APP_WIDTH, APP_HEIGHT - 410
START_POS = pygame.Rect(150, 325, 300, 50)
ABOUT_POS = pygame.Rect(150, 405, 300, 50)
EXIT_POS = pygame.Rect(150, 485, 300, 50)


# Map screen
MAP_1_POS = pygame.Rect(150, 320, 300, 50)
MAP_2_POS = pygame.Rect(150, 390, 300, 50)
MAP_3_POS = pygame.Rect(150, 460, 300, 50)
MAP_4_POS = pygame.Rect(150, 530, 300, 50)
MAP_5_POS = pygame.Rect(150, 600, 300, 50)
BACK_MAP_POS = pygame.Rect(500, 600, 70, 50)

# Level screen
LEVEL_1_POS = pygame.Rect(150, 320, 300, 50)
LEVEL_2_POS = pygame.Rect(150, 390, 300, 50)
LEVEL_3_POS = pygame.Rect(150, 460, 300, 50)
LEVEL_4_POS = pygame.Rect(150, 530, 300, 50)
BACK_LEVEL_POS = pygame.Rect(500, 600, 70, 50)


# About screen
BACK_POS = pygame.Rect(450, 580, 100, 40)

# Setting screen
OK_POS = pygame.Rect(255, 550, 100, 50)
TRIANGLE_1_POS = [[360, 620], [360, 670], [403.3, 645]]
TRIANGLE_2_POS = [[250, 620], [250, 670], [206.7, 645]]


# Play screen
ROW_PADDING, COL_PADDING = 50, 60
MAP_WIDTH, MAP_HEIGHT = APP_WIDTH - ROW_PADDING, APP_HEIGHT - COL_PADDING

MAP_POS_X, MAP_POS_Y = ROW_PADDING // 2, COL_PADDING * 2 // 3
SCORE_POS = (30, 10)
READY_POS = (APP_WIDTH // 2, 10)
HOME_RECT = (APP_WIDTH - ROW_PADDING - 35, 10, 70, 20)
SPEED_RECT = (APP_WIDTH - ROW_PADDING - 180, 10, 130, 20)

CELL_SIZE = 20
ROW, COL = MAP_WIDTH // CELL_SIZE, MAP_HEIGHT // CELL_SIZE

SPEED = 250


# Gameover screen

COIN_POS = (200, 430)
COIN_WIDTH, COIN_HEIGHT = (200, 200)
GAMEOVER_BACKGROUND_WIDTH, GAMEOVER_BACKGROUND_HEIGHT = HOME_BG_WIDTH - 50, HOME_BG_HEIGHT + 200


VICTORY_WIDTH, VICTORY_HEIGHT = (500, 400)
PACMAN_WIDTH, PACMAN_HEIGHT = (500, 280)


# Score
SCORE_BONUS = 20
SCORE_PENALTY = -1


# Font
FONT = "Comic Sans MS"


# Color
BACKGROUND_COLOR = (65, 98, 132)
LIGHT_GREY = (170, 170, 170)
BLUE = (223, 190, 0)
BLUE_LIGHT = (255, 217, 27)
DARK_GREY = (75, 75, 75)
RED = (255, 0, 0 )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE_GREY = (203, 203, 203)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


# Pacman, Food, ghost animations
FOOD_IMAGE = r"../Assets/effects/food.jpg"

PACMAN_IMAGE = r"../Assets/effects/pacman.png"
PACMAN_LEFT = r"../Assets/effects/pacman_left.png"
PACMAN_RIGHT = r"../Assets/effects/pacman_right.png"
PACMAN_DOWN = r"../Assets/effects/pacman_down.png"
PACMAN_UP = r"../Assets/effects/pacman_up.png"

BLACK_BG = r"../Assets/effects/bg.png"

GHOST_LEFT_IMAGE = r"../Assets/effects/red.png"
GHOST_RIGHT_IMAGE = r"../Assets/effects/red.png"
GHOST_UP_IMAGE = r"../Assets/effects/red.png"
GHOST_DOWN_IMAGE = r"../Assets/effects/red.png"
