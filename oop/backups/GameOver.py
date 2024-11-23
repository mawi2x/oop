import pygame
from modules.GameConstants import * 
# ruff: noqa: F403, F405, F541




class GameOver:
    def __init__(self, game):
        """Initialize with reference to main game instance."""
        self.game = game
        
    def show_popup(self, reset_level=False):
        """Display game over popup with messages and buttons."""
        self.game.popup_active = True

        # Create overlay
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(pygame.Color("#a11d33"))
        self.game.screen.blit(overlay, (0, 0))

        # Define messages
        messages = ["Game Over!", f"The word was '{self.game.current_word}'"]

        # Calculate positions
        center_x = constants.SCREEN_WIDTH // 2
        base_y = constants.SCREEN_HEIGHT // 2 - 100
        line_spacing = 80
        box_padding = 30

        # Draw messages
        for i, msg in enumerate(messages):
            if i == 0:  # Game Over message
                box_width = 400
                text_surf = constants.FONT_LARGE.render(msg, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, base_y + (i * line_spacing)))
                box_rect = pygame.Rect(0, 0, box_width, text_rect.height + box_padding)
                box_rect.centerx = center_x
                box_rect.centery = text_rect.centery
            else:
                text_surf = constants.FONT_MEDIUM.render(msg, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, base_y + (i * line_spacing)))
                box_rect = text_rect.inflate(box_padding * 2, box_padding)

            pygame.draw.rect(self.game.screen, constants.BUTTON_COLOR, box_rect)
            pygame.draw.rect(self.game.screen, constants.FONT_COLOR, box_rect, 3)
            self.game.screen.blit(text_surf, text_rect)

        # Button setup
        quit_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH // 2 - 200,
            constants.SCREEN_HEIGHT // 2 + 50,
            150,
            50
        )
        try_again_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH // 2 + 50,
            constants.SCREEN_HEIGHT // 2 + 50,
            150,
            50
        )

        # Draw buttons
        pygame.draw.rect(self.game.screen, pygame.Color("#FF0000"), quit_button_rect)
        pygame.draw.rect(self.game.screen, constants.FONT_COLOR, quit_button_rect, 3)
        quit_text = constants.FONT_SMALL.render("Quit", True, constants.FONT_COLOR)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        self.game.screen.blit(quit_text, quit_text_rect)

        pygame.draw.rect(self.game.screen, pygame.Color("#00FF00"), try_again_button_rect)
        pygame.draw.rect(self.game.screen, constants.FONT_COLOR, try_again_button_rect, 3)
        try_text = constants.FONT_SMALL.render("Try Again", True, constants.FONT_COLOR)
        try_text_rect = try_text.get_rect(center=try_again_button_rect.center)
        self.game.screen.blit(try_text, try_text_rect)

        pygame.display.flip()

        # Event loop
        while self.game.popup_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
                    if try_again_button_rect.collidepoint(mouse_pos):
                        self.game.reset_game(reset_level=True)
                        self.game.popup_active = False

            self.game.clock.tick(30)