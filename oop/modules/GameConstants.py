import pygame



pygame.init()




class constants:

    STANDARD_WIDTH = 1920
    STANDARD_HEIGHT = 1080
    # DISPLAY
    info = pygame.display.Info()
    # SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w -100 , info.current_h - 100
    # SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    
    scale_x = info.current_w / STANDARD_WIDTH
    scale_y = info.current_h / STANDARD_HEIGHT

    # SCALING
    # width = 300
    # height = 300


    margin = 100 * min(scale_x, scale_y)  # Scale margin proportionally
    SCREEN_WIDTH = int(info.current_w - margin)
    SCREEN_HEIGHT = int(info.current_h - margin)

    width = int(300 * min(scale_x, scale_y))
    height = int(300 * min(scale_x, scale_y))

    
    # DISPLAY


    # STYLES

    # FONT_LARGE = pygame.font.Font(None, 64)
    # FONT_MEDIUM = pygame.font.Font(None, 48)
    # FONT_SMALL = pygame.font.Font(None, 32)

    font_scale = min(scale_x, scale_y)
    FONT_LARGE = pygame.font.Font(None, int(64 * font_scale))
    FONT_MEDIUM = pygame.font.Font(None, int(48 * font_scale))
    FONT_SMALL = pygame.font.Font(None, int(32 * font_scale))


    BG_COLOR = pygame.Color("#f1faee")
    FONT_COLOR = (0, 0, 0)

    BUTTON_COLOR = pygame.Color("#c3c4c2")
    BUTTON_HOVER_COLOR = (255, 140, 0)
    TEXT_COLOR = (0, 0, 0)

    # STYLES


    # GAME LOGIC CONSTANTS
    TIMER_DURATION = 30
    MAX_ATTEMPTS = 9
    # GAME LOGIC CONSTANTS

    # CONSTANTS






  