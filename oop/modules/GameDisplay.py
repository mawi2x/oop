from modules.GameConstants import *
from modules.GameUtility import *

class GameDisplay:
    def __init__(self, game):
        """Initialize hangman display with game reference."""
        self.game = game
        self.images = paths.hangman_stages
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Hangman Game")

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


        