import pygame
import random
from modules.GameConstants import * 

# LetterButtons.py
class LetterButtons:
    def __init__(self, game):
        self.game = game
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        random.shuffle(self.alphabet)
        self.button_positions = {}


        # LETTER BUTTONS
    def draw_buttons_letter(self):
        button_width = 50
        button_height = 50
        max_columns = 13
        spacing = 10  # Space between buttons
        border_thickness = 2  # Border thickness in pixels

        # Calculate total width of a row of buttons
        total_width = (button_width + spacing) * max_columns - spacing

        # Start x position to center the buttons
        x = (constants.SCREEN_WIDTH - total_width) // 2
        y = constants.SCREEN_HEIGHT - 150  # Vertical position

        mouse_pos = pygame.mouse.get_pos()

        for i, letter in enumerate(self.alphabet):
            if letter not in self.game.guesses:
                column = i % max_columns
                row = i // max_columns
                x_pos = x + column * (button_width + spacing)
                y_pos = y + row * (button_height + spacing)

                # Create button rectangle
                rect = pygame.Rect(x_pos, y_pos, button_width, button_height)

                # Draw filled button
                color = (
                    constants.BUTTON_HOVER_COLOR
                    if rect.collidepoint(mouse_pos)
                    else constants.BUTTON_COLOR
                )
                pygame.draw.rect(self.game.screen, color, rect)

                # Draw border
                pygame.draw.rect(
                    self.game.screen, (0, 0, 0), rect, border_thickness
                )  # Black border


                # Draw letter
                letter_surf = constants.FONT_MEDIUM.render(
                    letter.upper(), True, constants.FONT_COLOR
                )
                letter_rect = letter_surf.get_rect(
                    center=(x_pos + button_width // 2, y_pos + button_height // 2)
                )
                self.game.screen.blit(letter_surf, letter_rect)
                self.button_positions[letter] = rect
            else:
                if letter in self.button_positions:
                    del self.button_positions[letter]
