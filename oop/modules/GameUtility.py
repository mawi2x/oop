import os
import pygame
from modules.GameConstants import *

# ruff: noqa: F403, F405, F541

pygame.init()

class paths:

    wordlist_1 = os.path.join("assets", "programming_terms.txt")

    hangman_stages = [
            pygame.transform.smoothscale(
                pygame.image.load(f"assets/stage_{i}.png"), (constants.width, constants.height)
            )
            for i in range(10)
        ]

    
    gameover_fx = pygame.mixer.Sound('assets/game_over.wav')