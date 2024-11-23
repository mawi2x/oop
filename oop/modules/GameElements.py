import pygame
import random
from modules.GameConstants import *


class GameElements:
    def __init__(self, game):
        self.game = game

        # LETTER ELEMENTS VAIRABLES
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        random.shuffle(self.alphabet)

        # HINT BUTTON VARIABLES
        self.button_positions = {}
        self.is_hovered = False
        self.hover_color = constants.BUTTON_HOVER_COLOR  
        self.shuffle_letters()  # Initial shuffle

    # SHUFFLE LETTERS
    def shuffle_letters(self):
        """Shuffle the alphabet for new game/level."""
        random.shuffle(self.alphabet)
    #  SHUFFLE LETTERS

    # HINT 
    def draw_hint_button(self):
        """Draw the hint button and counter."""
        button_width = 50
        max_columns = 13
        spacing = 10
        y_offset = -100
        total_keyboard_width = (button_width + spacing) * max_columns - spacing
        keyboard_x = (constants.SCREEN_WIDTH - total_keyboard_width) // 2
        keyboard_y = constants.SCREEN_HEIGHT - 150 + y_offset
    
        # Hint button dimensions
        hint_button_width = 150
        hint_button_height = 50
        hint_x = keyboard_x + total_keyboard_width - hint_button_width
        hint_y = keyboard_y - hint_button_height - spacing
        hint_button_rect = pygame.Rect(
            hint_x, hint_y, hint_button_width, hint_button_height
        )
    
        # Check hover state
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = hint_button_rect.collidepoint(mouse_pos) and self.game.hint_count > 0
    
        # Draw button background and border with hover effect
        button_color = self.hover_color if self.is_hovered else constants.BUTTON_COLOR
        pygame.draw.rect(self.game.screen, button_color, hint_button_rect)
        pygame.draw.rect(self.game.screen, (0, 0, 0), hint_button_rect, 2)
    
        # Render hint text
        if self.game.hint_count > 0:
            hint_text = constants.FONT_SMALL.render(f"Hints: {self.game.hint_count}", True, constants.FONT_COLOR)
            
        else:
            hint_text = constants.FONT_SMALL.render("No Hint!", True, constants.FONT_COLOR)
    
        # Draw hint text
        hint_text_rect = hint_text.get_rect(
            center=(hint_x + hint_button_width // 2, hint_y + hint_button_height // 2)
        )
        self.game.screen.blit(hint_text, hint_text_rect)
    

        # Store button position
        self.game.button_positions["hint"] = hint_button_rect

    def use_hint(self,):
        """Reveal one unguessed letter as a hint."""
        if self.game.hint_count > 0:
            unguessed_letters = [
                letter for letter in self.game.current_word 
                if letter not in self.game.guesses
            ]
            if unguessed_letters:
                hint_letter = random.choice(unguessed_letters)
                self.game.guesses.append(hint_letter)
                self.game.hint_count -= 1
    # HINT 


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
    # LETTER BUTTONS


    # GAME DRAW
    # def draw_text_box(self, text, font, center_pos, padding=(40, 20)):
    #     """Draw text with surrounding box."""
    #     text_surface = font.render(text, True, constants.TEXT_COLOR)
    #     text_rect = text_surface.get_rect(center=center_pos)
    #     box_rect = text_rect.inflate(*padding)
        
    #     pygame.draw.rect(self.screen, constants.BUTTON_COLOR, box_rect)
    #     pygame.draw.rect(self.screen, constants.TEXT_COLOR, box_rect, 2)
    #     self.screen.blit(text_surface, text_rect)
    # GAME DRAW