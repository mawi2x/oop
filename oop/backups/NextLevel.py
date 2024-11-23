import pygame
from modules.GameConstants import *

# for ruff ignored errors
# ruff: noqa: F403, F405, F541 - ignore import errors - dahil pala sa ruff na yan kaya nagkakaroon ng error


class NextLevel:
    def __init__(self, game):
        """Initialize with reference to main game instance."""
        self.game = game

    def show_success_popup(self):
        """Display a success pop-up message."""
        self.game.popup_active = True
        center_x = constants.SCREEN_WIDTH // 2
        y_start = constants.SCREEN_HEIGHT // 2 - 100
        box_spacing = 70

        # Draw overlay
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(pygame.Color("#68c3a3"))
        self.game.screen.blit(overlay, (0, 0))

        # Define messages
        messages = [
            f"Level {self.game.level} Cleared!",
            "Congrats!",
            f"You guessed the word '{self.game.current_word}'!",
        ]

        # Draw messages
        for i, message in enumerate(messages):
            if i == 0:  # Level cleared message
                box_width = 400
                text_surf = constants.FONT_LARGE.render(message, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, y_start + (i * box_spacing)))
                box_rect = pygame.Rect(0, 0, box_width, text_rect.height + 30)
                box_rect.centerx = center_x
                box_rect.centery = text_rect.centery
            else:
                text_surf = constants.FONT_MEDIUM.render(message, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, y_start + (i * box_spacing)))
                box_rect = text_rect.inflate(40, 20)

            pygame.draw.rect(self.game.screen, constants.BUTTON_COLOR, box_rect)
            pygame.draw.rect(self.game.screen, constants.FONT_COLOR, box_rect, 3)
            self.game.screen.blit(text_surf, text_rect)

        pygame.display.flip()

        # Set a timer event for 2 seconds later
        pygame.time.set_timer(pygame.USEREVENT + 3, 2000)

        # Event loop waiting for the timer
        while self.game.popup_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.USEREVENT + 3:
                    # Timer finished
                    self.game.popup_active = False
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    # Proceed to next level
                    self.game.level += 1
                    self.game.hint_count += 1
                    self.game.reset_game()

            self.game.clock.tick(30)