from modules.GameConstants import *
from modules.GameUtility import *

class HangmanDisplay:
    def __init__(self, game):
        """Initialize hangman display with game reference."""
        self.game = game
        self.images = paths.hangman_stages  # Store images in this class

    def draw_hangman(self):
        """Draw hangman state based on attempts."""
        if self.game.attempts < len(self.images):
            self.game.screen.blit(
                self.images[self.game.attempts],  # Use self.images
                (
                    constants.SCREEN_WIDTH // 2 - constants.width // 2,
                    constants.SCREEN_HEIGHT // 4,
                )
            )