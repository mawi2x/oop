import pygame
import random
from modules.GameConstants import *

class HintButton:
    def __init__(self, game):
        """Initialize hint button with game reference."""
        self.game = game
        self.is_hovered = False
        self.hover_color = constants.BUTTON_HOVER_COLOR  # Darker shade for hover

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
                # Set notification for hint used
                # self.game.notification_message = "Hint used!"
                # self.game.notification_timer = 60
        