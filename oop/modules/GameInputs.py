import pygame
from modules.GameElements import *

# InputHandler.py
class GameInputs:
    def __init__(self, game):
        self.game = game
        self.hint_button = GameElements(game)
        
    def handle_input(self, event: pygame.event.Event) -> None:
        if self.game.popup_active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
            mouse_pos = event.pos
            # print(f"Mouse click at: {mouse_pos}")  # Debug print
            
            # First check hint button
            hint_rect = self.game.button_positions.get("hint")
            if hint_rect and hint_rect.collidepoint(mouse_pos):
                # print("Hint button clicked!")  # Debug print
                self.hint_button.use_hint()
                return
            
            # Then check letter buttons
            for letter, rect in self.game.GameElements.button_positions.items():
                if rect.collidepoint(mouse_pos):
                    # print(f"Clicked letter: {letter}")  # Debug print
                    if letter not in self.game.guesses:
                        self.game.guesses.append(letter)
                        if letter not in self.game.current_word:
                            self.game.attempts += 1
                            
                    # Remove clicked letter from button positions
                    if letter in self.game.GameElements.button_positions:
                        del self.game.GameElements.button_positions[letter]
                    break

        elif event.type == pygame.KEYDOWN:
            letter = event.unicode.lower()
            if letter.isalpha() and len(letter) == 1:
                if letter in self.game.guesses:
                    self.game.notification_message = f"Letter '{letter.upper()}' already guessed!"
                    self.game.notification_timer = 60
                else:
                    self.game.guesses.append(letter)
                    if letter not in self.game.current_word:
                        self.game.attempts += 1


    